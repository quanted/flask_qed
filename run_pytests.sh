#!/bin/bash


python -m pytest -k "agdrift" --html=pram_qaqc_reports/agdrift.html
python -m pytest -k "beerex" --html=pram_qaqc_reports/beerex.html
python -m pytest -k "earthworm" --html=pram_qaqc_reports/beerex.html
python -m pytest -k "iec" --html=pram_qaqc_reports/iec.html
python -m pytest -k "kabam" --html=pram_qaqc_reports/kabam.html
python -m pytest -k "rice" --html=pram_qaqc_reports/rice.html
python -m pytest -k "screenip" --html=pram_qaqc_reports/sip.html
python -m pytest -k "stir" --html=pram_qaqc_reports/stir.html
python -m pytest -k "ted" --html=pram_qaqc_reports/ted.html
python -m pytest -k "terrplant" --html=pram_qaqc_reports/terrplant.html
python -m pytest -k "therps" --html=pram_qaqc_reports/therps.html
python -m pytest -k "trex" --html=pram_qaqc_reports/trex.html



