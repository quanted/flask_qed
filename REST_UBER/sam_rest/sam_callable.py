__author__ = 'jflaisha'

import logging, numpy as np, requests, json, cPickle
from bson.binary import Binary

try:
    import superprzm  #  Import superprzm.dll / .so
    _dll_loaded = True
except ImportError, e:
    logging.exception(e)
    _dll_loaded = False

def run(sam_bin_path, name_temp, section, array_size):

    np_array_out = superprzm.runmain.run(sam_bin_path, name_temp, section, array_size)  # Run SuperPRZM as DLL
    test_array = np.random.rand(50,3)
    mongo_motor_insert(test_array, name_temp, section)  # Motor only works on Linux
    #mongo_pymongo_insert(out, name_temp, section)  # Pymongo used for testing on Windows

    return True


def mongo_motor_insert(np_array, name_temp, section):

    jid = name_temp + "_" +section
    url = 'http://localhost:8787/sam/daily/' + jid
    http_headers = {'Content-Type': 'application/json'}
    data = json.dumps(create_mongo_document(np_array, name_temp, section))

    requests.post(url, data=data, headers=http_headers, timeout=30)


def mongo_pymongo_insert(np_array, name_temp, section):

    # Dummy-fy the np_array
    # np_array = [1, 2, 3]

    # Connect to MongoDB server
    try:
        import pymongo
        client = pymongo.MongoClient('localhost', 27017)
        db = client.ubertool
    except:
        return None

    # Crete MongoDB document
    document = json.dumps(create_mongo_document(np_array, name_temp, section))

    db.sam.insert(document)


def create_mongo_document(np_array, name_temp, section):
    return {
        "user_id": "admin",
        "jid": name_temp + "_" + section,
        "run_type": 'single',
        "model_object_dict": {
            #'filename': filename,
            #'input': args
            'output': Binary(cPickle.dumps(np_array, protocol=2))
        }
    }
