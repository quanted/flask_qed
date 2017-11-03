import os
import json
import math

import numpy as np
import pandas as pd

from tempfile import mkdtemp
from json import encoder
from numba import guvectorize, njit


class MemoryMatrix(object):
    """ A wrapper for NumPy 'memmap' functionality which allows the storage and recall of arrays from disk """

    def __init__(self, index, y_size, z_size=None, path=None, base=None, name=None, dtype=np.float32, overwrite=True,
                 input_only=False):
        self.name = name if name else "temp"
        self.dtype = dtype
        self.index = index
        self.count = len(self.index)
        self.lookup = dict(zip(self.index, np.arange(self.count)))
        self.shape = (self.count, y_size) if not z_size else (self.count, y_size, z_size)
        overwrite = False if input_only else overwrite

        # Load from saved file if one is specified, else generate
        default_path = mkdtemp()
        path = default_path if path is None else path
        if not os.path.exists(path):
            os.makedirs(path)
        base = name if not base else base
        self.path = os.path.join(path, base + ".dat")

        # Determine whether to load existing or create new matrix
        assert not input_only or os.path.exists(self.path), "Matrix {} not found".format(self.path)
        if overwrite or not os.path.exists(self.path):
            np.memmap(self.path, dtype=dtype, mode='w+', shape=self.shape)
            self.new = True
        else:
            self.new = False

    def fetch(self, get_index, verbose=True, raw_index=False, dtype=None, copy=False):
        array = self.copy if copy else self.reader
        location = self.lookup.get(get_index) if not raw_index else get_index
        if location is not None:
            output = array[location]
        else:
            if verbose:
                print("{} not found".format(get_index))
            output = None
        del array
        return output

    def fetch_multiple(self, indices, copy=False, verbose=False, aliased=True, return_index=False, columns=None):

        # If selecting by aliases, get indices for aliases
        index = None
        if aliased:
            addresses = np.int32([self.lookup.get(x, -1) for x in indices])
            found = np.where(addresses >= 0)[0]
            not_found = indices.size - found.size
            if not_found:
                index = found
                if verbose:
                    print("Missing {} of {} indices in {} matrix".format(not_found, len(addresses), self.name))
            indices = addresses[found]

        # Fetch data from memory map
        array = np.memmap(self.path, dtype='float32', mode='c' if copy else 'r', shape=self.shape)
        out_array = array[indices] if columns is None else array[np.ix_(indices, columns)]
        del array

        if return_index:
            return out_array, index
        else:
            return out_array

    def update(self, key, value, aliased=True):
        array = self.writer
        array_index = self.lookup.get(key) if aliased else key
        if array_index is not None:
            array[array_index] = value
        else:
            print("Index {} not found in {} array".format(key, self.name))
        del array

    @property
    def reader(self):
        return np.memmap(self.path, dtype=self.dtype, mode='r', shape=self.shape)

    @property
    def copy(self):
        return np.memmap(self.path, dtype=self.dtype, mode='c', shape=self.shape)

    @property
    def writer(self):
        mode = 'r+' if os.path.isfile(self.path) else 'w+'
        return np.memmap(self.path, dtype=self.dtype, mode=mode, shape=self.shape)


class HydroTable(pd.DataFrame):
    def __init__(self, region, path):
        super().__init__()
        self.region = region
        self.path = path
        self.table_path = os.path.join(path, "region_{}.npz".format(region))

        data, header = self.read_table()
        super(HydroTable, self).__init__(data=data, columns=header)

        index_col = 'wb_comid' if 'wb_comid' in self.columns else 'comid'
        self.set_index(index_col, inplace=True)
        self.index = np.int32(self.index)

    def read_table(self):
        assert os.path.isfile(self.table_path), "Table not found for region {} in {}".format(self.region, self.path)
        data = np.load(self.table_path)
        return data['table'], data['key']

    def flows(self, reach, month_index):
        return self.loc[reach].as_matrix()[month_index]


class Hydroregion(object):
    """
    Contains all datasets and functions related to the NHD Plus region, including all hydrological features and links
    """

    def __init__(self, region, map_path, flowfile_dir, upstream_dir, lakefile_dir):
        self.id = region

        # Read hydrological input files
        self.flow_file = HydroTable(self.id, flowfile_dir)
        self.lake_table = HydroTable(self.id, lakefile_dir)
        self.nav = Navigator(self.id, upstream_dir)
        self.recipe_map = RecipeMap(self.id, map_path)

        # Confine to available reaches and assess what's missing
        self.active_reaches = self.confine()
        self.run_reaches = set()

    def cascade(self):
        # Identify all outlets (and therefore, reservoirs) that exist in the current run scope
        confined_outlets = self.lake_table.outlet_comid.isin(self.active_reaches)

        # Confine lake table to these outlets and sort by number of upstream reservoirs
        confined_lake_table = self.lake_table[confined_outlets].sort_values('n_upstream')

        # Loop through reservoirs in a downstream direction and process all upstream reaches
        for i, lake in confined_lake_table.iterrows():
            upstream_reaches, warning = self.nav.upstream_watershed(lake.outlet_comid, mode='reach', return_times=False)
            upstream_reaches = set(upstream_reaches)
            reaches = upstream_reaches & self.active_reaches - {lake.outlet_comid}
            yield reaches - self.run_reaches, lake
            self.run_reaches |= reaches
        remaining_reaches = self.active_reaches - self.run_reaches
        yield remaining_reaches, None

    def confine(self):
        # Recipe/reaches that are (1) in the upstream file and (2) have a recipe file in at least 1 yr
        map_reaches = {reach_id for reach_id, _ in self.recipe_map.lookup.keys()}
        region_reaches = set(self.nav.reach_to_alias.keys())
        active_reaches = map_reaches & region_reaches
        active_reaches.discard(0)

        # Identify full watershed extent of reaches and get matching lakes
        # full_watershed = {us for r in active_reaches for us in self.upstream_watershed(r, return_times=False)}

        return active_reaches


class ImpulseResponseMatrix(MemoryMatrix):
    """ A matrix designed to hold the results of an impulse response function for 50 day offsets """

    def __init__(self, n_dates):
        self.n_dates = n_dates
        super(ImpulseResponseMatrix, self).__init__(np.arange(50), n_dates, name="impulse response")

    def fetch(self, index):
        irf = super(ImpulseResponseMatrix, self).fetch(index, verbose=False)
        if irf is None:
            irf = impulse_response_function(index, 1, self.n_dates)
            self.update(index, irf)
        return irf


class InputFile(object):
    """ User-specified parameters and parameters derived from them """

    def __init__(self, input_dict):
        from .parameters import time_of_travel, crop_groups, paths

        # Read input dictionary
        self.__dict__.update(input_dict)
        self.endpoints = pd.DataFrame(self.endpoints)

        # Crops
        self.crops = set(self.applications[:, 0])

        # Set dates
        self.dates = pd.date_range(self.sim_date_start, self.sim_date_end)
        self.n_dates = len(self.dates)
        self.year = self.dates.year
        self.month_index = self.dates.month - 1
        self.unique_years, self.year_length = np.unique(self.year, return_counts=True)
        self.new_year = np.int32([(np.datetime64("{}-01-01".format(year)) - self.sim_date_start).astype(int)
                                  for year in self.unique_years])

        # Initialize an impulse response matrix if convolving timesheds
        self.irf = None if not time_of_travel.gamma_convolve else ImpulseResponseMatrix(self.dates.size)

        # Initialize output directory
        try:
            self.token = self.csrfmiddlewaretoken
        except AttributeError:
            print("No token provided: output will be written to directory \'dummy\'")
            self.token = 'dummy'

        # To be added to front en
        self.write_contributions = True
        self.write_exceedances = True
        self.write_time_series = True


class Navigator(object):
    def __init__(self, region_id, upstream_path):
        self.file = os.path.join(upstream_path, "region_{}.npz".format(region_id))
        self.paths, self.times, self.map, self.alias_to_reach, self.reach_to_alias = self.load()

    def load(self):
        assert os.path.isfile(self.file), "Upstream file {} not found".format(self.file)
        data = np.load(self.file, mmap_mode='r')
        conversion_array = data['alias_index']
        reverse_conversion = dict(zip(conversion_array, np.arange(conversion_array.size)))
        return data['paths'], data['time'], data['path_map'], conversion_array, reverse_conversion

    def upstream_watershed(self, reach_id, mode='reach', return_times=True):

        def unpack(array):
            first_row = [array[start_row][start_col:]]
            remaining_rows = list(array[start_row + 1:end_row])
            return np.concatenate(first_row + remaining_rows)

        # Look up reach ID and fetch address from upstream object
        reach = reach_id if mode == 'alias' else self.reach_to_alias.get(reach_id)
        reaches, adjusted_times, warning = [], [], None
        try:
            start_row, end_row, col = map(int, self.map[reach])
            start_col = list(self.paths[start_row]).index(reach)
        except TypeError:
            warning = "Reach {} not found in region".format(reach)
        except ValueError:
            warning = "{} not in upstream lookup".format(reach)
        else:
            # Fetch upstream reaches and times
            aliases = unpack(self.paths)
            reaches = aliases if mode == 'alias' else np.int32(self.alias_to_reach[aliases])
        if not return_times:
            return reaches, warning
        else:
            if warning is None:
                times = unpack(self.times)
                adjusted_times = np.int32(times - self.times[start_row][start_col])
            return reaches, adjusted_times, warning


class RecipeMap(MemoryMatrix):
    def __init__(self, region, in_path):
        self.memmap_file = os.path.join(in_path, "region_{}".format(region))
        self.dir, self.base = os.path.split(self.memmap_file)
        self.key_file = self.memmap_file + "_key.npy"
        self.key = list(map(tuple, np.load(self.key_file)))
        self.n_cols = self.key.pop(-1)[0]

        super(RecipeMap, self).__init__(self.key, self.n_cols, 2, name="recipe map", path=self.dir, base=self.base,
                                        dtype=np.int32, input_only=True)

    def fetch(self, get_index, verbose=False):
        results = super(RecipeMap, self).fetch(get_index, verbose)
        if results is not None:
            results = results[results[:, 0] > [0]]
            if not results.any():
                results = None
        return results


class Recipes(object):
    def __init__(self, i, o, year, region, scenario_matrix, output_path, write_list=set()):
        self.i = i
        self.o = o
        self.year = year
        self.region = region
        self.output_dir = os.path.join(output_path, i.token)
        self.scenario_matrix = scenario_matrix
        self.write_list = sorted(write_list)
        self.recipe_ids = sorted(region.active_reaches)
        self.outlets = set(self.recipe_ids) & set(self.region.lake_table.outlet_comid)

        self.processed_count = 0

        # Initialize local matrix: matrix of local runoff and mass, for rapid internal recall
        self.local = MemoryMatrix(self.recipe_ids, 2, self.i.n_dates, name="recipe")

    def burn_reservoir(self, lake, upstream_reaches):

        from .parameters import time_of_travel as time_of_travel_params

        if lake is not None and upstream_reaches:

            # Get the convolution function
            irf = impulse_response_function(1, lake.residence_time, self.i.n_dates)

            # Pull mass and runoff time series for all upstream reaches and add together
            if upstream_reaches:

                upstream_reaches = np.array(list(upstream_reaches))

                old_mass, old_runoff = self.local.fetch_multiple(upstream_reaches).sum(axis=0)

                # Modify combined time series to reflect reservoir
                new_mass = np.convolve(old_mass, irf)[:self.i.n_dates]
                if time_of_travel_params.convolve_runoff:  # Convolve runoff
                    new_runoff = np.convolve(old_runoff, irf)[:self.i.n_dates]
                else:  # Flatten runoff
                    new_runoff = np.repeat(np.mean(old_runoff), self.i.n_dates)

                # Add all lake mass and runoff to outlet
                self.local.update(lake.outlet_comid, np.array([new_mass, new_runoff]))

    def fetch_scenarios(self, recipe_id):
        try:
            data = self.region.recipe_map.fetch((recipe_id, self.year)).T
            scenarios, areas = data
        except AttributeError:
            return None, None
        else:
            # Fetch all scenarios and multiply by area.  For erosion, area is adjusted.
            # JCH - processing time here is 50/50 on fetch_multiple and math operations
            # (scenarios, vars, dates)
            array = self.scenario_matrix.processed_matrix.fetch_multiple(scenarios, copy=True, aliased=False)
            array = np.rollaxis(array, 0, 3)
            array[:2] *= areas  # runoff, runoff_mass.
            array[2:] *= np.power(areas / 10000., .12)  # erosion, erosion_mass
            return scenarios, array  # (var, date, scenario)

    def local_loading(self, recipe_id, cumulative, process_benthic=False):
        """Pull all scenarios in recipe from scenario matrix and adjust for area"""

        # Sum time series from all scenarios
        runoff, erosion, runoff_mass, erosion_mass = cumulative

        # Run benthic/water column partitioning
        benthic_conc = self.partition_benthic(recipe_id, erosion, erosion_mass) if process_benthic else None

        # If it's a lake outlet, do this
        if recipe_id in self.outlets:
            runoff_mass, runoff = np.array([runoff_mass, runoff]) + self.local.fetch(recipe_id)

        return runoff_mass, runoff, benthic_conc

    def partition_benthic(self, recipe_id, erosion, erosion_mass):

        from ..Tool.parameters import benthic

        surface_area = self.region.flow_file.loc[recipe_id]["surface_area"]
        soil_volume = benthic.depth * surface_area
        pore_water_volume = soil_volume * benthic.porosity
        benthic_mass = benthic_loop(erosion, erosion_mass, soil_volume)
        return benthic_mass / pore_water_volume

    def process_recipes(self, recipe_ids, progress_interval=1000):

        for recipe_id in recipe_ids:

            # Determine whether to do additional analysis on recipe
            active_recipe = recipe_id in self.write_list

            self.processed_count += 1
            if not self.processed_count % progress_interval:
                print("Processed {} of {} recipes".format(self.processed_count, len(self.recipe_ids)))

            # Fetch time series data from all scenarios in re cipe
            scenarios, time_series = self.fetch_scenarios(recipe_id)  # (var, date, scenario)

            if scenarios is not None:

                # Assess the contributions to the recipe from each source (runoff/erosion) and crop
                self.o.update_contributions(recipe_id, scenarios, time_series[[1, 3]].sum(axis=1))

                # Process local contributions
                local_mass, local_runoff, benthic_conc = \
                    self.local_loading(recipe_id, time_series.sum(axis=2), active_recipe)

                # Update local array with mass and runoff
                self.local.update(recipe_id, np.array([local_mass, local_runoff]))

                # Upstream processing and output generation only done if the recipe is in the write list
                if active_recipe:

                    # Process upstream contributions
                    total_flow, total_runoff, total_mass, total_conc = self.upstream_loading(recipe_id)

                    if total_conc is not None:
                        # Calculate exceedances
                        self.o.update_exceedances(recipe_id, total_conc)

                        # Store results in output array
                        self.o.update_time_series(recipe_id, total_flow, total_runoff, total_mass, total_conc, benthic_conc)

    def upstream_loading(self, reach):
        def confine_reaches():
            indices = np.int16([i for i, r in enumerate(reaches) if r not in self.region.run_reaches])
            return reaches[indices], times[indices]

        from .parameters import time_of_travel

        # Fetch all upstream reaches and corresponding travel times
        reaches, times, warning = self.region.nav.upstream_watershed(reach)
        reaches, times = confine_reaches()
        if len(reaches) > 1:  # Don't need to do this if it's a headwater
            # Check here to confirm that all upstream_reaches have been processed?
            mnr, index = self.local.fetch_multiple(reaches, return_index=True)  # (reaches, mass/runoff, dates)
            if index is not None:
                reaches, times = reaches[index], times[index]
            totals = np.zeros((2, self.i.n_dates))  # (mass/runoff, dates)
            for tank in range(np.max(times) + 1):
                in_tank = mnr[times == tank].sum(axis=0)
                if tank > 0:
                    if time_of_travel.gamma_convolve:
                        irf = self.region.irf.fetch(tank)  # Get the convolution function
                        in_tank[0] = np.convolve(in_tank[0], irf)[:self.i.n_dates]  # mass
                        in_tank[1] = np.convolve(in_tank[1], irf)[:self.i.n_dates]  # runoff
                    else:
                        in_tank = np.pad(in_tank[:, :-tank], ((0, 0), (tank, 0)), mode='constant')
                totals += in_tank  # Add the convolved tank time series to the total for the reach
            mass, runoff = totals
        else:
            mass, runoff = self.local.fetch(reach)

        flow = self.region.flow_file.flows(reach, self.i.month_index)
        if flow is not None:
            total_flow, (concentration, runoff_conc) = \
                compute_concentration(mass, runoff, self.i.n_dates, flow)
            return total_flow, runoff, mass, concentration
        else:
            return None, None, None, None


class Scenarios(object):
    def __init__(self, i, input_memmap_path, retain=None):
        self.i = i
        self.path, self.base = os.path.split(input_memmap_path)
        self.keyfile_path = input_memmap_path + "_key.txt"

        # Load key file for interpreting input matrices
        self.arrays, self.variables, self.names, self.array_shape, self.variable_shape, \
        self.start_date, self.n_dates = self.load_key()

        # Calculate date offsets
        self.end_date = self.start_date + np.timedelta64(self.n_dates, 'D')
        self.start_offset, self.end_offset = self.date_offsets()

        # Initialize input matrices
        self.array_matrix = MemoryMatrix(self.names, len(self.arrays), self.n_dates, self.path,
                                         self.base + "_arrays", name="arrays", input_only=True)
        self.variable_matrix = MemoryMatrix(self.names, len(self.variables), path=self.path,
                                            base=self.base + "_vars", name="variables", input_only=True)

        # Initialize empty matrix for procesed scenarios
        if retain is not None:
            self.processed_matrix = MemoryMatrix(self.names, 4, i.dates.size, path=self.path, base=retain,
                                                 name="scenario", overwrite=False)
        else:
            self.processed_matrix = MemoryMatrix(self.names, 4, i.dates.size, name="scenario")

        # Populate scenario matrix if it doesn't exist
        if self.processed_matrix.new:
            self.process_scenarios()

    def date_offsets(self):
        if self.start_date > self.i.sim_date_start:
            self.i.sim_date_start = self.start_date
            print("Simulation dates start earlier than the dates in the scenario matrix. Adjusting run dates")
        if self.end_date < self.i.sim_date_end:
            self.i.sim_date_end = self.end_date
            print("Simulation dates end after the dates in scenario matrix. Adjusting run dates")
        start_offset = (self.i.sim_date_start - self.start_date).astype(int)
        end_offset = (self.i.sim_date_end - self.end_date).astype(int) + 1
        if not end_offset:
            end_offset = self.n_dates + 1
        return start_offset, end_offset

    def load_key(self):
        with open(self.keyfile_path) as f:
            arrays, variables, scenarios = (next(f).strip().split(",") for _ in range(3))
            start_date = np.datetime64(next(f).strip())
            shape = np.array([int(val) for val in next(f).strip().split(",")])
        return arrays, variables, np.array(scenarios), shape[:3], shape[3:], start_date, int(shape[2])

    def process_scenarios(self, chunk=5000, progress_interval=10000):

        from .parameters import crop_groups, soil, plant

        # Initialize readers and writers
        # Reminder: array_matrix.shape, processed_matrix.shape = (scenario, variable, date)
        array_reader, variable_reader = self.array_matrix.reader, self.variable_matrix.reader
        processed_writer = self.processed_matrix.writer

        # Iterate scenarios
        for n, scenario_id in enumerate(self.names):

            # Report progress and reset readers/writers at intervals
            if not (n + 1) % progress_interval:
                print("{}/{}".format(n + 1, len(self.names)))

            # Open and close read/write cursors at intervals. This seems to help
            if not n % chunk:
                if n != 0:
                    del array_reader, variable_reader, processed_writer
                    array_reader, variable_reader = self.array_matrix.reader, self.variable_matrix.reader
                    processed_writer = self.processed_matrix.writer

            # Get crop ID of scenario and find all associated crops in group
            crop = int(scenario_id.split("cdl")[1])
            if crop in self.i.crops:

                # Extract arrays
                leaching, runoff, erosion, soil_water, plant_factor, rain = \
                    array_reader[n][:, self.start_offset:self.end_offset]

                # Read non-sequential variables from scenario and process
                covmax, org_carbon, bulk_density, *plant_dates = variable_reader[n]

                # Set kd depending on settings
                kd = self.i.koc * org_carbon if self.i.kd_flag else self.koc

                # Assert that all data is the proper shape for use in the functions
                assert len(plant_dates) == 5, "Looking for 5 planting dates, found {}".format(len(plant_dates))
                assert self.i.applications.shape[1] == 11, "Invalid application matrix, should have 11 columns"

                # Calculate the daily input of pesticide to the soil and plant canopy
                application_mass = \
                    pesticide_to_field(self.i.applications, self.i.new_year, crop, plant_dates, rain)

                # Calculate the daily mass of pesticide in the soil
                pesticide_mass_soil = pesticide_to_soil(application_mass, rain, plant_factor, soil.cm_2,
                                                        plant.deg_foliar, plant.washoff_coeff, covmax)

                # Determine the loading of pesticide into runoff and eroded sediment
                runoff_mass, erosion_mass = \
                    pesticide_to_water(pesticide_mass_soil, runoff, erosion, leaching, bulk_density, soil_water, kd,
                                       self.i.deg_aqueous, soil.runoff_effic, soil.delta_x, soil.erosion_effic,
                                       soil.soil_depth)

                # Write runoff, erosion, runoff mass and erosion mass to processed matrix
                processed_writer[n] = runoff, runoff_mass, erosion, erosion_mass

            else:
                # Write runoff and erosion
                processed_writer[n, [0, 2]] = array_reader[n][1:3, self.start_offset:self.end_offset]

        del array_reader, variable_reader


class Outputs(object):
    def __init__(self, i, recipe_ids, scenario_ids, output_path, write_list=[]):
        self.i = i
        self.recipe_ids = sorted(recipe_ids)
        self.scenario_ids = scenario_ids
        self.output_dir = os.path.join(output_path, i.token)
        self.write_list = write_list

        # Initialize output JSON dict
        self.out_json = {}

        # Initialize output matrices
        self.output_fields = ['total_flow', 'total_runoff', 'total_mass', 'total_conc', 'benthic_conc']
        if self.write_list:
            self.time_series = \
                MemoryMatrix(sorted(self.write_list), len(self.output_fields), self.i.n_dates, name="output")
        else:
            self.i.write_time_series = False
            self.time_series = None

        # Initialize contributions matrix: loading data broken down by crop and runoff v. erosion source
        self.exceedances = MemoryMatrix(self.recipe_ids, self.i.endpoints.shape[0], name="exceed")

        # Initialize contributions matrix: loading data broken down by crop and runoff v. erosion source
        self.contributions = MemoryMatrix(self.recipe_ids, 2, len(self.i.crops), name="contributions")
        self.contributions.columns = np.int32(sorted(self.i.crops))
        self.contributions.labels = ["cls" + str(c) for c in self.contributions.columns]

    def update_contributions(self, recipe_id, scenario_index, loads):
        """ Sum the total contribution by land cover class and add to running total """

        scenario_names = self.scenario_ids[scenario_index]
        classes = [int(name.split("cdl")[1]) for name in scenario_names]
        contributions = np.zeros((2, 255))
        for i in range(2):  # Runoff Mass, Erosion Mass
            contributions[i] += np.bincount(classes, weights=loads[i], minlength=255)
        self.contributions.update(recipe_id, contributions[:, self.contributions.columns])

    def update_exceedances(self, recipe_id, concentration):
        durations, endpoints = self.i.endpoints[["duration", "endpoint"]].as_matrix().T
        years = self.i.year - self.i.year[0]
        exceed = exceedance_probability(concentration, *map(np.int16, (durations, endpoints, years)))
        self.exceedances.update(recipe_id, exceed)

    def update_time_series(self, recipe_id, total_flow=None, total_runoff=None, total_mass=None, total_conc=None,
                           benthic_conc=None):

        writer = self.time_series.writer
        index = self.time_series.index.index(recipe_id)

        # This must match self.fields as designated in __init__
        rows = [total_flow, total_runoff, total_mass, total_conc, benthic_conc]
        for i, row in enumerate(rows):
            if row is not None:
                writer[index, i] = row
        del writer

    def write_json(self, write_exceedances=False, write_contributions=False):

        encoder.FLOAT_REPR = lambda o: format(o, '.4f')
        out_file = os.path.join(self.output_dir, "{}_json.csv".format(self.i.chemical_name))
        out_json = {"COMID": {}}
        for recipe_id in self.recipe_ids:
            out_json["COMID"][str(recipe_id)] = {}
            if write_exceedances:
                exceedance_dict = dict(zip(self.i.endpoints.short_name, map(float, self.exceedances.fetch(recipe_id))))
                out_json["COMID"][str(recipe_id)].update(exceedance_dict)
            if write_contributions:
                contributions = self.contributions.fetch(recipe_id)
                for i, category in enumerate(("runoff", "erosion")):
                    labels = ["{}_load_{}".format(category, label) for label in self.contributions.labels]
                    contribution_dict = dict(zip(labels, map(float, contributions[i])))
                    out_json["COMID"][str(recipe_id)].update(contribution_dict)

        out_json = json.dumps(dict(out_json), sort_keys=True, indent=4, separators=(',', ': '))
        with open(out_file, 'w') as f:
            f.write(out_json)

    def write_output(self):

        # Create output directory
        if not os.path.isdir(self.output_dir):
            os.makedirs(self.output_dir)

        # Write JSON output
        self.write_json(self.i.write_exceedances, self.i.write_contributions)

        # Write time series
        if self.i.write_time_series:
            self.write_time_series()

    def write_time_series(self, fields='all'):
        if fields == 'all':
            fields = self.output_fields
            field_indices = np.arange(len(self.output_fields))
        else:
            field_indices = [self.output_fields.index(field) for field in fields]

        heading_lookup = {'runoff_conc': 'RunoffConc(ug/L)',
                          'local_runoff': 'LocalRunoff(m3)',
                          'total_runoff': 'TotalRunoff(m3)',
                          'local_mass': 'LocalMass(m3)',
                          'total_flow': 'TotalFlow(m3)',
                          'baseflow': 'Baseflow(m3)',
                          'total_conc': 'TotalConc(ug/L)',
                          'total_mass': 'TotalMass(kg)',
                          'wc_conc': 'WC_Conc(ug/L)',
                          'erosion': 'Erosion(kg)',
                          'erosion_mass': 'ErodedMass(kg)',
                          'runoff_mass': 'RunoffMass(kg)',
                          'benthic_conc': 'BenthicConc(ug/L)'}

        headings = [heading_lookup.get(field, "N/A") for field in fields]

        for recipe_id in self.write_list:
            out_file = os.path.join(self.output_dir, "time_series_{}.csv".format(recipe_id))
            out_data = self.time_series.fetch(recipe_id)[field_indices].T
            df = pd.DataFrame(data=out_data, index=self.i.dates, columns=headings)
            df.to_csv(out_file)


@njit
def benthic_loop(eroded_soil, erosion_mass, soil_volume):
    benthic_mass = np.zeros(erosion_mass.size, dtype=np.float32)
    benthic_mass[0] = erosion_mass[0]
    for i in range(1, erosion_mass.size):
        influx_ratio = eroded_soil[i] / (eroded_soil[i] + soil_volume)
        benthic_mass[i] = (benthic_mass[i - 1] * (1. - influx_ratio)) + (erosion_mass[i] * (1. - influx_ratio))
    return benthic_mass


def compute_concentration(transported_mass, runoff, n_dates, q):
    """ Concentration function for time of travel """
    mean_runoff = runoff.mean()  # m3/d
    baseflow = np.subtract(q, mean_runoff, out=np.zeros(n_dates), where=(q > mean_runoff))
    total_flow = runoff + baseflow
    concentration = np.divide(transported_mass, total_flow, out=np.zeros(n_dates),
                              where=(total_flow != 0))
    runoff_concentration = np.divide(transported_mass, runoff, out=np.zeros(n_dates),
                                     where=(runoff != 0))

    return total_flow, map(lambda x: x * 1000000., (concentration, runoff_concentration))  # kg/m3 -> ug/L


def confine_regions(nhd_regions, map_path, write_list):
    """ Determine which NHD regions need to be run to process the specified reaches """
    print("In confine_regions...")
    # write_list is a set of all reaches to be processed
    if write_list is not None:
        active_regions = set()
        for region in nhd_regions:
            print(region)
            region_map = os.path.join(map_path, "region_{}_key.npy".format(region))
            print(region_map)
            if os.path.exists(region_map):
                print("region added")
                reaches = set(np.load(region_map).T[0])
                if any(set(write_list) & reaches):
                    active_regions.add(region)
        return sorted(active_regions)
    else:
        # If none specified, run whole country
        return nhd_regions


@guvectorize(['void(float64[:], int16[:], int16[:], int16[:], float64[:])'], '(p),(o),(o),(p)->(o)')
def exceedance_probability(time_series, window_sizes, endpoints, years_since_start, res):
    # Count the number of times the concentration exceeds the test threshold in each year
    n_years = years_since_start.max()
    for test_number in range(window_sizes.size):
        window_size = window_sizes[test_number]
        threshold = endpoints[test_number]
        window_sum = np.sum(time_series[:window_size])
        exceedances = np.zeros(n_years)
        for day in range(window_size, len(time_series)):
            year = years_since_start[day]
            window_sum += time_series[day] - time_series[day - window_size]
            avg = window_sum / window_size
            if avg > threshold:
                exceedances[year] = 1
        res[test_number] = exceedances.sum() / n_years


def impulse_response_function(alpha, beta, length):
    def gamma_distribution(t, a, b):
        a, b = map(float, (a, b))
        tau = a * b
        return ((t ** (a - 1)) / (((tau / a) ** a) * math.gamma(a))) * math.exp(-(a / tau) * t)

    return np.array([gamma_distribution(i, alpha, beta) for i in range(length)])


@njit
def pesticide_to_field(applications, new_years, active_crop, event_dates, rain):
    """ Simulate timing of pesticide appplication to field """

    application_mass = np.zeros((2, rain.size))
    for i in range(applications.shape[0]):
        crop, event, offset, canopy, step, window1, pct1, window2, pct2, effic, rate = applications[i]
        if crop == active_crop:
            event_date = int(event_dates[int(event)])
            daily_mass_1 = rate * (pct1 / 100.) / window1
            if step:
                daily_mass_2 = rate * (pct2 / 100.) / window2
            for year in range(new_years.size):
                new_year = new_years[year]
                for k in range(int(window1)):
                    date = int(new_year + event_date + offset + k)
                    application_mass[int(canopy), date] = daily_mass_1
                if step:
                    for l in range(window2):
                        date = int(new_year + event_date + window1 + offset + l)
                        application_mass[int(canopy), date] = daily_mass_2
    return application_mass


@njit
def pesticide_to_soil(application_mass, rain, plant_factor, soil_2cm, foliar_degradation, washoff_coeff, covmax):
    """ Calcluate pesticide in soil and simulate movement of pesticide from canopy to soil """

    # Initialize output
    pesticide_mass_soil = np.zeros(rain.size)
    canopy_mass, last_application = 0, 0  # Running variables

    # Determine if any pesticide has been applied to canopy
    canopy_applications = application_mass[1].sum() > 0

    # Loop through each day
    for day in range(plant_factor.size):
        # Start with pesticide applied directly to soil
        pesticide_mass_soil[day] = application_mass[0, day] * soil_2cm
        # If pesticide has been applied to the canopy, simulate movement from canopy to soil
        if canopy_applications:
            if application_mass[1, day] > 0:  # Pesticide applied to canopy on this day
                canopy_pesticide_additions = application_mass[1, day] * plant_factor[day] * covmax
                pesticide_mass_soil[day] += (application_mass[1, day] - canopy_pesticide_additions) * soil_2cm
                canopy_mass = canopy_pesticide_additions + \
                              canopy_mass * np.exp((day - last_application) * foliar_degradation)
                last_application = day
            if rain[day] > 0:  # Simulate washoff
                canopy_mass *= np.exp((day - last_application) * foliar_degradation)
                pesticide_remaining = canopy_mass * np.exp(-rain[day] * washoff_coeff)
                pesticide_mass_soil[day] += canopy_mass - pesticide_remaining
                last_application = day  # JCH - sure?
    return pesticide_mass_soil


@njit
def pesticide_to_water(pesticide_mass_soil, runoff, erosion, leaching, bulk_density, soil_water, kd, deg_aqueous,
                       runoff_effic, delta_x, erosion_effic, soil_depth):
    # Initialize output arrays
    runoff_mass, erosion_mass = np.zeros(runoff.size), np.zeros(runoff.size)

    # Initialize running variables
    total_mass, degradation_rate = 0, 0

    # Initialize erosion intensity
    erosion_intensity = erosion_effic / soil_depth

    # Loop through days
    for day in range(runoff.size):
        daily_runoff = runoff[day] * runoff_effic
        total_mass = total_mass * degradation_rate + pesticide_mass_soil[day]
        retardation = (soil_water[day] / delta_x) + (bulk_density * kd)
        deg_total = deg_aqueous + ((daily_runoff + leaching[day]) / (delta_x * retardation))
        if leaching[day] > 0:
            degradation_rate = np.exp(-deg_total)
        else:
            degradation_rate = np.exp(-deg_aqueous)

        average_conc = ((total_mass / retardation / delta_x) / deg_total) * (1 - degradation_rate)

        if leaching[day] > 0:
            runoff_mass[day] = average_conc * daily_runoff
        if erosion[day] > 0:
            enrich = np.exp(2.0 - (0.2 * np.log10(erosion[day])))
            enriched_eroded_mass = erosion[day] * enrich * kd * erosion_intensity * 0.1
            erosion_mass[day] = average_conc * enriched_eroded_mass

    return runoff_mass, erosion_mass


if __name__ == "__main__":
    import cProfile
    from ubertool_ecorest.ubertool.ubertool.sam.Tool.pesticide_calculator import main

    if True:
        cProfile.run('main()')
    else:
        main()
