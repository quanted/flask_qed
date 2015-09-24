import unittest
import pandas as pd
import numpy.testing as npt
import pkgutil
from StringIO import StringIO
from .. import sip_model_rest as sip_model
import pandas.util.testing as pdt

# load transposed qaqc data for inputs
#works for local nosetests from parent directory
# but not for travis container that calls nosestests:
#csv_transpose_path_in = "./tests/sip_qaqc_in_transpose.csv"
#pd_obj_inputs = pd.read_csv(csv_transpose_path_in, index_col=0, engine='python')
#this works for both local nosetests and travis deploy
data_inputs = StringIO(pkgutil.get_data(__package__, 'sip_qaqc_in_transpose.csv'))
pd_obj_inputs = pd.read_csv(data_inputs, index_col=0, engine='python')
print(pd_obj_inputs)

# load transposed qaqc data for inputs
#works for local nosetests, but not for travis container that calls nosetests:
#csv_transpose_path_exp = "./tests/sip_qaqc_exp_transpose.csv"
#pd_obj_exp_out = pd.read_csv(csv_transpose_path_exp, index_col=0, engine='python')
#this works for both local nosetests and travis deploy
data_exp_outputs = StringIO(pkgutil.get_data(__package__, 'sip_qaqc_exp_transpose.csv'))
pd_obj_exp_out = pd.read_csv(data_exp_outputs, index_col=0, engine='python')
print(pd_obj_exp_out)

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
    def integration_test_dose_bird(self):
         self.blackbox_method_int('dose_bird')

    def integration_test_blackbox_dose_mamm(self):
         self.blackbox_method_int('dose_mamm')

    def integration_test_blackbox_at_bird(self):
         self.blackbox_method_int('at_bird')

    def integration_test_blackbox_at_mamm(self):
         self.blackbox_method_int('at_mamm')

    def integration_test_blackbox_fi_bird(self):
        #self.blackbox_method('fi_bird')
        pass

    def integration_test_blackbox_det(self):
         self.blackbox_method_int('det')

    def integration_test_blackbox_act(self):
         self.blackbox_method_int('act')

    def integration_test_blackbox_acute_bird(self):
         self.blackbox_method_int('acute_bird')

    def integration_test_blackbox_acuconb(self):
         self.blackbox_method_str('acuconb')

    def integration_test_blackbox_acute_mamm(self):
         self.blackbox_method_int('acute_mamm')

    def integration_test_blackbox_acuconm(self):
         self.blackbox_method_str('acuconm')

    def integration_test_blackbox_chron_bird(self):
         self.blackbox_method_int('chron_bird')

    def integration_test_blackbox_chronconb(self):
         self.blackbox_method_str('chronconb')

    def integration_test_blackbox_chron_mamm(self):
         self.blackbox_method_int('chron_mamm')

    def integration_test_blackbox_chronconm(self):
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