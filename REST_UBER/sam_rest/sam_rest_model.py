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


##########################################################################################
#####AMAZON KEY, store output files. You might have to write your own import approach#####
##########################################################################################
key = keys_Picloud_S3.amazon_s3_key
secretkey = keys_Picloud_S3.amazon_s3_secretkey
##########################################################################################    
##########################################################################################


from functools import wraps
import time
def timefn(fn):
    """
    Decorator to time methods
    :rtype : object
    :param fn:
    :return:
    """
    @wraps(fn)
    def measure_time(*args, **kwargs):
        t1 = time.time()
        result = fn(*args, **kwargs)
        t2 = time.time()
        print ("@timefn:" + fn.func_name + " took " + str(t2 - t1) + " seconds")
        return result
    return measure_time


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


def update_mongo(temp_sam_run_path, jid, run_type):
    """
    sam_input_file_path: String; Absolute path to SAM output temporary directory
    jid: String; SAM run jid
    run_type: String; SAM run type ('single', 'qaqc', or 'batch')

    Saves SAM output and SAM.inp to MongoDB.
    """

    logging.info("update_mongo() executed!")
    import pymongo
    client = pymongo.MongoClient('localhost', 27017)
    db = client.ubertool

    """
        This needs to be updated to handle all Output Post-Processing types
    """
    try:
        logging.info("Trying to open Eco_mth_avgdur.out file")
        f_out = open(os.path.join(temp_sam_run_path, "EcoPestOut_all", "EcoPestOut_UpdatedGUI", "Test1", "Eco_mth_avgdur.out"), 'r')
        logging.info("Eco_mth_avgdur.out opened!")
        sam_output = f_out.read()

        logging.info("Trying to open SAM.inp file")
        f_input = open(os.path.join(temp_sam_run_path, "SAM.inp"), 'r')
        logging.info("SAM.inp opened!")
        sam_input = f_input.read()

    except Exception, e:
        logging.exception(e)
        sam_output = "Error reading SAM output file"
        sam_input = "Error reading SAM input file"
   
    document = {
        "user_id": "admin",
        "_id": jid,
        "run_type": run_type,
        "model_object_dict": {
            'filename': "Eco_mth_avgdur.out",
            'output': sam_output,
            'input': sam_input
        }
    }
    db['sam'].save(document)


def split_csv(number, curr_path):
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

    if number > 9:
        number = 9
    if number < 1:
        number = 1

    try:
        rows_per_sect = df.shape[0] / number
        print rows_per_sect
        print type(rows_per_sect)
    except:
        number = 1
        rows_per_sect = df.shape[0] / number

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
            curr_path, 'bin', 'EcoRecipes_huc12', 'recipe_combos2012', 'huc12_outlets_metric_' + str(i) + '.csv'
        ), index=False)

        i += 1


def sam_callback(temp_sam_run_path, jid, run_type, future):
    """
    temp_sam_run_path: String; Absolute path to SAM output temporary directory
    jid: String; SAM run jid
    run_type: String; SAM run type ('single', 'qaqc', or 'batch')
    future: concurrent.Future object; automatically passed in from concurrent.Future.add_done_callback()

    Callback function for when SuperPRZMPestide.exe has completed. 
    Calls update_mongo() to insert output file into MongoDB. 
    Deletes SAM output temporary directory.
    """
    logging.info("temp_sam_run_path = %s" %temp_sam_run_path)
    logging.info("jid = %s" %jid)
    logging.info("run_type = %s" %run_type)

    # update_mongo(temp_sam_run_path, jid, run_type)

    # shutil.rmtree(temp_sam_run_path)

@timefn
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
    returns: String (HTML); SAM.inp formatted in HTML.

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
        # Run SAM, but first generate SAM input file        

        try:
            no_of_workers = int(args['workers'])
        except:
            no_of_workers = 1

        print no_of_workers

        try:
            # Create temporary dir based on "name_temp" to store SAM run input file and outputs
            curr_path = os.path.abspath(os.path.dirname(__file__))
            temp_sam_run_path = os.path.join(curr_path, 'bin', name_temp)
            if not os.path.exists(temp_sam_run_path):
                os.makedirs(temp_sam_run_path)
                os.makedirs(os.path.join(temp_sam_run_path, 'EcoPestOut_all', 'EcoPestOut_UpdatedGUI', 'Test1'))

            sam_input_file_path = os.path.join(temp_sam_run_path, 'SAM.inp')

            # Generate "SAM.inp" file
            import sam_input_generator
            sam_input_generator.generate_sam_input_file(args, sam_input_file_path)
            
            # Set "SuperPRZMpesticide.exe" based on OS
            if os.name == 'posix':
                print "Linux OS"
                # Linux / UNIX based OS
                exe = "SuperPRZMpesticide.exe"
                
                import subprocess32 as subprocess    # Use subprocess32 for Linux (Python 3.2 backport)
                from concurrent.futures import ThreadPoolExecutor as Pool
                from functools import partial

                # Create ThreadPoolExecutor (as 'Pool') instance to store threads which execute Fortran exe as subprocesses
                pool = Pool(max_workers=no_of_workers)

                sam_path = os.path.join(curr_path, 'bin', 'ubertool_superprzm_src', 'Debug', exe)
                print sam_path
                # Define SuperPRZMpesticide.exe command line arguments
                sam_arg1 = os.path.join(curr_path, 'bin')     # Absolute path to "root" of SAM model
                sam_arg2 = name_temp                          # Temp directory name for SAM run
                # Create list of args
                args = [sam_path, sam_arg1, sam_arg2, "1"]

                split_csv(no_of_workers, curr_path)

                i = 1
                while i <= no_of_workers:
                    args[3] = str(i)
                    print args
                    pool.submit(subprocess.call, args).add_done_callback(
                        partial(sam_callback, temp_sam_run_path, jid, run_type)
                    )
                    i += 1

                # Destroy the Pool object which hosts the threads
                pool.shutdown(wait=False)

            else:
                print "Windows (really NOT Linux) OS"
                # Assuming Windows here, could be other tho and this will break
                exe = "SuperPRZMpesticide_win.exe"
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
                    # sam_arg3 = "2"
                    # Create list of args
                    # args = sam_path + " " + sam_arg1 + " " + sam_arg2# + " " + sam_arg3
                    # args = sam_path + " " + sam_arg1 + " " + sam_arg2
                    args = [sam_path, sam_arg1, sam_arg2, "1"]

                    split_csv(no_of_workers, curr_path)


                    args_dict = {}

                    for x in range(no_of_workers):

                        args_dict[x + 1] = [sam_path, sam_arg1, sam_arg2, str(x + 1)]

                        # args[3] = str(x + 1)
                        # args_dict[x + 1] = args
                        # print args
                        print args_dict[x + 1]
                    # print args_dict
                    j = 1
                    while j <= no_of_workers:
                        pool.submit(subprocess.call, args_dict[j]).add_done_callback(
                            partial(sam_callback, temp_sam_run_path, jid, run_type)
                        )
                        j += 1
                        # pool.submit(subprocess.call, args + " " + str(i)).add_done_callback(
                        #     partial(sam_callback, temp_sam_run_path, jid, run_type)
                        # )
                        # i += 1

                    # future1 = pool.submit(subprocess.call, args + " 1")
                    # future2 = pool.submit(subprocess.call, args + " 2")
                    # future3 = pool.submit(subprocess.call, args + " 3")
                    # future4 = pool.submit(subprocess.call, args + " 4")
                    # future5 = pool.submit(subprocess.call, args + " 5")
                    # future6 = pool.submit(subprocess.call, args + " 6")
                    # future7 = pool.submit(subprocess.call, args + " 7")
                    # future8 = pool.submit(subprocess.call, args + " 8")
                    # future9 = pool.submit(subprocess.call, args + " 9")
                    # # When the Fortran exe finishes call "sam_callback" callback function
                    # future1.add_done_callback(partial(sam_callback, temp_sam_run_path, jid, run_type))
                    # future2.add_done_callback(partial(sam_callback, temp_sam_run_path, jid, run_type))
                    # future3.add_done_callback(partial(sam_callback, temp_sam_run_path, jid, run_type))
                    # future4.add_done_callback(partial(sam_callback, temp_sam_run_path, jid, run_type))
                    # future5.add_done_callback(partial(sam_callback, temp_sam_run_path, jid, run_type))
                    # future6.add_done_callback(partial(sam_callback, temp_sam_run_path, jid, run_type))
                    # future7.add_done_callback(partial(sam_callback, temp_sam_run_path, jid, run_type))
                    # future8.add_done_callback(partial(sam_callback, temp_sam_run_path, jid, run_type))
                    # future9.add_done_callback(partial(sam_callback, temp_sam_run_path, jid, run_type))

                    # Destroy the Pool object which hosts the threads, but do not wait for the threads to finish
                    pool.shutdown(wait=False)

                except Exception, e:
                    logging.exception(e)

                    """
                    Don't actually run SAM, just delay a few seconds...
                    """
                    future = pool.submit(subprocess.Popen, "timeout 3")


            input_file_html = convert_text_to_html(sam_input_file_path)

            return input_file_html


        except Exception, e:
            logging.exception(e)
            return {'user_id':'admin', 'result': {'error': str(e)}, '_id':jid}
    else:
        logging.info('++++++++++++ E L S E ++++++++++++')
        # Canned model run; do not run SAM
        return {'user_id':'admin', 'result': ["https://s3.amazonaws.com/super_przm/SAM_IB2QZS.zip"], '_id':jid}
