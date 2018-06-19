#!/bin/bash

sh ./run_pytests_docker.sh > run_pytests_docker_output.txt
cp -r /src/pram_flask/pram_qaqc_reports /src/collected_static/pram_qaqc_reports 
exec uwsgi /etc/uwsgi/uwsgi.ini

# celery worker -A tasks -c 1 -Q sam --loglevel=DEBUG -n sam_worker
