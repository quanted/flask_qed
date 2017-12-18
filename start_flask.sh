#!/bin/bash

celery worker -A tasks -c 1 -Q sam --loglevel=DEBUG -n sam_worker

exec uwsgi /etc/uwsgi/uwsgi.ini