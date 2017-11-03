import pandas as pd
import numpy as np
import os

from Tool.functions import Navigator, HydroTable
from Preprocessing.utilities import read_dbf


def get_residence_times(reservoir_table, volume_path):
    # Read and reformat volume table
    volume_table = read_dbf(volume_path)[["comid", "volumecorr"]]
    volume_table = volume_table.rename(columns={"comid": "wb_comid", "volumecorr": "volume"})

    # Join reservoir table with volumes
    joined_table = pd.merge(reservoir_table, volume_table, on="wb_comid")
    joined_table['residence_time'] = joined_table.volume / (joined_table.flow * 0.0283168) / 86400.

    del joined_table['volume']

    return joined_table


def identify_outlets(comid_table):
    """ Identify the outlet reach corresponding to each reservoir """
    # Filter the reach table down to only outlet reaches by getting the highest hydroseq for each wb_comid
    outlets = comid_table.loc[comid_table.groupby(["wb_comid"])["hydroseq"].idxmin()]
    outlets = outlets[[f for f in outlets.columns if f != 'hydroseq']].rename(columns={'comid': 'outlet_comid'})
    return outlets


def make_lake_bins(nav, reservoir_table):
    lentic_reaches = set(reservoir_table.outlet_comid)
    reservoir_table['n_upstream'] = 0
    for index, row in reservoir_table.iterrows():
        upstream_reaches, warning = nav.upstream_watershed(row.outlet_comid, return_times=False)
        upstream_lentics = set(map(float, upstream_reaches)) & lentic_reaches
        if upstream_lentics:
            reservoir_table.loc[index, 'n_upstream'] = \
                reservoir_table['outlet_comid'].isin(upstream_lentics).sum()
    return reservoir_table


def save_table(reservoir_table, outfile_path):
    reservoir_table[["outlet_comid", "wb_comid"]] = \
        np.int32(reservoir_table[["outlet_comid", "wb_comid"]].as_matrix())
    np.savez_compressed(outfile_path, table=reservoir_table.as_matrix(), key=reservoir_table.columns)


def main():
    from Preprocessing.utilities import nhd_states

    # Set initial paths
    nhd_path = os.path.join("..", "bin", "Preprocessed", "CondensedNHD")
    nav_path = os.path.join("..", "bin", "Preprocessed", "Navigators")
    volume_path = os.path.join(r"T:\NationalData\LakeMorphometry", "region_{}.dbf")
    output_path = os.path.join(r"..\bin\Preprocessed\LakeFiles", "region_{}.npz")

    # Loop through regions
    for region in nhd_states.keys():
        # Read tables and set output path
        nhd_table = HydroTable(region, nhd_path)
        nav = Navigator(region, nav_path)
        volume_table_path = volume_path.format(region)
        outfile_path = output_path.format(region)

        # Get a table of all lentic reaches, with the COMID of the reach and waterbody
        reservoir_table = nhd_table[["comid", "wb_comid", "hydroseq", "qma"]].rename(columns={'qma': 'flow'})

        # Get the outlets for each reservoir
        reservoir_table = identify_outlets(reservoir_table)

        # Get residence times
        reservoir_table = get_residence_times(reservoir_table, volume_table_path)

        # Count number of reservoirs upstream of each reservoir
        reservoir_table = make_lake_bins(nav, reservoir_table)

        # Save table
        save_table(reservoir_table, outfile_path)


main()
