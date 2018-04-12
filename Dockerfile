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
#COPY . /flask_qed/
#WORKDIR /flask_qed
EXPOSE 7777

#ENV PYTHONPATH $PYTHONPATH:/flask_qed

RUN chmod 755 /src/start_flask.sh
#RUN chmod 755 /flask_qed/start_flask.sh

#CMD ["uwsgi", "/etc/uwsgi/uwsgi.ini"]
#RUN celery worker -A tasks -c 1 -Q sam --loglevel=DEBUG -n sam_worker
CMD ["sh", "/src/start_flask.sh"]
#CMD ["sh", "/flask_qed/start_flask.sh"]
