import unittest
import sip_model_rest as sip_model
import pandas as pd
import numpy.testing as npt

csv_transpose_path_in = "./sip_qaqc_in_transpose.csv"
csv_transpose_path_exp = "./sip_qaqc_exp_transpose.csv"

# # needs to be run whenever the qaqc csv is updated
# csv_path = "./sip_qaqc.csv"
#
# pd_obj_inputs = pd.read_csv(csv_path, index_col=0, header=None, skiprows=1, skipfooter=32, engine='python')
# pd_obj_inputs = pd_obj_inputs.drop(labels=pd_obj_inputs.columns[range(4)], axis=1)
# pd_obj_inputs.index.name = None
# pd_obj_inputs.columns -= 5
# pd_obj_inputs_transposed = pd_obj_inputs.transpose()
# pd_obj_inputs_transposed.to_csv(csv_transpose_path_in)
#
# pd_obj_exp_out = pd.read_csv(csv_path, index_col=0, header=None, skiprows=33, engine='python')
# pd_obj_exp_out = pd_obj_exp_out.drop(labels=pd_obj_exp_out.columns[range(4)], axis=1)
# pd_obj_exp_out.index.name = None
# pd_obj_exp_out.columns -= 5
# pd_obj_exp_out_transposed = pd_obj_exp_out.transpose()
# pd_obj_exp_out_transposed.to_csv(csv_transpose_path_exp)

# load transposed qaqc data for inputs and expected outputs
pd_obj_inputs = pd.read_csv(csv_transpose_path_in, index_col=0, engine='python')
# print(pd_obj_inputs)
pd_obj_exp_out = pd.read_csv(csv_transpose_path_exp, index_col=0, engine='python')
# print(pd_obj_exp_out)

# create an instance of sip object with qaqc data
sip_calc = sip_model.sip(0, pd_obj_inputs, pd_obj_exp_out)
sip_empty = sip_model.sip(1, pd_obj_inputs, pd_obj_exp_out)

class TestSip(unittest.TestCase):
    def setup(self):
        # sip2 = sip_model.sip(0, pd_obj_inputs, pd_obj_exp_out)
        pass
        # setup the test as needed
        # e.g. pandas to open sip qaqc csv
        #  Read qaqc csv and create pandas DataFrames for inputs and expected outputs

    def teardown(self):
        pass
        # teardown called after each test
        # e.g. maybe write test results to some text file

    def test_fw_bird(self):
        result = sip_calc.fw_bird()
        self.assertEquals(result, 0.0162)
        return

    def test_fw_mamm(self):
        result = sip_calc.fw_mamm()
        self.assertEquals(result, 0.172)
        return

    def test_dose_bird(self):
        # self.fw_bird_out * self.solubility)/(self.bodyweight_assessed_bird / 1000.
        sip_empty.fw_bird_out = 10.
        sip_empty.solubility = 100.
        sip_empty.bodyweight_assessed_bird = 1.
        result = sip_empty.dose_bird()
        self.assertEquals(result, 1000000.)
        return

# #Amber
#     def test_dose_mamm(self):
#         # self.fw_mamm_out * self.solubility)/(self.bodyweight_assessed_mammal / 1000.
#
#         result =
#         self.assertEquals(result, )
#         return
#
# #Amber
#     def test_at_bird(self):
#         #self.ld50_avian_water) * ((self.bodyweight_assessed_bird / self.bodyweight_tested_bird)**(self.mineau_scaling_factor - 1.))
#         result =
#         self.assertEquals(result, )
#         return
#
# #Amber
#     def test_at_mamm(self):
#         #self.ld50_mammal_water) * ((self.bodyweight_tested_mammal / self.bodyweight_assessed_mammal)**0.25
#         result =
#         self.assertEquals(result, )
#         return
#
# #Amber
#     def test_fi_bird(self):
#         #0.0582 * ((bw_grams / 1000.)**0.651)
#         result =
#         self.assertEquals(result, )
#         return

# #Weird equation. Let's talk about this one.
#     def test_det(self):
#         """
#         Dose Equiv. Toxicity:
#
#         The FI value (kg-diet) is multiplied by the reported NOAEC (mg/kg-diet) and then divided by
#         the test animal's body weight to derive the dose-equivalent chronic toxicity value (mg/kg-bw):
#
#         Dose Equiv. Toxicity = (NOAEC * FI) / BW
#
#         NOTE: The user enters the lowest available NOAEC for the mallard duck, for the bobwhite quail,
#         and for any other test species. The model calculates the dose equivalent toxicity values for
#         all of the modeled values (Cells F20-24 and results worksheet) and then selects the lowest dose
#         equivalent toxicity value to represent the chronic toxicity of the chemical to birds.
#         """
#         result =
#         self.assertEquals(result, )
#         return

# #Amber
#     def act(self):
#         #(self.noael_mammal_water) * ((self.bodyweight_tested_mammal / self.bodyweight_assessed_mammal)**0.25)
#         result =
#         self.assertEquals(result, )
#         return
#

#Carmen
    def test_acute_bird(self):
        #self.dose_bird_out / self.at_bird_out
        sip_empty.dose_bird_out = 100
        sip_empty.at_bird_out = 10
        result = sip_empty.acute_bird_out()
        self.assertEquals(result, 10)
        return

#Carmen
    def test_acuconb(self):
        """
        Message stating whether or not a risk is present
        """
        # if self.acuconb_out == -1:
        #     if self.acute_bird_out == None:
        #         raise ValueError\
        #         ('acute_bird variable equals None and therefor this function cannot be run.')
            # if self.acute_bird_out < 0.1:
            #     self.acuconb_out = ('Drinking water exposure alone is NOT a potential concern for birds')
            # else:
            #     self.acuconb_out = ('Exposure through drinking water alone is a potential concern for birds')
        sip_empty.acute_bird_out = 0.2
        self.acuconb_out = sip_empty.acute_bird_out.map(lambda x:
                                                        'Drinking water exposure alone is NOT a potential concern for birds'
                                                        if x == True
                                                        else 'Exposure through drinking water alone is a potential concern for birds')
        result = self.acuconb_out()  # NOT SURE IF SIP_EMPTY IS CORRECT
        self.assertTrue(result, 'Exposure through drinking water alone is a potential concern for birds')
        return

#Carmen
    def test_acute_mamm(self):
        #self.acute_mamm_out = self.dose_mamm_out / self.at_mamm_out
        sip_empty.dose_mamm_out = 100
        sip_empty.at_mamm_out = 10
        result = sip_empty.acute_mamm_out()
        self.assertEquals(result, 10)
        return

#Carmen
    def test_acuconm(self):
        """
        Message stating whether or not a risk is present
        """
        # if self.acuconm_out == -1:
        #     if self.acute_mamm_out == None:
        #         raise ValueError\
        #         ('acute_mamm variable equals None and therefor this function cannot be run.')
        #     if self.acute_mamm_out < 0.1:
        #         self.acuconm_out = ('Drinking water exposure alone is NOT a potential concern for mammals')
        #     else:
        #         self.acuconm_out = ('Exposure through drinking water alone is a potential concern for mammals')
        #     return self.acuconm_out
        sip_empty.acute_mamm_out = 0.2
        self.acuconm_out = sip_empty.acute_mamm_out.map(lambda x:
                                                        'Drinking water exposure alone is NOT a potential concern for mammals'
                                                        if x == True
                                                        else 'Exposure through drinking water alone is a potential concern for mammals')
        result = self.acuconm_out()
        self.assertTrue(result, 'Exposure through drinking water alone is a potential concern for mammals')
        return

# #Marcia
#     def test_chron_bird(self):
#         result =
#         self.assertEquals(result, )
#         return
#
# #Marcia
#     def test_chronconb(self):
#         result =
#         self.assertEquals(result, )
#         return
#
# #Marcia
#     def test_chron_mamm(self):
#         result =
#         self.assertEquals(result, )
#         return
#
# #Marcia
#     def test_chronconm(self):
#         result =
#         self.assertEquals(result, )
#         return

    def test_blackbox_act(self):
        result = sip_calc.pd_obj_out["act_out"]
        expected = sip_calc.pd_obj_exp["act_exp"]
        npt.assert_array_equal(result, expected)
        #self.assertEquals(result, expected)
        # setup sip object
        # compare sip qaqc csv expected output to
        # sip object output with an assertEquals

# unittest will
# 1) call the setup method,
# 2) then call every method starting with "test",
# 3) then the teardown method
if __name__ == '__main__':
    unittest.main()
