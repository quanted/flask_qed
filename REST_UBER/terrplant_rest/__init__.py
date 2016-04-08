from flask_restful import Resource
from ubertool.ubertool.terrplant import terrplant
from flask import request
from REST_UBER import rest_validation, rest_schema, rest_model_caller


class TerrplantHandler(Resource):
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


class TerrplantGet(TerrplantHandler):

    def get(self, jobId="YYYYMMDDHHMMSSuuuuuu"):
        """
        Terrplant get handler.
        :param jobId: (format = %Y%m%d%H%M%S%f) (15 digits)
        :return:
        """
        return rest_schema.get_schema(self.name, jobId)


class TerrplantPost(TerrplantHandler):

    def post(self, jobId="000000100000011"):
        """
        Terrplant post handler.
        :param jobId:
        :return:
        """

        inputs = rest_validation.parse_inputs(request.json)

        if inputs:
            return rest_model_caller.model_run(self.name, jobId, inputs, module=terrplant)
        else:
            return rest_model_caller.error(self.name, jobId, inputs)
