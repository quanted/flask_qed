import unittest
import pandas as pd
import numpy.testing as npt
import pkgutil
from StringIO import StringIO
from .. import stir_model_rest as stir_model
from tabulate import tabulate

# load transposed qaqc data for inputs
# works for local nosetests from parent directory
# but not for travis container that calls nosetests:
# csv_transpose_path_in = "./stir_qaqc_in_transpose.csv"
# pd_obj_inputs = pd.read_csv(csv_transpose_path_in, index_col=0, engine='python')
# this works for both local nosetests and travis deploy
data_inputs = StringIO(pkgutil.get_data(__package__, 'stir_qaqc_in_transpose.csv'))
pd_obj_inputs = pd.read_csv(data_inputs, index_col=0, engine='python')
print("stir inputs")
print(pd_obj_inputs.shape)
print(tabulate(pd_obj_inputs.iloc[:,0:5], headers='keys', tablefmt='fancy_grid'))
print(tabulate(pd_obj_inputs.iloc[:,6:10], headers='keys', tablefmt='fancy_grid'))
print(tabulate(pd_obj_inputs.iloc[:,11:13], headers='keys', tablefmt='fancy_grid'))
print(tabulate(pd_obj_inputs.iloc[:,14:17], headers='keys', tablefmt='fancy_grid'))

# load transposed qaqc data for expected outputs
# works for local nosetests from parent directory
# but not for travis container that calls nosetests:
# csv_transpose_path_exp = "./stir_qaqc_exp_transpose.csv"
# pd_obj_exp_out = pd.read_csv(csv_transpose_path_exp, index_col=0, engine='python')
# this works for both local nosetests and travis deploy
data_exp_outputs = StringIO(pkgutil.get_data(__package__, 'stir_qaqc_exp_transpose.csv'))
pd_obj_exp= pd.read_csv(data_exp_outputs, index_col=0, engine='python')
print("stir expected outputs")
print(pd_obj_exp.shape)
print(tabulate(pd_obj_exp.iloc[:,0:5], headers='keys', tablefmt='fancy_grid'))
print(tabulate(pd_obj_exp.iloc[:,6:10], headers='keys', tablefmt='fancy_grid'))
print(tabulate(pd_obj_exp.iloc[:,11:13], headers='keys', tablefmt='fancy_grid'))
print(tabulate(pd_obj_exp.iloc[:,14:17], headers='keys', tablefmt='fancy_grid'))
print(tabulate(pd_obj_exp.iloc[:,18:22], headers='keys', tablefmt='fancy_grid'))

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
        """
        integration test for stir.sat_air_conc
        """
        try:
            self.blackbox_method_int('sat_air_conc')
        finally:
            pass
        return

    def test_inh_rate_avian(self):
        """
        integration test for stir.inh_rate_avian
        """
        try:
            self.blackbox_method_int('inh_rate_avian')
        finally:
            pass
        return

    def test_vid_avian(self):
        """
        integration test for stir.vid_avian
        """
        try:
            self.blackbox_method_int('vid_avian')
        finally:
            pass
        return

    def test_inh_rate_mammal(self):
        """
        integration test for stir.inh_rate_mammal
        """
        try:
            self.blackbox_method_int('inh_rate_mammal')
        finally:
            pass
        return

    def test_vid_mammal(self):
        """
        integration test for stir.vid_mammal
        """
        try:
            self.blackbox_method_int('vid_mammal')
        finally:
            pass
        return

    def test_air_conc(self):
        """
        integration test for stir.air_conc
        """
        try:
            self.blackbox_method_int('air_conc')
        finally:
            pass
        return

    def test_sid_avian(self):
        """
        integration test for stir.sid_avian
        """
        try:
            self.blackbox_method_int('sid_avian')
        finally:
            pass
        return

    def test_sid_mammal(self):
        """
        integration test for stir.sid_mammal
        """
        try:
            self.blackbox_method_int('sid_mammal')
        finally:
            pass
        return

    def test_mammal_inhalation_ld50(self):
        """
        integration test for stir.mammal_inhalation_ld50
        """
        try:
            self.blackbox_method_int('mammal_inhalation_ld50')
        finally:
            pass
        return

    def test_adjusted_mammal_inhalation_ld50(self):
        """
        integration test for stir.adjusted_mammal_inhalation_ld50
        """
        try:
            self.blackbox_method_int('adjusted_mammal_inhalation_ld50')
        finally:
            pass
        return

    def test_estimated_avian_inhalation_ld50(self):
        """
        integration test for stir.estimated_avian_inhalation_ld50
        """
        try:
            self.blackbox_method_int('estimated_avian_inhalation_ld50')
        finally:
            pass
        return

    def test_adjusted_avian_inhalation_ld50(self):
        """
        integration test for stir.adjusted_avian_inhalation_ld50
        """
        try:
            self.blackbox_method_int('adjusted_avian_inhalation_ld50')
        finally:
            pass
        return

    def test_ratio_vid_avian(self):
        """
        integration test for stir.ratio_vid_avian
        """
        try:
            self.blackbox_method_int('ratio_vid_avian')
        finally:
            pass
        return

    def test_loc_vid_avian(self):
        """
        integration test for stir.loc_vid_avian
        """
        try:
            self.blackbox_method_str('loc_vid_avian')
        finally:
            pass
        return

    def test_ratio_sid_avian(self):
        """
        integration test for stir.ratio_sid_avian
        """
        try:
            self.blackbox_method_int('ratio_sid_avian')
        finally:
            pass
        return

    def test_loc_sid_avian(self):
        """
        integration test for stir.loc_sid_avian
        """
        try:
            self.blackbox_method_str('loc_sid_avian')
        finally:
            pass
        return

    def test_ratio_vid_mammal(self):
        """
        integration test for stir.ratio_vid_mammal
        """
        try:
            self.blackbox_method_int('ratio_vid_mammal')
        finally:
            pass
        return

    def test_loc_vid_mammal(self):
        """
        integration test for stir.loc_vid_mammal
        """
        try:
            self.blackbox_method_str('loc_vid_mammal')
        finally:
            pass
        return

    def test_ratio_sid_mammal(self):
        """
        integration test for stir.ratio_sid_mammal
        """
        try:
            self.blackbox_method_int('ratio_sid_mammal')
        finally:
            pass
        return

    def test_loc_sid_mammal(self):
        """
        integration test for stir.loc_sid_mammal
        """
        try:
            self.blackbox_method_str('loc_sid_mammal')
        finally:
            pass
        return

    def blackbox_method_int(self, output):
        """
        Helper method to reuse code for testing numpy array outputs from STIR model
        :param output: String; Pandas Series name (e.g. column name) without '_out'
        :return:
        """
        pd.set_option('display.float_format','{:.4E}'.format) # display model output in scientific notation
        result = stir_calc.pd_obj_out[output]
        expected = stir_calc.pd_obj_exp["exp_" + output]
        tab = pd.concat([result, expected], axis=1)
        print(" ")
        print(tabulate(tab, headers='keys', tablefmt='fancy_grid'))
        # npt.assert_array_almost_equal(result, expected, 4, '', True)
        rtol = 1e-5
        npt.assert_allclose(result, expected, rtol, 0, '', True)

    def blackbox_method_str(self, output):
        result = stir_calc.pd_obj_out[output]
        expected = stir_calc.pd_obj_exp["exp_" + output]
        tab = pd.concat([result, expected], axis=1)
        print(" ")
        print(tabulate(tab, headers='keys', tablefmt='fancy_grid'))
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