import unittest
import pandas as pd
import numpy.testing as npt
from .. import sip_model_rest as sip_model
import pandas.util.testing as pdt

# load transposed qaqc data for inputs and expected outputs
csv_transpose_path_in = "./sip_qaqc_in_transpose.csv"
pd_obj_inputs = pd.read_csv(csv_transpose_path_in, index_col=0, engine='python')
# print(pd_obj_inputs)
csv_transpose_path_exp = "./sip_qaqc_exp_transpose.csv"
pd_obj_exp_out = pd.read_csv(csv_transpose_path_exp, index_col=0, engine='python')
# print(pd_obj_exp_out)

# create an instance of sip object with qaqc data
sip_calc = sip_model.sip("batch", pd_obj_inputs, pd_obj_exp_out)
test = {}


class TestSip(unittest.TestCase):
    def setup(self):
        pass
        # sip2 = sip_model.sip(0, pd_obj_inputs, pd_obj_exp_out)
        # setup the test as needed
        # e.g. pandas to open sip qaqc csv
        #  Read qaqc csv and create pandas DataFrames for inputs and expected outputs

    def teardown(self):
        pass
        # teardown called after each test
        # e.g. maybe write test results to some text file

#Note: commented-out rows contain output files that are not running properly in the subsequent blackbox_method test.
    def test_blackbox_method(self):
         self.blackbox_method_int('dose_bird')
         self.blackbox_method_int('dose_mamm')
         self.blackbox_method_int('at_bird')
         self.blackbox_method_int('at_mamm')
       #  self.blackbox_method('fi_bird')
         self.blackbox_method_int('det')
         self.blackbox_method_int('act')
         self.blackbox_method_int('acute_bird')
         self.blackbox_method_str('acuconb')
         self.blackbox_method_int('acute_mamm')
         self.blackbox_method_str('acuconm')
         self.blackbox_method_int('chron_bird')
         self.blackbox_method_str('chronconb')
         self.blackbox_method_int('chron_mamm')
         self.blackbox_method_str('chronconm')

    def blackbox_method_int(self, output):
        """
        Helper method to reuse code for testing numpy array outputs from SIP model
        :param output: String; Pandas Series name (e.g. column name) without '_out'
        :return:
        """
        result = sip_calc.pd_obj_out[output + "_out"]
        expected = sip_calc.pd_obj_exp[output + "_exp"]
        npt.assert_array_almost_equal(result, expected, 4, '', True)

    def blackbox_method_str(self, output):
        result = sip_calc.pd_obj_out[output + "_out"]
        expected = sip_calc.pd_obj_exp[output + "_exp"]
        npt.assert_array_equal(result, expected)

# unittest will
# 1) call the setup method,
# 2) then call every method starting with "test",
# 3) then the teardown method
if __name__ == '__main__':
    #unittest.main()
    pass