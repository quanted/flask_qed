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

# Generate a random ID for file save
def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for x in range(size))


def sam_read_input_file(sam_input_file_path):

    html = "<br><b>SAM.inp created:</b><br>"

    with open(sam_input_file_path) as f:
        html += f.read().replace('\n', '<br>')

    return html


def sam_callback(temp_sam_run_path):
    logging.info("sam_callback executed!")
    os.makedirs(os.path.join(temp_sam_run_path, 'callback'))

def sam(inputs_json, jid):

##########################################################################################
#####AMAZON KEY, store output files. You might have to write your own import approach#####
##########################################################################################
    key = keys_Picloud_S3.amazon_s3_key
    secretkey = keys_Picloud_S3.amazon_s3_secretkey
##########################################################################################
##########################################################################################
##########################################################################################

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

        from concurrent.futures import ProcessPoolExecutor as Pool

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
                #import subprocess32 as subprocess    # I want to use subprocess32 for Linux, but it will not compile on CGI
                import subprocess
            else:
                print "Windows (really NOT Linux) OS"
                # Assuming Windows here, could be other tho and this will break
                exe = "SuperPRZMpesticide_win.exe"
                import subprocess

            sam_path = os.path.join(curr_path, 'bin', 'ubertool_superprzm_src', 'Debug', exe)
            print sam_path

            # Define SuperPRZMpesticide.exe command line arguments
            sam_arg1 = os.path.join(curr_path, 'bin')     # Absolute path to "root" of SAM model
            sam_arg2 = name_temp                          # Temp directory name for SAM run
            # Create list of args
            args = [sam_path, sam_arg1, sam_arg2]
            # args = sam_path + " " + sam_arg1 + " " + sam_arg2

            # Create ProcessPoolExecutor (as 'Pool') instance to run FORTRAN exe in separate process as a Future
            pool = Pool(max_workers=1)
            future = pool.submit([subprocess.call, args], shell=1)
            future.add_done_callback(sam_callback(temp_sam_run_path))
            pool.shutdown(wait=False)

            # a = subprocess.Popen(args, shell=1)
            
            input_file_string = sam_read_input_file(sam_input_file_path)

            return input_file_string


        except Exception, e:
            logging.info("Error Msg: " + str(e))
            return {'user_id':'admin', 'result': {'error': str(e)}, '_id':jid}
    else:
        logging.info('++++++++++++ E L S E ++++++++++++')
        # Canned model run; do not run SAM
        return {'user_id':'admin', 'result': ["https://s3.amazonaws.com/super_przm/SAM_IB2QZS.zip"], '_id':jid}