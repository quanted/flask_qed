# -*- coding: utf-8 -*-
import unittest
import pandas as pd
import numpy.testing as npt
import pandas.util.testing as pdt
# the following works when running test script in parent directory as package:
# python -m tests.test_terrplant_unittest
# the following works for running as nosetests from parent directory:
from .. import terrplant_model_rest as terrplant_model

# load transposed qaqc data for inputs and expected outputs
# csv_transpose_path_in = "./terrplant_qaqc_in_transpose.csv"
# pd_obj_inputs = pd.read_csv(csv_transpose_path_in, index_col=0, engine='python')
# print(pd_obj_inputs)
# csv_transpose_path_exp = "./terrplant_qaqc_exp_transpose.csv"
# pd_obj_exp_out = pd.read_csv(csv_transpose_path_exp, index_col=0, engine='python')
# print(pd_obj_exp_out)

# create empty pandas dataframes to create empty terrplant object
df_empty = pd.DataFrame()
terrplant_empty = terrplant_model.terrplant("empty", df_empty, df_empty)

test = {}


class TestTerrplant(unittest.TestCase):
    def setup(self):
        pass
        # setup the test as needed
        # e.g. pandas to open terrplant qaqc csv
        #  Read qaqc csv and create pandas DataFrames for inputs and expected outputs

    def teardown(self):
        pass
        # teardown called after each test
        # e.g. maybe write test results to some text file

# each of these functions are queued by "run_methods" and have outputs defined as properties in the terrplant qaqc csv
    def test_rundry(self):
        """
        unittest for function terrplant.rundry
        """
        #(self.application_rate/self.incorporation_depth) * self.runoff_fraction
        try:
            terrplant_empty.application_rate = pd.Series([10.], dtype='int')
            terrplant_empty.incorporation_depth = pd.Series([2.], dtype='int')
            terrplant_empty.runoff_fraction = pd.Series([.1], dtype='float')
            result = terrplant_empty.rundry()
            npt.assert_array_almost_equal(result, 0.5, 4, '', True)
        finally:
            pass
        return

    def test_runsemi(self):
        """
        unittest for function terrplant.runsemi
        """
        #self.out_runsemi = (self.application_rate/self.incorporation_depth) * self.runoff_fraction * 10
        try:
            terrplant_empty.application_rate = pd.Series([10.], dtype='int')
            terrplant_empty.incorporation_depth = pd.Series([2.], dtype='int')
            terrplant_empty.runoff_fraction = pd.Series([.1], dtype='float')
            result = terrplant_empty.runsemi()
            npt.assert_array_almost_equal(result,5, 4, '', True)
        finally:
            pass
        return

    def test_spray(self):
        """
        unittest for function terrplant.spray
        """
        #self.out_spray = self.application_rate * self.drift_fraction
        try:
            terrplant_empty.application_rate = pd.Series([10.], dtype='int')
            terrplant_empty.drift_fraction = pd.Series([0.5], dtype='float')
            result = terrplant_empty.spray()
            npt.assert_array_almost_equal(result, 5, 4, '', True)
        finally:
            pass
        return

    def test_totaldry(self):
        """
        unittest for function terrplant.totaldry
        """
        #self.out_totaldry = self.out_rundry + self.out_spray
        try:
            terrplant_empty.rundry = pd.Series([0.5], dtype='float')
            terrplant_empty.spray = pd.Series([5.], dtype='int')
            result = terrplant_empty.totaldry()
            npt.assert_array_almost_equal(result, 5.5, 4, '', True)
        finally:
            pass
        return

    def test_totalsemi(self):
        """
        unittest for function terrplant.totalsemi
        """
        #self.out_totalsemi = self.out_runsemi + self.out_spray
        try:
            terrplant_empty.out_runsemi = pd.Series([5.], dtype='int')
            terrplant_empty.out_spray = pd.Series([5.], dtype='int')
            result = terrplant_empty.totalsemi()
            npt.assert_array_almost_equal(result, 10, 4, '', True)
        finally:
            pass
        return

    def test_nms_rq_dry(self):
        """
        unittest for function terrplant.nms_rq_dry
        """
        #self.out_nms_rq_dry = self.out_totaldry/self.ec25_nonlisted_seedling_emergence_monocot
        try:
            terrplant_empty.out_totaldry = pd.Series([5.5], dtype='float')
            terrplant_empty.ec25_nonlisted_seedling_emergence_monocot = pd.Series([0.05], dtype='float')
            result = terrplant_empty.nmsRQdry()
            npt.assert_array_almost_equal(result, 110, 4, '', True)
        finally:
            pass
        return

    def test_nms_loc_dry(self):
        """
        unittest for function terrplant.nms_loc_dry
        """
        # if self.out_nms_rq_dry >= 1.0:
        #     self.out_nms_loc_dry = ('The risk quotient for non-listed monocot seedlings exposed to'\
        #     ' the pesticide via runoff to a dry area indicates a potential risk.')
        # else:
        #     self.out_nms_loc_dry = ('The risk quotient for non-listed monocot seedlings exposed to'\
        #     ' the pesticide via runoff to a dry area indicates that potential risk is minimal.')
        try:
            terrplant_empty.out_nms_rq_dry = pd.Series([3.4], dtype='float')
            result = terrplant_empty.LOCnmsdry()
            exp = pd.Series("The risk quotient for non-listed monocot seedlings exposed to the pesticide via runoff to dry areas indicates a potential risk.")
            pdt.assert_series_equal(result, exp, True)
        finally:
            pass
        return

    def test_nms_rq_semi(self):
        """
        unittest for function terrplant.nms_rq_semi
        """
        #self.out_nms_rq_semi = self.out_totalsemi/self.ec25_nonlisted_seedling_emergence_monocot
        try:
            terrplant_empty.out_totalsemi = pd.Series([10.], dtype='int')
            terrplant_empty.ec25_nonlisted_seedling_emergence_monocot = pd.Series([0.05], dtype='float')
            result = terrplant_empty.nmsRQsemi()
            npt.assert_array_almost_equal(result, 200, 4, '', True)
        finally:
            pass
        return

    def test_out_nms_loc_semi(self):
        """
        unittest for function terrplant.nms_loc_semi
        """
        # if self.out_nms_rq_semi >= 1.0:
        #     self.out_nms_loc_semi = ('The risk quotient for non-listed monocot seedlings exposed to'\
        #     ' the pesticide via runoff to a semi-aquatic area indicates a potential risk.')
        # else:
        #     self.out_nms_loc_semi = ('The risk quotient for non-listed monocot seedlings exposed to the'\
        #     ' pesticide via runoff to a semi-aquatic area indicates that potential risk is minimal.')
        try:
            terrplant_empty.out_nms_rq_semi = pd.Series([2.7], dtype='float')
            result = terrplant_empty.LOCnmssemi()
            exp = pd.Series("The risk quotient for non-listed monocot seedlings exposed to the pesticide via runoff to semi-aquatic areas indicates a potential risk.")
            pdt.assert_series_equal(result, exp)
        finally:
            pass
        return

    def test_nms_rq_spray(self):
        """
        unittest for function terrplant.nms_rq_spray
        """
        #self.out_nms_rq_spray = self.out_spray/self.ec25_nonlisted_seedling_emergence_monocot
        try:
            terrplant_empty.out_spray = pd.Series([5.], dtype='int')
            terrplant_empty.ec25_nonlisted_seedling_emergence_monocot = pd.Series([0.05], dtype='float')
            terrplant_empty.ec25_nonlisted_vegetative_vigor_monocot = pd.Series([0.15], dtype='float')
            result = terrplant_empty.nmsRQspray()
            npt.assert_array_almost_equal(result, 99.8004, 4, '', True)
        finally:
            pass
        return

    def test_nms_loc_spray(self):
        """
        unittest for function terrplant.nms_loc_spray
        """
        # if self.out_nms_rq_spray >= 1.0:
        #     self.out_nms_loc_spray = ('The risk quotient for non-listed monocot seedlings exposed to'\
        # ' the pesticide via spray drift indicates a potential risk.')
        # else:
        #     self.out_nms_loc_spray = ('The risk quotient for non-listed monocot seedlings exposed to the'\
        # ' pesticide via spray drift indicates that potential risk is minimal.')
        try:
            terrplant_empty.out_nms_rq_spray = pd.Series([2.2], dtype='float')
            result = terrplant_empty.LOCnmsspray()
            exp = pd.Series("The risk quotient for non-listed monocot seedlings exposed to the pesticide via spray drift indicates a potential risk.")
            pdt.assert_series_equal(result, exp)
        finally:
            pass
        return

    def test_lms_rq_dry(self):
        """
        unittest for function terrplant.lms_rq_dry
        """
        #self.out_lms_rq_dry = self.out_totaldry/self.ec25_nonlisted_seedling_emergence_dicot
        try:
            terrplant_empty.out_totaldry = pd.Series([5.5], dtype='float')
            terrplant_empty.noaec_listed_seedling_emergence_monocot = pd.Series([0.01], dtype='float')
            result = terrplant_empty.lmsRQdry()
            npt.assert_array_almost_equal(result, 550, 4, '', True)
        finally:
            pass
        return

    def test_lms_loc_dry(self):
        """
        unittest for function terrplant.lms_loc_dry
        """
        # if self.out_lms_rq_dry >= 1.0:
        #     self.out_lms_loc_dry = ('The risk quotient for listed monocot seedlings exposed to'\
        #     ' the pesticide via runoff to a dry area indicates a potential risk.')
        # else:
        #     self.out_lms_loc_dry = ('The risk quotient for listed monocot seedlings exposed to the'\
        #     ' pesticide via runoff to a dry area indicates that potential risk is minimal.')
        try:
            terrplant_empty.out_lms_rq_dry = pd.Series([1.6], dtype='float')
            result = terrplant_empty.LOClmsdry()
            exp = pd.Series("The risk quotient for listed monocot seedlings exposed to the pesticide via runoff to dry areas indicates a potential risk.")
            pdt.assert_series_equal(result, exp)
        finally:
            pass
        return

    def test_lms_rq_semi(self):
        """
        unittest for function terrplant.lms_rq_semi
        """
        #self.out_lms_rq_semi = self.out_totalsemi/self.ec25_nonlisted_seedling_emergence_dicot
        try:
            terrplant_empty.out_totalsemi = pd.Series([10.], dtype='int')
            terrplant_empty.noaec_listed_seedling_emergence_monocot = pd.Series([0.01], dtype='float')
            result = terrplant_empty.lmsRQsemi()
            npt.assert_array_almost_equal(result, 1000, 4, '', True)
        finally:
            pass
        return

    def test_lms_loc_semi(self):
        """
        unittest for function terrplant.lms_loc_semi
        """
        # if self.out_lms_rq_semi >= 1.0:
        #     self.out_lms_loc_semi = ('The risk quotient for listed monocot seedlings exposed to'\
        #     ' the pesticide via runoff to a semi-aquatic area indicates a potential risk.')
        # else:
        #     self.out_lms_loc_semi = ('The risk quotient for listed monocot seedlings exposed to the'\
        #     ' pesticide via runoff to a semi-aquatic area indicates that potential risk is minimal.')
        try:
            terrplant_empty.out_lms_rq_semi = pd.Series([0.9], dtype= 'float')
            result = terrplant_empty.LOClmssemi()
            exp = pd.Series("The risk quotient for listed monocot seedlings exposed to the pesticide via runoff to semi-aquatic areas indicates that potential risk is minimal.")
            pdt.assert_series_equal(result, exp)
        finally:
            pass
        return

    def test_lms_rq_spray(self):
        """
        unittest for function terrplant.lms_rq_spray
        """
        #self.out_lms_rq_spray = self.out_spray/self.ec25_nonlisted_seedling_emergence_dicot
        try:
            terrplant_empty.out_spray = pd.Series([5.], dtype='int')
            terrplant_empty.noaec_listed_seedling_emergence_monocot = pd.Series([0.01], dtype='float')
            terrplant_empty.noaec_listed_vegetative_vigor_monocot = pd.Series([0.05], dtype='float')
            terrplant_empty.out_min_lms_spray = terrplant_empty.minlmsspray()
            result = terrplant_empty.lmsRQspray()
            npt.assert_array_almost_equal(result, 500, 4, '', True)
        finally:
            pass
        return

    def test_lms_loc_spray(self):
        """
        unittest for function terrplant.lms_loc_spray
        """
        # if self.out_lms_rq_spray >= 1.0:
        #     self.out_lms_loc_spray = ('The risk quotient for listed monocot seedlings exposed to'\
        #     ' the pesticide via spray drift indicates a potential risk.')
        # else:
        #     self.out_lms_loc_spray = ('The risk quotient for listed monocot seedlings exposed to the'\
        #     ' pesticide via spray drift indicates that potential risk is minimal.')
        try:
            terrplant_empty.out_lms_rq_spray = pd.Series([1.1], dtype= 'float')
            result = terrplant_empty.LOClmsspray()
            exp = pd.Series("The risk quotient for listed monocot seedlings exposed to the pesticide via spray drift indicates a potential risk.")
            pdt.assert_series_equal(result, exp)
        finally:
            pass
        return

    def test_nds_rq_dry(self):
        """
        unittest for function terrplant.nds_rq_dry
        """
        #self.out_nds_rq_dry = self.out_totaldry/self.noaec_listed_seedling_emergence_monocot
        try:
            terrplant_empty.out_totaldry = pd.Series([5.5], dtype='float')
            terrplant_empty.ec25_nonlisted_seedling_emergence_dicot = pd.Series([0.02], dtype='float')
            result = terrplant_empty.ndsRQdry()
            npt.assert_array_almost_equal(result, 275, 4, '', True)
        finally:
            pass
        return

    def test_nds_loc_dry(self):
        """
        unittest for function terrplant.nds_loc_dry
        """
        # if self.out_nds_rq_dry >= 1.0:
        #     self.out_nds_loc_dry = ('The risk quotient for non-listed monocot seedlings exposed to'\
        #     ' the pesticide via runoff to dry areas indicates a potential risk.')
        # else:
        #     self.out_nds_loc_dry = ('The risk quotient for non-listed monocot seedlings exposed to the'\
        #     ' pesticide via runoff to dry areas indicates that potential risk is minimal.')
        try:
            terrplant_empty.out_nds_rq_dry = pd.Series([2.7], dtype='float')
            result = terrplant_empty.LOCndsdry()
            exp = pd.Series("The risk quotient for non-listed dicot seedlings exposed to the pesticide via runoff to dry areas indicates a potential risk.")
            pdt.assert_series_equal(result, exp)
        finally:
            pass
        return

    def test_nds_rq_semi(self):
        """
        unittest for function terrplant.nds_rq_semi
        """
        #self.out_nds_rq_semi = self.out_totalsemi/self.noaec_listed_seedling_emergence_monocot
        try:
            terrplant_empty.out_totalsemi = pd.Series([10.], dtype='int')
            terrplant_empty.ec25_nonlisted_seedling_emergence_dicot = pd.Series([0.02], dtype='float')
            result = terrplant_empty.ndsRQsemi()
            npt.assert_array_almost_equal(result, 500, 4, '', True)
        finally:
            pass
        return

    def test_nds_loc_semi(self):
        """
        unittest for function terrplant.nds_loc_semi
        """
        # if self.out_nds_rq_semi >= 1.0:
        #     self.out_nds_loc_semi = ('The risk quotient for non-listed monocot seedlings exposed to'\
        #     ' the pesticide via runoff to semi-aquatic areas indicates a potential risk.')
        # else:
        #     self.out_nds_loc_semi = ('The risk quotient for non-listed monocot seedlings exposed to the'\
        #     ' pesticide via runoff to semi-aquatic areas indicates that potential risk is minimal.')
        try:
            terrplant_empty.out_nds_rq_semi = pd.Series([0.7], dtype='float')
            result = terrplant_empty.LOCndssemi()
            exp = pd.Series("The risk quotient for non-listed dicot seedlings exposed to the pesticide via runoff to semi-aquatic areas indicates that potential risk is minimal.")
            pdt.assert_series_equal(result, exp)
        finally:
            pass
        return

    def test_nds_rq_spray(self):
        """
        unittest for function terrplant.nds_rq_spray
        """
        #self.out_nds_rq_spray = self.out_spray/self.noaec_listed_seedling_emergence_monocot
        try:
            terrplant_empty.out_spray = pd.Series([5.], dtype='int')
            terrplant_empty.ec25_nonlisted_seedling_emergence_dicot = pd.Series([0.02], dtype='float')
            terrplant_empty.ec25_nonlisted_vegetative_vigor_dicot = pd.Series([0.05], dtype='float')
            result = terrplant_empty.ndsRQspray()
            npt.assert_array_almost_equal(result, 153.84615, 4, '', True)
        finally:
            pass
        return

    def test_nds_loc_spray(self):
        """
        unittest for function terrplant.nds_loc_spray
        """
        # if self.out_nds_rq_spray >= 1.0:
        #     self.out_nds_loc_semi = ('The risk quotient for non-listed monocot seedlings exposed to'\
        #     ' the pesticide via spray drift indicates a potential risk.')
        # else:
        #     self.out_nds_loc_semi = ('The risk quotient for non-listed monocot seedlings exposed to the'\
        #     ' pesticide via spray drift indicates that potential risk is minimal.')
        try:
            terrplant_empty.out_nds_rq_spray = pd.Series([0.2], dtype='float')
            result = terrplant_empty.LOCndsspray()
            exp = pd.Series("The risk quotient for non-listed dicot seedlings exposed to the pesticide via spray drift indicates that potential risk is minimal.")
            pdt.assert_series_equal(result, exp)
        finally:
            pass
        return

    def test_lds_rq_dry(self):
        """
        unittest for function terrplant.lds_rq_dry
        """
        #self.out_lds_rq_dry = self.out_totaldry/self.noaec_listed_seedling_emergence_dicot
        try:
            terrplant_empty.out_totaldry = pd.Series([5.5], dtype='float')
            terrplant_empty.noaec_listed_seedling_emergence_dicot = pd.Series([0.1], dtype='float')
            result = terrplant_empty.ldsRQdry()
            npt.assert_array_almost_equal(result, 55, 4, '', True)
        finally:
            pass
        return

    def test_lds_loc_dry(self):
        """
        unittest for function terrplant.lds_loc_dry
        """
        # if self.out_lds_rq_dry >= 1.0:
        #     self.out_lds_loc_dry = ('The risk quotient for listed monocot seedlings exposed to'\
        #     ' the pesticide via runoff to dry areas indicates a potential risk.')
        # else:
        #     self.out_lds_loc_dry = ('The risk quotient for listed monocot seedlings exposed to the'\
        #     ' pesticide via runoff to dry areas indicates that potential risk is minimal.')
        try:
            terrplant_empty.out_lds_rq_dry = pd.Series([1.5], dtype= 'float')
            result = terrplant_empty.LOCldsdry()
            exp = pd.Series("The risk quotient for listed dicot seedlings exposed to the pesticide via runoff to dry areas indicates a potential risk.")
            pdt.assert_series_equal(result, exp)
        finally:
            pass
        return

    def test_lds_rq_semi(self):
        """
        unittest for function terrplant.lds_rq_semi
        """
        #self.out_lds_rq_semi = self.out_totalsemi/self.noaec_listed_seedling_emergence_dicot
        try:
            terrplant_empty.out_totalsemi = pd.Series([10.], dtype='int')
            terrplant_empty.noaec_listed_seedling_emergence_dicot = pd.Series([0.1], dtype='float')
            result = terrplant_empty.ldsRQsemi()
            npt.assert_array_almost_equal(result, 100, 4, '', True)
        finally:
            pass
        return

    def test_lds_loc_semi(self):
        """
        unittest for function terrplant.lds_loc_semi
        """
        # if self.out_lds_rq_semi >= 1.0:
        #     self.out_lds_loc_semi = ('The risk quotient for listed monocot seedlings exposed to'\
        #     ' the pesticide via runoff to semi-aquatic areas indicates a potential risk.')
        # else:
        #     self.out_lds_loc_semi = ('The risk quotient for listed monocot seedlings exposed to the'\
        #     ' pesticide via runoff to semi-aquatic areas indicates that potential risk is minimal.')
        try:
            terrplant_empty.out_lds_rq_semi = pd.Series([4.5], dtype= 'float')
            result = terrplant_empty.LOCldssemi()
            exp = pd.Series("The risk quotient for listed dicot seedlings exposed to the pesticide via runoff to semi-aquatic areas indicates a potential risk.")
            pdt.assert_series_equal(result, exp)
        finally:
            pass
        return

    def test_lds_rq_spray(self):
        """
        unittest for function terrplant.lds_rq_spray
        """
        #self.out_lds_rq_spray = self.out_spray/self.noaec_listed_seedling_emergence_dicot
        try:
            terrplant_empty.out_spray = pd.Series([5])
            terrplant_empty.noaec_listed_seedling_emergence_dicot = pd.Series([0.1], dtype='float')
            terrplant_empty.noaec_listed_vegetative_vigor_dicot = pd.Series([0.05], dtype='float')
            terrplant_empty.out_min_lds_spray = terrplant_empty.minldsspray()
            result = terrplant_empty.ldsRQspray()
            npt.assert_array_almost_equal(result, 100, 4, '', True)
        finally:
            pass
        return

    def test_lds_loc_spray(self):
        """
        unittest for function terrplant.lds_loc_spray
        """
        # if self.out_lds_rq_spray >= 1.0:
        #     self.out_lds_loc_spray = ('The risk quotient for listed monocot seedlings exposed to'\
        #     ' the pesticide via spray drift indicates a potential risk.')
        # else:
        #     self.out_lds_loc_spray = ('The risk quotient for listed monocot seedlings exposed to the'\
        #     ' pesticide via spray drift indicates that potential risk is minimal.')
        try:
            terrplant_empty.out_lds_rq_spray = pd.Series([0.8], dtype='float')
            result = terrplant_empty.LOCldsspray()
            exp = pd.Series("The risk quotient for listed dicot seedlings exposed to the pesticide via spray drift indicates that potential risk is minimal.")
            pdt.assert_series_equal(result, exp)
        finally:
            pass
        return

    def test_min_nms_spray(self):
        """
        unittest for function terrplant.min_nms_spray
        """
        try:
            terrplant_empty.ec25_nonlisted_seedling_emergence_monocot = pd.Series([0.0501], dtype='float')
            terrplant_empty.ec25_nonlisted_vegetative_vigor_monocot = pd.Series([0.0801], dtype='float')
            result = terrplant_empty.minnmsspray()
            npt.assert_array_almost_equal(result, 0.0501, 4, '', True)
        finally:
            pass
        return

    def test_min_lms_spray(self):
        """
        unittest for function terrplant.min_lms_spray
        """
        try:
            terrplant_empty.noaec_listed_vegetative_vigor_monocot = pd.Series([0.0211], dtype='float')
            terrplant_empty.noaec_listed_seedling_emergence_monocot = pd.Series([0.0205], dtype='float')
            result = terrplant_empty.minlmsspray()
            npt.assert_array_almost_equal(result, 0.0205, 4, '', True)
        finally:
            pass
        return

    def test_min_nds_spray(self):
        """
        unittest for function terrplant.min_nds_spray
        """
        try:
            terrplant_empty.ec25_nonlisted_vegetative_vigor_dicot = pd.Series([0.0325], dtype='float')
            terrplant_empty.ec25_nonlisted_seedling_emergence_dicot = pd.Series([0.5022], dtype='float')
            result = terrplant_empty.minndsspray()
            npt.assert_array_almost_equal(result, 0.0325, 4, '', True)
        finally:
            pass
        return

    def test_min_lds_spray(self):
        """
        unittest for function terrplant.min_lds_spray
        """
        try:
            terrplant_empty.noaec_listed_seedling_emergence_dicot = pd.Series([0.3206], dtype='float')
            terrplant_empty.noaec_listed_vegetative_vigor_dicot = pd.Series([0.5872], dtype='float')
            result = terrplant_empty.minldsspray()
            npt.assert_array_almost_equal(result, 0.3206, 4, '', True)
        finally:
            pass
        return

# unittest will
# 1) call the setup method,
# 2) then call every method starting with "test",
# 3) then the teardown method
if __name__ == '__main__':
    unittest.main()