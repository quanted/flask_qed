#!/bin/bash


python -m pytest -k "agdrift" --html=pram_qaqc_reports/agdrift.html --self-contained-html
python -m pytest -k "beerex" --html=pram_qaqc_reports/beerex.html --self-contained-html
python -m pytest -k "earthworm" --html=pram_qaqc_reports/earthworm.html --self-contained-html
python -m pytest -k "iec" --html=pram_qaqc_reports/iec.html --self-contained-html
python -m pytest -k "kabam" --html=pram_qaqc_reports/kabam.html --self-contained-html
python -m pytest -k "rice" --html=pram_qaqc_reports/rice.html --self-contained-html
python -m pytest -k "screenip" --html=pram_qaqc_reports/sip.html --self-contained-html
python -m pytest -k "stir" --html=pram_qaqc_reports/stir.html --self-contained-html
python -m pytest -k "ted" --html=pram_qaqc_reports/ted.html --self-contained-html
python -m pytest -k "terrplant" --html=pram_qaqc_reports/terrplant.html --self-contained-html
python -m pytest -k "therps" --html=pram_qaqc_reports/therps.html --self-contained-html
python -m pytest -k "trex" --html=pram_qaqc_reports/trex.html --self-contained-html



