from __future__ import division
import numpy as np
import pandas as pd
from ..base.uber_model import UberModel, ModelSharedInputs
# from base.uber_model import UberModel, ModelSharedInputs


class SamInputs(ModelSharedInputs):
    """
    Input class for SAM.
    """

    def __init__(self):
        """Class representing the inputs for SAM"""
        super(SamInputs, self).__init__()


class SamOutputs(object):
    """
    Output class for SAM.
    """

    def __init__(self):
        """Class representing the outputs for SAM"""
        super(SamOutputs, self).__init__()


class InputDict(dict):
    """
    Convert JSON input string and modify for easy digestion by pesticide calculator
    """

    def __init__(self, pd_obj):
        # Unpack JSON string into dictionary
        super(InputDict, self).__init__((k, v['0']) for k, v in pd_obj.to_dict().items())

        # Specify required inputs and field types
        self.fields = \
            [["chemical_name", str],  # Atrazine
             ["region", str],  # Ohio Valley
             ["endpoints", dict],
             ["soil_hl", float],  # Soil half life
             ["wc_metabolism_hl", float],  # Water column metabolism half life
             ["ben_metabolism_hl", float],  # Benthic metabolism half life
             ["aq_photolysis_hl", float],  # Aqueous photolysis half life
             ["hydrolysis_hl", float],  # Hydrolysis half life
             ["kd_flag", int],  # 1
             ["koc", float],  # 100
             ["sim_date_start", self.date],  # 01/01/1984
             ["sim_date_end", self.date],
             ["csrfmiddlewaretoken", str]]  # asrWb6LtFnBbULD0JXz3l71cCEyVi8dpPhiwo5rGO489v8NRNjpt9N4nTy0eNJGh

        self.application_fields = \
            [['crop', str],
             ['event', str],
             ['offset', np.int32],
             ['method', str],
             ['dist', str],
             ['window1', np.int32],
             ['pct1', np.float32],
             ['window2', np.int32],
             ['pct2', np.float32],
             ['effic', np.float32],
             ['apprate', np.float32], ]

        self.endpoint_format = \
            [(r"Human health DWLOC (ug/L)", 'human', (4, 21, 60)),
             (r"Freshwater Fish (Tox x LOC)", 'fw_fish', (4, 60,)),
             (r"Freshwater Invertebrate (Tox x LOC)", 'fw_inv', (4, 21,)),
             (r"Estuarine/Marine Fish (Tox x LOC)", 'em_fish', (4, 21,)),
             (r"Estuarine/Marine Invertebrate (Tox x LOC)", 'em_inv', (4, 21,)),
             (r"Aquatic nonvascular plant (Tox x LOC)", 'nonvasc_plant', (4, 21,)),
             (r"Aquatic vascular plant (Tox x LOC)", 'vasc_plant', (4, 21,))]

        # Pull out and aggregate all data inputs related to applications
        self['applications'] = self.process_applications()

        # Pull out and aggregate endpoints
        self['endpoints'] = self.process_endpoints()


        # Check to make sure that all necessary data is provided
        self.check_data()

        # Format data to correct data types
        self.format_data()

        # Apply adjustments.  These may be permanent or to be implemented in scenario matrix
        self.adjust_data()

    def adjust_data(self):
        # Convert half-lives to degradation rates
        adjust = lambda x: 0.693 / x if x else 0.
        self['deg_aqueous'], self['deg_photolysis'], self['deg_hydrolysis'], self['deg_wc'] = \
            map(adjust, (self['soil_hl'], self['aq_photolysis_hl'], self['hydrolysis_hl'], self['wc_metabolism_hl']))

        # Adjust koc
        self['koc'] /= 1000.0  # now in m3/kg

    def check_data(self):
        # Check if any required input data are missing or extraneous data are provided
        provided_fields = set(self.keys())
        required_fields = {field[0] for field in self.fields}
        unknown_fields = provided_fields - required_fields
        missing_fields = required_fields - provided_fields
        if unknown_fields:
            print("Input field(s) \"{}\" not understood".format(", ".join(unknown_fields)))
        assert not missing_fields, "Required input field(s) \"{}\" not provided".format(", ".join(missing_fields))

    def format_data(self):
        # Coerce data types
        for field, data_type in self.fields:
            self[field] = data_type(self[field])

    def process_applications(self):
        from .Tool.parameters import crop_groups
        # Process application matrix
        applications = []
        for i in range(int(self['napps'])):
            default = {np.int32: 0, np.float32: 0., str: ''}
            app = [self.pop("{}_{}".format(field, i + 1), default[field_type])
                   for field, field_type in self.application_fields]
            if " " in app[0]:  # crop must be first
                crops = set(map(int, (app[0].split())))
                all_crops = crops | {c for crop in crops for c in crop_groups.get(crop, set())}
                for crop in all_crops:
                    applications.append([crop] + app[1:])
            else:
                applications.append(app)
        field_names, data_types = map(list, zip(*self.application_fields))
        application_matrix = pd.DataFrame(applications, columns=field_names)

        for field_name, data_type in self.application_fields:
            application_matrix[field_name] = application_matrix[field_name].astype(data_type)

        # Turn application matrix into a numerical array for faster array processing
        replacements = {'event': ['plant', 'harvest', 'emergence', 'bloom', 'maturity'],
                        'dist': ['ground', 'foliar'],
                        'method': ['uniform', 'step']}

        # Replace certain values with indices
        for field, values in replacements.items():
            try:
                application_matrix[field] = np.vectorize(lambda x: values.index(x))(
                    application_matrix[field].as_matrix())
            except ValueError:
                print("Invalid value  provided for application in field '{}'".format(field))
        return np.float32(application_matrix.as_matrix())

    def process_endpoints(self):
        endpoints = []
        for long_name, species, durations in self.endpoint_format:
            for level, duration in zip(('acute', 'chronic', 'overall'), durations):
                short_name = "{}_{}".format(level, species)
                endpoint = self.pop(short_name, None)
                if endpoint:
                    endpoints.append((long_name, short_name, np.int16(duration), np.float32(endpoint)))
        data = np.zeros(len(endpoints), dtype=[("long_name", object), ("short_name", object),
                                               ("duration", np.int16), ("endpoint", np.float16)])
        data[:] = endpoints
        return pd.DataFrame(data).to_dict()

    @staticmethod
    def date(datestring):
        m, d, y = datestring.split("/")
        return np.datetime64("{}-{}-{}".format(y, m, d))


class Sam(UberModel, SamInputs, SamOutputs):
    """
    Estimate chemical exposure from drinking water alone in birds and mammals.
    """

    def __init__(self, pd_obj, pd_obj_exp):
        """Class representing the Terrplant model and containing all its methods"""
        super(Sam, self).__init__()
        self.pd_obj = pd_obj
        self.pd_obj_exp = pd_obj_exp
        self.pd_obj_out = None
        self.input_dict = InputDict(self.pd_obj)

    def execute_model(self):
        from .Tool.pesticide_calculator import pesticide_calculator
        outputs = pesticide_calculator(self.input_dict)
