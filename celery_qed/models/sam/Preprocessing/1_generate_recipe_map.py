import os
import numpy as np
import pandas as pd
from collections import defaultdict


def identify_local(recipe_path):
    import re

    local_dir = os.path.dirname(recipe_path)
    file_format = os.path.basename(recipe_path)
    regex_format = file_format.replace("{}", "(.+?)")
    locals_dict = defaultdict(dict)
    for f in os.listdir(local_dir):
        match = re.match(regex_format, f)
        if match:
            comid, year = match.groups()
            locals_dict[comid][year] = os.path.join(local_dir, f)
    return locals_dict


def max_scenarios(local_sets):
    sizes = {os.stat(_file).st_size: _file for pair in local_sets.values() for _file in pair.values()}
    biggest_file = sizes[max(sizes.keys())]
    with open(biggest_file) as f:
        n_lines = len(f.readlines())
    return n_lines


def make_table(local_sets, outfile, scenario_matrix, n_scenarios):
    # Read scenario matrix keyfile so that scenario indices match up between matrix and map
    matrix_key = scenario_matrix + "_key.txt"
    with open(matrix_key) as f:
        *_, scenarios = (next(f).strip().split(",") for _ in range(3))
    scenario_dict = dict(zip(scenarios, np.arange(len(scenarios))))
    recipes = list(local_sets.keys())
    years = sorted({year for local_set in local_sets.values() for year in local_set.keys()})
    n_years = len(years)
    out_shape = (len(recipes) * n_years, n_scenarios, 2)
    array = np.memmap(outfile + ".dat", dtype=np.int32, mode='w+', shape=out_shape)
    key = np.zeros(len(recipes) * n_years + 1, dtype=(int, 2))
    for i, recipe_id in enumerate(recipes):
        if not i % 100:
            print(i)
        for j, year in enumerate(years):
            try:
                recipe_file = local_sets[recipe_id][year]
            except KeyError:
                pass
            else:
                data = pd.read_csv(recipe_file).as_matrix()
                if data.shape[0]:
                    data[:, 0] = np.vectorize(lambda x: scenario_dict.get(x, -1))(data[:, 0])
                    counter = (i * n_years) + j
                    columns = data.shape[0]
                    array[counter, :columns] = data
                    key[counter] = ((recipe_id, year))
    key[-1] = n_scenarios

    # Write key to file
    keyfile = outfile + "_key"
    np.save(keyfile, key)


def main():
    scenario_matrix = r"..\bin\Preprocessed\Scenarios\mark_twain"
    recipe_path = r"..\bin\Preprocessed\Recipes\MTB\nhd_recipe_{}_{}.txt"
    output_file = os.path.join(r"..\bin\Preprocessed\InputMaps", "mtb_map1")

    # Identify all recipe files, indexed by recipe ID and year
    local_sets = identify_local(recipe_path)
    n_scenarios = max_scenarios(local_sets)
    make_table(local_sets, output_file, scenario_matrix, n_scenarios)


main()