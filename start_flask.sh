#!/bin/bash

#sh ./run_pytests_docker.sh > run_pytests_docker_output.txt
sh ./run_pytests.sh > run_pytests_docker_output.txt
rm -rf /src/collected_static/pram_qaqc_reports 
cp -r /src/pram_flask/pram_qaqc_reports /src/collected_static 
exec uwsgi /etc/uwsgi/uwsgi.ini

# celery worker -A tasks -c 1 -Q sam --loglevel=DEBUG -n sam_worker
