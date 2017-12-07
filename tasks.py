"""
QED celery instance
"""

from __future__ import absolute_import
import os
import logging
import redis
import json
import sys
# sys.path.append("..")
# sys.path.remove(os.path.dirname(__file__))
# add your path to the sys path
# sys.path.append(os.getcwd())

from celery import Celery
from flask import request, Response
from flask_restful import Resource

try:
    from ubertool_ecorest.ubertool.ubertool.sam import sam_exe as sam
    from ubertool_ecorest.REST_UBER import rest_model_caller, rest_validation
except:
    from ubertool.ubertool.sam import sam_exe as sam
    from REST_UBER import rest_model_caller, rest_validation

# import ubertool_ecorest.ubertool.ubertool.sam.sam_exe as sam
# import REST_UBER.rest_model_caller as rest_model_caller
# from .ubertool.ubertool.sam import sam_exe as sam
# from .REST_UBER import rest_model_caller


logging.getLogger('celery.task.default').setLevel(logging.DEBUG)
logging.getLogger().setLevel(logging.DEBUG)

redis_hostname = os.environ.get('REDIS_HOSTNAME')
redis_port = os.environ.get('REDIS_PORT')
REDIS_HOSTNAME = os.environ.get('REDIS_HOSTNAME')

if not os.environ.get('REDIS_HOSTNAME'):
    os.environ.setdefault('REDIS_HOSTNAME', 'localhost')
    REDIS_HOSTNAME = os.environ.get('REDIS_HOSTNAME')

logging.info("REDIS HOSTNAME: {}".format(REDIS_HOSTNAME))

redis_conn = redis.StrictRedis(host=REDIS_HOSTNAME, port=6379, db=0)

app = Celery('tasks',
             broker='redis://redis:6379/0',
             backend='redis://redis:6379/0',)

app.conf.update(
    CELERY_ACCEPT_CONTENT=['json'],
    CELERY_TASK_SERIALIZER='json',
    CELERY_RESULT_SERIALIZER='json',
    CELERY_IGNORE_RESULT=False,
    CELERY_TRACK_STARTED=True,
)

class SamStatus(Resource):
    def get(self, task_id):
        """
        SAM task status
        :param jobId:
        :return:
        """
        logging.info("celery_qed received request for sam status")
        task = {}
        try:
            task = sam_status(task_id)
        except Exception as ex:
            task['status'] = str(ex)
        resp_body = json.dumps({'task_id': task_id, 'task_status': task['status']})
        logging.info("sam task id: " + task_id + " status: " + task['status'])
        response = Response(resp_body, mimetype='application/json')
        return response


class SamRun(Resource):
    def post(self, jobId="000000100000011"):
        """
        SAM post handler.
        :param jobId:
        :return:
        """
        logging.info("celery_qed task start request with inputs: {}".format(str(request.form))
        indexed_inputs = {}
        # index the input dictionary
        for k, v in request.form.items():
            indexed_inputs[k] = {"0": v}
        valid_input = {"inputs": indexed_inputs, "run_type": "single"}
        task_id = sam_run.apply_async(args=(jobId, valid_input["inputs"]), taskset_id=jobId)
        #task_id = sam_run(jobId, valid_input["inputs"]) #run tasks in flask thread (does not use celery)
        logging.info("celery_qed initiated with session id:" {}.format(task_id)
        resp_body = json.dumps({'task_id': str(task_id.id)})
        response = Response(resp_body, mimetype='application/json')
        return response


class SamData(Resource):
    def get(self, task_id):
        data_json = ""
        dir_path = os.getcwd()
        try:
            # TODO: NOT CORRECT OUTPUT FILE.
            with open(dir_path + '\\ubertool\\ubertool\\sam\\bin\\Results\\' + str(task_id) + '\\Custom_json.csv', 'rb') as data:
                data_json = data.read()
            data_json = json.dumps(json.loads(data_json))
        except FileNotFoundError as er:
            return "{'error': 'data file not found'}"
        return Response(data_json, mimetype='application/json')


@app.task(name='tasks.sam_run', bind=True, ignore_result=False)
def sam_run(self, jobID, inputs):
    task_id = sam_run.request.id
    logging.info("celery_qed session id: {}".format(task_id))
    logging.info("sam starting...")
    inputs["csrfmiddlewaretoken"] = {"0": task_id}
    rest_model_caller.model_run("sam", task_id, inputs, module=sam)


def sam_status(task_id):
    task = app.AsyncResult(task_id)
    return {"status": task.status}
