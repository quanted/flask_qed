import unittest
import terrplant_model_rest as terrplant_model
import pandas as pd
import numpy.testing as npt


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

# each of these functions are queued by "run_methods" and have outputs defined as properties in the terrplant qaqc csv
    def test_rundry(self):
        #(self.application_rate/self.incorporation_depth) * self.runoff_fraction
        terrplant_empty.application_rate = pd.Series([10.], dtype='int')
        terrplant_empty.incorporation_depth = pd.Series([2.], dtype='int')
        terrplant_empty.runoff_fraction = pd.Series([.1], dtype='float')
        result = terrplant_empty.rundry()
        npt.assert_array_almost_equal(result, 0.5, '', True)
        return

    def test_runsemi(self):
        #self.out_runsemi = (self.application_rate/self.incorporation_depth) * self.runoff_fraction * 10
        terrplant_empty.application_rate = pd.Series([10.], dtype='int')
        terrplant_empty.incorporation_depth = pd.Series([2.], dtype='int')
        terrplant_empty.runoff_fraction = pd.Series([.1], dtype='float')
        result = terrplant_empty.runsemi()
        npt.assert_array_almost_equal(result,5, '', True)
        return

    def test_spray(self):
        #self.out_spray = self.application_rate * self.drift_fraction
        terrplant_empty.application_rate = pd.Series([10.], dtype='int')
        terrplant_empty.drift_fraction = pd.Series([0.5], dtype='float')
        result = terrplant_empty.spray()
        npt.assert_array_almost_equal(result, 5, '', True)
        return

    def test_totaldry(self):
        #self.out_totaldry = self.out_rundry + self.out_spray
        terrplant_empty.rundry = pd.Series([0.5], dtype='float')
        terrplant_empty.spray = pd.Series([5.], dtype='int')
        result = terrplant_empty.totaldry()
        npt.assert_array_almost_equal(result, 5.5, '', True)
        return

    def test_totalsemi(self):
        #self.out_totalsemi = self.out_runsemi + self.out_spray
        terrplant_empty.out_runsemi = pd.Series([5.], dtype='int')
        terrplant_empty.out_spray = pd.Series([5.], dtype='int')
        result = terrplant_empty.totalsemi()
        npt.assert_array_almost_equal(result, 10, '', True)
        return

    def test_nms_rq_dry(self):
        #self.out_nms_rq_dry = self.out_totaldry/self.ec25_nonlisted_seedling_emergence_monocot
        terrplant_empty.out_totaldry = pd.Series([5.5], dtype='float')
        terrplant_empty.ec25_nonlisted_seedling_emergence_monocot = pd.Series([0.05], dtype='float')
        result = terrplant_empty.out_nms_rq_dry()
        npt.assert_array_almost_equal(result, 110, '', True)
        return

    def test_nms_rq_semi(self):
        #self.out_nms_rq_semi = self.out_totalsemi/self.ec25_nonlisted_seedling_emergence_monocot
        terrplant_empty.out_totalsemi = pd.Series([10.], dtype='int')
        terrplant_empty.ec25_nonlisted_seedling_emergence_monocot = pd.Series([0.05], dtype='float')
        result = terrplant_empty.out_nms_rq_semi()
        npt.assert_array_almost_equal(result, 200, '', True)
        return

    def test_nms_rq_spray(self):
        #self.out_nms_rq_spray = self.out_spray/self.ec25_nonlisted_seedling_emergence_monocot
        terrplant_empty.out_spray = pd.Series([5.], dtype='int')
        terrplant_empty.ec25_nonlisted_seedling_emergence_monocot = pd.Series([0.05], dtype='float')
        result = terrplant_empty.out_nms_rq_spray()
        npt.assert_array_almost_equal(result, 100, '', True)
        return

    def test_lms_rq_dry(self):
        #self.out_lms_rq_dry = self.out_totaldry/self.ec25_nonlisted_seedling_emergence_dicot
        terrplant_empty.out_totaldry = pd.Series([5.5], dtype='float')
        terrplant_empty.ec25_nonlisted_seedling_emergence_dicot = pd.Series([0.01], dtype='float')
        result = terrplant_empty.out_lms_rq_dry()
        npt.assert_array_almost_equal(result, 550, '', True)
        return

    def test_lms_rq_semi(self):
        #self.out_lms_rq_semi = self.out_totalsemi/self.ec25_nonlisted_seedling_emergence_dicot
        terrplant_empty.out_totalsemi = pd.Series([10.], dtype='int')
        terrplant_empty.ec25_nonlisted_seedling_emergence_dicot = pd.Series([0.01], dtype='float')
        result = terrplant_empty.out_lms_rq_semi()
        npt.assert_array_almost_equal(result, 1000, '', True)
        return

    def test_lms_rq_spray(self):
        #self.out_lms_rq_spray = self.out_spray/self.ec25_nonlisted_seedling_emergence_dicot
        terrplant_empty.out_spray = pd.Series([5.], dtype='int')
        terrplant_empty.ec25_nonlisted_seedling_emergence_dicot = pd.Series([0.01], dtype='float')
        result = terrplant_empty.out_lms_rq_spray()
        npt.assert_array_almost_equal(result, 500, '', True)
        return

    def test_nds_rq_dry(self):
        #self.out_nds_rq_dry = self.out_totaldry/self.noaec_listed_seedling_emergence_monocot
        terrplant_empty.out_totaldry = pd.Series([5.5], dtype='float')
        terrplant_empty.noaec_listed_seedling_emergence_monocot = pd.Series([0.02], dtype='float')
        result = terrplant_empty.out_nds_rq_dry()
        npt.assert_array_almost_equal(result, 275, '', True)
        return

    def test_nds_rq_semi(self):
        #self.out_nds_rq_semi = self.out_totalsemi/self.noaec_listed_seedling_emergence_monocot
        terrplant_empty.out_totalsemi = pd.Series([10.], dtype='int')
        terrplant_empty.noaec_listed_seedling_emergence_monocot = pd.Series([0.02], dtype='float')
        result = terrplant_empty.out_nds_rq_semi()
        npt.assert_array_almost_equal(result, 500, '', True)
        return

    def test_nds_rq_spray(self):
        #self.out_nds_rq_spray = self.out_spray/self.noaec_listed_seedling_emergence_monocot
        terrplant_empty.out_spray = pd.Series([5.], dtype='int')
        terrplant_empty.noaec_listed_seedling_emergence_monocot = pd.Series([0.02], dtype='float')
        result = terrplant_empty.out_nds_rq_spray()
        npt.assert_array_almost_equal(result, 250, '', True)
        return

    def test_lds_rq_dry(self):
        #self.out_lds_rq_dry = self.out_totaldry/self.noaec_listed_seedling_emergence_dicot
        terrplant_empty.out_totaldry = pd.Series([5.5], dtype='float')
        terrplant_empty.noaec_listed_seedling_emergence_dicot = pd.Series([0.1], dtype='float')
        result = terrplant_empty.out_lds_rq_dry()
        npt.assert_array_almost_equal(result, 55, '', True)
        return

    def test_lds_rq_semi(self):
        #self.out_lds_rq_semi = self.out_totalsemi/self.noaec_listed_seedling_emergence_dicot
        terrplant_empty.out_totalsemi = pd.Series([10.], dtype='int')
        terrplant_empty.noaec_listed_seedling_emergence_dicot = pd.Series([0.1], dtype='float')
        result = terrplant_empty.out_lds_rq_semi()
        npt.assert_array_almost_equal(result, 100, '', True)
        return

    def test_lds_rq_spray(self):
        #self.out_lds_rq_spray = self.out_spray/self.noaec_listed_seedling_emergence_dicot
        terrplant_empty.out_spray = pd.Series([5.], dtype='int')
        terrplant_empty.noaec_listed_seedling_emergence_dicot = pd.Series([0.1], dtype='float')
        result = terrplant_empty.out_lds_rq_spray()
        npt.assert_array_almost_equal(result, 50, '', True)
        return


#the below functions are called in the run methods.
    def test_blackbox_method(self):
        self.blackbox_method_int('rundry')
        self.blackbox_method_int('runsemi')
        self.blackbox_method_int('spray')
        self.blackbox_method_int('totaldry')
        self.blackbox_method_int('totalsemi')
        self.blackbox_method_int('nms_rq_dry')
        self.blackbox_method_int('nms_rq_semi')
        self.blackbox_method_int('nms_rq_spray')
        self.blackbox_method_int('lms_rq_dry')
        self.blackbox_method_int('lms_rq_semi')
        self.blackbox_method_int('lms_rq_spray')
        self.blackbox_method_int('nds_rq_dry')
        self.blackbox_method_int('nds_rq_semi')
        self.blackbox_method_int('nds_rq_spray')
        self.blackbox_method_int('lds_rq_dry')
        self.blackbox_method_int('lds_rq_semi')
        self.blackbox_method_int('lds_rq_spray')

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