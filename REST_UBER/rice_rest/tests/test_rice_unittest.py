import unittest

import numpy.testing as npt
import pandas as pd
import pandas.util.testing as pdt

from .. import rice_model_rest as rice_model

# create empty pandas dataframes to create empty sip object for testing
df_empty = pd.DataFrame()
# create an empty sip object
rice_empty = rice_model.rice("empty", df_empty, df_empty)

test = {}


class TestRice(unittest.TestCase):
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

    #   dsed * area * pb
    #   (self.dsed * self.area * self.pb)
    def test_Calcmsed(self):
        rice_empty.dsed = pd.Series([2.2], dtype='float')
        rice_empty.area = pd.Series([3.3], dtype='float')
        rice_empty.pb = pd.Series([4.4], dtype='float')

        result = rice_empty.Calcmsed()
        npt.assert_array_almost_equal(result, 31.944, 4, '', True)
        return

    # (self.dw * self.area) + (self.dsed * self.osed * self.area)
    def test_Calcvw(self):
        rice_empty.dw = pd.Series([2.2], dtype='float')
        rice_empty.area = pd.Series([3.3], dtype='float')
        rice_empty.dsed = pd.Series([4.4], dtype='float')
        rice_empty.osed = pd.Series([5.5], dtype='float')

        result = rice_empty.Calcvw()
        npt.assert_array_almost_equal(result, 87.12, 4, '', True)
        return

    # (self.mai/self.area)*10000
    def test_Calcmass_area(self):
        rice_empty.area = pd.Series([100.0], dtype='float')
        rice_empty.mai = pd.Series([90.0], dtype='float')
        result = rice_empty.Calcmass_area()
        npt.assert_array_almost_equal(result, 9000.0, 4, '', True)
        return

    # (self.out_mass_area / (self.dw + (self.dsed * (self.osed + (self.pb * self.Kd*1e-5)))))*100
    def test_Calccw(self):
        rice_empty.dw = pd.Series([5.0], dtype='float')
        rice_empty.dsed = pd.Series([4.0], dtype='float')
        rice_empty.osed = pd.Series([3.0], dtype='float')
        rice_empty.pb = pd.Series([2.0], dtype='float')
        rice_empty.Kd = pd.Series([100000.0], dtype='float')
        rice_empty.out_mass_area = pd.Series([400.0], dtype='float')
        result = rice_empty.Calccw()
        npt.assert_array_almost_equal(result, 1600.0, 4, '', True)
        return



# unittest will
# 1) call the setup method,
# 2) then call every method starting with "test",
# 3) then the teardown method
if __name__ == '__main__':
    unittest.main()
    #pass