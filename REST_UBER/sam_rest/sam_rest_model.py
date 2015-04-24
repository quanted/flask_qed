#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import zipfile
import shutil
from boto.s3.connection import S3Connection
from boto.s3.key import Key
from boto.s3.bucket import Bucket
import string
import random
import keys_Picloud_S3
import json
import logging
import sam_db

done_list = []
huc_output = {} # Dictionary to hold output data

##########################################################################################
#####AMAZON KEY, store output files. You might have to write your own import approach#####
##########################################################################################
key = keys_Picloud_S3.amazon_s3_key
secretkey = keys_Picloud_S3.amazon_s3_secretkey
##########################################################################################
##########################################################################################


def sam(inputs_json, jid, run_type):
    """
    inputs_json; String (JSON);
    jid: String; SAM run jid
    run_type: String; SAM run type ('single', 'qaqc', or 'batch')

    SAM model run entry point.  Determines if run is to be pre-canned (demo)
    or an actual SuperPRZMpesticide.exe run.

    If pre-canned:
    returns: dict; Filled with dummy values.

    If actual run:
    returns: String; "jid"

    Actual run launches SuperPRZMPesticide after determining which OS is being used
    in a separate process.  A Futures object is created and when the process is finished
    executing (SAM completes or is killed) a callback function is fired (sam_callback()).
    The callback function stores the output and input file into MongoDB for later
    retrieval.
    """
    args = json.loads(inputs_json)

    # Generate random name for current run
    name_temp = id_generator()
    print name_temp

    # Custom or pre-canned run?
    if args['scenario_selection'] == '0':
        logging.info('++++++++++++ C U S T O M ++++++++++++')
        # Run SAM
        try:
            no_of_workers = int(args['workers'])
        except:
            no_of_workers = 1
        try:
            no_of_processes = no_of_workers * int(args['processes'])
        except:
            no_of_processes = no_of_workers

        empty_global_output_holders()

        try:
            # Create temporary dir based on "name_temp" to store SAM run input file and outputs
            curr_path = os.path.abspath(os.path.dirname(__file__))
            temp_sam_run_path = os.path.join(curr_path, 'bin', name_temp)
            if not os.path.exists(temp_sam_run_path):
                print "Creating SAM run temporary directory: ",\
                    str(temp_sam_run_path)
                os.makedirs(temp_sam_run_path)
                print "Creating SAM run temporary sub-directory: ",\
                    str(os.path.join(temp_sam_run_path, 'output'))
                os.makedirs(os.path.join(temp_sam_run_path, 'output'))
                #     str(os.path.join(temp_sam_run_path, 'EcoPestOut_all', 'EcoPestOut_UpdatedGUI', 'Test1'))
                # os.makedirs(os.path.join(temp_sam_run_path, 'EcoPestOut_all', 'EcoPestOut_UpdatedGUI', 'Test1'))

            sam_input_file_path = os.path.join(temp_sam_run_path, 'SAM.inp')

            # Generate "SAM.inp" file
            import sam_input_generator
            sam_input_generator.generate_sam_input_file(args, sam_input_file_path)

            for x in range(no_of_workers):
                shutil.copyfile(sam_input_file_path, os.path.join(temp_sam_run_path, 'SAM' + two_digit(x) + '.inp'))

            # Set "SuperPRZMpesticide.exe" based on OS
            if os.name == 'posix':
                print "Linux OS"
                # Linux / UNIX based OS
                exe = "SuperPRZMpesticide.exe"
            else:
                print "Windows (really NOT Linux/POSIX) OS"
                # Assuming Windows here, could be other tho and this will break
                exe = "SuperPRZMpesticide_win.exe"

            try:
                import subprocess32 as subprocess    # Use subprocess32 for Linux (Python 3.2 backport)
            except ImportError:
                import subprocess

            try:

                from concurrent.futures import ThreadPoolExecutor as Pool
                from functools import partial

                # Create ThreadPoolExecutor (as 'Pool') instance to store threads which execute Fortran exe as subprocesses
                pool = Pool(max_workers=no_of_workers)

                sam_path = os.path.join(curr_path, 'bin', 'ubertool_superprzm_src', 'Debug', exe)
                print sam_path
                # Define SuperPRZMpesticide.exe command line arguments
                sam_arg1 = os.path.join(curr_path, 'bin')     # Absolute path to "root" of SAM model
                sam_arg2 = name_temp                          # Temp directory name for SAM run

                # Divide master HUC CSV into subsets for current run
                split_csv(no_of_processes, curr_path, name_temp)

                for x in range(no_of_processes):

                    print [sam_path, sam_arg1, sam_arg2, two_digit(x)]
                    pool.submit(subprocess.call,
                        [sam_path, sam_arg1, sam_arg2, two_digit(x)]
                    ).add_done_callback(
                        partial(sam_callback, temp_sam_run_path, jid, run_type, no_of_processes, args, two_digit(x))
                    )

                # Destroy the Pool object which hosts the threads when the pending Futures objects are finished,
                # but do not wait until all Futures are done to have this function return
                pool.shutdown(wait=False)

            except ImportError, e:
                logging.exception(e)

                """
                Don't actually run SAM, just delay a few seconds...
                """
                pool.submit(subprocess.Popen, "timeout 3")

            # Create MongoDB document skeleton for SAM run output
            sam_db.create_mongo_document(jid, run_type, args)

            return jid


        except Exception, e:
            logging.exception(e)
            return { 'user_id': 'admin', 'result': { 'error': str(e) }, '_id': jid }
    else:
        logging.info('++++++++++++ E L S E ++++++++++++')
        # Canned model run; do not run SAM
        return  {'user_id': 'admin', 'result': ["https://s3.amazonaws.com/super_przm/SAM_IB2QZS.zip"], '_id': jid }


def sam_callback(temp_sam_run_path, jid, run_type, no_of_processes, args, section, future):
    """
    temp_sam_run_path: String; Absolute path to SAM output temporary directory
    jid: String; SAM run jid
    run_type: String; SAM run type ('single', 'qaqc', or 'batch')
    future: concurrent.Future object; automatically passed in from concurrent.Future.add_done_callback()

    Callback function for when SuperPRZMPestide.exe has completed.
    Calls update_mongo() to insert output file into MongoDB.
    Deletes SAM output temporary directory.
    """

    if future.done():
        logging.info("Future is done")
        if future.cancelled():
            logging.info("but was cancelled")
        else:
            global huc_output  # Use global (module) variable 'huc_output'
            done_list.append("Done")
            logging.info("Appended 'Done' to list with len = %s", len(done_list))

            if args['output_type'] == '1': # Daily Concentrations
                if len(done_list) == no_of_processes:
                    # Read output files
                    update_global_output_holder(temp_sam_run_path, args, section)
                    sam_db.update_mongo(temp_sam_run_path, jid, run_type, args, section, huc_output)

                    logging.info("jid = %s" %jid)
                    logging.info("run_type = %s" %run_type)
                    logging.info("Last SuperPRZMpesticide process completed")

                    # Remove temporary SAM run directory upon completion
                    shutil.rmtree(temp_sam_run_path)
                    empty_global_output_holders()
                else:
                    pass # Do nothing, wait until all runs are done

            else: # Time-Averaged Concentrations
                if len(done_list) == no_of_processes:
                    # Last SAM run has completed or was cancelled
                    update_global_output_holder(temp_sam_run_path, args, section)
                    sam_db.update_mongo(temp_sam_run_path, jid, run_type, args, section, huc_output)

                    logging.info("jid = %s" %jid)
                    logging.info("run_type = %s" %run_type)
                    logging.info("Last SuperPRZMpesticide process completed")

                    # Remove temporary SAM run directory upon completion
                    shutil.rmtree(temp_sam_run_path)
                    empty_global_output_holders()
                else:
                    update_global_output_holder(temp_sam_run_path, args, section)


##########################################################################################
##########################################################################################
################################# SAM HELPER FUNCTIONS ###################################
##########################################################################################
##########################################################################################

def two_digit(x):
    """
    Convert "1" to "01", etc., up to 9
    :param x:
    :return: String, two digit representation of int
    """
    if x < 9:
        number_string = "0" + str(x + 1)
    else:
        number_string = str(x + 1)

    return number_string

# Generate a random ID for file save
def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for x in range(size))

def convert_text_to_html(sam_input_file_path):
    """
    sam_input_file_path: String; Absolute path to SAM.inp for current run

    returns: String; SAM.inp as HTML, where endline chars are replace with <br>

    Converts SAM.inp from text file to HTML.
    """

    html = "<br><b>SAM.inp created:</b><br>"

    with open(sam_input_file_path) as f:
        html += f.read().replace('\n', '<br>')

    return html

def split_csv(number, curr_path, name_temp):
    """
    Load master CSV for SuperPRZM run as Pandas DataFrame and slice it
    based on the number of Futures objects created to execute it.
    (Currently Fortran is set to accept only a 1 char digit; therefore,
    the max number here is 9)
    :param number: int (1 - 9)
    :param curr_path: String; absolute path to this module
    :return: None
    """

    print "number = ", number
    import pandas as pd
    df = pd.read_csv(os.path.join(
        curr_path, 'bin', 'EcoRecipes_huc12', 'recipe_combos2012', 'huc12_outlets_metric.csv'
    ))

    if number > 99:
        number = 99
    if number < 1:
        number = 1

    try:
        rows_per_sect = df.shape[0] / number
        print rows_per_sect
        print type(rows_per_sect)
    except:
        number = 1
        rows_per_sect = df.shape[0] / number

    os.makedirs(os.path.join(curr_path, 'bin', name_temp, 'EcoRecipes_huc12', 'recipe_combos2012'))
    i = 1
    while i <= number:
        if i == 1:
            print 1
            # First slice
            df_slice = df[:rows_per_sect]
        elif i == number:
            print str(i) + " (last)"
            # End slice: slice to the end of the DataFrame
            df_slice = df[((i - 1) * rows_per_sect):]
        else:
            print i
            # Middle slices (not first or last)
            df_slice = df[((i - 1) * rows_per_sect):i * rows_per_sect]

        df_slice.to_csv(os.path.join(
            curr_path, 'bin', name_temp, 'EcoRecipes_huc12', 'recipe_combos2012', 'huc12_outlets_metric_' + two_digit(i - 1) + '.csv'
        ), index=False)

        i += 1

def empty_global_output_holders():
    # Empty output dictionary if needed
    global huc_output
    if len(huc_output.keys()) is not 0:
        print "huc_output contains keys....it should not, removing them"
        huc_output = {}
    else:
        print "huc_output is an empty dictionary....proceed normally"

    # Empty done_list holder if needed
    global done_list
    if len(done_list) is not 0:
        print "done_list is not empty....it should be, making empty now"
        done_list = []
    else:
        print "done_list is an empty list....proceed normally"

def update_global_output_holder(temp_sam_run_path, args, section):

    """ Set the path to output files based on output preferences
        This should really be handled in the FORTRAN code more reasonably,
        but for now....
    """

    if args['output_type'] == '1': # Daily Concentrations

        output_file_path = os.path.join(
            temp_sam_run_path,
            'output',
        )
        output_files = os.listdir(output_file_path)

        print len(output_files)

        for file in output_files:
            # Read each file in the output directory

            huc_id = file.split('_')[1]
            huc_output[huc_id] = {} # Create empty dictionary for 'huc_id' key in 'huc_output'

            f_out = open(os.path.join(
                output_file_path,
                file
            ), 'r')

            f_out.next() # Skip first line

            for line in f_out: # Loop over lines in output file
                out = [x for x in line.split(' ') if x not in ('', '\n')] # List comprehension: remove '' & '\n'
                huc_output[huc_id][out[0]] = out[1] # Update dictionary with desired line values

            f_out.close()

    else: # Time-Averaged Results

        if args['output_time_avg_option'] == '2': # Toxicity threshold exceedances

            if args['output_tox_thres_exceed'] == '1': # Avg Duration of Exceed (days), by year
                file_out = "Eco_ann_toxfreq_" + section + ".out"

            elif args['output_tox_thres_exceed'] == '2': # Avg Duration of Exceed (days), by year
                file_out = "Eco_mth_toxfreq_" + section + ".out"

            elif args['output_tox_thres_exceed'] == '3': # Avg Duration of Exceed (days), by year
                file_out = "Eco_ann_avgdur_" + section + ".out"

            else: # '4'  Avg Duration of Exceed (days), by month
                file_out = "Eco_mth_avgdur_" + section + ".out"

            try: # Some output files will not be created if there is no crop cover there

                f_out = open(os.path.join(
                    temp_sam_run_path,
                    'output',
                    file_out), 'r')

                f_out.next() # Skip first line

                for line in f_out:
                    line_list = line.split(',')
                    if line_list[0][0] == " ": # If 1st char in first item (HUC #) is "space", replace it with a "0"
                        line_list[0] = '0' + line_list[0][1:]
                    i = 0
                    for item in line_list:
                        line_list[i] = item.lstrip() # Remove whitespace from beginning of string
                        i += 1

                    # Assign HUC id as key and output values as values (list)
                    try:
                        huc_output[line_list[0]] = line_list[1:]

                    except IndexError, e:
                        logging.info(line_list)
                        logging.exception(e)

                f_out.close()

            except IOError, e:
                logging.exception(e)

    print len(huc_output.keys())
