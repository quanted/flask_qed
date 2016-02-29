from flask_restful import Resource
from ubertool.ubertool.rice import rice
from flask import request
import pandas as pd


class RiceHandler(Resource):
    def __init__(self):
        self.name = "rice"

    def get(self, jobId):
        """
        RICE get handler.
        :param jobId:
        :return:
        """
        return {
            'result': {
                'model: ' + self.name,
                'jid: %s' % jobId
            }
        }

    def post(self, jobId):
        """
        RICE post handler.
        :param jobId:
        :return:
        """
        pd_obj = pd.DataFrame.from_dict(request.json["inputs"], dtype='float64')
        rice_obj = rice.Rice(pd_obj, None)
        rice_obj.execute_model()
        inputs_json, outputs_json, exp_out_json = rice_obj.get_dict_rep(rice_obj)

        return {
            'user_id': 'admin',
            'inputs': inputs_json,
            'outputs': outputs_json,
            'exp_out': exp_out_json,
            '_id': jobId,
            'run_type': "single"
        }

    @staticmethod
    def get_model_inputs():
        """
        Return model's input class.
        :return:
        """
        return rice.RiceInputs()

    @staticmethod
    def get_model_outputs():
        """
        Return model's output class.
        :return:
        """
        return rice.RiceOutputs()
