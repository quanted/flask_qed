#!/bin/bash

sh ./run_pytests_docker.sh
exec uwsgi /etc/uwsgi/uwsgi.ini

# celery worker -A tasks -c 1 -Q sam --loglevel=DEBUG -n sam_worker
