import unittest
import stir_model_rest as stir_model
import pandas as pd
import numpy.testing as npt

# load transposed qaqc data for inputs and expected outputs
csv_transpose_path_in = "./stir_qaqc_in_transpose.csv"
pd_obj_inputs = pd.read_csv(csv_transpose_path_in, index_col=0, engine='python')
# print(pd_obj_inputs)
csv_transpose_path_exp = "./stir_qaqc_exp_transpose.csv"
pd_obj_exp_out = pd.read_csv(csv_transpose_path_exp, index_col=0, engine='python')
# print(pd_obj_exp_out)

# create an instance of stir object with qaqc data
stir_calc = stir_model.stir("batch", pd_obj_inputs, pd_obj_exp_out)
stir_empty = stir_model.stir("empty", pd_obj_inputs, pd_obj_exp_out)

class TestStir(unittest.TestCase):
    def setup(self):
        pass
        # setup the test as needed
        # e.g. pandas to open stir qaqc csv
        #  Read qaqc csv and create pandas DataFrames for inputs and expected outputs

    def test_blackbox_method(self):
        self.blackbox_method_int('sat_air_conc')
        self.blackbox_method_int('inh_rate_avian')
        self.blackbox_method_int('vid_avian')
        self.blackbox_method_int('inh_rate_mammal')
        self.blackbox_method_int('vid_mammal')
        self.blackbox_method_int('air_conc')
        self.blackbox_method_int('sid_avian')
        self.blackbox_method_int('sid_mammal')
        self.blackbox_method_int('mammal_inhalation_ld50')
        self.blackbox_method_int('adjusted_mammal_inhalation_ld50')
        self.blackbox_method_int('estimated_avian_inhalation_ld50')
        self.blackbox_method_int('adjusted_avian_inhalation_ld50')
        self.blackbox_method_int('ratio_vid_avian')
        self.blackbox_method_str('loc_vid_avian')
        self.blackbox_method_int('ratio_sid_avian')
        self.blackbox_method_str('loc_sid_avian')
        self.blackbox_method_int('ratio_vid_mammal')
        self.blackbox_method_str('loc_vid_mammal')
        self.blackbox_method_int('ratio_sid_mammal')
        self.blackbox_method_str('loc_sid_mammal')

    def blackbox_method_int(self, output):
        """
        Helper method to reuse code for testing numpy array outputs from STIR model
        :param output: String; Pandas Series name (e.g. column name) without '_out'
        :return:
        """
        result = stir_calc.pd_obj_out
        expected = stir_calc.pd_obj_exp
        npt.assert_array_almost_equal(result, expected, 4, '', True)

    def blackbox_method_str(self, output):
        result = stir_calc.pd_obj_out
        expected = stir_calc.pd_obj_exp
        npt.assert_array_equal(result, expected)

    def teardown(self):
        pass
        # teardown called after each test
        # e.g. maybe write test results to some text file



# unittest will
# 1) call the setup method,
# 2) then call every method starting with "test",
# 3) then the teardown method
if __name__ == '__main__':
    unittest.main()