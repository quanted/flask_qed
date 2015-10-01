__author__ = 'jflaisha'

import logging, numpy as np, requests, json, cPickle

try:
    import superprzm  #  Import superprzm.dll / .so
    _dll_loaded = True
except ImportError, e:
    logging.exception(e)
    _dll_loaded = False

def run(sam_bin_path, name_temp, section, array_size, list_of_julian_days):

    # np_array_out = np.random.rand(50,3)  # Dummy NumPy data
    np_array_out = superprzm.runmain.run(sam_bin_path, name_temp, section, array_size)  # Run SuperPRZM as DLL

    # Send Numpy array to MongoDB/Motor server
    mongo_motor_insert(np_array_out, name_temp, section, list_of_julian_days)  # Motor only works on Unix-based OS
    # mongo_pymongo_insert(np_array_out, name_temp, section)  # Pymongo used for testing on Windows

    return True


def get_sim_days(jid):

    url = 'http://localhost:8787/sam/metadata/' + jid

    document = requests.get(url, timeout=30)
    doc_dict = json.loads(document.body)
    print doc_dict

    return doc_dict['model_object_dict']['sim_days']


def mongo_motor_insert(np_array, name_temp, section, list_of_julian_days):

    jid = name_temp + "_" +section
    url = 'http://localhost:8787/sam/daily/' + jid
    # http_headers = {'Content-Type': 'application/json'}
    http_headers = {'Content-Type': 'application/octet-stream'}
    #data = json.dumps(create_mongo_document(np_array, name_temp, section))
    data = serialize(np_array, name_temp, section, list_of_julian_days)

    # Send data to Mongo server
    requests.post(url, data=data, headers=http_headers, timeout=30)


def mongo_pymongo_insert(np_array, name_temp, section):

    # Dummy-fy the np_array
    # np_array = [1, 2, 3]

    # Connect to MongoDB server using Pymongo
    try:
        import pymongo
        client = pymongo.MongoClient('localhost', 27017)
        db = client.ubertool
    except:
        return None

    # Crete MongoDB document
    document = serialize(np_array, name_temp, section)

    db.sam.insert(document)


def serialize(np_array, name_temp, section, list_of_julian_days):
    """
    Returns pickle to be sent to Mongo server.
    :param np_array:
    :param name_temp:
    :param section:
    :return:
    """
    return  cPickle.dumps({
        "user_id": "admin",
        "jid": name_temp + "_" + section,
        "run_type": 'single',
        "model_object_dict": {
            #'filename': filename,
            #'input': args
            'sim_days': list_of_julian_days,
            'output': np_array
        }
    }, protocol=2)
