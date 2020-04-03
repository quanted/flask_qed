@ECHO OFF

ECHO "Starting redis from '%REDIS_PATH%'"
ECHO "Starting mongoDB from '%MONGODB_PATH%'"
ECHO "Activating %QED_PY_ENV% to run Celery from %QED_FLASK_PATH%"

SET /P proceed = "Press enter to launch"

start cmd.exe @cmd /k "%REDIS_PATH%"
start cmd.exe @cmd /k "%MONGODB_PATH%"
start cmd.exe @cmd /k "CD %QED_FLASK_PATH% && activate %QED_PY_ENV% && celery worker -A celery_cgi -Q qed --loglevel=DEBUG -c 2 -n qed_worker"
