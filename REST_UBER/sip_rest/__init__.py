from flask_restful import Resource
from ubertool.ubertool.sip import sip
from flask import request
import pandas as pd


class SipHandler(Resource):
    def get(self, jid):
        """
        Terrplant get handler.
        :param jid:
        :return:
        """
        return {'result': 'model=sip, jid=%s' % jid}

    def post(self, jid):
        """
        Terrplant post handler.
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
        Return terrplant input class.
        :return:
        """
        return sip.SipInputs()

    @staticmethod
    def get_model_outputs():
        """
        Return terrplant output class.
        :return:
        """
        return sip.SipOutputs()