import unittest
import sip_model_rest as sip_model
import pandas as pd
import numpy.testing as npt


# load transposed qaqc data for inputs and expected outputs
csv_transpose_path_in = "./sip_qaqc_in_transpose.csv"
pd_obj_inputs = pd.read_csv(csv_transpose_path_in, index_col=0, engine='python')
# print(pd_obj_inputs)
csv_transpose_path_exp = "./sip_qaqc_exp_transpose.csv"
pd_obj_exp_out = pd.read_csv(csv_transpose_path_exp, index_col=0, engine='python')
# print(pd_obj_exp_out)

# create an instance of sip object with qaqc data
sip_calc = sip_model.sip("batch", pd_obj_inputs, pd_obj_exp_out)
sip_empty = sip_model.sip("empty", pd_obj_inputs, pd_obj_exp_out)

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
        #(self.fw_bird_out * self.solubility)/(self.bodyweight_assessed_bird / 1000.)
        sip_empty.fw_bird_out = 10.
        sip_empty.solubility = 100.
        sip_empty.bodyweight_assessed_bird = 1.
        result = sip_empty.dose_bird()
        self.assertEquals(result, 1000000.)
        return

#Amber
    def test_dose_mamm(self):
        #(self.fw_mamm_out * self.solubility)/(self.bodyweight_assessed_mammal / 1000)
        sip_empty.fw_mamm_out = 20.
        sip_empty.solubility = 400.
        sip_empty.bodyweight_assessed_mammal = 1.
        result = sip_empty.dose_mamm()
        self.assertEquals(result, 8000000.)
        return

#Amber
    def test_at_bird(self):
        #(self.ld50_avian_water) * ((self.bodyweight_assessed_bird / self.bodyweight_tested_bird)**(self.mineau_scaling_factor - 1.))
        sip_empty.ld50_avian_water = 2000.
        sip_empty.bodyweight_assessed_bird = 100.
        sip_empty.bodyweight_tested_bird = 200.
        sip_empty.mineau_scaling_factor = 2.
        result = sip_empty.at_bird()
        self.assertEquals(result, 1000.)
        return

#Amber
    def test_at_mamm(self):
        #(self.ld50_mammal_water) * ((self.bodyweight_tested_mammal / self.bodyweight_assessed_mammal)**0.25)
        sip_empty.ld50_mammal_water = 10.
        sip_empty.bodyweight_tested_mammal = 100.
        sip_empty.bodyweight_assessed_mammal = 200.
        result = sip_empty.at_mamm()
        self.assertAlmostEquals(result, 8.408964, 4)
        return

###Error. Issue with fi_bird and bw_grams? In sip_model_rest.py, fi_bird only equation using an argument
### and fi_bird is not included in run_methods function. ?
#     def test_fi_bird(self):
#         #0.0582 * ((bw_grams / 1000.)**0.651)
#         sip_empty.bw_grams = 100.
#         result = sip_calc.fi_bird()
#         self.assertEquals(result, 0.012999)
#         return

#Amber.
    def test_act(self):
        #(self.noael_mammal_water) * ((self.bodyweight_tested_mammal / self.bodyweight_assessed_mammal)**0.25)
        sip_empty.noael_mammal_water = 10.
        sip_empty.bodyweight_tested_mammal = 500.
        sip_empty.bodyweight_assessed_mammal = 400.
        result = sip_empty.act()
        self.assertAlmostEquals(result, 10.5737, 4)
        return

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

#Carmen
    def test_acute_bird(self):
        #self.dose_bird_out / self.at_bird_out
        sip_empty.dose_bird_out = 100
        sip_empty.at_bird_out = 10
        result = sip_empty.acute_bird()
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
        result = sip_empty.acuconb()  # NOT SURE IF SIP_EMPTY IS CORRECT
        self.assertEqual(result, "Exposure through drinking water alone is a potential concern for birds")
        return

#Carmen
    def test_acute_mamm(self):
        #self.acute_mamm_out = self.dose_mamm_out / self.at_mamm_out
        sip_empty.dose_mamm_out = 100
        sip_empty.at_mamm_out = 10
        result = sip_empty.acute_mamm()
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
        result = sip_empty.acuconm()
        self.assertEqual(result, "Exposure through drinking water alone is a potential concern for mammals")
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
        #self.assertEquals(result, expected)
        # setup sip object
        # compare sip qaqc csv expected output to
        # sip object output with an assertEquals
        npt.assert_array_almost_equal(result, expected, 4, '', True)

# unittest will
# 1) call the setup method,
# 2) then call every method starting with "test",
# 3) then the teardown method
if __name__ == '__main__':
    unittest.main()
