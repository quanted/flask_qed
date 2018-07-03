#!/bin/bash

python -m pytest -k "agdrift" --rootdir=/src/pram_flask --html=pram_flask/pram_qaqc_reports/agdrift.html --self-contained-html
python -m pytest -k "beerex" --rootdir=/src/pram_flask --html=pram_flask/pram_qaqc_reports/beerex.html --self-contained-html
python -m pytest -k "earthworm" --rootdir=/src/pram_flask --html=pram_flask/pram_qaqc_reports/earthworm.html --self-contained-html
python -m pytest -k "iec" --rootdir=/src/pram_flask --html=pram_flask/pram_qaqc_reports/iec.html --self-contained-html
python -m pytest -k "kabam" --rootdir=/src/pram_flask --html=pram_flask/pram_qaqc_reports/kabam.html --self-contained-html
python -m pytest -k "rice" --rootdir=/src/pram_flask --html=pram_flask/pram_qaqc_reports/rice.html --self-contained-html
python -m pytest -k "screenip" --rootdir=/src/pram_flask --html=pram_flask/pram_qaqc_reports/sip.html --self-contained-html
python -m pytest -k "stir" --rootdir=/src/pram_flask --html=pram_flask/pram_qaqc_reports/stir.html --self-contained-html
python -m pytest -k "ted" --rootdir=/src/pram_flask --html=pram_flask/pram_qaqc_reports/ted.html --self-contained-html
python -m pytest -k "terrplant" --rootdir=/src/pram_flask --html=pram_flask/pram_qaqc_reports/terrplant.html --self-contained-html
python -m pytest -k "therps" --rootdir=/src/pram_flask --html=pram_flask/pram_qaqc_reports/therps.html --self-contained-html
python -m pytest -k "trex" --rootdir=/src/pram_flask --html=pram_flask/pram_qaqc_reports/trex.html --self-contained-html



