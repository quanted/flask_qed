from __future__ import division
import pandas as pd
import logging


class rice(object):
    def __init__(self, run_type, pd_obj, pd_obj_exp):

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
        # Callable from Bottle that returns JSON
        self.json = self.json(self.pd_obj, self.pd_obj_out, self.pd_obj_exp)

    def populate_input_properties(self):
        # Inputs: Assign object attribute variables from the input Pandas DataFrame
        # Inputs: Assign object attribute variables from the input Pandas DataFrame
        self.chemical_name = self.pd_obj["chemical_name"]
        self.mai = self.pd_obj["mai"]
        self.dsed = self.pd_obj["dsed"]
        self.area = self.pd_obj["area"]
        self.pb = self.pd_obj["pb"]
        self.dw = self.pd_obj["dw"]
        self.osed = self.pd_obj["osed"]
        self.Kd = self.pd_obj["Kd"]

    def create_output_properties(self):
        # Outputs: Assign object attribute variables to Pandas Series
        self.out_msed = pd.Series(name="out_msed")
        self.out_vw = pd.Series(name="out_vw")
        self.out_mass_area = pd.Series(name="out_mass_area")
        self.out_cw = pd.Series(name="out_cw")

    def create_output_dataframe(self):
        # Create DataFrame containing output value Series
        pd_obj_out = pd.DataFrame({
            'out_msed': self.out_msed,
            'out_vw': self.out_vw,
            'out_mass_area': self.out_mass_area,
            'out_cw': self.out_cw
        })
        self.pd_obj_out = pd_obj_out

    def run_methods(self):
        self.Calcmsed()
        self.Calcvw()
        self.Calcmass_area()
        self.Calccw()

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

    # The mass of the sediment at equilibrium with the water column
    # Sediment depth (dsed) * Area of rice paddy (area) * Bulk density of sediment(mass/volume) pb
    def Calcmsed(self):
        self.out_msed = self.dsed * self.area * self.pb
        return self.out_msed

    # The volume of the water column plus pore water
    def Calcvw(self):
        self.out_vw = (self.dw * self.area) + (self.dsed * self.osed * self.area)
        return self.out_vw

    # The pesticide mass per unit area
    def Calcmass_area(self):
        self.out_mass_area = (self.mai / self.area) * 10000
        return self.out_mass_area

    #    if a <= 0:
    #     print('The area of the rice paddy must be greater than 0 m2')

    # Water Concentration
    def Calccw(self):
        self.out_cw = (self.out_mass_area / (self.dw + (self.dsed * (self.osed + (self.pb * self.Kd * 1e-5))))) * 100
        return self.out_cw
