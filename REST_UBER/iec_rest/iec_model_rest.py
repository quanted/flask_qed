# -*- coding: utf-8 -*-
import math
import pandas as pd

class iec(object):
    def __init__(self, run_type, pd_obj, pd_obj_exp):
        # run_type can be single, batch or qaqc
        # 0 to run calculation, else it wont
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
        # Callable from Bottle that returns JSON
        return pd_obj_json, pd_obj_out_json, pd_obj_exp_json

    def populate_input_properties(self):
        # Inputs: Assign object attribute variables from the input Pandas DataFrame
        self.dose_response = self.pd_obj['dose_response']
        self.LC50 = self.pd_obj['LC50']
        self.threshold = self.pd_obj['threshold']

    def create_output_dataframe(self):
    # Create DataFrame containing output value Series
        pdj_obj_out = pd.DataFrame({
            'z_score_f_out': self.z_score_f_out,
            'F8_f_out': self.F8_f_out,
            'chance_f_out': self.chance_f_out
        })
        # create pandas properties for acceptance testing
        self.pd_obj_out = pdj_obj_out

    def create_output_properties(self):
        # Outputs: Assign object attribute variables to Pandas Series
        self.z_score_f_out = pd.Series(name='z_score_f_out')
        self.F8_f_out = pd.Series(name='F8_f_out')
        self.chance_f_out = pd.Series(name='chance_f_out')

    # begin model methods
    def run_methods(self):
        try:
            self.z_score_f()
            self.F8_f()
            self.chance_f()
        except TypeError:
            print "Type Error: Your variables are not set correctly."

    def z_score_f(self):
        if self.dose_response < 0:
            raise ValueError\
            ('self.dose_response=%g is a non-physical value.' % self.dose_response)
        if self.LC50 < 0:
            raise ValueError\
            ('self.LC50=%g is a non-physical value.' % self.LC50)
        if self.threshold < 0:
            raise ValueError
            ('self.threshold=%g is a non-physical value.' % self.threshold)
        if self.z_score_f_out == -1:
            self.z_score_f_out = self.dose_response * (math.log10(self.LC50 * self.threshold) - math.log10(self.LC50))
        return self.z_score_f_out
        
    def F8_f(self):
        if self.z_score_f_out == None:
            raise ValueError\
            ('z_score_f variable equals None and therefor this function cannot be run.')
        if self.F8_f_out == -1:
            self.F8_f_out = 0.5 * math.erfc(-self.z_score_f_out/math.sqrt(2))
            if self.F8_f_out == 0:
                self.F8_f_out = 10^-16
            else:
                self.F8_f_out = self.F8_f_out
        return self.F8_f_out
        
    def chance_f(self):
        if self.F8_f_out == None:
            raise ValueError\
            ('F8_f variable equals None and therefor this function cannot be run.')
        if self.chance_f_out == -1:
            self.chance_f_out = 1 / self.F8_f_out
        return self.chance_f_out

