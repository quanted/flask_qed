from flask_restful import Resource
from ubertool.ubertool.varroapop import varroapop_exe as varroapop
from flask import request
from REST_UBER import rest_validation, rest_schema, rest_model_caller


class VarroapopHandler(Resource):
    def __init__(self):
        self.name = "varroapop"

    @staticmethod
    def get_model_inputs():
        """
        Return model's input class.
        :return:
        """
        return varroapop.VarroapopInputs()

    @staticmethod
    def get_model_outputs():
        """
        Return model's output class.
        :return:
        """
        return varroapop.VarroapopOutputs()


class VarroapopGet(VarroapopHandler):

    def get(self, jobId="YYYYMMDDHHMMSSuuuuuu"):
        """
        Varroapop get handler.
        :param jobId:
        :return:
        """
        return rest_schema.get_schema(self.name, jobId)


class VarroapopPost(VarroapopHandler):

    def post(self, jobId="000000100000011"):
        """
        Varroapop post handler.
        :param jobId:
        :return:
        """
        inputs = rest_validation.parse_inputs(request.json)

        if inputs:
            return rest_model_caller.model_run(self.name, jobId, inputs, module=varroapop)
        else:
            return rest_model_caller.error(self.name, jobId, inputs)