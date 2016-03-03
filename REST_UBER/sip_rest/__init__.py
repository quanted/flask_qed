from flask_restful import Resource
from ubertool.ubertool.sip import sip
from flask import request
import pandas as pd
from REST_UBER import rest_validation, rest_schema


class SipHandler(Resource):
    def __init__(self):
        self.name = "sip"

    def get(self, jobId="YYYYMMDDHHMMSSuuuuuu"):
        """
        SIP get handler.
        :param jobId:
        :return:
        """
        return rest_schema.get_schema(self.name, jobId)

    def post(self, jobId="000000100000011"):
        """
        SIP post handler.
        :param jobId:
        :return:
        """
        inputs = rest_validation.parse_inputs(request.json)
        pd_obj = pd.DataFrame.from_dict(inputs, dtype='float64')
        sip_obj = sip.Sip(pd_obj, None)
        sip_obj.execute_model()
        inputs_json, outputs_json, exp_out_json = sip_obj.get_dict_rep(sip_obj)

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
        return sip.SipInputs()

    @staticmethod
    def get_model_outputs():
        """
        Return model's output class.
        :return:
        """
        return sip.SipOutputs()