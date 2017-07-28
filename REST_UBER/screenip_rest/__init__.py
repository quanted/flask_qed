from flask_restful import Resource
from ubertool.ubertool.screenip import screenip_exe as screenip
from flask import request
from REST_UBER import rest_validation, rest_schema, rest_model_caller


class ScreenipHandler(Resource):
    def __init__(self):
        self.name = "screenip"

    @staticmethod
    def get_model_inputs():
        """
        Return model's input class.
        :return:
        """
        return screenip.ScreenipInputs()

    @staticmethod
    def get_model_outputs():
        """
        Return model's output class.
        :return:
        """
        return screenip.ScreenipOutputs()


class ScreenipGet(ScreenipHandler):

    def get(self, jobId="YYYYMMDDHHMMSSuuuuuu"):
        """
        SIP get handler.
        :param jobId:
        :return:
        """
        return rest_schema.get_schema(self.name, jobId)


class ScreenipPost(ScreenipHandler):

    def post(self, jobId="000000100000011"):
        """
        SIP post handler.
        :param jobId:
        :return:
        """
        inputs = rest_validation.parse_inputs(request.json)
        print("ScreenipPost")
        if inputs:
            return rest_model_caller.model_run(self.name, jobId, inputs, module=screenip)
        else:
            return rest_model_caller.error(self.name, jobId, inputs)
