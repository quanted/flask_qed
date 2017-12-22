"""
QED celery instance
"""

from __future__ import absolute_import
import os
import logging
import redis
import json
import uuid

from celery import Celery
from flask import request, Response
from flask_restful import Resource

logging.getLogger('celery.task.default').setLevel(logging.DEBUG)
logging.getLogger().setLevel(logging.DEBUG)

try:
    from ubertool_ecorest.ubertool.ubertool.sam import sam_exe as sam
    from ubertool_ecorest.REST_UBER import rest_model_caller, rest_validation
except:
    logging.info("SAM Task except import attempt..")
    from ubertool.ubertool.sam import sam_exe as sam
    from REST_UBER import rest_model_caller, rest_validation
    logging.info("SAM Task except import complete!")


from temp_config.set_environment import DeployEnv
runtime_env = DeployEnv()
runtime_env.load_deployment_environment()

redis_hostname = os.environ.get('REDIS_HOSTNAME')
redis_port = os.environ.get('REDIS_PORT')
REDIS_HOSTNAME = os.environ.get('REDIS_HOSTNAME')

if not os.environ.get('REDIS_HOSTNAME'):
    os.environ.setdefault('REDIS_HOSTNAME', 'redis')
    REDIS_HOSTNAME = os.environ.get('REDIS_HOSTNAME')

logging.info("REDIS HOSTNAME: {}".format(REDIS_HOSTNAME))

redis_conn = redis.StrictRedis(host=REDIS_HOSTNAME, port=6379, db=0)

#app = Celery('tasks', broker='redis://localhost:6379/0', backend='redis://localhost:6379/0',)
app = Celery('tasks', broker='redis://redis:6379/0', backend='redis://redis:6379/0',)

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
        logging.info("SAM task status request received for task: {}".format(str(task_id)))
        task = {}
        try:
            task = sam_status(task_id)
            logging.info("SAM task id: " + task_id + " status: " + task['status'])
        except Exception as ex:
            task['status'] = str(ex)
            logging.info("SAM task status request error: " + str(ex))
        resp_body = json.dumps({'task_id': task_id, 'task_status': task['status']})
        response = Response(resp_body, mimetype='application/json')
        return response


class SamRun(Resource):
    def post(self, jobId="000000100000011"):
        """
        SAM post handler.
        :param jobId:
        :return:
        """
        logging.info("SAM task start request with inputs: {}".format(str(request.form)))
        indexed_inputs = {}
        # TODO: set based on env variable
        use_celery = True
        # index the input dictionary
        for k, v in request.form.items():
            indexed_inputs[k] = {"0": v}
        valid_input = {"inputs": indexed_inputs, "run_type": "single"}
        if use_celery:
            # SAM Run with celery
            try:
                task_id = sam_run.apply_async(args=(jobId, valid_input["inputs"]), queue="sam", taskset_id=jobId)
                logging.info("SAM celery task initiated with task id:{}".format(task_id))
                resp_body = json.dumps({'task_id': str(task_id.id)})
            except Exception as ex:
                logging.info("SAM celery task failed: " + str(ex))
                resp_body = json.dumps({'task_id': "1234567890"})
        else:
            # SAM Run without celery
            task_id = uuid.uuid4()
            sam_run(task_id, valid_input["inputs"])
            logging.info("SAM flask task completed with task id:{}".format(task_id))
            resp_body = json.dumps({'task_id': str(task_id)})
        response = Response(resp_body, mimetype='application/json')
        return response


class SamData(Resource):
    def get(self, task_id):
        dir_path = os.getcwd()
        logging.info("SAM data request for task id: {}".format(task_id))
        file_path = './ubertool/ubertool/sam/bin/Results/' + str(task_id) + '/out_json.csv'
        try:
            logging.info("SAM data request file path: {}".format(file_path))
            with open(file_path, 'rb') as data:
                data_json = data.read()
            data_json = json.dumps(json.loads(data_json))
        except FileNotFoundError as er:
            logging.info("SAM data file not found, data request not successful.")
            return "{'error': 'data file not found', 'file_path': " + str(file_path) + "}"
        logging.info("SAM data file found, data request successful.")
        return Response(data_json, mimetype='application/json')


@app.task(name='tasks.sam_run', bind=True, ignore_result=False)
def sam_run(self, jobID, inputs):
    if sam_run.request.id is not None:
        task_id = sam_run.request.id
    else:
        task_id = jobID
    logging.info("SAM CELERY task id: {}".format(task_id))
    logging.info("SAM CELERY task starting...")
    inputs["csrfmiddlewaretoken"] = {"0": task_id}
    # Commented out model call for celery connection testing
    rest_model_caller.model_run("sam", task_id, inputs, module=sam)
    # logging.info("SAM CELERY task test answer is: 42")
    logging.info("SAM CELERY task completed.")


def sam_status(task_id):
    task = app.AsyncResult(task_id)
    return {"status": task.status}
