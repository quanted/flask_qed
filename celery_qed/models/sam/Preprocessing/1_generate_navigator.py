import os
import numpy as np

from Tool.functions import HydroTable


def get_nodes(nhd_table):
    nodes = np.int32(nhd_table[["tocomid", "comid"]].as_matrix())
    comids, index = np.unique(nodes.T[1], return_index=True)
    times = nhd_table["travel_time"].as_matrix()[index]
    conversion_dict = dict(zip(comids, np.arange(comids.size)))
    nodes = np.vectorize(lambda x: conversion_dict.get(x, -1))(nodes)

    return nodes, times, conversion_dict


def identify_outlets(nhd_table, conversion_dict):
    # Identify reaches that drain to a coastline or a reach not in the region
    non_coastal = nhd_table[nhd_table.coastal == 0]
    outlets = non_coastal[~non_coastal['tocomid'].isin(non_coastal.comid)].comid.as_matrix()
    outlets = np.vectorize(lambda x: conversion_dict.get(x))(outlets)

    return outlets


def upstream_trace(nodes, outlets, attributes=np.array([]), max_length=3000, max_paths=500000):
    n_attributes = attributes.shape[0]

    # Output arrays
    all_paths = np.zeros((max_paths, max_length), dtype=np.int32)
    all_attributes = np.zeros((n_attributes, max_paths, max_length), dtype=np.float)

    # Bounds
    path_cursor = 0
    longest_path = 0

    for index, start_node in enumerate(outlets):

        # Reset everything except the master. Trace is done separately for each outlet
        # Holders
        queue = np.zeros((nodes.shape[0], 2), dtype=np.int32)
        active_reach = np.zeros(max_length, dtype=np.int32)
        active_attributes = np.zeros((n_attributes, max_length), dtype=np.float)

        # Cursors
        start_cursor = 0
        queue_cursor = 0
        active_reach_cursor = 0
        active_node = start_node

        while True:
            upstream = nodes[nodes[:, 0] == active_node]
            active_reach[active_reach_cursor] = active_node
            for i, attribute_array in enumerate(attributes):
                active_attributes[i, active_reach_cursor] = attribute_array[active_node]
            active_reach_cursor += 1
            if active_reach_cursor > longest_path:
                longest_path = active_reach_cursor
            if upstream.size:
                active_node = upstream[0][1]
                for j in range(1, upstream.shape[0]):
                    queue[queue_cursor] = upstream[j]
                    queue_cursor += 1
            else:
                all_paths[path_cursor, start_cursor:] = active_reach[start_cursor:]
                for i in range(n_attributes):
                    all_attributes[i, path_cursor] = np.cumsum(active_attributes[i]) * (all_paths[path_cursor] > 0)
                queue_cursor -= 1
                path_cursor += 1
                last_node, active_node = queue[queue_cursor]
                if not any((last_node, active_node)):
                    break
                active_reach_cursor = np.where(active_reach == last_node)[0][0] + 1
                start_cursor = active_reach_cursor
                active_reach[active_reach_cursor:] = 0.
                for i in range(n_attributes):
                    active_attributes[i, active_reach_cursor:] = 0.

    return all_paths[:path_cursor, :longest_path + 1], all_attributes[:, :path_cursor, :longest_path + 1]


def map_paths(paths):
    # Get starting row and column for each value
    column_numbers = np.tile(np.arange(paths.shape[1]) + 1, (paths.shape[0], 1)) * (paths > 0)
    path_begins = np.argmax(column_numbers > 0, axis=1)
    max_reach = np.max(paths)
    path_map = np.zeros((max_reach + 1, 3))
    n_paths = paths.shape[0]
    for i, path in enumerate(paths):
        for j, val in enumerate(path):
            if val:
                if i == n_paths:
                    end_row = 0
                else:
                    next_row = (path_begins[i + 1:] <= j)
                    if next_row.any():
                        end_row = np.argmax(next_row)
                    else:
                        end_row = n_paths - i - 1
                values = np.array([i, i + end_row + 1, j])
                path_map[val] = values

    return path_map


def collapse_array(paths, attribute_matrix):
    out_paths = []
    out_attributes = [[] for _ in range(attribute_matrix.shape[0])]
    path_starts = []
    for i, row in enumerate(paths):
        active_path = (row > 0)
        path_starts.append(np.argmax(active_path))
        out_paths.append(row[active_path])
        for j in range(attribute_matrix.shape[0]):
            out_attributes[j].append(attribute_matrix[j][i][active_path])
    out_attributes = np.array(out_attributes)
    return np.array(out_paths), np.array(out_attributes), np.array(path_starts)


def write_outfile(outfile, paths, path_map, conversion_array, times):
    np.savez_compressed(outfile, paths=paths, path_map=path_map, alias_index=conversion_array, time=times)


def dict_to_array(cd):
    comids, aliases = map(np.array, zip(*cd.items()))
    out_array = np.zeros(max(aliases) + 1)
    out_array[aliases[aliases > 0]] = comids[aliases > 0]
    return out_array


def main():
    from Preprocessing.utilities import nhd_states

    # Set parameters
    overwrite = True

    # Set initial paths
    nhd_path = os.path.join("..", "bin", "Preprocessed", "CondensedNHD")
    output_path = os.path.join(r"..\bin\Preprocessed\Navigators", "region_{}.npz")

    # Loop through regions
    for region in nhd_states.keys():

        print(region)

        # Designate paths
        nhd_table = HydroTable(region, nhd_path)

        nodes, times, conversion_dict = get_nodes(nhd_table)
        attributes = np.array([times])

        outlets = identify_outlets(nhd_table, conversion_dict)

        paths, attribute_matrix = upstream_trace(nodes, outlets, attributes)

        path_map = map_paths(paths)

        paths, attribute_matrix, start_cols = collapse_array(paths, attribute_matrix)

        conversion_array = dict_to_array(conversion_dict)

        write_outfile(output_path.format(region), paths, path_map, conversion_array, attribute_matrix[0])

main()