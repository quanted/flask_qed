from __future__ import division
import logging
import pandas as pd


class earthworm(object):
    def __init__(self, run_type, pd_obj, pd_obj_exp):
        logging.info(pd_obj)

        # Inputs: Assign object attribute variables from the input Pandas DataFrame
        self.run_type = run_type
        self.pd_obj = pd_obj
        self.pd_obj_exp = pd_obj_exp

        # Execute model methods if requested
        if self.run_type != "empty":
            self.execute_model()

    def execute_model(self):
        self.populate_input_properties()
        self.create_output_properties()
        self.run_methods()
        self.create_output_dataframe()
        self.json = self.json(self.pd_obj, self.pd_obj_out, self.pd_obj_exp)

    def populate_input_properties(self):
        # Inputs: Assign object attribute variables from the input Pandas Dataframe
        self.k_ow = self.pd_obj['k_ow']
        self.l_f_e = self.pd_obj['l_f_e']
        self.c_s = self.pd_obj['c_s']
        self.k_d = self.pd_obj['k_d']
        self.p_s = self.pd_obj['p_s']
        # self.c_w = self.pd_obj['c_w']
        # self.m_w = self.pd_obj['m_w']
        # self.p_e = self.pd_obj['p_e']

    def create_output_properties(self):
        # Outputs: Assign object attribute variables to Pandas Series
        self.earthworm_fugacity_out = pd.Series(name="earthworm_fugacity_out")

    # Begin model methods
    def run_methods(self):
        self.earthworm_fugacity()

    def create_output_dataframe(self):
        # Create DataFrame containing output value Series
        pd_obj_out = pd.DataFrame({
            'earthworm_fugacity_out': self.earthworm_fugacity_out,
        })
        #create pandas properties for acceptance testing
        self.pd_obj_out = pd_obj_out

    def json(self, pd_obj, pd_obj_out, pd_obj_exp):
        """
            Convert DataFrames to JSON, returning a tuple
            of JSON strings (inputs, outputs, exp_out)
        """

        pd_obj_json = pd_obj.to_json()
        pd_obj_out_json = pd_obj_out.to_json()
        try:
            pd_obj_exp_json = pd_obj_exp.to_json()
        except:
            pd_obj_exp_json = "{}"

        return pd_obj_json, pd_obj_out_json, pd_obj_exp_json

    def earthworm_fugacity(self):
        #self.earthworm_fugacity_out = self.k_ow*self.l_f_e*(self.c_s/(self.k_d*self.p_s)+self.c_w)*self.m_w/self.p_e

        # most recent version of EFED equation circa 3-26-2013 is implemented in the formula below
        # model runs documented in ubertool crosswalk use the EFED model in "earthworm models 3-26-13b.xlsx"
        self.earthworm_fugacity_out = self.k_ow*self.l_f_e*(self.c_s/(self.k_d*self.p_s))
        return self.earthworm_fugacity_out
