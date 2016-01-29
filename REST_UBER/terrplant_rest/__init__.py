from flask_restful import Resource
from ubertool.ubertool.terrplant import terrplant
from flask import request
import pandas as pd


class TerrplantHandler(Resource):
    def __init__(self):
        self.name = "terrplant"

    def get(self, jid="000000100000011"):
        """
        Terrplant get handler.
        :param jid:
        :return:
        """
        return {
            'result': {
                'model: ' + self.name,
                'jid: %s' % jid
            }
        }

    def post(self, jid):
        """
        Terrplant post handler.
        :param jid:
        :return:
        """
        pd_obj = pd.DataFrame.from_dict(request.json["inputs"], dtype='float64')
        terrplant_obj = terrplant.Terrplant(pd_obj, None)
        terrplant_obj.execute_model()
        inputs_json, outputs_json, exp_out_json = terrplant_obj.get_dict_rep(terrplant_obj)

        return {
            'user_id': 'admin',
            'inputs': inputs_json,
            'outputs': outputs_json,
            'exp_out': exp_out_json,
            '_id': jid,
            'run_type': "single"
        }

    @staticmethod
    def get_model_inputs():
        """
        Return terrplant input class.
        :return:
        """
        return terrplant.TerrplantInputs()

    @staticmethod
    def get_model_outputs():
        """
        Return terrplant output class.
        :return:
        """
        return terrplant.TerrplantOutputs()
