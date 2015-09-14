import unittest
import terrplant_model_rest as terrplant_model
import pandas as pd
import numpy.testing as npt
import pandas.util.testing as pdt


# load transposed qaqc data for inputs and expected outputs
csv_transpose_path_in = "./terrplant_qaqc_in_transpose.csv"
pd_obj_inputs = pd.read_csv(csv_transpose_path_in, index_col=0, engine='python')
# print(pd_obj_inputs)
csv_transpose_path_exp = "./terrplant_qaqc_exp_transpose.csv"
pd_obj_exp_out = pd.read_csv(csv_transpose_path_exp, index_col=0, engine='python')
# print(pd_obj_exp_out)

# create an instance of sip object with qaqc data
terrplant_calc = terrplant_model.terrplant("batch", pd_obj_inputs, pd_obj_exp_out)
terrplant_empty = terrplant_model.terrplant("empty", pd_obj_inputs, pd_obj_exp_out)
test = {}


class TestTerrplant(unittest.TestCase):
    def setup(self):
        pass
        # setup the test as needed
        # e.g. pandas to open sip qaqc csv
        #  Read qaqc csv and create pandas DataFrames for inputs and expected outputs

    def teardown(self):
        pass
        # teardown called after each test
        # e.g. maybe write test results to some text file

#each of these functions are queued by "run_methods" and have outputs defined as properties in the terrplant qaqc csv
    # def rundry(self):
    #     #(self.application_rate/self.incorporation_depth) * self.runoff_fraction
    #     sip_empty.application_rate = pd.Series([10.], dtype='int')
    #     sip_empty.incorporation_depth = pd.Series([2.], dtype='int')
    #     sip_empty.runoff_fraction = pd.Series([.1], dtype='int')
    #     result = sip_empty.rundry()
    #     npt.assert_array_almost_equal(result, 0.5, 4, '', True)
    #     return
    #
    # def runsemi(self):
    #     #self.out_runsemi = (self.application_rate/self.incorporation_depth) * self.runoff_fraction * 10
    #     sip_empty.out_runsemi = pd.Series([##.], dtype='int')
    #     return
    #
    # def spray(self):
    #     #self.out_spray = self.application_rate * self.drift_fraction
    #     sip_empty.out_spray = pd.Series([##.], dtype='int')
    #     return
    #
    # def totaldry(self):
    #     #self.out_totaldry = self.out_rundry + self.out_spray
    #     sip_empty.out_totaldry = pd.Series([##.], dtype='int')
    #     return
    #
    # def totalsemi(self):
    #     #self.out_totalsemi = self.out_runsemi + self.out_spray
    #     sip_empty.out_totalsemi = pd.Series([##.], dtype='int')
    #     return
    #
    # def nms_rq_dry(self):
    #     #self.out_nms_rq_dry = self.out_totaldry/self.ec25_nonlisted_seedling_emergence_monocot
    #     sip_empty.out_nms_rq_dry = pd.Series([##.], dtype='int')
    #     return
    #
    # def nms_rq_semi(self):
    #     #self.out_nms_rq_semi = self.out_totalsemi/self.ec25_nonlisted_seedling_emergence_monocot
    #     sip_empty.out_nms_rq_semi = pd.Series([##.], dtype='int')
    #     return
    #
    # def nms_rq_spray(self):
    #     #self.out_nms_rq_spray = self.out_spray/self.ec25_nonlisted_seedling_emergence_monocot
    #     sip_empty.out_nms_rq_spray = pd.Series([##.], dtype='int')
    #     return
    #
    # def lms_rq_dry(self):
    #     #self.out_lms_rq_dry = self.out_totaldry/self.ec25_nonlisted_seedling_emergence_dicot
    #     sip_empty.out_lms_rq_dry = pd.Series([##.], dtype='int')
    #     return
    #
    # def lms_rq_semi(self):
    #     #self.out_lms_rq_semi = self.out_totalsemi/self.ec25_nonlisted_seedling_emergence_dicot
    #     sip_empty.out_lms_rq_semi = pd.Series([##.], dtype='int')
    #     return
    #
    # def lms_rq_spray(self):
    #     #self.out_lms_rq_spray = self.out_spray/self.ec25_nonlisted_seedling_emergence_dicot
    #     sip_empty.out_lms_rq_spray = pd.Series([##.], dtype='int')
    #     return
    #
    # def nds_rq_dry(self):
    #     #self.out_nds_rq_dry = self.out_totaldry/self.noaec_listed_seedling_emergence_monocot
    #     sip_empty.out_nds_rq_dry = pd.Series([##.], dtype='int')
    #     return
    #
    # def nds_rq_semi(self):
    #     #self.out_nds_rq_semi = self.out_totalsemi/self.noaec_listed_seedling_emergence_monocot
    #     sip_empty.out_nds_rq_semi = pd.Series([##.], dtype='int')
    #     return
    #
    # def nds_rq_spray(self):
    #     #self.out_nds_rq_spray = self.out_spray/self.noaec_listed_seedling_emergence_monocot
    #     sip_empty.out_nds_rq_spray = pd.Series([##.], dtype='int')
    #     return
    #
    # def lds_rq_dry(self):
    #     #self.out_lds_rq_dry = self.out_totaldry/self.noaec_listed_seedling_emergence_dicot
    #     sip_empty.out_lds_rq_dry = pd.Series([##.], dtype='int')
    #     return
    #
    # def lds_rq_semi(self):
    #     #self.out_lds_rq_semi = self.out_totalsemi/self.noaec_listed_seedling_emergence_dicot
    #     sip_empty.out_lds_rq_semi = pd.Series([##.], dtype='int')
    #     return
    #
    # def lds_rq_spray(self):
    #     #self.out_lds_rq_spray = self.out_spray/self.noaec_listed_seedling_emergence_dicot
    #     sip_empty.out_lds_rq_spray = pd.Series([##.], dtype='int')
    #     return


#the below functions are called in the run methods.
    def test_blackbox_method(self):
        self.blackbox_method_int('rundry')
        self.blackbox_method_str('runsemi')
        self.blackbox_method_str('spray')
        self.blackbox_method_str('totaldry')
        self.blackbox_method_str('totalsemi')
        self.blackbox_method_str('nms_rq_dry')
        self.blackbox_method_str('nms_rq_semi')
        self.blackbox_method_str('nms_rq_spray')
        self.blackbox_method_str('lms_rq_dry')
        self.blackbox_method_str('lms_rq_semi')
        self.blackbox_method_str('lms_rq_spray')
        self.blackbox_method_str('nds_rq_dry')
        self.blackbox_method_str('nds_rq_semi')
        self.blackbox_method_str('nds_rq_spray')
        self.blackbox_method_str('lds_rq_dry')
        self.blackbox_method_str('lds_rq_semi')
        self.blackbox_method_str('lds_rq_spray')

    def blackbox_method_int(self, output):
        """
        Helper method to reuse code for testing numpy array outputs from TerrPlant model
        :param output: String; Pandas Series name (e.g. column name) without '_out'
        :return:
        """
        result = terrplant_calc.pd_obj_out[output + "_out"]
        expected = terrplant_calc.pd_obj_exp[output + "_exp"]
        npt.assert_array_almost_equal(result, expected, 4, '', True)

    def blackbox_method_str(self, output):
        result = terrplant_calc.pd_obj_out[output + "_out"]
        expected = terrplant_calc.pd_obj_exp[output + "_exp"]
        npt.assert_array_equal(result, expected)

# unittest will
# 1) call the setup method,
# 2) then call every method starting with "test",
# 3) then the teardown method
if __name__ == '__main__':
    unittest.main()