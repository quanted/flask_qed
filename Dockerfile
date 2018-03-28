#FROM python:3
#FROM quanted/qed_py3
FROM dbsmith88/py-gdal

# Install Python Dependencies
# COPY requirements.txt /tmp/
# RUN pip install --requirement /tmp/requirements.txt

# Install uWSGI
RUN pip install uwsgi

# Overwrite the uWSGI config
COPY uwsgi.ini /etc/uwsgi/

COPY . /src/
WORKDIR /src
EXPOSE 7777

RUN chmod 755 /src/start_flask.sh

#CMD ["uwsgi", "/etc/uwsgi/uwsgi.ini"]
#RUN celery worker -A tasks -c 1 -Q sam --loglevel=DEBUG -n sam_worker
CMD ["sh", "/src/start_flask.sh"]
