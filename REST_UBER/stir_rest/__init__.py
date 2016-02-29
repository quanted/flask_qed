from flask_restful import Resource
from ubertool.ubertool.stir import stir
from flask import request
import pandas as pd


class StirHandler(Resource):
    def __init__(self):
        self.name = "stir"

    def get(self, jobId):
        """
        STIR get handler.
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
        STIR post handler.
        :param jobId:
        :return:
        """
        pd_obj = pd.DataFrame.from_dict(request.json["inputs"], dtype='float64')
        stir_obj = stir.Stir(pd_obj, None)
        stir_obj.execute_model()
        inputs_json, outputs_json, exp_out_json = stir_obj.get_dict_rep(stir_obj)

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
        return stir.StirInputs()

    @staticmethod
    def get_model_outputs():
        """
        Return model's output class.
        :return:
        """
        return stir.StirOutputs()
