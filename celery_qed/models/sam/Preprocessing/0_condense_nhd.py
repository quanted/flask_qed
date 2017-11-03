import os
import pandas as pd
import numpy as np
from collections import defaultdict, OrderedDict

from Preprocessing.utilities import read_dbf, nhd_states


def get_nhd(nhd_dir=r"T:\NationalData\NHDPlusV2"):
    all_paths = defaultdict()
    regions = list(nhd_states.keys())
    region_dirs = {"NHDPlus{}".format(region) for region in regions}
    for root_dir, sub_dirs, _ in os.walk(nhd_dir):
        if set(sub_dirs) & region_dirs:
            for sub_dir in sub_dirs:
                region = sub_dir.lstrip("NHDPlus")
                if region in regions:
                    all_paths[sub_dir.lstrip("NHDPlus")] = os.path.join(root_dir, sub_dir)
    return OrderedDict(sorted(all_paths.items()))


def sever_divergences(flow_table, vaa_table):
    flow_table = read_dbf(flow_table)[["fromcomid", "tocomid"]]
    vaa_table = read_dbf(vaa_table)[["comid", "streamcalc", "divergence"]]
    for direction in ("to", "from"):
        flow_table = pd.merge(flow_table, vaa_table, left_on="{}comid".format(direction), right_on="comid")
        flow_table = flow_table.rename(columns={var: direction + var for var in ("streamcalc", "divergence")})
    flow_table = flow_table[~((flow_table.fromstreamcalc > 0) & (flow_table.tostreamcalc == 0))]
    flow_table = flow_table[~(flow_table.todivergence == 2)]

    return flow_table[["fromcomid", "tocomid"]].rename(columns={"fromcomid": "comid"})


def extract_tables(flow_table, flow_lines, vaa_table, gridcode_table):
    extract_fields = [["featureid", "gridcode"],  # gridcode_table
                      ["comid", "fcode", "wbareacomi"],  # flow lines
                      ["comid", "hydroseq", "lengthkm", "streamcalc"]]  # vaa_table

    rename_fields = [("wbareacomi", "wb_comid"), ("terminalpa", "terminal_path")]

    for i, (table, fields) in enumerate(zip((gridcode_table, flow_lines, vaa_table, flow_table), extract_fields)):
        new_table = read_dbf(table)[fields]
        if fields[0] != "comid":
            new_table = new_table.rename(columns={fields[0]: 'comid'})
        flow_table = pd.merge(flow_table, new_table, how='outer', on='comid')

    # Rename fields and filter out COMID = 0
    flow_table = flow_table.rename(columns=dict(rename_fields))[flow_table.comid > 0]

    return flow_table


def add_erom_data(erom_dir):
    # Read all monthly EROM tables
    master_table = None
    months = list(map(str, range(1, 13))) + ['ma']
    for month in months:
        table_path = os.path.join(erom_dir, "EROM_{}0001.dbf".format(month.zfill(2)))
        fields = ["comid", "q0001e", "v0001e"] if month == 'ma' else ["comid", "q0001e"]
        erom_table = read_dbf(table_path)[fields]
        erom_table.columns = [c.replace("0001e", month) for c in erom_table.columns]
        if master_table is None:
            master_table = erom_table
        else:
            master_table = pd.merge(master_table, erom_table, on='comid')

    return master_table


def calculate_attributes(table):

    months = list(map(str, range(1, 13)))

    # Convert units and calculate travel times
    table['length'] = table.lengthkm * 1000.  # km -> m
    for month in months:
        table["q{}".format(month)] *= 2446.58  # cfs -> cmd
    table["vma"] *= 26334.7  # f/s -> md
    table["travel_time".format(month)] = table.length / table.vma

    # Calculate surface area
    stream_channel_a = 4.28
    stream_channel_b = 0.55
    cross_section = table.qma / table.vma
    table['surface_area'] = stream_channel_a * np.power(cross_section, stream_channel_b)

    # Indicate whether reaches are coastal
    table['coastal'] = np.int16(table.fcode == 56600)
    del table['fcode'], table['vma'], table['lengthkm']

    return table


def main():
    out_dir = os.path.join("..", "bin", "Preprocessed", "CondensedNHD")
    overwrite = True
    for region, region_dir in get_nhd().items():
        print(region)

        import time

        start = time.time()
        # Set paths
        flow_table = os.path.join(region_dir, "NHDPlusAttributes", "PlusFlow.dbf")
        flow_lines = os.path.join(region_dir, "NHDSnapshot", "Hydrography", "NHDFlowline.dbf")
        vaa_table = os.path.join(region_dir, "NHDPlusAttributes", "PlusFlowlineVAA.dbf")
        gridcode_table = os.path.join(region_dir, "NHDPlusCatchment", "featureidgridcode.dbf")
        erom_dir = os.path.join(region_dir, "EROMExtension")
        output_flow_file = os.path.join(out_dir, "region_{}.npz".format(region))

        if overwrite or not os.path.exists(output_flow_file):

            # Extract data
            nodes = sever_divergences(flow_table, vaa_table)

            attribute_table = extract_tables(nodes, flow_lines, vaa_table, gridcode_table)

            erom_table = add_erom_data(erom_dir)

            # Merge and save
            region_table = pd.merge(attribute_table, erom_table, on='comid', how='outer')
            region_table = calculate_attributes(region_table)
            np.savez_compressed(output_flow_file, table=region_table.as_matrix(), key=region_table.columns.tolist())

main()