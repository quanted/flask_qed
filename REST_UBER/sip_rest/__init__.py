from flask_restful import Resource
from REST_UBER.sip_rest import documentation
from ubertool.ubertool.sip import sip
from flask import request
import pandas as pd


class SipHandler(Resource):
    def __init__(self):
        self.name = "sip"
        self.api_spec = documentation.Documentation(self.name)

    def get(self, jid):
        """
        SIP get handler.
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
        SIP post handler.
        :param jid:
        :return:
        """
        pd_obj = pd.DataFrame.from_dict(request.json["inputs"], dtype='float64')
        sip_obj = sip.Sip(pd_obj, None)
        sip_obj.execute_model()
        inputs_json, outputs_json, exp_out_json = sip_obj.get_dict_rep(sip_obj)

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