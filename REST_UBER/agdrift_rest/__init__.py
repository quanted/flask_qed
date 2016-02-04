from flask_restful import Resource
from ubertool.ubertool.agdrift import agdrift
from REST_UBER.agdrift_rest import documentation
from flask import request
import pandas as pd


class AgdriftHandler(Resource):
    def __init__(self):
        self.name = "agdrift"
        self.api_spec = documentation.Documentation(self.name)

    def get(self, jid="000000100000011"):
        """
        Agdrift get handler.
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
        Agdrift post handler.
        :param jid:
        :return:
        """
        pd_obj = pd.DataFrame.from_dict(request.json["inputs"], dtype='float64')
        agdrift_obj = agdrift.Agdrift(pd_obj, None)
        agdrift_obj.execute_model()
        inputs_json, outputs_json, exp_out_json = agdrift_obj.get_dict_rep(agdrift_obj)

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
        Return agdrift input class.
        :return:
        """
        return agdrift.AgdriftInputs()

    @staticmethod
    def get_model_outputs():
        """
        Return agdrift output class.
        :return:
        """
        return agdrift.AgdriftOutputs()
