import unittest
import pandas as pd
import numpy.testing as npt
from rice_rest import rice_model_rest as rice_model
import pandas.util.testing as pdt

# load transposed qaqc data for inputs
#csv_transpose_path_in = "./tests/rice_qaqc_in_transpose.csv"
csv_transpose_path_in = "./rice_qaqc_in_transpose.csv"
pd_obj_inputs = pd.read_csv(csv_transpose_path_in, index_col=0, engine='python')
# print(pd_obj_inputs)
# load transposed qaqc data for inputs
#csv_transpose_path_exp = "./tests/rice_qaqc_exp_transpose.csv"
csv_transpose_path_exp = "./rice_qaqc_exp_transpose.csv"
pd_obj_exp_out = pd.read_csv(csv_transpose_path_exp, index_col=0, engine='python')
# print(pd_obj_exp_out)

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
    def test_blackbox_dose_bird(self):
         self.blackbox_method_float('Calcmsed')

    def test_blackbox_dose_mamm(self):
         self.blackbox_method_int('Calcvw')

    def test_blackbox_at_bird(self):
         self.blackbox_method_int('Calcmass_area')

    def test_blackbox_at_mamm(self):
         self.blackbox_method_int('Calccw')


    def blackbox_method_float(self, output):
        """
        Helper method to reuse code for testing numpy array outputs from rice model
        :param output: String; Pandas Series name (e.g. column name) without '_out'
        :return:
        """
        result = rice_calc.pd_obj_out[output + "_out"]
        expected = rice_calc.pd_obj_exp[output + "_exp"]
        npt.assert_array_almost_equal(result, expected, 4, '', True)

    def blackbox_method_str(self, output):
        result = rice_calc.pd_obj_out[output + "_out"]
        expected = rice_calc.pd_obj_exp[output + "_exp"]
        npt.assert_array_equal(result, expected)

# unittest will
# 1) call the setup method,
# 2) then call every method starting with "test",
# 3) then the teardown method
if __name__ == '__main__':
    #unittest.main()
    pass