from celery import Celery


celery_tasks = [
    'flask_qed.hms_flask.modules.hms_controller',
    'flask_qed.pram_flask.tasks'
]

# celery = Celery('flask_qed', broker='redis://localhost:6379/0', backend='redis://localhost:6379/0', include=celery_tasks)
celery = Celery('flask_qed', broker='redis://redis:6379/0', backend='redis://redis:6379/0', include=['flask_qed.hms_flask'])

celery.conf.update(
    CELERY_ACCEPT_CONTENT=['json'],
    CELERY_TASK_SERIALIZER='json',
    CELERY_RESULT_SERIALIZER='json',
    CELERY_IGNORE_RESULT=False,
    CELERY_TRACK_STARTED=True,
)
