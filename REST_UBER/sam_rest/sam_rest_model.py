#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import subprocess
#import zipfile
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
    name_temp=id_generator()
    print name_temp

    if args['scenario_selection'] == '0':
        logging.info('++++++++++++ C U S T O M ++++++++++++')
        # Run SAM, but first generate SAM input file
        try:
            import sam_input_generator
            sam_input_file_path = sam_input_generator.generate_sam_input_file(args, name_temp)
        except Exception, e:
            logging.info("Error Msg: " + str(e))
            return {'user_id':'admin', 'result': {'error': str(e)}, '_id':jid}
    else:
        logging.info('++++++++++++ E L S E ++++++++++++')
        # Canned model run; do not run SAM
        return {'user_id':'admin', 'result': ["https://s3.amazonaws.com/super_przm/SAM_IB2QZS.zip"], '_id':jid}
    
    curr_dir = os.path.dirname(os.path.realpath(__file__))
    #exe = "SuperPRZMpesticide.exe"
    exe = "SuperPRZMpesticide_win.exe"
    sam_path = os.path.join(curr_dir, 'bin', 'ubertool_superprzm_src', 'Debug', exe)
    print sam_path

    sam_arg1 = os.path.join(curr_dir, 'bin')
    sam_arg2 = sam_input_file_path
    # sam_arg2_out_path_unique = name_temp

    # Unique output path to be passeed to FORTRAN ----- Not Currently Being Used
    # out_path_unique = os.path.join(sam_arg1_curr_path, name_temp)
    # os.makedirs(out_path_unique)
    os.makedirs(os.path.join(out_path_unique, 'EcoPestOut_all', 'EcoPestOut_SoilGrps'))

    # Call SuperPRZMpesticide.exe with arguments
    a = subprocess.Popen(sam_path + " " + sam_arg1 + " " + sam_arg2, shell=1)
    a.wait()
    print "Done"
    
    ##zip the output files
    #zout=zipfile.ZipFile("temp.zip", "w", zipfile.ZIP_DEFLATED)
    
    # dwr
    # superPRZM_ouput = os.path.join(curr_dir, 'bin', 'dwPestOut_all', 'dwPestOut_SoilGrps', 'Reservoirs', '1838_pestAvgConc_distrib.out')
    # eco
    superPRZM_ouput = os.path.join(curr_dir, 'bin', 'EcoPestOut_all', 'EcoPestOut_SoilGrps')
    # print superPRZM_ouput
    #zout.write(superPRZM_ouput, os.path.basename(superPRZM_ouput))
    #zout.close()
    zout = shutil.make_archive(os.path.join(out_path_unique, 'temp'), "zip", root_dir=superPRZM_ouput)
    print "zout =", zout

    ##Create connection to S3
    conn = S3Connection(key, secretkey)
    bucket = Bucket(conn, 'super_przm')
    k=Key(bucket)

    ##Generate link to zip file
    name1='SAM_'+name_temp+'.zip'
    k.key=name1
    link='https://s3.amazonaws.com/super_przm/'+name1
    print link
    
    ##Upload zip file to S3
    #k.set_contents_from_filename('temp.zip')
    k.set_contents_from_filename(zout)
    k.set_acl('public-read-write')
    print 'upload finished'

    # Delete zip
    shutil.rmtree(out_path_unique)

    return link, "Done!"
