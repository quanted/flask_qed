from flask_restful import Resource
from ubertool.ubertool.iec import iec
from flask import request
import pandas as pd


class IecHandler(Resource):
    def __init__(self):
        self.name = "iec"

    def get(self, jid):
        """
        IEC get handler.
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
        IEC post handler.
        :param jid:
        :return:
        """
        pd_obj = pd.DataFrame.from_dict(request.json["inputs"], dtype='float64')
        iec_obj = iec.Iec(pd_obj, None)
        iec_obj.execute_model()
        inputs_json, outputs_json, exp_out_json = iec_obj.get_dict_rep(iec_obj)

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
        return iec.IecInputs()

    @staticmethod
    def get_model_outputs():
        """
        Return model's output class.
        :return:
        """
        return iec.IecOutputs()
