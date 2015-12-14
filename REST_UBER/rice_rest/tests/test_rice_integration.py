import pkgutil
import unittest
import pandas as pd
import numpy.testing as npt
from .. import rice_model_rest as rice_model
from StringIO import StringIO
from tabulate import tabulate
import pandas.util.testing as pdt

# load transposed qaqc data for inputs
#csv_transpose_path_in = "./tests/rice_qaqc_in_transpose.csv"
#csv_transpose_path_in = "./rice_qaqc_in_transpose.csv"
#pd_obj_inputs = pd.read_csv(csv_transpose_path_in, index_col=0, engine='python')
# print(pd_obj_inputs)
# load transposed qaqc data for inputs
#csv_transpose_path_exp = "./tests/rice_qaqc_exp_transpose.csv"
#csv_transpose_path_exp = "./rice_qaqc_exp_transpose.csv"
#pd_obj_exp_out = pd.read_csv(csv_transpose_path_exp, index_col=0, engine='python')
# print(pd_obj_exp_out)
data_inputs = StringIO(pkgutil.get_data(__package__, 'rice_qaqc_in_transpose.csv'))
pd_obj_inputs = pd.read_csv(data_inputs, index_col=0, engine='python')
print("rice inputs")
print(pd_obj_inputs.shape)
print(tabulate(pd_obj_inputs.iloc[:,:], headers='keys', tablefmt='fancy_grid'))

# load transposed qaqc data for inputs
#works for local nosetests, but not for travis container that calls nosetests:
#csv_transpose_path_exp = "./tests/sip_qaqc_exp_transpose.csv"
#pd_obj_exp_out = pd.read_csv(csv_transpose_path_exp, index_col=0, engine='python')
#this works for both local nosetests and travis deploy
data_exp_outputs = StringIO(pkgutil.get_data(__package__, 'rice_qaqc_exp_transpose.csv'))
pd_obj_exp_out = pd.read_csv(data_exp_outputs, index_col=0, engine='python')
print("rice expected outputs")
print(pd_obj_exp_out.shape)
print(tabulate(pd_obj_exp_out.iloc[:,:], headers='keys', tablefmt='fancy_grid'))

# create an instance of rice object with qaqc data
rice_calc = rice_model.rice("batch", pd_obj_inputs, pd_obj_exp_out)
test = {}

class Testrice(unittest.TestCase):
    def setup(self):
        pass
        # rice2 = rice_model.rice(0, pd_obj_inputs, pd_obj_exp_out)
        # setup the test as needed
        # e.g. pandas to open rice qaqc csv
        #  Read qaqc csv and create pandas DataFrames for inputs and expected outputs

    def teardown(self):
        pass
        # teardown called after each test
        # e.g. maybe write test results to some text file

#Note: commented-out rows contain output files that are not running properly in the subsequent blackbox_method test.
    def test_integration_Calcmsed(self):
         self.blackbox_method_float('msed')

    def test_integration_Calcvw(self):
         self.blackbox_method_float('vw')

    def test_integration_Calcmass_area(self):
         self.blackbox_method_float('mass_area')

    def test_integration_Calccw(self):
         self.blackbox_method_float('cw')


    def blackbox_method_float(self, output):
        """
        Helper method to reuse code for testing numpy array outputs from rice model
        :param output: String; Pandas Series name (e.g. column name) without '_out'
        :return:
        """
        pd.set_option('display.float_format','{:.4E}'.format) # display model output in scientific notation
        result = rice_calc.pd_obj_out["out_" + output]
        expected = rice_calc.pd_obj_exp["exp_" + output]
        # npt.assert_array_almost_equal(result, expected, 4, '', True)
        rtol = 1e-5
        npt.assert_allclose(result, expected, rtol, 0, '', True)

# unittest will
# 1) call the setup method,
# 2) then call every method starting with "test",
# 3) then the teardown method
if __name__ == '__main__':
    unittest.main()
    pass