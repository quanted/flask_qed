import unittest
import pandas as pd
import numpy.testing as npt
import pkgutil
from StringIO import StringIO
from .. import stir_model_rest as stir_model

# load transposed qaqc data for inputs
# works for local nosetests from parent directory
# but not for travis container that calls nosetests:
# csv_transpose_path_in = "./stir_qaqc_in_transpose.csv"
# pd_obj_inputs = pd.read_csv(csv_transpose_path_in, index_col=0, engine='python')
# this works for both local nosetests and travis deploy
data_inputs = StringIO(pkgutil.get_data(__package__, 'stir_qaqc_in_transpose.csv'))
pd_obj_inputs = pd.read_csv(data_inputs, index_col=0, engine='python')

# load transposed qaqc data for expected outputs
# works for local nosetests from parent directory
# but not for travis container that calls nosetests:
# csv_transpose_path_exp = "./stir_qaqc_exp_transpose.csv"
# pd_obj_exp_out = pd.read_csv(csv_transpose_path_exp, index_col=0, engine='python')
# this works for both local nosetests and travis deploy
data_exp_outputs = StringIO(pkgutil.get_data(__package__, 'stir_qaqc_exp_transpose.csv'))
pd_obj_exp= pd.read_csv(data_exp_outputs, index_col=0, engine='python')

# create an instance of stir object with qaqc data
stir_calc = stir_model.stir("batch", pd_obj_inputs, pd_obj_exp)
test = {}


class TestStir(unittest.TestCase):
    def setup(self):
        pass
        # setup the test as needed
        # e.g. pandas to open stir qaqc csv
        #  Read qaqc csv and create pandas DataFrames for inputs and expected outputs
#Note: commented-out rows contain output files that are not running properly in the subsequent blackbox_method test.
    def test_sat_air_conc(self):
        self.blackbox_method_int('sat_air_conc')

    def test_inh_rate_avian(self):
        self.blackbox_method_int('inh_rate_avian')

    def test_vid_avian(self):
        self.blackbox_method_int('vid_avian')

    def test_inh_rate_mammal(self):
        self.blackbox_method_int('inh_rate_mammal')

    def test_vid_mammal(self):
        self.blackbox_method_int('vid_mammal')

    def test_air_conc(self):
        self.blackbox_method_int('air_conc')

    def test_sid_avian(self):
        self.blackbox_method_int('sid_avian')

    def test_sid_mammal(self):
        self.blackbox_method_int('sid_mammal')

    def test_mammal_inhalation_ld50(self):
        self.blackbox_method_int('mammal_inhalation_ld50')

    def test_adjusted_mammal_inhalation_ld50(self):
        self.blackbox_method_int('adjusted_mammal_inhalation_ld50')

    def test_estimated_avian_inhalation_ld50(self):
        self.blackbox_method_int('estimated_avian_inhalation_ld50')

    def test_adjusted_avian_inhalation_ld50(self):
        self.blackbox_method_int('adjusted_avian_inhalation_ld50')

    def test_ratio_vid_avian(self):
        self.blackbox_method_int('ratio_vid_avian')

    def test_loc_vid_avian(self):
        self.blackbox_method_str('loc_vid_avian')

    def test_ratio_sid_avian(self):
        self.blackbox_method_int('ratio_sid_avian')

    def test_loc_sid_avian(self):
        self.blackbox_method_str('loc_sid_avian')

    def test_ratio_vid_mammal(self):
        self.blackbox_method_int('ratio_vid_mammal')

    def test_loc_vid_mammal(self):
        self.blackbox_method_str('loc_vid_mammal')

    def test_ratio_sid_mammal(self):
        self.blackbox_method_int('ratio_sid_mammal')

    def test_loc_sid_mammal(self):
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