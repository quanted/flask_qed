from celery import Celery


celery_tasks = [
    'hms_flask.modules.hms_controller',
    'pram_flask.tasks'
]

celery = Celery('flask_qed', broker='redis://localhost:6379/0', backend='redis://localhost:6379/0', include=celery_tasks)
# celery = Celery('flask_qed', broker='redis://redis:6379/0', backend='redis://redis:6379/0', include=celery_tasks)

celery.conf.update(
    CELERY_ACCEPT_CONTENT=['json'],
    CELERY_TASK_SERIALIZER='json',
    CELERY_RESULT_SERIALIZER='json',
    CELERY_IGNORE_RESULT=False,
    CELERY_TRACK_STARTED=True,
)
