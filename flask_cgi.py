import importlib
import json
import logging
import os
import pandas as pd
import requests
import sys
import tabulate
try:
    from flask_cors import CORS
    cors = True
except ImportError:
    cors = False
from flask import Flask, request, jsonify, render_template
from flask_restful import Resource, Api


#from modules.hms_flask import surface_runoff_curve_number as cn
#from modules.hms_flask import locate_timezone as timezones
from REST_UBER import agdrift_rest as agdrift
from REST_UBER import beerex_rest as beerex
from REST_UBER import earthworm_rest as earthworm
from REST_UBER import exponential_rest as exponential
from REST_UBER import iec_rest as iec
from REST_UBER import kabam_rest as kabam
from REST_UBER import leslie_probit_rest as leslie_probit
from REST_UBER import rice_rest as rice
from REST_UBER import sam_rest as sam
from REST_UBER import screenip_rest as screenip
from REST_UBER import stir_rest as stir
from REST_UBER import terrplant_rest as terrplant
from REST_UBER import therps_rest as therps
from REST_UBER import trex_rest as trex


PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
os.environ.update({
    'PROJECT_ROOT': PROJECT_ROOT
})

#needs to be after project root is set
import uber_swagger

app = Flask(__name__)
api = Api(app)
if cors:
    CORS(app)
else:
    logging.debug("CORS not enabled")

# TODO: Remove this and Generic model handler below... (not used with refactored models)
_ACTIVE_MODELS = (
    'agdrift',
    'beerex',
    'earthworm',
    'exponential',
    'fellerarley',
    'foxsurplus',
    'gompertz',
    'iec',
    'kabam',
    'leslie',
    'leslie_logistic',
    'leslie_probit',
    'logistic',
    'loons',
    'maxsus',
    'rice',
    'sam',
    'sip',
    'screenip',
    'stir',
    'swc',
    'terrplant',
    'therps',
    'trex',
    'yulefurry',
)
_NO_MODEL_ERROR = "{} model is not available through the REST API"


# TODO: Generic API endpoint (TEMPORARY, remove once all endpoints are explicitly stated)
class ModelCaller(Resource):
    def get(self, model, jid):
        return {'result': 'model={0!s}, jid={1!s}'.format(model, jid)}

    def post(self, model, jid):
        # TODO: Remove the YAML part of this docstring
        """
        Execute model
        """
        if model in _ACTIVE_MODELS:
            if model == 'sip':
                model = 'screenip'
            try:
                # Dynamically import the model Python module
                model_module = importlib.import_module('ubertool.ubertool.' + model)
                logging.info('============= ' + model)
                # Set the model Object to a local variable (class name = model)
                model_cap = model.capitalize()
                model_object = getattr(model_module, model_cap)
                #logging.info('============= ' + model_object)

                try:
                    run_type = request.json["run_type"]
                    logging.info('============= run_type =' + run_type)
                except KeyError as e:
                    return rest_error_message(e, jid)

                if run_type == "qaqc":
                    logging.info('============= QAQC Run =============')

                    # pd_obj = pd.io.json.read_json(json.dumps(request.json["inputs"]))
                    pd_obj = pd.DataFrame.from_dict(request.json["inputs"], dtype='float64')
                    # pd_obj_exp = pd.io.json.read_json(json.dumps(request.json["out_exp"]))
                    pd_obj_exp = pd.DataFrame.from_dict(request.json["out_exp"], dtype='float64')

                    result_json_tuple = model_object(run_type, pd_obj, pd_obj_exp).json

                elif run_type == "batch":
                    logging.info('============= Batch Run =============')
                    # pd_obj = pd.io.json.read_json(json.dumps(request.json["inputs"]))
                    pd_obj = pd.DataFrame.from_dict(request.json["inputs"], dtype='float64')

                    result_json_tuple = model_object(run_type, pd_obj, None).json

                else:
                    logging.info('============= Single Run =============')
                    pd_obj = pd.DataFrame.from_dict(request.json["inputs"], dtype='float64')

                    result_json_tuple = model_object(run_type, pd_obj, None).json

                # Values returned from model run: inputs, outputs, and expected outputs (if QAQC run)
                inputs_json = json.loads(result_json_tuple[0])
                outputs_json = json.loads(result_json_tuple[1])
                exp_out_json = json.loads(result_json_tuple[2])

                return {'user_id': 'admin',
                        'inputs': inputs_json,
                        'outputs': outputs_json,
                        'exp_out': exp_out_json,
                        '_id': jid,
                        'run_type': run_type}

            except Exception as e:
                return rest_error_message(e, jid)
        else:
            return rest_error_message(_NO_MODEL_ERROR.format(model), jid)


def rest_error_message(error, jid):
    """Returns exception error message as valid JSON string to caller
    :param error: Exception, error message
    :param jid: string, job ID
    :return: JSON string
    """
    logging.exception(error)
    e = str(error)
    return json.dumps({'user_id': 'admin', 'result': {'error': e}, '_id': jid})




@app.route("/api/ubertool/spec/")
def spec():
    """
    Route that returns the Swagger formatted JSON representing the Ubertool API.
    :return: Swagger formatted JSON string
    """

    swag = uber_swagger.swagger(app)

    # TODO: Use in production and remove 'jsonify' below
    # return json.dumps(
    #     swag,
    #     separators=(',', ':')  # This produces a 'minified' JSON output
    # )

    return jsonify(swag)  # This produces a 'pretty printed' JSON output


@app.route("/api/ubertool/")
def api_doc():
    """
    Route to serve the API documentation (Swagger UI) static page being served by the backend.
    :return:
    """
    return render_template('index.html')


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


"""
=============================================================================================
                              HMS REST API
=============================================================================================
"""


@app.route('/hms/rest/', methods=['POST'])
def hms_rest():
    """
    HMS POST request, generic. Forwarded to HMS backend for data retrieval.
    :return: json object of the requested dataset.
    """
    # url = 'http://134.67.114.8/HMSWS/api/WSHMS/'
    url = os.environ.get('HMS_BACKEND_SERVER')
    data = request.form
    result = requests.post(str(url) + '/HMSWS/api/WSHMS/', data=data, timeout=10000)
    return result.content


@app.route('/hms/rest/<submodel>/', methods=['POST'])
def post_hms_submodel_rest(submodel):
    """
    HMS POST request, submodel specified. Forwarded to HMS backend for data retrieval.
    :param submodel: Dataset for requested data.
    :return: json object of the requested dataset.
    """
    # url = 'http://134.67.114.8/HMSWS/api/WS' + submodel
    url = os.environ.get('HMS_BACKEND_SERVER')
    data = request.form
    result = requests.post(str(url) + '/HMSWS/api/WS' + submodel, data=data, timeout=10000)
    return result.content


@app.route('/hms/rest/<submodel>/<parameters>', methods=['GET'])
def get_hms_submodel_rest(submodel, parameters):
    """
    HMS GET request, submodel specified. Forwarded to HMS backend for data retrieval.
    :param submodel: Dataset for requested data.
    :param parameters: Query string containing the required parameters described the in the API.
    :return: json object of the requested dataset.
    """
    # url = 'http://134.67.114.8/HMSWS/api/WS' + submodel + '/' + parameters
    url = os.environ.get('HMS_BACKEND_SERVER')
    result = requests.get(str(url) + '/HMSWS/api/WS' + submodel + '/' + parameters, timeout=10000)
    return result.content


"""
=============================================================================================
                              HMS PYTHON REST API
=============================================================================================
"""

# #TODO: CurveNumber dates required yyyy-MM-dd format, need to convert any provided date into this format prior to data request
# @app.route('/hms/rest/sim/', methods=['POST'])
# def post_hms_flask_rest():
#     """
#     POST request for hms simulation data.
#     :return: json of simulation data for the specified location and time period.
#     """
#     parameters = request.form
#     if parameters["dataset"] == "curvenumber":
#         # Date format restriction yyyy-MM-dd
#         data = cn.get_cn_runoff(parameters["startdate"], parameters["enddate"], parameters["latitude"], parameters["longitude"])
#         return data
#     else:
#         print("ERROR: dataset not curvenumber")
#         return
#
#
# @app.route('/hms/rest/runoff/', methods=['POST'])
# def post_hms_runoff_flask_rest():
#     """
#     POST request for hms runoff data.
#     :return: json of runoff data for the specified location and time period.
#     """
#     parameters = request.form
#     if parameters["dataset"] == "curvenumber":
#         # Date format restriction yyyy-MM-dd
#         data = cn.get_cn_runoff(parameters["startdate"], parameters["enddate"], parameters["latitude"], parameters["longitude"])
#         return data
#     else:
#         print("ERROR: dataset not curvenumber")
#         return
#
#
# @app.route('/hms/rest/runoff/<parameters>', methods=['GET'])
# def get_hms_runoff_flask_rest(parameters):
#     """
#     GET request for hms runoff data.
#     :param parameters: query string, requiring: startdate, enddate, latitude and longitude
#     :return: json of runoff data for the specified location and time period.
#     """
#     if parameters["dataset"] == "curvenumber":
#         # Date format restriction yyyy-MM-dd
#         data = cn.get_cn_runoff(parameters["startdate"], parameters["enddate"], parameters["latitude"], parameters["longitude"])
#         return data
#     else:
#         print("ERROR: dataset not curvenumber")
#         return
#
#
# @app.route('/hms/rest/timezone/', methods=['POST'])
# def post_hms_timezone():
#     """
#     POST request for timezone data from latitude/longitude values.
#     :return: json of timezone details.
#     """
#     parameters = request.form
#     return timezones.get_timezone(parameters["latitude"], parameters["longitude"])
#
#
# @app.route('/hms/rest/timezone/<latitude>&<longitude>', methods=['GET'])
# def get_hms_timezone(latitude, longitude):
#     """
#     GET request for timezone data from latitude/longitude values.
#     :param latitude: Latitude of requested location.
#     :param longitude: Longitude of requested location.
#     :return: json of timezone details.
#     """
#     lat = latitude.split('=')
#     lon = longitude.split('=')
#     return timezones.get_timezone(lat[1], lon[1])


# Declare endpoints for each model
# These are the endpoints that will be introspected by the swagger() method & shown on API spec page
# TODO: Add model endpoints here once they are refactored

print('http://localhost:7777/api/ubertool/')
print('http://localhost:7777/api/ubertool/spec/')
print('http://localhost:7777/rest/ubertool/agdrift/')
api.add_resource(agdrift.AgdriftGet, '/rest/ubertool/agdrift/')
api.add_resource(agdrift.AgdriftPost, '/rest/ubertool/agdrift/<string:jobId>')
print('http://localhost:7777/rest/ubertool/beerex/')
api.add_resource(beerex.BeerexGet, '/rest/ubertool/beerex/')
api.add_resource(beerex.BeerexPost, '/rest/ubertool/beerex/<string:jobId>')
print('http://localhost:7777/rest/ubertool/earthworm/')
api.add_resource(earthworm.EarthwormGet, '/rest/ubertool/earthworm/')
api.add_resource(earthworm.EarthwormPost, '/rest/ubertool/earthworm/<string:jobId>')
print('http://localhost:7777/rest/ubertool/exponential/')
api.add_resource(exponential.ExponentialGet, '/rest/ubertool/exponential/')
api.add_resource(exponential.ExponentialPost, '/rest/ubertool/exponential/<string:jobId>')
print('http://localhost:7777/rest/ubertool/iec/')
api.add_resource(iec.IecGet, '/rest/ubertool/iec/')
api.add_resource(iec.IecPost, '/rest/ubertool/iec/<string:jobId>')
print('http://localhost:7777/rest/ubertool/kabam/')
api.add_resource(kabam.KabamGet, '/rest/ubertool/kabam/')
api.add_resource(kabam.KabamPost, '/rest/ubertool/kabam/<string:jobId>')
print('http://localhost:7777/rest/ubertool/leslie_probit/')
api.add_resource(leslie_probit.LeslieProbitGet, '/rest/ubertool/leslie_probit/')
api.add_resource(leslie_probit.LeslieProbitPost, '/rest/ubertool/leslie_probit/<string:jobId>')
print('http://localhost:7777/rest/ubertool/rice/')
api.add_resource(rice.RiceGet, '/rest/ubertool/rice/')
api.add_resource(rice.RicePost, '/rest/ubertool/rice/<string:jobId>')
print('http://localhost:7777/rest/ubertool/sam/')
api.add_resource(sam.SamGet, '/rest/ubertool/sam/')
api.add_resource(sam.SamPost, '/rest/ubertool/sam/<string:jobId>')
#importing screenip instead of sip because of conda problems
print('http://localhost:7777/rest/ubertool/sip/')
api.add_resource(screenip.ScreenipGet, '/rest/ubertool/sip/')
api.add_resource(screenip.ScreenipPost, '/rest/ubertool/sip/<string:jobId>')
print('http://localhost:7777/rest/ubertool/stir/')
api.add_resource(stir.StirGet, '/rest/ubertool/stir/')
api.add_resource(stir.StirPost, '/rest/ubertool/stir/<string:jobId>')
print('http://localhost:7777/rest/ubertool/terrplant/')
api.add_resource(terrplant.TerrplantGet, '/rest/ubertool/terrplant/')
api.add_resource(terrplant.TerrplantPost, '/rest/ubertool/terrplant/<string:jobId>')
print('http://localhost:7777/rest/ubertool/therps/')
api.add_resource(therps.TherpsGet, '/rest/ubertool/therps/')
api.add_resource(therps.TherpsPost, '/rest/ubertool/therps/<string:jobId>')
print('http://localhost:7777/rest/ubertool/trex/')
api.add_resource(trex.TrexGet, '/rest/ubertool/trex/')
api.add_resource(trex.TrexPost, '/rest/ubertool/trex/<string:jobId>')
#api.add_resource(ModelCaller, '/rest/ubertool/<string:model>/<string:jid>')  # Temporary generic route for API endpoints



if __name__ == '__main__':
    app.run(port=7777, debug=True)  # To run on locahost
    # app.run(host='0.0.0.0', port=7777, debug=True)  # 'host' param needed to expose server publicly w/o NGINX/uWSGI
