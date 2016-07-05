FROM python:2

MAINTAINER Ubertool Dev Team <ubertool-dev@googlegroups.com>

COPY ./requirements.txt /tmp/requirements.txt
RUN pip install -qr /tmp/requirements.txt

COPY . /src/
WORKDIR /src
EXPOSE 7777
CMD ["python", "flask_cgi.py"]