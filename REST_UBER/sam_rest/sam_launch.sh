#!/usr/bin/env bash
#Activate the Python virtual environment
#LD_LIBRARY_PATH=/opt/python2.7.10/lib
#source /var/www/ubertool/env2.7.10/bin/activate
source /var/www/ubertool/ubertool_ecorest/env/bin/activate

if [ $# -gt 0 ]; then
    echo '1st command line arg: ' $1
    echo '2nd command line arg: ' $2
    echo '3rd command line arg: ' $3
    SAM_PY=$1
    NAME_TEMP=$2
    NUMBER_OF_ROWS_LIST=$3

    #sleep 15  # Testing
    python $SAM_PY $NAME_TEMP "$NUMBER_OF_ROWS_LIST"
else
    echo "Expected arguments missing"
fi