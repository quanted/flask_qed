import pkgutil
import unittest
from StringIO import StringIO
from tabulate import tabulate

import numpy.testing as npt
import pandas as pd
import pandas.util.testing as pdt

from .. import sip_model_rest as sip_model

# load transposed qaqc data for inputs
#works for local nosetests from parent directory
# but not for travis container that calls nosestests:
#csv_transpose_path_in = "./tests/sip_qaqc_in_transpose.csv"
#pd_obj_inputs = pd.read_csv(csv_transpose_path_in, index_col=0, engine='python')
#this works for both local nosetests and travis deploy
data_inputs = StringIO(pkgutil.get_data(__package__, 'sip_qaqc_in_transpose.csv'))
pd_obj_inputs = pd.read_csv(data_inputs, index_col=0, engine='python')
print("sip inputs")
print(pd_obj_inputs.shape)
print(tabulate(pd_obj_inputs.iloc[:,0:5], headers='keys', tablefmt='fancy_grid'))
print(tabulate(pd_obj_inputs.iloc[:,6:10], headers='keys', tablefmt='fancy_grid'))
print(tabulate(pd_obj_inputs.iloc[:,11:16], headers='keys', tablefmt='fancy_grid'))

# load transposed qaqc data for inputs
#works for local nosetests, but not for travis container that calls nosetests:
#csv_transpose_path_exp = "./tests/sip_qaqc_exp_transpose.csv"
#pd_obj_exp_out = pd.read_csv(csv_transpose_path_exp, index_col=0, engine='python')
#this works for both local nosetests and travis deploy
data_exp_outputs = StringIO(pkgutil.get_data(__package__, 'sip_qaqc_exp_transpose.csv'))
pd_obj_exp_out = pd.read_csv(data_exp_outputs, index_col=0, engine='python')
print("sip expected outputs")
print(pd_obj_exp_out.shape)
print(tabulate(pd_obj_exp_out.iloc[:,0:5], headers='keys', tablefmt='fancy_grid'))
print(tabulate(pd_obj_exp_out.iloc[:,6:10], headers='keys', tablefmt='fancy_grid'))
print(tabulate(pd_obj_exp_out.iloc[:,11:13], headers='keys', tablefmt='fancy_grid'))
print(tabulate(pd_obj_exp_out.iloc[:,14:16], headers='keys', tablefmt='fancy_grid'))

# create an instance of sip object with qaqc data
sip_calc = sip_model.sip("batch", pd_obj_inputs, pd_obj_exp_out)
test = {}


class TestSip(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        #adding to TestCase constructor so super
        super(TestSip, self).__init__(*args, **kwargs)
        self.ncases = len(pd_obj_inputs)

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
        '''
        integration test for output sip.dose_bird
        '''
        try:
            self.blackbox_method_int('dose_bird')
        finally:
            pass
        return

    def integration_test_dose_mamm(self):
        '''
        integration test for output sip.dose_mamm
        '''
        try:
            self.blackbox_method_int('dose_mamm')
        finally:
            pass
        return

    def integration_test_at_bird(self):
        '''
        integration test for output sip.at_bird
        '''
        try:
            self.blackbox_method_int('at_bird')
        finally:
            pass
        return

    def integration_test_at_mamm(self):
        '''
        integration test for output sip.at_mamm
        '''
        try:
            self.blackbox_method_int('at_mamm')
        finally:
            pass
        return

    def integration_test_fi_bird(self):
        '''
        integration test for output sip.fi_bird
        '''
        try:
            #self.blackbox_method('fi_bird')
            pass
        finally:
            pass
        return

    def integration_test_det(self):
        '''
        integration test for output sip.det
        '''
        try:
            self.blackbox_method_int('det')
        finally:
            pass
        return

    def integration_test_act(self):
        '''
        integration test for output sip.act
        '''
        try:
            self.blackbox_method_int('act')
        finally:
            pass
        return

    def integration_test_acute_bird(self):
        '''
        integration test for output sip.acute_bird
        '''
        try:
            self.blackbox_method_int('acute_bird')
        finally:
            pass
        return

    def integration_test_acuconb(self):
        '''
        integration test for output sip.acuconb
        '''
        try:
            self.blackbox_method_str('acuconb')
        finally:
            pass
        return

    def integration_test_acute_mamm(self):
        '''
        integration test for output sip.acute_mamm
        '''
        try:
            self.blackbox_method_int('acute_mamm')
        finally:
            pass
        return

    def integration_test_acuconm(self):
        '''
        integration test for output sip.acuconm
        '''
        try:
            self.blackbox_method_str('acuconm')
        finally:
            pass
        return

    def integration_test_chron_bird(self):
        '''
        integration test for output sip.chron_bird
        '''
        try:
            self.blackbox_method_int('chron_bird')
        finally:
            pass
        return

    def integration_test_chronconb(self):
        '''
        integration test for output sip.chronconb
        '''
        try:
            self.blackbox_method_str('chronconb')
        finally:
            pass
        return

    def integration_test_chron_mamm(self):
        '''
        integration test for output sip.chron_mamm
        '''
        try:
            self.blackbox_method_int('chron_mamm')
        finally:
            pass
        return

    def integration_test_chronconm(self):
        '''
        integration test for output sip.chronconm
        '''
        try:
            self.blackbox_method_str('chronconm')
        finally:
            pass
        return

    def blackbox_method_int(self, output):
        """
        Helper method to reuse code for testing numpy array outputs from SIP model
        :param output: String; Pandas Series name (e.g. column name) without '_out'
        :return:
        """
        pd.set_option('display.float_format','{:.4E}'.format) # display model output in scientific notation
        result = sip_calc.pd_obj_out[output + "_out"]
        expected = sip_calc.pd_obj_exp[output + "_exp"]
        tab = pd.concat([result, expected], axis=1)
        print(" ")
        print(tabulate(tab, headers='keys', tablefmt='fancy_grid'))
        # npt.assert_array_almost_equal(result, expected, 4, '', True)
        rtol = 1e-5
        npt.assert_allclose(result, expected, rtol, 0, '', True)

    def blackbox_method_str(self, output):
        result = sip_calc.pd_obj_out[output + "_out"]
        expected = sip_calc.pd_obj_exp[output + "_exp"]
        tab = pd.concat([result, expected], axis=1)
        print(" ")
        print(tabulate(tab, headers='keys', tablefmt='fancy_grid'))
        npt.assert_array_equal(result, expected)

# unittest will
# 1) call the setup method,
# 2) then call every method starting with "test",
# 3) then the teardown method
if __name__ == '__main__':
    #unittest.main()
    pass
