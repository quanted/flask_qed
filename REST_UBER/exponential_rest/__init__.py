from flask_restful import Resource
from ubertool.ubertool.exponential import exponential_exe as exponential
from flask import request
from REST_UBER import rest_validation, rest_schema, rest_model_caller


class ExponentialHandler(Resource):
    def __init__(self):
        self.name = "exponential"

    @staticmethod
    def get_model_inputs():
        """
        Return model's input class.
        :return:
        """
        return exponential.ExponentialInputs()

    @staticmethod
    def get_model_outputs():
        """
        Return model's output class.
        :return:
        """
        return exponential.ExponentialOutputs()


class ExponentialGet(ExponentialHandler):

    def get(self, jobId="YYYYMMDDHHMMSSuuuuuu"):
        """
        Exponential get handler.
        :param jobId:
        :return:
        """
        return rest_schema.get_schema(self.name, jobId)


class ExponentialPost(ExponentialHandler):

    def post(self, jobId="000000100000011"):
        """
        Exponential post handler.
        :param jobId:
        :return:
        """
        inputs = rest_validation.parse_inputs(request.json)

        if inputs:
            return rest_model_caller.model_run(self.name, jobId, inputs, module=exponential)
        else:
            return rest_model_caller.error(self.name, jobId, inputs)
