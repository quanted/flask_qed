# qed_py3 is debian linux with buildpack-deps
# updated with all needed qed python dependencies
# Use 'version' ARG for grabbing correct qed_py3 base image.
# Defaults to 'latest' if not set.
FROM quanted/qed_py3:mc3.8_3.1.4

# Install UWSGI
RUN pip install uwsgi

# Overwrite the uWSGI config
COPY uwsgi.ini /etc/uwsgi/

COPY . /src/
WORKDIR /src
EXPOSE 7777 8080

RUN conda install -c conda-forge --force-reinstall -y xarray numpy netCDF4
RUN pip install importlib_metadata==3.8.2

RUN chmod 755 /src/start_flask.sh

CMD ["sh", "/src/start_flask.sh"]
