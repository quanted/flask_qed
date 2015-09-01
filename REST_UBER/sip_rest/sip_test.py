import unittest
import sip_model_rest
import pandas as pd


class TestSip(unittest.TestCase):
    def setup(self):
        # setup the test as needed
        # e.g. pandas to open sip qaqc csv
        #  Read qaqc csv and create pandas DataFrames for inputs and expected outputs
        csv_path = "./sip_qaqc.csv"
        pd_obj_inputs = pd.read_csv(csv_path, index_col=0, header=None, skiprows=1, skipfooter=32, engine='python')
        pd_obj_inputs = pd_obj_inputs.drop(labels=pd_obj_inputs.columns[range(4)], axis=1)
        pd_obj_inputs.index.name = None
        pd_obj_inputs.columns -= 5

        pd_obj_exp_out = pd.read_csv(csv_path, index_col=0, header=None, skiprows=33, engine='python')
        pd_obj_exp_out = pd_obj_exp_out.drop(labels=pd_obj_exp_out.columns[range(4)], axis=1)
        pd_obj_exp_out.index.name = None
        pd_obj_exp_out.columns -= 5

        # instance sip object
        sip_obj = sip_model_rest.sip(0, pd_obj_inputs, pd_obj_exp_out)
        return

    def teardown(self):
        pass
        # teardown called after each test
        # e.g. maybe write test results to some text file

    def test_fail(self):
        result = [1, 2, 3]
        self.assertEquals(result, [2, 3, 4])

    def test_pass(self):
        result = [2, 3, 4]
        self.assertEquals(result, [2, 3, 4])

    def test_sip_blackbox(self):
        pass
        # setup sip object
        # compare sip qaqc csv expected output to
        # sip object output with an assertEquals

# unittest will
# 1) call the setup method,
# 2) then call every method starting with "test",
# 3) then the teardown method
if __name__ == '__main__':
    unittest.main()
