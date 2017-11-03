import os
import numpy as np

from Tool.functions import HydroTable
from Preprocessing.utilities import nhd_states


def extract_flow_data(nhd_table, out_table):

    # Specify fields to extract
    use_fields = ["comid", "surface_area"] + ["q{}".format(month) for month in range(1, 13)]

    # Extract fields
    flow_table = nhd_table[use_fields]

    # Save to file
    np.savez_compressed(out_table, table=flow_table.as_matrix(), key=flow_table.columns.tolist())


def main():
    condensed_nhd_path = os.path.join("..", "bin", "Preprocessed", "CondensedNHD")
    output_path = os.path.join("..", "bin", "Preprocessed", "FlowFiles")

    for region in nhd_states.keys():
        nhd_table = HydroTable(region, condensed_nhd_path)
        out_table = os.path.join(output_path, "region_{}.npz".format(region))
        extract_flow_data(nhd_table, out_table)

if __name__ == "__main__":
    main()
