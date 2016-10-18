FROM puruckertom/uber_py27

# Install uWSGI
RUN pip install uwsgi

# Overwrite the uWSGI config
COPY uwsgi.ini /etc/uwsgi/

COPY . /src/
WORKDIR /src
EXPOSE 7777
#CMD ["python", "flask_cgi.py"]
CMD ["uwsgi", "/etc/uwsgi/uwsgi.ini"]