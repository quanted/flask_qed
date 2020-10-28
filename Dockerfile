# qed_py3 is debian linux with buildpack-deps
# updated with all needed qed python dependencies
FROM quanted/qed_py3:dev

# Install uWSGI
RUN pip install uwsgi

# Overwrite the uWSGI config
COPY uwsgi.ini /etc/uwsgi/

RUN mkdir /src/
COPY start_flask.sh /src/start_flask.sh
WORKDIR /src
EXPOSE 7777 8080

RUN chmod 755 /src/start_flask.sh

CMD ["sh", "/src/start_flask.sh"]
