from flask_restful import Resource
from ubertool.ubertool.sam import sam_exe as sam
from flask import request
from REST_UBER import rest_validation, rest_schema, rest_model_caller
from celery_qed import tasks

class SamHandler(Resource):
    def __init__(self):
        self.name = "sam"

    @staticmethod
    def get_model_inputs():
        """
        Return model's input class.
        :return:
        """
        return sam.SamInputs()

    @staticmethod
    def get_model_outputs():
        """
        Return model's output class.
        :return:
        """
        return sam.SamOutputs()


class SamGet(SamHandler):

    def get(self, jobId="YYYYMMDDHHMMSSuuuuuu"):
        """
        SAM get handler.
        :param jobId:
        :return:
        """

        return rest_schema.get_schema(self.name, jobId)


class SamStatus(SamHandler):

    def get(self, jobId="YYYYMMDDHHMMSSuuuuuu"):
        """
        SAM task status
        :param jobId:
        :return:
        """
        return tasks.sam_status(jobId)


class SamPost(SamHandler):

    def post(self, jobId="000000100000011"):
        """
        SAM post handler.
        :param jobId:
        :return:
        """

        inputs = rest_validation.parse_inputs(request.json)

        if inputs:
            # return rest_model_caller.model_run(self.name, jobId, inputs, module=sam)
            tasks.sam_run(jobId, inputs)
            return
        else:
            return rest_model_caller.error(self.name, jobId, inputs)
