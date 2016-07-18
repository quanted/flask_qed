FROM puruckertom/uber_py27

COPY . /src/
WORKDIR /src
EXPOSE 7777
CMD ["python", "flask_cgi.py"]