import importlib
import json
import logging
import os
import pandas as pd

try:
    from flask_cors import CORS
    cors = True
except ImportError:
    cors = False
from flask import Flask, Response, request, jsonify, render_template
from flask_restful import Resource, Api
from nta_flask.dsstox_rest import batch_query


app = Flask(__name__)
app.config.update(
    DEBUG=True,
)

api = Api(app)
if cors:
    CORS(app)
else:
    logging.debug("CORS not enabled")



PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
os.environ.update({
    'PROJECT_ROOT': PROJECT_ROOT
})

# nta prefix needed if running from this file instead of flask_cgi,
# to replicate url when running from flask_cgi using middleware
api.add_resource(batch_query.DsstoxBatchSearch, '/nta/rest/ms1/batch/<string:jobId>')


if __name__ == '__main__':
    app.run(port=7777, debug=True)
