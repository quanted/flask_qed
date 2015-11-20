import json, logging, importlib
from flask import Flask, request, jsonify, render_template, make_response
from flask_restful import Resource, Api
from flask_swagger import swagger
import pandas as pd
from terrplant_rest import terrplant_model_rest

app = Flask(__name__)
api = Api(app)


class ModelCaller(Resource):
    def get(self, model, jid):
        return {'result': 'model=%s, jid=%s' % (model, jid)}

    def post(self, model, jid):
        """
        Execute model
        ---
        tags:
          - users
        parameters:
          - in: body
            name: body
            schema:
              id: User
              required:
                - email
                - name
              properties:
                email:
                  type: string
                  description: email for user
                name:
                  type: string
                  description: name for user
                address:
                  description: address for user
                  schema:
                    id: Address
                    properties:
                      street:
                        type: string
                      state:
                        type: string
                      country:
                        type: string
                      postalcode:
                        type: string
        responses:
          201:
            description: User created
        """
        try:
            # Dynamically import the model Python module
            model_module = importlib.import_module('.' + model + '_model_rest', model + '_rest')
            # Set the model Object to a local variable (class name = model)
            model_object = getattr(model_module, model)

            try:
                run_type = request.json["run_type"]
            except KeyError, e:
                return self.errorMessage(e, jid)

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

        except Exception, e:
            return self.errorMessage(e, jid)

    def errorMessage(self, error, jid):
        """Returns exception error message as valid JSON string to caller"""
        logging.exception(error)
        e = str(error)
        return {'user_id': 'admin', 'result': {'error': e}, '_id': jid}


class TerrplantHandler(Resource):
    def get(self, jid):
        return {'result': 'model=terrplant, jid=%s' % (jid)}

    def post(self, jid):
        pd_obj = pd.DataFrame.from_dict(request.json["inputs"], dtype='float64')
        terrplant = terrplant_model_rest.Terrplant(pd_obj, None)
        terrplant.execute_model()
        result_json_tuple = terrplant.get_json(terrplant)
        inputs_json = json.loads(result_json_tuple[0])
        outputs_json = json.loads(result_json_tuple[1])
        exp_out_json = json.loads(result_json_tuple[2])

        return {
            'user_id': 'admin',
            'inputs': inputs_json,
            'outputs': outputs_json,
            'exp_out': exp_out_json,
            '_id': jid,
            'run_type': "single"
        }


api.add_resource(TerrplantHandler, '/terrplant/<string:jid>')
api.add_resource(ModelCaller, '/<string:model>/<string:jid>')


@app.route("/api/spec")
def spec():
    swag = swagger(app)
    swag['info']['version'] = "0.1"
    swag['info']['title'] = u"\u00FCbertool API Documentation"
    swag['info']['description'] = "Welcome to the EPA's ubertool interactive RESTful API documentation."
    return jsonify(swag)


@app.route("/api")
def api_doc():
    return render_template('index.html')


if __name__ == '__main__':
    app.run(port=7777, debug=True)
