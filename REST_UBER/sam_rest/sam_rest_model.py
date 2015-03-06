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

    update_mongo(temp_sam_run_path, jid, run_type)

    shutil.rmtree(temp_sam_run_path)


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
                pool = Pool(max_workers=1)

                sam_path = os.path.join(curr_path, 'bin', 'ubertool_superprzm_src', 'Debug', exe)
                print sam_path
                # Define SuperPRZMpesticide.exe command line arguments
                sam_arg1 = os.path.join(curr_path, 'bin')     # Absolute path to "root" of SAM model
                sam_arg2 = name_temp                          # Temp directory name for SAM run
                # Create list of args
                args = [sam_path, sam_arg1, sam_arg2]

                future = pool.submit(subprocess.call, args)
                # When the Fortran exe finishes call "sam_callback" callback function
                future.add_done_callback(partial(sam_callback, temp_sam_run_path, jid, run_type))
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
                    pool = Pool(max_workers=1)

                    sam_path = os.path.join(curr_path, 'bin', 'ubertool_superprzm_src', 'Debug', exe)
                    print sam_path
                    # Define SuperPRZMpesticide.exe command line arguments
                    sam_arg1 = os.path.join(curr_path, 'bin')     # Absolute path to "root" of SAM model
                    sam_arg2 = name_temp                          # Temp directory name for SAM run
                    # Create list of args
                    args = sam_path + " " + sam_arg1 + " " + sam_arg2

                    future = pool.submit(subprocess.call, args)
                    # When the Fortran exe finishes call "sam_callback" callback function
                    future.add_done_callback(partial(sam_callback, temp_sam_run_path, jid, run_type))
                    # Destroy the Pool object which hosts the threads
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
