# -*- coding: utf-8 -*-
import unittest
import pandas as pd
import numpy.testing as npt
import pkgutil
from StringIO import StringIO
from .. import terrplant_model_rest as terrplant_model
from tabulate import tabulate

# load transposed qaqc data for inputs and expected outputs
# works for local nosetests from parent directory
# but not for travis container that calls nosetests:
# csv_transpose_path_in = "./terrplant_qaqc_in_transpose.csv"
# pd_obj_inputs = pd.read_csv(csv_transpose_path_in, index_col=0, engine='python')
# print(pd_obj_inputs)
# this works for both local nosetests and travis deploy
data_inputs = StringIO(pkgutil.get_data(__package__, 'terrplant_qaqc_in_transpose.csv'))
pd_obj_inputs = pd.read_csv(data_inputs, index_col=0, engine='python')
print("terrplant inputs")
print(pd_obj_inputs.shape)
print(tabulate(pd_obj_inputs.iloc[:,0:5], headers='keys', tablefmt='fancy_grid'))
print(tabulate(pd_obj_inputs.iloc[:,6:10], headers='keys', tablefmt='fancy_grid'))
print(tabulate(pd_obj_inputs.iloc[:,11:13], headers='keys', tablefmt='fancy_grid'))
print(tabulate(pd_obj_inputs.iloc[:,14:17], headers='keys', tablefmt='fancy_grid'))

# load transposed qaqc data for expected outputs
# works for local nosetests from parent directory
# but not for travis container that calls nosetests:
# csv_transpose_path_exp = "./terrplant_qaqc_exp_transpose.csv"
# pd_obj_exp_out = pd.read_csv(csv_transpose_path_exp, index_col=0, engine='python')
# print(pd_obj_exp_out)
# this works for both local nosetests and travis deploy
data_exp_outputs = StringIO(pkgutil.get_data(__package__, 'terrplant_qaqc_exp_transpose.csv'))
pd_obj_exp = pd.read_csv(data_exp_outputs, index_col=0, engine= 'python')
print("terrplant expected outputs")
print(pd_obj_exp.shape)
print(tabulate(pd_obj_exp.iloc[:,0:5], headers='keys', tablefmt='fancy_grid'))
print(tabulate(pd_obj_exp.iloc[:,6:10], headers='keys', tablefmt='fancy_grid'))
print(tabulate(pd_obj_exp.iloc[:,11:14], headers='keys', tablefmt='fancy_grid'))
print(tabulate(pd_obj_exp.iloc[:,15:16], headers='keys', tablefmt='fancy_grid'))

# create an instance of terrplant object with qaqc data
terrplant_calc = terrplant_model.terrplant("batch", pd_obj_inputs, pd_obj_exp)
print("####")
print(terrplant_calc)
test = {}


class TestTerrplant(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_rundry(self):
        """
        Integration test for terrplant.rundry
        """
        try:
            self.blackbox_method_int('rundry')
        finally:
            pass
        return

    def test_runsemi(self):
        """
        Integration test for terrplant.runsemi
        """
        try:
            self.blackbox_method_int('runsemi')
        finally:
            pass
        return

    def test_spray(self):
        """
        Integration test for terrplant.spray
        """
        try:
            self.blackbox_method_int('spray')
        finally:
            pass
        return
    def test_totaldry(self):
        """
        Integration test for terrplant.totaldry
        """
        try:
            self.blackbox_method_int('totaldry')
        finally:
            pass
        return
    def test_totalsemi(self):
        """
        Integration test for terrplant.totalsemi
        """
        try:
            self.blackbox_method_int('totalsemi')
        finally:
            pass
        return
    def test_nms_rq_dry(self):
        """
        Integration test for terrplant.nms_rq_dry
        """
        try:
            self.blackbox_method_int('nms_rq_dry')
        finally:
            pass
        return
    def test_nms_loc_dry(self):
        """
        Integration test for terrplant.nms_loc_dry
        """
        try:
            self.blackbox_method_str('nms_loc_dry')
        finally:
            pass
        return
    def test_nms_rq_semi(self):
        """
        Integration test for terrplant.nms_rq_semi
        """
        try:
            self.blackbox_method_int('nms_rq_semi')
        finally:
            pass
        return
    def test_nms_loc_semi(self):
        """
        Integration test for terrplant.nms_loc_semi
        """
        try:
            self.blackbox_method_str('nms_loc_semi')
        finally:
            pass
        return
    def test_nms_rq_spray(self):
        """
        Integration test for terrplant.nms_rq_spray
        """
        try:
            self.blackbox_method_int('nms_rq_spray')
        finally:
            pass
        return
    def test_nms_loc_spray(self):
        """
        Integration test for terrplant.nms_loc_spray
        """
        try:
            self.blackbox_method_str('nms_loc_spray')
        finally:
            pass
        return
    def test_lms_rq_dry(self):
        """
        Integration test for terrplant.lms_rq_dry
        """
        try:
            self.blackbox_method_int('lms_rq_dry')
        finally:
            pass
        return
    def test_lms_loc_dry(self):
        """
        Integration test for terrplant.lms_loc_dry
        """
        try:
            self.blackbox_method_str('lms_loc_dry')
        finally:
            pass
        return
    def test_lms_rq_semi(self):
        """
        Integration test for terrplant.lms_rq_semi
        """
        try:
            self.blackbox_method_int('lms_rq_semi')
        finally:
            pass
        return
    def test_lms_loc_semi(self):
        """
        Integration test for terrplant.lms_loc_semi
        """
        try:
            self.blackbox_method_str('lms_loc_semi')
        finally:
            pass
        return
    def test_lms_rq_spray(self):
        """
        Integration test for terrplant.lms_rq_spray
        """
        try:
            self.blackbox_method_int('lms_rq_spray')
        finally:
            pass
        return
    def test_lms_loc_spray(self):
        """
        Integration test for terrplant.lms_loc_spray
        """
        try:
            self.blackbox_method_str('lms_loc_spray')
        finally:
            pass
        return
    def test_nds_rq_dry(self):
        """
        Integration test for terrplant.nds_rq_dry
        """
        try:
            self.blackbox_method_int('nds_rq_dry')
        finally:
            pass
        return
    def test_nds_loc_dry(self):
        """
        Integration test for terrplant.nds_loc_dry
        """
        try:
            self.blackbox_method_str('nds_loc_dry')
        finally:
            pass
        return
    def test_nds_rq_semi(self):
        """
        Integration test for terrplant.nds_rq_semi
        """
        try:
            self.blackbox_method_int('nds_rq_semi')
        finally:
            pass
        return
    def test_nds_loc_semi(self):
        """
        Integration test for terrplant.nds_loc_semi
        """
        try:
            self.blackbox_method_str('nds_loc_semi')
        finally:
            pass
        return
    def test_nds_rq_spray(self):
        """
        Integration test for terrplant.nds_rq_spray
        """
        try:
            self.blackbox_method_int('nds_rq_spray')
        finally:
            pass
        return
    def test_nds_loc_spray(self):
        """
        Integration test for terrplant.nds_loc_spray
        """
        try:
            self.blackbox_method_str('nds_loc_spray')
        finally:
            pass
        return
    def test_lds_rq_dry(self):
        """
        Integration test for terrplant.lds_rq_dry
        """
        try:
            self.blackbox_method_int('lds_rq_dry')
        finally:
            pass
        return
    def test_lds_loc_dry(self):
        """
        Integration test for terrplant.lds_loc_dry
        """
        try:
            self.blackbox_method_str('lds_loc_dry')
        finally:
            pass
        return
    def test_lds_rq_semi(self):
        """
        Integration test for terrplant.lds_rq_semi
        """
        try:
            self.blackbox_method_int('lds_rq_semi')
        finally:
            pass
        return
    def test_lds_loc_semi(self):
        """
        Integration test for terrplant.lds_loc_semi
        """
        try:
            self.blackbox_method_str('lds_loc_semi')
        finally:
            pass
        return
    def test_lds_rq_spray(self):
        """
        Integration test for terrplant.lds_rq_spray
        """
        try:
            self.blackbox_method_int('lds_rq_spray')
        finally:
            pass
        return
    def test_lds_loc_spray(self):
        """
        Integration test for terrplant.lds_loc_spray
        """
        try:
            self.blackbox_method_str('lds_loc_spray')
        finally:
            pass
        return
    def test_min_nms_spray(self):
        """
        Integration test for terrplant.minnmsspray
        """
        try:
            self.blackbox_method_int('min_nms_spray')
        finally:
            pass
        return
    def test_min_lms_spray(self):
        """
        Integration test for terrplant.minlmsspray
        """
        try:
            self.blackbox_method_int('min_lms_spray')
        finally:
            pass
        return
    def test_min_nds_spray(self):
        """
        Integration test for terrplant.minndsspray
        """
        try:
            self.blackbox_method_int('min_nds_spray')
        finally:
            pass
        return
    def test_min_lds_spray(self):
        """
        Integration test for terrplant.minldsspray
        """
        try:
            self.blackbox_method_int('min_lds_spray')
        finally:
            pass
        return


    def blackbox_method_int(self, output):
        """
        Helper method to reuse code for testing numpy array outputs from TerrPlant model
        :param output: String; Pandas Series name (e.g. column name) without '_out'
        :return:
        """
        pd.set_option('display.float_format','{:.4E}'.format) # display model output in scientific notation
        result = terrplant_calc.pd_obj_out["out_" + output]
        expected = terrplant_calc.pd_obj_exp["exp_" + output]
        tab = pd.concat([result,expected], axis=1)
        print(" ")
        print(tabulate(tab, headers='keys', tablefmt='fancy_grid'))
        # npt.assert_array_almost_equal(result, expected, 4, '', True)
        rtol = 1e-5
        npt.assert_allclose(result, expected, rtol, 0, '', True)

    def blackbox_method_str(self, output):
        result = terrplant_calc.pd_obj_out["out_" + output]
        expected = terrplant_calc.pd_obj_exp["exp_" + output]
        tab = pd.concat([result,expected], axis=1)
        print(" ")
        print(tabulate(tab, headers='keys', tablefmt='fancy_grid'))
        npt.assert_array_equal(result, expected)

# unittest will
# 1) call the setup method,
# 2) then call every method starting with "test",
# 3) then the teardown method
if __name__ == '__main__':
    unittest.main()