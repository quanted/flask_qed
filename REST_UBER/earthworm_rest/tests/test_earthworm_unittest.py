from .. import earthworm_model_rest as earthworm_model
import pandas as pd
import unittest
import numpy.testing as npt

df_empty = pd.DataFrame()
earthworm_empty = earthworm_model.earthworm("empty", df_empty, df_empty)

test = {}


class TestEarthworm(unittest.TestCase):
    def setup(self):
        pass
        # setup the test as needed
        # e.g. pandas to open stir qaqc csv
        #  Read qaqc csv and create pandas DataFrames for inputs and expected outputs
    def test_earthworm_fugacity(self):
        try:
            earthworm_empty.k_ow = pd.Series([1])
            earthworm_empty.l_f_e = pd.Series([0.01])
            earthworm_empty.c_s = pd.Series([0.038692165])
            earthworm_empty.k_d = pd.Series([0.0035])
            earthworm_empty.p_s = pd.Series([1.5])
            result = earthworm_empty.earthworm_fugacity()
            npt.assert_array_almost_equal(result,0.073699363, 4, '', True)
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