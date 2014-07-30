"""
File: summarize_sam.py
Author: James (Trip) Hook III
Date: 7/18/2014

Takes SAM output files and summarizes them by user-specified concentration and exceedence metrics.  Writes tables and
shapefiles containing summary data
"""

import glob
import datetime
import os
import csv
import sys
import itertools
import shapefile
import math
import re
import getopt

from __builtin__ import max

def clear_tables(d, files):
    del_files = [os.path.join(d, f) for f in os.listdir(d) if f.split(".")[0] in files]
    for f in del_files:
        os.remove(f)
    print "Removed {} existing files".format(len(del_files))


def get_parameters(parameter_file):
    """
    Reads parameters from an external parameter file and modifies them for processing as necessary
    :param parameter_file: External parameter file
    :return: Dictionary containing parameter names and values
    """
    with open(parameter_file, 'rb') as f:
        params = [[x.strip() for x in line.split("-")] for line in f if "-" in line]
    if not set(map(len, params)) == {2}:
        sys.exit("Error reading parameters")
    else:
        params = dict(params)
    for key in 'operations', 'conc_intervals', 'exp_intervals', 'infile_header', 'exp_percentiles':
        params[key] = params[key].split(",")
    for key in 'concentration', 'exceedance', 'write_shapefile', 'write_csv', 'overwrite':
        params[key] = bool(params[key])
    for key in 'conc_intervals', 'exp_intervals', 'exp_percentiles':
        params[key] = map(int, params[key])
    params['threshold'] = int(params['threshold'])
    params['files'] = glob.glob(os.path.join(params['in_dir'], params['file_flag']))
    month, day, year = map(int, params['julian_start'].split("/"))
    params['julian_start'] = datetime.datetime(year, month, day)
    params['operations'] = map(lambda x: globals()[x.strip()], params['operations'])
    params['conc_combinations'] = [(i, o) for o in params['operations'] for i in params['conc_intervals']]
    params['exp_combinations'] = [(i, o) for o in params['exp_percentiles'] for i in params['exp_intervals']]
    return params


def mean(iterable):
    """Returns an average value for an iterable
    :param iterable: Iterable (list or set) to be averaged
    """
    return float(sum(iterable)) / float(len(iterable))


def n_grams(dates, window):
    """Creates a 'moving window' of dates from a given range and window size
    :param dates: Set of all dates from which to create the moving window
    :param window: Window size
    """
    return zip(*[itertools.islice(dates, d, None) for d in range(window)])


def read_file(in_file, julian_start, infile_header):
    """
    Reads a SAM output file
    :param in_file: SAM output file
    :param julian_start: Day one of the julian calendar used by SAM
    :param infile_header: List of field names in the SAM output file
    :return: Dictionary of output value for each day in format {date: value}
    """
    with open(in_file, 'rb') as f:
        csv_obj = ((re.sub(' +', " ", line).replace(" ", ",")[1:] for line in f))
        reader = csv.DictReader(csv_obj, infile_header, delimiter=',')
        for i in range(3):
            reader.next()
        records = {julian_start + datetime.timedelta(days=int(line["JulianDate"])): line for line in reader}
    return records


def summarize_exceedance(subset, attr, threshold):
    """
    Summarizes the frequency and duration of exceedences of the given threshold within the given subset
    :param subset: Subset of data read from SAM output file, limited to a given year with format {date: value}
    :param attr: Attribute to be read from record (typically "AvgC")
    :param threshold: Number above which an exceedance is recorded
    :return:
    """
    output_attributes = ("exceed_tox_num", "exceed_tox_pct", "exceed_tox_max_dur", "exceed_tox_avg_dur")
    output_values = (0, 0, 0, 0)
    exceedances = {d for d, v in subset.iteritems() if v[attr] and float(v[attr]) > threshold}
    exceedance_lengths = []
    if exceedances:
        for k, g in itertools.groupby(enumerate(sorted(exceedances)), lambda (i, x): x - datetime.timedelta(days=i)):
            exceedance_lengths.append(len([h[1] for h in g]))
        output_values = len(exceedances), (float(len(exceedances)) / float(len(subset))) * 100, \
                        max(exceedance_lengths), float(sum(exceedance_lengths)) / float(len(exceedance_lengths))
    return dict(zip(output_attributes, output_values))


def summarize_concentration(subset, attr, run_combinations):
    """
    Summarizes concentration data based on specified combinations of attribute (typically AvgC), operation (typically
    'max' or 'mean'), and interval (typically 1, 30, or 365 days)
    :param subset: Subset of data read from SAM output file, limited to a given year with format {date: value}
    :param run_combinations: A set of tuples containing the attribute, operation, and interval to be run
    :return: Returns a dictionary with format {Output Filename: Value}
    """
    out = {}
    for ivl, op in run_combinations:
        run_id = "{}_{}d_{}".format(attr, ivl, op.__name__)
        out[run_id] = 'nan'
        if len(subset) > ivl:
            out[run_id] = op([sum((float(subset[day][attr]) for day in period if subset[day][attr])) / ivl
                              for period in n_grams(subset.keys(), ivl)])
    return out


def summarize_exposure(subset, attr, run_combinations):
    """
    Summarizes concentration data based on specified combinations of attribute (typically AvgC), operation (typically
    'max' or 'mean'), and interval (typically 1, 30, or 365 days)
    :param subset: Subset of data read from SAM output file, limited to a given year with format {date: value}
    :param run_combinations: A set of tuples containing the attribute, operation, and interval to be run
    :return: Returns a dictionary with format {Output Filename: Value}
    """

    def percentile(data, pct):
        index = (float(pct) / 100.0) * len(data)
        floor = int(math.floor(index))
        return data[floor-1] + ((data[floor] - data[floor-1]) * (index - floor))

    out = {}
    for pct, ivl in run_combinations:
        run_id = "{}_{}pct_{}d".format(attr, ivl, pct)
        out[run_id] = 'nan'
        if len(subset) > ivl:
            data = sorted([float(v[attr]) if not math.isnan(float(v[attr])) else -1 for v in subset.values()])
            out[run_id] = percentile(data, pct)
    return out


def write_shapefile(out_map, out_dir, table, bid_field, geom_file):
    """
    Creates a new shapefile or updates an existing shapefile with geometry from a template shapefile matched with
    summarized SAM output data
    :param out_map: Dict of data to be written to file in the form {year1: val, year2: val...}
    :param out_dir: Directory to which output shapefile will be written
    :param table: Filename of output shapefile
    :param bid_field: Field name in input geometry file which matches basin id
    :param geom_file: Shapefile containing geometry to be copied to output file
    """
    output_file = os.path.join(out_dir, table + ".shp")
    if not os.path.exists(output_file):
        print "Writing to file {}...".format(output_file)
        w = shapefile.Writer(shapefile.POLYGON)
        w.field("BasinID", 'C', '20')
        for year in sorted(out_map):
            w.field(year, 'F')
    else:
        w = shapefile.Editor(output_file)
    r = shapefile.Reader(geom_file)
    id_index = [j[0] for j in r.fields].index(bid_field) - 1
    basin_address = {i for i, rec in enumerate(r.iterRecords()) if str(rec[id_index]) == out_map["BasinID"]}
    if basin_address:
        # noinspection PyProtectedMember,PyUnresolvedReferences
        w._shapes.extend([r.shape(i) for i in basin_address])
        for _ in basin_address:
            w.record(**out_map)
        w.save(output_file)
    else:
        print "No matches between basin ID's and shapefile - examine basin ID field values"
    del w, r


def write_table(out_map, out_dir, table):
    """
    Writes summarized SAM output data to a csv table
    :param out_map: Dict of data to be written to file in the form {year1: val, year2: val...}
    :param out_dir: Directory to which output shapefile will be written
    :param table: Filename of output table
    """
    output_file = os.path.join(out_dir, table + ".csv")
    mode = 'a' if os.path.exists(output_file) else 'wb'
    with open(output_file, mode) as f:
        writer = csv.DictWriter(f, sorted(out_map.keys()), 'nan', "ignore")
        if mode == 'wb':
            print "Writing to file {}...".format(output_file)
            writer.writeheader()
        writer.writerow(out_map)


def main(argv):
    """Main body of script"""
    # parameter_file = r"C:\Models\Python_Scripts\parameters_v2_mmf.txt"
    parameter_file = ''
    try:
        opts, args = getopt.getopt(argv,"hi:",["input="])
    except getopt.GetoptError:
        print 'summarize_sam.py -i <inputfile>'
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print 'test.py -i <inputfile> -o <outputfile>'
            sys.exit()
        elif opt in ("-i", "--input"):
            parameter_file = arg
    p = get_parameters(parameter_file)
    for i, h in enumerate(iter(p['files'])):
        basin = os.path.basename(h).split("_")[0]
        print "Processing basin {} ({}/{})...".format(basin, i+1, len(p['files']))
        record = read_file(h, p['julian_start'], p['infile_header'])
        output = {}
        intervals = sorted({('year', d.year) for d in record}) if p['annual'] else []
        intervals += sorted({('month', d.month) for d in record}) if ['monthly'] else []
        for type, interval in intervals:
            key = "{}{}".format(type[0], interval)
            subset = {date: val for date, val in record.iteritems() if getattr(date, type) == interval}
            output[key] = summarize_concentration(subset, "AvgC", p['conc_combinations']) if p['concentration'] else []
            output[key].update(summarize_exceedance(subset, "AvgC", p['threshold']) if p['exceedance'] else {})
            output[key].update(summarize_exposure(subset, "AvgC", p['exp_combinations'] if p['exposure'] else {}))
        tables = {t for k in output for t in output[k]}
        if p['overwrite'] and not i:
            clear_tables(p['out_dir'], tables)
        for table, out_map in ((t, {k: output[k][t] for k in output}) for t in tables):
            out_map["BasinID"] = basin
            if p['write_csv']:
                write_table(out_map, p['out_dir'], table)
            # if p['write_shapefile']:
            #     write_shapefile(out_map, p['out_dir'], table, p['shp_key'], p['in_shp'])


if __name__ == "__main__":
    main(sys.argv[1:])
