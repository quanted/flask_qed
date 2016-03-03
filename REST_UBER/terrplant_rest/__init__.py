from flask_restful import Resource
from ubertool.ubertool.terrplant import terrplant
from flask import request
import pandas as pd
from REST_UBER import rest_validation, rest_schema


class TerplantHandler(Resource):
    def __init__(self):
        self.name = "terrplant"

    @staticmethod
    def get_model_inputs():
        """
        Return model's input class.
        :return:
        """
        return terrplant.TerrplantInputs()

    @staticmethod
    def get_model_outputs():
        """
        Return model's output class.
        :return:
        """
        return terrplant.TerrplantOutputs()


class TerrplantGet(TerplantHandler):

    def get(self, jobId="YYYYMMDDHHMMSSuuuuuu"):
        """
        Terrplant get handler.
        :param jobId: (format = %Y%m%d%H%M%S%f) (15 digits)
        :return:
        """
        return rest_schema.get_schema(self.name, jobId)


class TerrplantPost(TerplantHandler):

    def post(self, jobId="000000100000011"):
        """
        Terrplant post handler.
        :param jobId:
        :return:
        """
        inputs = rest_validation.parse_inputs(request.json)
        pd_obj = pd.DataFrame.from_dict(inputs, dtype='float64')
        terrplant_obj = terrplant.Terrplant(pd_obj, None)
        terrplant_obj.execute_model()
        inputs_json, outputs_json, exp_out_json = terrplant_obj.get_dict_rep(terrplant_obj)

        return {
            'user_id': 'admin',
            'inputs': inputs_json,
            'outputs': outputs_json,
            'exp_out': exp_out_json,
            '_id': jobId,
            'run_type': "single"
        }
