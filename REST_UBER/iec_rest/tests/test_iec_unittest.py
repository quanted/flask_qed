import unittest

import numpy.testing as npt
import pandas as pd

from .. import iec_model_rest as iec_model

# create empty pandas dataframes to create empty sip object for testing
df_empty = pd.DataFrame()
# create an empty sip object
iec_empty = iec_model.iec("empty", df_empty, df_empty)

rtol = 1e-5 # set relative tolerance level for npt.assert_allclose assertion tests
test = {}

class TestIEC(unittest.TestCase):
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

    def test_z_score_f(self):
        '''
        unittest for function iec.z_score_f:
        '''
        try:
            iec_empty.threshold = pd.Series([0.6])
            iec_empty.LC50 = pd.Series([3])
            iec_empty.dose_response = pd.Series([2.5])
            result = iec_empty.z_score_f()
            #npt.assert_array_almost_equal(result, -0.554622, 4, '', True)
            npt.assert_allclose(result,-0.554622,rtol,0,'',True)
        finally:
            pass
        return

    def test_F8_f(self):
        '''
        unittest for function iec.F8_f:
        '''
        try:
            iec_empty.z_score_f_out = pd.Series([-0.87])
            result = iec_empty.F8_f()
            #npt.assert_array_almost_equal(result, 0.19215, 4, '', True)
            npt.assert_allclose(result,0.19215,rtol,0,'',True)
        finally:
            pass
        return

    def test_chance_f(self):
        '''
        unittest for function iec.chance_f:
        '''
        try:
            iec_empty.F8_f_out = pd.Series([0.34])
            result = iec_empty.chance_f()
            #npt.assert_array_almost_equal(result, 2.941176, 4, '', True)
            npt.assert_allclose(result,2.941176,rtol,0,'',True)
        finally:
            pass
        return

# unittest will
# 1) call the setup method,
# 2) then call every method starting with "test",
# 3) then the teardown method
if __name__ == '__main__':
    unittest.main()
    #pass
