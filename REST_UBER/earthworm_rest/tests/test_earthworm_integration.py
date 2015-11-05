# -*- coding: utf-8 -*-

from .. import earthworm_model_rest as earthworm_model
import pandas as pd
import numpy.testing as npt
import unittest
import pkgutil
from StringIO import StringIO
from tabulate import tabulate

# load transposed qaqc data for inputs and expected outputs
# works for local nosetests from parent directory
# but not for travis container that calls nosetests:
# csv_transpose_path_in = "./terrplant_qaqc_in_transpose.csv"
# pd_obj_inputs = pd.read_csv(csv_transpose_path_in, index_col=0, engine='python')
# print(pd_obj_inputs)
# this works for both local nosetests and travis deploy
data_inputs = StringIO(pkgutil.get_data(__package__, 'earthworm_qaqc_in_transpose.csv'))
pd_obj_inputs = pd.read_csv(data_inputs, index_col=0, engine='python')
print("earthworm inputs")
print(pd_obj_inputs.shape)
print(tabulate(pd_obj_inputs.iloc[:,0:5], headers='keys', tablefmt='fancy_grid'))
print(tabulate(pd_obj_inputs.iloc[:,6:11], headers='keys', tablefmt='fancy_grid'))
print(tabulate(pd_obj_inputs.iloc[:,12:17], headers='keys', tablefmt='fancy_grid'))

# load transposed qaqc data for expected outputs
# works for local nosetests from parent directory
# but not for travis container that calls nosetests:
# csv_transpose_path_exp = "./terrplant_qaqc_exp_transpose.csv"
# pd_obj_exp_out = pd.read_csv(csv_transpose_path_exp, index_col=0, engine='python')
# print(pd_obj_exp_out)
# this works for both local nosetests and travis deploy
data_exp_outputs = StringIO(pkgutil.get_data(__package__, 'earthworm_qaqc_exp_transpose.csv'))
pd_obj_exp = pd.read_csv(data_exp_outputs, index_col=0, engine= 'python')
print("earthworm expected outputs")
print(pd_obj_exp.shape)
print(tabulate(pd_obj_exp.iloc[:,0:1], headers='keys', tablefmt='fancy_grid'))

earthworm_calc = earthworm_model.earthworm("batch", pd_obj_inputs, pd_obj_exp)
print("####")
print(earthworm_calc)
test = {}


class TestEarthworm(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_earthworm_fugacity(self):
        """
        Integration test for earthworm.earthworm_fugacity
        """
        try:
            self.blackbox_method_int('earthworm_fugacity')
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
        result = earthworm_calc.pd_obj_out[output + "_out"]
        expected = earthworm_calc.pd_obj_exp[output + "_exp"]
        tab = pd.concat([result,expected], axis=1)
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
    unittest.main()