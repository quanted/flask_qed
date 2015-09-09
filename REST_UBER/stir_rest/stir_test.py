import unittest
import stir_model_rest as stir_model
import pandas as pd
import numpy.testing as npt
import pandas.util.testing as pdt

# load transposed qaqc data for inputs and expected outputs
csv_transpose_path_in = "./stir_qaqc_in_transpose.csv"
pd_obj_inputs = pd.read_csv(csv_transpose_path_in, index_col=0, engine='python')
# print(pd_obj_inputs)
csv_transpose_path_exp = "./stir_qaqc_exp_transpose.csv"
pd_obj_exp_out = pd.read_csv(csv_transpose_path_exp, index_col=0, engine='python')

# create an instance of sip object with qaqc data
stir_calc = stir_model.stir("batch", pd_obj_inputs, pd_obj_exp_out)
stir_empty = stir_model.stir("empty", pd_obj_inputs, pd_obj_exp_out)
test = {}

class TestStir(unittest.TestCase):
    def setup(self):
        pass
        # setup the test as needed
        # e.g. pandas to open sip qaqc csv
        #  Read qaqc csv and create pandas DataFrames for inputs and expected outputs

    def teardown(self):
        pass
        # teardown called after each test
        # e.g. maybe write test results to some text file

    # # each of these functions are queued by "run_methods" and have outputs defined as properties in the stir qaqc
    #
    # #eq. 1 saturated air concentration in mg/m^3
    # def CalcSatAirConc(self):
    #     #if self.sat_air_conc == -1:
    #     #    self.vapor_pressure = float(self.vapor_pressure)
    #     #    self.molecular_weight = float(self.molecular_weight)
    #     air_vol = 24.45
    #     pressure = 760.0
    #     conv = 1000000.0
    #     self.sat_air_conc = (self.vapor_pressure * self.molecular_weight * conv)/(pressure * air_vol)
    #     logging.info(self.sat_air_conc)
    #     return self.sat_air_conc
    #
    # #eq. 2 Avian inhalation rate
    # def CalcInhRateAvian(self):
    #     #if self.inh_rate_avian == -1:
    #     #    self.body_weight_assessed_bird = float(self.body_weight_assessed_bird)
    #     magic1 = 284.
    #     magic2 = 0.77
    #     conversion = 60.
    #     activity_factor = 3.
    #     self.inh_rate_avian = magic1 * (self.body_weight_assessed_bird**magic2) * conversion * activity_factor
    #     logging.info(self.inh_rate_avian)
    #     return self.inh_rate_avian
    #
    # #eq. 3  Maximum avian vapor inhalation dose
    # def CalcVidAvian(self):
    #     #if self.vid_avian == -1:
    #     #    self.sat_air_conc = float(self.sat_air_conc)
    #     #    self.inh_rate_avian = float(self.inh_rate_avian)
    #     #    self.body_weight_assessed_bird = float(self.body_weight_assessed_bird)
    #     duration_hours = 1.
    #     conversion_factor = 1000000. # cm3/m3
    #     # 1 (hr) is duration of exposure
    #     self.vid_avian = (self.sat_air_conc * self.inh_rate_avian * duration_hours)/(conversion_factor * self.body_weight_assessed_bird)
    #     logging.info(self.vid_avian)
    #     return self.vid_avian
    #
    # #eq. 4 Mammalian inhalation rate
    # def CalcInhRateMammal(self):
    #     #if self.inh_rate_mammal == -1:
    #     #    self.body_weight_assessed_mammal = float(self.body_weight_assessed_mammal)
    #     magic1 = 379.0
    #     magic2 = 0.8
    #     minutes_conversion = 60.
    #     activity_factor = 3.
    #     self.inh_rate_mammal = magic1 * (self.body_weight_assessed_mammal**magic2) * minutes_conversion * activity_factor
    #     logging.info(self.inh_rate_mammal)
    #     return self.inh_rate_mammal
    #
    # #eq. 5 Maximum mammalian vapor inhalation dose
    # def CalcVidMammal(self):
    #     #if self.vid_mammal == -1:
    #     #    self.sat_air_conc = float(self.sat_air_conc) # eq. 1
    #     #    self.inh_rate_mammal = float(self.inh_rate_mammal) # eq. 4
    #     #    self.body_weight_assessed_mammal = float(self.body_weight_assessed_mammal)
    #     duration_hours = 1.
    #     conversion_factor = 1000000.
    #     # 1 hr = duration of exposure
    #     self.vid_mammal = (self.sat_air_conc * self.inh_rate_mammal * duration_hours)/(conversion_factor * self.body_weight_assessed_mammal)
    #     logging.info(self.vid_mammal)
    #     return self.vid_mammal
    #
    # #eq. 6 Air column concentration after spray
    # def CalcConcAir(self):
    #     #if self.air_conc == -1:
    #     #    self.application_rate = float(self.application_rate)
    #     #    self.column_height = float(self.column_height)
    #     conversion_factor = 100. #cm/m
    #     # conversion of application rate from lbs/acre to mg/cm2
    #     cf_g_lbs = 453.59237
    #     cf_mg_g = 1000.
    #     cf_cm2_acre = 40468564.2
    #     self.ar2 = (self.application_rate*cf_g_lbs*cf_mg_g)/cf_cm2_acre
    #     logging.info(self.ar2)
    #     self.air_conc = self.ar2/(self.column_height * conversion_factor)
    #     logging.info(self.air_conc)
    #     return self.air_conc
    #
    # #eq. 7 Avian spray droplet inhalation dose
    # def CalcSidAvian(self):
    #     #if self.sid_avian == -1:
    #     #    self.air_conc = float(self.air_conc)
    #     #    self.inh_rate_avian = float(self.inh_rate_avian)
    #     #    self.direct_spray_duration = float(self.direct_spray_duration)
    #     #    self.spray_drift_fraction = float(self.spray_drift_fraction)
    #     #    self.body_weight_assessed_bird = float(self.body_weight_assessed_bird)
    #     self.sid_avian = (self.air_conc * self.inh_rate_avian * self.direct_spray_duration * self.spray_drift_fraction)/(60.0 * self.body_weight_assessed_bird)
    #     #logging.info("self.air_conc = " + self.air_conc)
    #     #logging.info("self.inh_rate_avian = " + self.inh_rate_avian)
    #     #logging.info("self.direct_spray_duration = " + self.direct_spray_duration)
    #     #logging.info("self.spray_drift_fraction = " + self.spray_drift_fraction)
    #     #logging.info("self.body_weight_assessed_bird = " + self.body_weight_assessed_bird)
    #     #logging.info("self.sid_avian = " + self.sid_avian)
    #     return self.sid_avian
    #
    # #eq. 8 Mammalian spray droplet inhalation dose
    # def CalcSidMammal(self):
    #     #if self.sid_mammal == -1:
    #     #    self.air_conc = float(self.air_conc)
    #     #    self.inh_rate_mammal = float(self.inh_rate_mammal)
    #     #    self.direct_spray_duration = float(self.direct_spray_duration)
    #     #    self.spray_drift_fraction = float(self.spray_drift_fraction)
    #     #    self.body_weight_assessed_mammal = float(self.body_weight_assessed_mammal)
    #     self.sid_mammal = (self.air_conc * self.inh_rate_mammal * self.direct_spray_duration * self.spray_drift_fraction)/(60.0 * self.body_weight_assessed_mammal)
    #     logging.info(self.sid_mammal)
    #     return self.sid_mammal
    #
    # #eq. 9 Conversion of mammalian LC50 to LD50
    # def CalcConvertMammalInhalationLC50toLD50(self):
    #     #if self.mammal_inhalation_ld50 == -1:
    #     #    self.mammal_inhalation_lc50 = float(self.mammal_inhalation_lc50)
    #     #    #conversion factor
    #     #    self.inh_rate_mammal = float(self.inh_rate_mammal)
    #     #    self.body_weight_tested_mammal = float(self.body_weight_tested_mammal)
    #     #    self.duration_mammal_inhalation_study = float(self.duration_mammal_inhalation_study)
    #     self.cf = ((self.inh_rate_mammal * 0.001)/self.body_weight_tested_mammal)
    #     logging.info(self.cf)
    #     activity_factor = 1.
    #     absorption = 1.
    #     self.mammal_inhalation_ld50 = self.mammal_inhalation_lc50 * absorption * self.cf * self.duration_mammal_inhalation_study * activity_factor
    #     logging.info(self.mammal_inhalation_ld50)
    #     return self.mammal_inhalation_ld50
    #
    # #eq. 10 Adjusted mammalian inhalation LD50
    # def CalcAdjustedMammalInhalationLD50(self):
    #     #if self.adjusted_mammal_inhalation_ld50 == -1:
    #     #    self.mammal_inhalation_ld50 = float(self.mammal_inhalation_ld50)
    #     #    self.body_weight_assessed_mammal = float(self.body_weight_assessed_mammal)
    #     #    self.body_weight_tested_mammal = float(self.body_weight_tested_mammal)
    #     magicpower = 0.25
    #     self.adjusted_mammal_inhalation_ld50 = self.mammal_inhalation_ld50 * (self.body_weight_tested_mammal/self.body_weight_assessed_mammal)**magicpower
    #     logging.info(self.adjusted_mammal_inhalation_ld50)
    #     return self.adjusted_mammal_inhalation_ld50
    #
    # #eq. 11 Estimated avian inhalation LD50
    # def CalcEstimatedAvianInhalationLD50(self):
    #     #if self.estimated_avian_inhalation_ld50 == -1:
    #     #    self.avian_oral_ld50 = float(self.avian_oral_ld50)
    #     #    self.mammal_inhalation_ld50 = float(self.mammal_inhalation_ld50)
    #     #    self.mammal_oral_ld50 = float(self.mammal_oral_ld50)
    #     three_five = 3.5
    #     self.estimated_avian_inhalation_ld50 = (self.avian_oral_ld50 * self.mammal_inhalation_ld50)/(three_five * self.mammal_oral_ld50)
    #     logging.info(self.estimated_avian_inhalation_ld50)
    #     return self.estimated_avian_inhalation_ld50
    #
    # #eq. 12 Adjusted avian inhalation LD50
    # def CalcAdjustedAvianInhalationLD50(self):
    #     #if self.adjusted_avian_inhalation_ld50 == -1:
    #     #    self.estimated_avian_inhalation_ld50 = float(self.estimated_avian_inhalation_ld50)
    #     #    self.body_weight_assessed_bird = float(self.body_weight_assessed_bird)
    #     #    self.body_weight_tested_bird = float(self.body_weight_tested_bird)
    #     #    self.mineau_scaling_factor = float(self.mineau_scaling_factor)
    #     self.adjusted_avian_inhalation_ld50 = self.estimated_avian_inhalation_ld50 * (self.body_weight_assessed_bird/self.body_weight_tested_bird)**(self.mineau_scaling_factor - 1)
    #     logging.info(self.adjusted_avian_inhalation_ld50)
    #     return self.adjusted_avian_inhalation_ld50
    #
    # # ----------------------------------------------
    # # results
    # # ----------------------------------------------
    # # results #1: Ratio of avian vapor dose to adjusted inhalation LD50
    # def ReturnRatioVidAvian(self):
    #     #if self.ratio_vid_avian == -1:
    #     #    self.vid_avian = float(self.vid_avian)
    #     #    self.adjusted_avian_inhalation_ld50 = float(self.adjusted_avian_inhalation_ld50)
    #     self.ratio_vid_avian = self.vid_avian/self.adjusted_avian_inhalation_ld50
    #     logging.info(self.ratio_vid_avian)
    #     return self.ratio_vid_avian
    #
    # # results #2: Level of Concern for avian vapor phase risk
    # def ReturnLocVidAvian(self):
    #     #if self.ratio_vid_avian < 0.1:
    #     #    self.loc_vid_avian = 'Exposure not Likely Significant'
    #     #else:
    #     #    self.loc_vid_avian = 'Proceed to Refinements'
    #     exceed_boolean = self.ratio_vid_avian < 0.1
    #     self.loc_vid_avian = exceed_boolean.map(lambda x:
    #                                             'Exposure not Likely Significant' if x == True
    #                                             else 'Proceed to Refinements')
    #     logging.info(self.loc_vid_avian)
    #     return self.loc_vid_avian
    #
    # # results #3: Ratio of avian droplet inhalation dose to adjusted inhalation LD50
    # def ReturnRatioSidAvian(self):
    #     #if self.ratio_sid_avian == -1:
    #     #    self.sid_avian = float(self.sid_avian)
    #     #    self.adjusted_avian_inhalation_ld50 = float(self.adjusted_avian_inhalation_ld50)
    #     self.ratio_sid_avian = self.sid_avian/self.adjusted_avian_inhalation_ld50
    #     logging.info(self.ratio_sid_avian)
    #     return self.ratio_sid_avian
    #
    # # results #4: Level of Concern for avian droplet inhalation risk
    # def ReturnLocSidAvian(self):
    #     #if self.ratio_sid_avian < 0.1:
    #     #    self.loc_sid_avian = 'Exposure not Likely Significant'
    #     #else:
    #     #    self.loc_sid_avian = 'Proceed to Refinements'
    #     exceed_boolean = self.ratio_sid_avian < 0.1
    #     self.loc_sid_avian = exceed_boolean.map(lambda x:
    #                                             'Exposure not Likely Significant' if x == True
    #                                             else 'Proceed to Refinements')
    #     logging.info(self.loc_sid_avian)
    #     return self.loc_sid_avian
    #
    # # results #5: Ratio of mammalian vapor dose to adjusted inhalation LD50
    # def ReturnRatioVidMammal(self):
    #     #if self.ratio_vid_mammal == -1:
    #     #    self.vid_mammal = float(self.vid_mammal)
    #     #    self.adjusted_mammal_inhalation_ld50 = float(self.adjusted_mammal_inhalation_ld50)
    #     self.ratio_vid_mammal = self.vid_mammal/self.adjusted_mammal_inhalation_ld50
    #     logging.info(self.ratio_vid_mammal)
    #     return self.ratio_vid_mammal
    #
    # # results #6: Level of Concern for mammalian vapor phase risk
    # def ReturnLocVidMammal(self):
    #     #if self.ratio_vid_mammal < 0.1:
    #     #    self.loc_vid_mammal = 'Exposure not Likely Significant'
    #     #else:
    #     #    self.loc_vid_mammal = 'Proceed to Refinements'
    #     exceed_boolean = self.ratio_vid_mammal < 0.1
    #     self.loc_vid_mammal = exceed_boolean.map(lambda x:
    #                                              'Exposure not Likely Significant' if x == True
    #                                              else 'Proceed to Refinements')
    #     logging.info(self.loc_vid_mammal)
    #     return self.loc_vid_mammal
    #
    # # results #7: Ratio of mammalian droplet inhalation dose to adjusted inhalation LD50
    # def ReturnRatioSidMammal(self):
    #     #if self.ratio_sid_mammal == -1:
    #     #    self.sid_mammal = float(self.sid_mammal)
    #     #    self.adjusted_mammal_inhalation_ld50 = float(self.adjusted_mammal_inhalation_ld50)
    #     self.ratio_sid_mammal = self.sid_mammal/self.adjusted_mammal_inhalation_ld50
    #     logging.info(self.ratio_sid_mammal)
    #     return self.ratio_sid_mammal
    #
    # # results #8: Level of Concern for mammaliam droplet inhalation risk
    # def ReturnLocSidMammal(self):
    #     #if self.ratio_sid_mammal < 0.1:
    #     #    self.loc_sid_mammal = 'Exposure not Likely Significant'
    #     #else:
    #     #    self.loc_sid_mammal = 'Proceed to Refinements'
    #     exceed_boolean = self.ratio_sid_mammal < 0.1
    #     self.loc_sid_mammal = exceed_boolean.map(lambda x:
    #                                              'Exposure not Likely Significant' if x == True
    #                                              else 'Proceed to Refinements')
    #     logging.info(self.loc_sid_mammal)
    #     return self.loc_sid_mammal

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
        result = stir_calc.pd_obj_out[output + "_out"]
        expected = stir_calc.pd_obj_exp[output + "_exp"]
        npt.assert_array_almost_equal(result, expected, 4, '', True)

    def blackbox_method_str(self, output):
        result = stir_calc.pd_obj_out[output + "_out"]
        expected = stir_calc.pd_obj_exp[output + "_exp"]
        npt.assert_array_equal(result, expected)
