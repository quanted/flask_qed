import os
import logging
from celery import Celery

from temp_config.set_environment import DeployEnv

runtime_env = DeployEnv()
runtime_env.load_deployment_environment()

redis_server = os.environ.get('REDIS_HOSTNAME')
redis_port = os.environ.get('REDIS_PORT')

celery_tasks = [
    'hms_flask.modules.hms_controller',
    'pram_flask.tasks'
]

if os.environ.get('DOCKER_HOSTNAME'):
    if "KUBERNETES" in os.environ.get('DOCKER_HOSTNAME'):
        redis = redis_port.replace("tcp", "redis")
    else:
        redis = 'redis://' + redis_server + ':' + redis_port + '/0'
else:
    redis = 'redis://' + redis_server + ':' + redis_port + '/0'
logging.warning("Celery connecting to redis server: " + redis)

celery = Celery('flask_qed', broker=redis, backend=redis, include=celery_tasks)

celery.conf.update(
    accept_content=['json'],
    # CELERY_TASK_SERIALIZER='json',
    result_serializer='json',
    task_ignore_result=False,
    # CELERY_TRACK_STARTED=True,
    worker_max_memory_per_child=50000000
)
