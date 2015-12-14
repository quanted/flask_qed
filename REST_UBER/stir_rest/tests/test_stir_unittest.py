import unittest
import pandas as pd
import numpy.testing as npt
import pandas.util.testing as pdt

#following works when running test script in parent directory as package:
# python -m tests.stir_unit_test
# following works for running as nosetests from parent directory:
#importing as a package (specified in ../../setup.py
from .. import stir_model_rest as stir_model

# # load transposed qaqc data for inputs and expected outputs
# csv_transpose_path_in = "./stir_qaqc_in_transpose.csv"
# pd_obj_inputs = pd.read_csv(csv_transpose_path_in, index_col=0, engine='python')
# # print(pd_obj_inputs)
# csv_transpose_path_exp = "./stir_qaqc_exp_transpose.csv"
# pd_obj_exp_out = pd.read_csv(csv_transpose_path_exp, index_col=0, engine='python')
# # print(pd_obj_exp_out)

# create empty pandas dataframes to create empty stir object
df_empty = pd.DataFrame()
stir_empty = stir_model.stir("empty", df_empty, df_empty)

test = {}

class TestStir(unittest.TestCase):
    def setup(self):
        pass
        # setup the test as needed
        # e.g. pandas to open stir qaqc csv
        #  Read qaqc csv and create pandas DataFrames for inputs and expected outputs

    # each of these functions are queued by "run_methods" and have outputs defined as properties in the stir qaqc

    # eq. 1 saturated air concentration in mg/m^3
    def test_CalcSatAirConc(self):
        """
        unittest for function stir.CalcSatAirConc
        """
        # self.sat_air_conc = (self.vapor_pressure * self.molecular_weight * conv)/(pressure * air_vol)
        try:
            stir_empty.vapor_pressure = pd.Series([0.000008])
            stir_empty.molecular_weight = pd.Series([200.])
            result = stir_empty.CalcSatAirConc()
            npt.assert_array_almost_equal(result,0.086105, 4, '', True)
        finally:
            pass
        return

    # eq. 2 Avian inhalation rate
    def test_CalcInhRateAvian(self):
        """
        unittest for function stir.CalcInhRateAvian
        """
        # self.inh_rate_avian = magic1 * (self.body_weight_assessed_bird**magic2) * conversion * activity_factor
        try:
            stir_empty.body_weight_assessed_bird = pd.Series([0.05])
            result = stir_empty.CalcInhRateAvian()
            npt.assert_array_almost_equal(result,5090.9373, 4, '', True)
        finally:
            pass
        return

    # eq. 3  Maximum avian vapor inhalation dose
    def test_CalcVidAvian(self):
        """
        unittest for function stir.CalcVidAvian
        """
        # self.vid_avian = (self.sat_air_conc * self.inh_rate_avian * duration_hours)/(conversion_factor * self.body_weight_assessed_bird)
        try:
            stir_empty.sat_air_conc = pd.Series([200.])
            stir_empty.inh_rate_avian = pd.Series([10.])
            stir_empty.body_weight_assessed_bird = pd.Series([0.05])
            result = stir_empty.CalcVidAvian()
            npt.assert_array_almost_equal(result,0.04, 4, '', True)
        finally:
            pass
        return

    # eq. 4 Mammalian inhalation rate
    def test_CalcInhRateMammal(self):
        """
        unittest for function stir.CalcInhRateMammal
        """
        # self.inh_rate_mammal = magic1 * (self.body_weight_assessed_mammal**magic2) * minutes_conversion * activity_factor
        try:
            stir_empty.body_weight_assessed_mammal = pd.Series([0.08])
            result = stir_empty.CalcInhRateMammal()
            npt.assert_array_almost_equal(result,9044.4821, 4, '', True)
        finally:
            pass
        return

    # eq. 5 Maximum mammalian vapor inhalation dose
    def test_CalcVidMammal(self):
        """
        unittest for function stir.CalcVidMammal
        """
        # self.vid_mammal = (self.sat_air_conc * self.inh_rate_mammal * duration_hours)/(conversion_factor * self.body_weight_assessed_mammal)
        try:
            stir_empty.sat_air_conc = pd.Series([100.])
            stir_empty.inh_rate_mammal = pd.Series([50.])
            stir_empty.body_weight_assessed_mammal = pd.Series([0.08])
            result = stir_empty.CalcVidMammal()
            npt.assert_array_almost_equal(result, 0.0625, 4, '', True)
        finally:
            pass
        return

    # eq. 6 Air column concentration after spray
    def test_CalcConcAir(self):
        """
        unittest for function stir.CalcConcAir
        """
        # conversion_factor = 100. #cm/m
        # cf_g_lbs = 453.59237
        # cf_mg_g = 1000.
        # cf_cm2_acre = 40468564.2
        # self.air_conc = ((self.application_rate*cf_g_lbs*cf_mg_g)/cf_cm2_acre)/(self.column_height * conversion_factor)
        try:
            stir_empty.application_rate = pd.Series([2.])
            stir_empty.column_height = pd.Series([2.])
            result = stir_empty.CalcConcAir()
            npt.assert_array_almost_equal(result, 0.0001121, 4, '', True)
        finally:
            pass
        return

    # eq. 7 Avian spray droplet inhalation dose
    def test_CalcSidAvian(self):
        """
        unittest for function stir.CalcSidAvian
        """
        # self.sid_avian = (self.air_conc * self.inh_rate_avian * self.direct_spray_duration * self.spray_drift_fraction)/(60.0 * self.body_weight_assessed_bird)
        try:
            stir_empty.air_conc = pd.Series([150.])
            stir_empty.inh_rate_avian = pd.Series([10.])
            stir_empty.direct_spray_duration = pd.Series([0.5])
            stir_empty.spray_drift_fraction = pd.Series([0.75])
            stir_empty.body_weight_assessed_bird = pd.Series([0.02])
            result = stir_empty.CalcSidAvian()
            npt.assert_array_almost_equal(result, 468.75, 4, '', True)
        finally:
            pass
        return

    # eq. 8 Mammalian spray droplet inhalation dose
    def test_CalcSidMammal(self):
        """
        unittest for function stir.CalcSidMammal
        """
        # self.sid_mammal = (self.air_conc * self.inh_rate_mammal * self.direct_spray_duration * self.spray_drift_fraction)/(60.0 * self.body_weight_assessed_mammal)
        try:
            stir_empty.air_conc = pd.Series([150.])
            stir_empty.inh_rate_mammal = pd.Series([50.])
            stir_empty.direct_spray_duration = pd.Series([0.5])
            stir_empty.spray_drift_fraction = pd.Series([0.75])
            stir_empty.body_weight_assessed_mammal = pd.Series([0.08])
            result = stir_empty.CalcSidMammal()
            npt.assert_array_almost_equal(result, 585.9375, 4, '', True)
        finally:
            pass
        return

    # eq. 9 Conversion of mammalian LC50 to LD50
    def test_CalcConvertMammalInhalationLC50toLD50(self):
        """
        unittest for function stir.CalcConvertMammalInhalationLC50toLD50
        """
        # activity_factor = 1.
        # absorption = 1.
        # self.mammal_inhalation_ld50 = self.mammal_inhalation_lc50 * absorption * ((self.inh_rate_mammal * 0.001)/self.body_weight_tested_mammal) * self.duration_mammal_inhalation_study * activity_factor
        try:
            stir_empty.mammal_inhalation_lc50 = pd.Series([0.5])
            stir_empty.inh_rate_mammal = pd.Series([50.])
            stir_empty.body_weight_tested_mammal = pd.Series([0.35])
            stir_empty.duration_mammal_inhalation_study = pd.Series([2.])
            result = stir_empty.CalcConvertMammalInhalationLC50toLD50()
            npt.assert_array_almost_equal(result, 0.14286, 4, '', True)
        finally:
            pass
        return

    # eq. 10 Adjusted mammalian inhalation LD50
    def test_CalcAdjustedMammalInhalationLD50(self):
        """
        unittest for function stir.CalcAdjustedMammalInhalationLD50
        """
        # self.adjusted_mammal_inhalation_ld50 = self.mammal_inhalation_ld50 * (self.body_weight_tested_mammal/self.body_weight_assessed_mammal)**magicpower
        try:
            stir_empty.mammal_inhalation_ld50 = pd.Series([2.])
            stir_empty.body_weight_tested_mammal = pd.Series([0.35])
            stir_empty.body_weight_assessed_mammal = pd.Series([0.2])
            result = stir_empty.CalcAdjustedMammalInhalationLD50()
            npt.assert_array_almost_equal(result, 2.3003, 4, '', True)
        finally:
            pass
        return

    #eq. 11 Estimated avian inhalation LD50
    def CalcEstimatedAvianInhalationLD50(self):
        """
        unittest for function stir.CalcEstimatedAvianInhalationLD50
        """
        # three_five = 3.5
        # self.estimated_avian_inhalation_ld50 = (self.avian_oral_ld50 * self.mammal_inhalation_ld50)/(three_five * self.mammal_oral_ld50)
        try:
            stir_empty.avian_oral_ld50 = pd.Series([500.])
            stir_empty.mammal_inhalation_ld50 = pd.Series([2.])
            stir_empty.mammal_oral_ld50 = pd.Series([20.])
            result = stir_empty.CalcEstimatedAvianInhalationLD50()
            npt.assert_array_almost_equal(result, 14.2857, 4, '', True)
        finally:
            pass
        return

    #eq. 12 Adjusted avian inhalation LD50
    def CalcAdjustedAvianInhalationLD50(self):
        """
        unittest for function stir.CalcAdjustedAvianInhalationLD50
        """
        # self.adjusted_avian_inhalation_ld50 = self.estimated_avian_inhalation_ld50 * (self.body_weight_assessed_bird/self.body_weight_tested_bird)**(self.mineau_scaling_factor - 1)
        try:
            stir_empty.estimated_avian_inhalation_ld50 = pd.Series([0.5])
            stir_empty.body_weight_assessed_bird = pd.Series([0.02])
            stir_empty.body_weight_tested_bird = pd.Series([0.1])
            stir_empty.mineau_scaling_factor = pd.Series([2.])
            result = stir_empty.CalcAdjustedAvianInhalationLD50()
            npt.assert_array_almost_equal(result, 0.1, 4, '', True)
        finally:
            pass
        return

    # ----------------------------------------------
    # results
    # ----------------------------------------------

    # results #1: Ratio of avian vapor dose to adjusted inhalation LD50
    def ReturnRatioVidAvian(self):
        """
        unittest for function stir.ReturnRatioVidAvian
        """
        # self.ratio_vid_avian = self.vid_avian/self.adjusted_avian_inhalation_ld50
        try:
            stir_empty.vid_avian = pd.Series([0.04])
            stir_empty.adjusted_avian_inhalation_ld50 = pd.Series([5.])
            result = stir_empty.ReturnRatioVidAvian()
            npt.assert_array_almost_equal(result, 0.008, 4, '', True)
        finally:
            pass
        return

    # results #2: Level of Concern for avian vapor phase risk
    def ReturnLocVidAvian(self):
        """
        unittest for function stir.ReturnLocVidAvian
        """
        #if self.ratio_vid_avian < 0.1:
        #    self.loc_vid_avian = 'Exposure not Likely Significant'
        #else:
        #    self.loc_vid_avian = 'Proceed to Refinements'
        try:
            stir_empty.loc_vid_avian = pd.Series([0.2])
            result = stir_empty.ReturnLocVidAvian()
            exp = pd.Series("Proceed to Refinements")
            pdt.assert_series_equal(result,exp)
        finally:
            pass
        return

    # results #3: Ratio of avian droplet inhalation dose to adjusted inhalation LD50
    def ReturnRatioSidAvian(self):
        """
        unittest for function stir.ReturnRatioSidAvian
        """
        # self.ratio_sid_avian = self.sid_avian/self.adjusted_avian_inhalation_ld50
        try:
            stir_empty.sid_avian = pd.Series([4.])
            stir_empty.adjusted_avian_inhalation_ld50 = pd.Series([10.])
            result = stir_empty.ReturnRatioSidAvian()
            npt.assert_array_almost_equal(result, 0.4, 4, '', True)
        finally:
            pass
        return

    # results #4: Level of Concern for avian droplet inhalation risk
    def ReturnLocSidAvian(self):
        """
        unittest for function stir.ReturnLocSidAvian
        """
        #if self.ratio_sid_avian < 0.1:
        #    self.loc_sid_avian = 'Exposure not Likely Significant'
        #else:
        #    self.loc_sid_avian = 'Proceed to Refinements'
        try:
            stir_empty.ratio_sid_avian = pd.Series([0.2])
            result = stir_empty.ReturnLocSidAvian()
            exp = pd.Series("Proceed to Refinements")
            pdt.assert_series_equal(result, exp)
        finally:
            pass
        return

    # results #5: Ratio of mammalian vapor dose to adjusted inhalation LD50
    def ReturnRatioVidMammal(self):
        """
        unittest for function stir.ReturnRatioVidMammal
        """
        # self.ratio_vid_mammal = self.vid_mammal/self.adjusted_mammal_inhalation_ld50
        try:
            stir_empty.vid_mammal = pd.Series([4.])
            stir_empty.adjusted_mammal_inhalation_ld50 = pd.Series([2.])
            result = stir_empty.ReturnRatioVidMammal()
            npt.assert_array_almost_equal(result, 2, '', True)
        finally:
            pass
        return

    # results #6: Level of Concern for mammalian vapor phase risk
    def ReturnLocVidMammal(self):
        """
        unittest for function stir.ReturnLocVidMammal
        """
        #if self.ratio_vid_mammal < 0.1:
        #    self.loc_vid_mammal = 'Exposure not Likely Significant'
        #else:
        #    self.loc_vid_mammal = 'Proceed to Refinements'
        try:
            stir_empty.ratio_vid_mammal = pd.Series([0.3])
            result = stir_empty.ReturnLocVidMammal()
            exp = pd.Series("Proceed to Refinements")
            pdt.assert_series_equal(result, exp)
        finally:
            pass
        return

    # results #7: Ratio of mammalian droplet inhalation dose to adjusted inhalation LD50
    def ReturnRatioSidMammal(self):
        """
        unittest for function stir.ReturnRatioSidMammal
        """
        # self.ratio_sid_mammal = self.sid_mammal/self.adjusted_mammal_inhalation_ld50
        try:
            stir_empty.sid_mammal = pd.Series([0.5])
            stir_empty.adjusted_mammal_inhalation_ld50 = pd.Series([2.])
            result = stir_empty.ReturnRatioSidMammal()
            npt.assert_array_almost_equal(result, 0.25, 4, '', True)
        finally:
            pass
        return

    # results #8: Level of Concern for mammaliam droplet inhalation risk
    def ReturnLocSidMammal(self):
        """
        unittest for function stir.ReturnLocSidMammal
        """
        #if self.ratio_sid_mammal < 0.1:
        #    self.loc_sid_mammal = 'Exposure not Likely Significant'
        #else:
        #    self.loc_sid_mammal = 'Proceed to Refinements'
        try:
            stir_empty.ratio_sid_mammal = pd.Series([0.6])
            result = stir_empty.ReturnLocSidMammal()
            exp = pd.Series("Proceed to Refinements")
            pdt.assert_series_equal(result, exp)
        finally:
            pass
        return

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