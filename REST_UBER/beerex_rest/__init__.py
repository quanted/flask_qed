from flask_restful import Resource
from ubertool.ubertool.beerex import beerex
from flask import request
from REST_UBER import rest_validation, rest_schema, rest_model_caller


class BeerexHandler(Resource):
    def __init__(self):
        self.name = "Bee-REX"

    @staticmethod
    def get_model_inputs():
        """
        Return model's input class.
        :return:
        """
        return beerex.BeerexInputs()

    @staticmethod
    def get_model_outputs():
        """
        Return model's output class.
        :return:
        """
        return beerex.BeerexOutputs()


class BeerexGet(BeerexHandler):

    def get(self, jobId="YYYYMMDDHHMMSSuuuuuu"):
        """
        Beerex get handler.
        :param jobId:
        :return:
        """
        return rest_schema.get_schema(self.name, jobId)


class BeerexPost(BeerexHandler):

    def post(self, jobId="000000100000011"):
        """
        Beerex post handler.
        :param jobId:
        :return:
        """
        inputs = rest_validation.parse_inputs(request.json)

        if inputs:
            return rest_model_caller.model_run(self.name, jobId, inputs, module=beerex)
        else:
            return rest_model_caller.error(self.name, jobId, inputs)
