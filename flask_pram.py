import importlib
import json
import logging
import os
import pandas as pd
import requests
import sys
import tabulate
import tasks

try:
    from flask_cors import CORS
    cors = True
except ImportError:
    cors = False
from flask import Flask, request, jsonify, render_template
from flask_restful import Resource, Api


app = Flask(__name__)
app.config.update(
    DEBUG=True,
)

api = Api(app)
if cors:
    CORS(app)
else:
    logging.debug("CORS not enabled")


from REST_UBER import agdrift_rest as agdrift
from REST_UBER import beerex_rest as beerex
from REST_UBER import earthworm_rest as earthworm
from REST_UBER import exponential_rest as exponential
from REST_UBER import iec_rest as iec
from REST_UBER import kabam_rest as kabam
from REST_UBER import leslie_probit_rest as leslie_probit
from REST_UBER import rice_rest as rice
# from REST_UBER import sam_rest as sam
from REST_UBER import screenip_rest as screenip
from REST_UBER import stir_rest as stir
from REST_UBER import terrplant_rest as terrplant
from REST_UBER import therps_rest as therps
from REST_UBER import trex_rest as trex
from REST_UBER import varroapop_rest as varroapop

PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
os.environ.update({
    'PROJECT_ROOT': PROJECT_ROOT
})

#needs to be after project root is set
import uber_swagger

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


@app.route("/api/pram/spec/")
def spec():
    """
    Route that returns the Swagger formatted JSON representing the pram API.
    :return: Swagger formatted JSON string
    """

    swag = uber_swagger.swagger(app)

    # TODO: Use in production and remove 'jsonify' below
    # return json.dumps(
    #     swag,
    #     separators=(',', ':')  # This produces a 'minified' JSON output
    # )

    return jsonify(swag)  # This produces a 'pretty printed' JSON output


@app.route("/api/pram/")
def api_doc():
    """
    Route to serve the API documentation (Swagger UI) static page being served by the backend.
    :return:
    """
    return render_template('index.html')


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


# Declare endpoints for each model
# These are the endpoints that will be introspected by the swagger() method & shown on API spec page
# TODO: Add model endpoints here once they are refactored
print('http://localhost:7777/api/pram/')
print('http://localhost:7777/api/pram/spec/')
print('http://localhost:7777/rest/pram/agdrift/')
api.add_resource(agdrift.AgdriftGet, '/rest/pram/agdrift/')
api.add_resource(agdrift.AgdriftPost, '/rest/pram/agdrift/<string:jobId>')
print('http://localhost:7777/rest/pram/beerex/')
api.add_resource(beerex.BeerexGet, '/rest/pram/beerex/')
api.add_resource(beerex.BeerexPost, '/rest/pram/beerex/<string:jobId>')
print('http://localhost:7777/rest/pram/earthworm/')
api.add_resource(earthworm.EarthwormGet, '/rest/pram/earthworm/')
api.add_resource(earthworm.EarthwormPost, '/rest/pram/earthworm/<string:jobId>')
print('http://localhost:7777/rest/pram/exponential/')
api.add_resource(exponential.ExponentialGet, '/rest/pram/exponential/')
api.add_resource(exponential.ExponentialPost, '/rest/pram/exponential/<string:jobId>')
print('http://localhost:7777/rest/pram/iec/')
api.add_resource(iec.IecGet, '/rest/pram/iec/')
api.add_resource(iec.IecPost, '/rest/pram/iec/<string:jobId>')
print('http://localhost:7777/rest/pram/kabam/')
api.add_resource(kabam.KabamGet, '/rest/pram/kabam/')
api.add_resource(kabam.KabamPost, '/rest/pram/kabam/<string:jobId>')
print('http://localhost:7777/rest/pram/leslie_probit/')
api.add_resource(leslie_probit.LeslieProbitGet, '/rest/pram/leslie_probit/')
api.add_resource(leslie_probit.LeslieProbitPost, '/rest/pram/leslie_probit/<string:jobId>')
print('http://localhost:7777/rest/pram/rice/')
api.add_resource(rice.RiceGet, '/rest/pram/rice/')
api.add_resource(rice.RicePost, '/rest/pram/rice/<string:jobId>')
print('http://localhost:7777/rest/pram/sam/')
api.add_resource(tasks.SamRun, '/rest/pram/sam/')
api.add_resource(tasks.SamStatus, '/rest/pram/sam/status/<string:task_id>')
api.add_resource(tasks.SamData, '/rest/pram/sam/data/<string:task_id>')
#importing screenip instead of sip because of conda problems
print('http://localhost:7777/rest/pram/sip/')
api.add_resource(screenip.ScreenipGet, '/rest/pram/sip/')
api.add_resource(screenip.ScreenipPost, '/rest/pram/sip/<string:jobId>')
print('http://localhost:7777/rest/pram/stir/')
api.add_resource(stir.StirGet, '/rest/pram/stir/')
api.add_resource(stir.StirPost, '/rest/pram/stir/<string:jobId>')
print('http://localhost:7777/rest/pram/terrplant/')
api.add_resource(terrplant.TerrplantGet, '/rest/pram/terrplant/')
api.add_resource(terrplant.TerrplantPost, '/rest/pram/terrplant/<string:jobId>')
print('http://localhost:7777/rest/pram/therps/')
api.add_resource(therps.TherpsGet, '/rest/pram/therps/')
api.add_resource(therps.TherpsPost, '/rest/pram/therps/<string:jobId>')
print('http://localhost:7777/rest/pram/trex/')
api.add_resource(trex.TrexGet, '/rest/pram/trex/')
api.add_resource(trex.TrexPost, '/rest/pram/trex/<string:jobId>')
print('http://localhost:7777/rest/pram/varroapop/')
api.add_resource(varroapop.VarroapopGet, '/rest/pram/varroapop/')
api.add_resource(varroapop.VarroapopPost, '/rest/pram/varroapop/<string:jobId>')
#api.add_resource(ModelCaller, '/rest/pram/<string:model>/<string:jid>')  # Temporary generic route for API endpoints



if __name__ == '__main__':
    app.run(port=7777, debug=True)
