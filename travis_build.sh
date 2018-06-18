#!/bin/sh
git clone https://github.com/quanted/requirements_qed.git

for package in $(cat requirements_qed/requirements.txt)
do
    if [[ "$package" == #* ]] || [[ "$package" == *gdal* ]] || [[ "$package" == *fiona* ]] || [[ "$package" == *coverage* ]] || [[ "$package" == *conda* ]]
    then
        echo "Not installing $package"
    else
        pip install $package
    fi
done