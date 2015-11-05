import pkgutil
import unittest
from StringIO import StringIO
from tabulate import tabulate

import numpy.testing as npt
import pandas as pd

from .. import iec_model_rest as iec_model

# load transposed qaqc data for inputs
#works for local nosetests from parent directory
# but not for travis container that calls nosestests:
#csv_transpose_path_in = "./tests/sip_qaqc_in_transpose.csv"
#pd_obj_inputs = pd.read_csv(csv_transpose_path_in, index_col=0, engine='python')
#this works for both local nosetests and travis deploy
data_inputs = StringIO(pkgutil.get_data(__package__, 'iec_qaqc_in_transpose.csv'))
pd_obj_inputs = pd.read_csv(data_inputs, index_col=0, engine='python')
print("iec inputs")
print(pd_obj_inputs.shape)
print(tabulate(pd_obj_inputs.iloc[:,0:5], headers='keys', tablefmt='fancy_grid'))
#print(tabulate(pd_obj_inputs.iloc[:,6:10], headers='keys', tablefmt='fancy_grid'))
#print(tabulate(pd_obj_inputs.iloc[:,11:16], headers='keys', tablefmt='fancy_grid'))

# load transposed qaqc data for inputs
#works for local nosetests, but not for travis container that calls nosetests:
#csv_transpose_path_exp = "./tests/sip_qaqc_exp_transpose.csv"
#pd_obj_exp_out = pd.read_csv(csv_transpose_path_exp, index_col=0, engine='python')
#this works for both local nosetests and travis deploy
data_exp = StringIO(pkgutil.get_data(__package__, 'iec_qaqc_exp_transpose.csv'))
pd_obj_exp = pd.read_csv(data_exp, index_col=0, engine='python')
#print("iec expected")
#print(pd_obj_exp.shape)
#print(tabulate(pd_obj_exp.iloc[:,0:5], headers='keys', tablefmt='fancy_grid'))
#print(tabulate(pd_obj_exp.iloc[:,6:10], headers='keys', tablefmt='fancy_grid'))


# create an instance of iec object with qaqc data
#print("####")
#print("dead here")
iec_calc = iec_model.iec("batch", pd_obj_inputs, pd_obj_exp)
#print("####")
#print(iec_calc)
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
    def integration_test_z_score_f(self):
        '''
        integration test for output iec.z_score_f
        '''
        try:
            self.blackbox_method_int('z_score_f')
        finally:
            pass
        return

    def integration_test_F8_f(self):
        '''
        integration test for output iec.F8_f
        '''
        try:
            self.blackbox_method_int('F8_f')
        finally:
            pass
        return

    def integration_test_chance_f(self):
        '''
        integration test for output iec.chance_f
        '''
        try:
            self.blackbox_method_int('chance_f')
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
        result = iec_calc.pd_obj_out[output + "_out"]
        expected = iec_calc.pd_obj_exp[output + "_exp"]
        tab = pd.concat([result, expected], axis=1)
        print(" ")
        print(tabulate(tab, headers='keys', tablefmt='fancy_grid'))
        #npt.assert_array_almost_equal(result, expected, 4, '', True)
        rtol = 1e-5
        npt.assert_allclose(result,expected,rtol,0,'',True)


# unittest will
# 1) call the setup method,
# 2) then call every method starting with "test",
# 3) then the teardown method
if __name__ == '__main__':
    #unittest.main()
    pass
