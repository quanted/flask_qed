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


def sam_read_input_file(sam_input_file_path):

    html = "<br><b>SAM.inp created:</b><br>"

    with open(sam_input_file_path) as f:
        html += f.read().replace('\n', '<br>')

    return html


# def s3_upload(temp_sam_run_path):

#     sam_output_zip = os.path.join(temp_sam_run_path, "sam_output.zip")
#     print sam_output_zip
#     zf = zipfile.ZipFile(sam_output_zip, "w", zipfile.ZIP_DEFLATED)
#     for dirname, subdirs, files in os.walk(temp_sam_run_path):
#         zf.write(dirname)
#         for filename in files:
#             if filename != "sam_output.zip":
#                 zf.write(os.path.join(dirname, filename))
#     zf.close()
    
    # try:
    #     # Connect to S3 bucket, create key and set value to zip file
    #     conn = S3Connection(key, secretkey, is_secure=False)
    #     bucket = Bucket(conn, 'super_przm')
    #     k = Key(bucket)
        
    #     name1 = 'SAM_'+name_temp+'.zip'
    #     k.key = name1
    #     k.set_contents_from_filename(sam_output_zip)
    #     link = 'https://s3.amazonaws.com/super_przm/' + name1
    #     k.set_acl('public-read-write')
    #     print link

    #     return link

    # except Exception, e:
    #     print "Upload failed"
    #     print "Error: ", str(e)

    #     return False


def update_mongo(run_type, jid):

    import pymongo
    client = pymongo.MongoClient('localhost', 27017)
    db = client.ubertool

    """
        This needs to be updated to handle all Output Post-Processing types
    """
    try:
        logging.info("Trying to open Eco_mth_avgdur.out file")
        f = open(os.path.join(temp_sam_run_path, "EcoPestOut_all", "EcoPestOut_UpdatedGUI", "Test1", "Eco_mth_avgdur.out"), 'r')
        output = f.read()

    except Exception, e:
        logging.info("Error: ", str(e))
        output = "Error reading SAM output file"
   
    document = {
        "user_id": "admin",
        "_id": jid,
        "run_type": run_type,
        "model_object_dict": {
            'filename': "Eco_mth_avgdur.out",
            'output': output
        }
    }
    db['sam'].save(document)


def sam_callback(temp_sam_run_path, run_type, jid):
    logging.info("sam_callback executed!")
    # os.makedirs(os.path.join(temp_sam_run_path, 'callback'))

    # link = s3_upload(temp_sam_run_path, name_temp)

    # if link:
    update_mongo(run_type, jid)


def sam(inputs_json, jid, run_type):
    """
        Custom or pre-canned run?
    """
    args = json.loads(inputs_json)

    # Generate random name for current run
    name_temp = id_generator()
    print name_temp

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
                
                sam_path = os.path.join(curr_path, 'bin', 'ubertool_superprzm_src', 'Debug', exe)
                print sam_path

                # Define SuperPRZMpesticide.exe command line arguments
                sam_arg1 = os.path.join(curr_path, 'bin')     # Absolute path to "root" of SAM model
                sam_arg2 = name_temp                          # Temp directory name for SAM run
                # Create list of args
                args = sam_path + " " + sam_arg1 + " " + sam_arg2

                # Create ThreadPoolExecutor (as 'Pool') instance to store threads which execute Fortran exe as subprocesses
                pool = Pool(max_workers=1)
                # Store execution of Fortran exe as a Future object, allowing the Python code to continue executing
                future = pool.submit(subprocess.call, args, shell=1)
                # When the Fortran exe finishes call "sam_callback" callback function
                future.add_done_callback(sam_callback(temp_sam_run_path, run_type))
                # Destroy the Pool object which hosts the threads
                pool.shutdown(wait=False)

            else:
                print "Windows (really NOT Linux) OS"
                # Assuming Windows here, could be other tho and this will break
                exe = "SuperPRZMpesticide_win.exe"
                # import subprocess
                """
                Don't actually run SAM, just delay 5 seconds
                """
                import time
                time.sleep(5)
                sam_callback(temp_sam_run_path, run_type, jid)

            #try:
            #    p = subprocess.Popen(args, shell=1)
                
            #except Exception, e:
            #    logging.info("Error Msg: " + str(e))
            #    pass
            
            input_file_string = sam_read_input_file(sam_input_file_path)

            return input_file_string


        except Exception, e:
            logging.info("Error Msg: " + str(e))
            return {'user_id':'admin', 'result': {'error': str(e)}, '_id':jid}
    else:
        logging.info('++++++++++++ E L S E ++++++++++++')
        # Canned model run; do not run SAM
        return {'user_id':'admin', 'result': ["https://s3.amazonaws.com/super_przm/SAM_IB2QZS.zip"], '_id':jid}
