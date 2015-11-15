# -*- coding: utf-8 -*-
from __future__ import division
import pandas as pd
import logging


class rice(object):
    def __init__(self, run_type, pd_obj, pd_obj_exp):

        logging.info("====== Rice constructor")
        self.run_type = run_type
        self.pd_obj = pd_obj
        self.pd_obj_exp = pd_obj_exp

        # Outputs: Assign object attribute variables to Pandas Series
        self.out_msed = pd.Series(name="out_msed")
        self.out_vw = pd.Series(name="out_vw")
        self.out_mass_area = pd.Series(name="out_mass_area")
        self.out_cw = pd.Series(name="out_cw")

        # run meth
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

    def run_methods(self):
        self.Calcmsed()
        self.Calcvw()
        self.Calcmass_area()
        self.Calccw()

    def create_output_dataframe(self):
        # Create DataFrame containing output value Series
        pd_obj_out = pd.DataFrame({
            'out_msed': self.out_msed,
            'out_vw': self.out_vw,
            'out_mass_area': self.out_mass_area,
            'out_cw': self.out_cw
        })

        # Callable from Bottle that returns JSON
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

        return pd_obj_json, pd_obj_out_json, pd_obj_exp_json

    # The mass of the sediment at equilibrium with the water column
    # Sediment depth (dsed) * Area of rice paddy (area) * Bulk density of sediment(mass/volume) pb
    def Calcmsed(self):
        # if self.msed == -1:
        #     try:
        #         self.dsed = float(self.dsed)
        #         self.a = float(self.a)
        #         self.pb = float(self.pb)
        #     except IndexError:
        #         raise IndexError\
        #         ('The sediment depth, area of the rice paddy, and/or the bulk'\
        #         ' density of the sediment must be supplied the command line.')
        #     except ValueError:
        #         raise ValueError\
        #         ('The sediment depth must be a real number, not "%m"' % self.dsed)
        #     except ValueError:
        #         raise ValueError\
        #         ('The area of the rice paddy must be a real number, not "%ha"' % self.a)
        #     except ValueError:
        #         raise ValueError\
        #         ('The bulk density of the sediment must be a real number, not "%kg/m3".' % self.pb)
        #     if self.dsed < 0:
        #         raise ValueError\
        #         ('dsed=%g is a non-physical value.' % self.dsed)
        #     if self.a < 0:
        #         raise ValueError\
        #         ('a=%g is a non-physical value.' % self.a)
        #     if self.pb < 0:
        #         raise ValueError\
        #         ('pb=%g is a non-physical value.' % self.pb)
        self.out_msed = self.dsed * self.area * self.pb
        return self.out_msed

    # The volume of the water column plus pore water
    def Calcvw(self):
        # if self.vw == -1:
        #     try:
        #         self.dw = float(self.dw)
        #         self.a = float(self.a)
        #         self.dsed = float(self.dsed)
        #         self.osed = float(self.osed)
        #     except IndexError:
        #         raise IndexError\
        #         ('The water column depth, area of the rice paddy, sediment depth, and/or'\
        #         ' porosity of sediment must be supplied the command line.')
        #     except ValueError:
        #         raise ValueError\
        #         ('The water column depth must be a real number, not "%m"' % self.dw)
        #     except ValueError:
        #         raise ValueError\
        #         ('The area of the rice paddy must be a real number, not "%ha"' % self.a)
        #     except ValueError:
        #         raise ValueError\
        #         ('The sediment depth must be a real number, not "%cm"' % self.dsed)
        #     except ValueError:
        #         raise ValueError\
        #         ('The porosity of sediment must be a real number"' % self.osed)
        #     if self.dw < 0:
        #         raise ValueError\
        #         ('dw=%g is a non-physical value.' % self.dw)
        #     if self.a < 0:
        #         raise ValueError\
        #         ('a=%g is a non-physical value.' % self.a)
        #     if self.dsed < 0:
        #         raise ValueError\
        #         ('dsed=%g is a non-physical value.' % self.dsed)
        #     if self.osed < 0:
        #         raise ValueError\
        #         ('osed=%g is a non-physical value.' % self.osed)
        self.out_vw = (self.dw * self.area) + (self.dsed * self.osed * self.area)
        return self.out_vw

    # The pesticide mass per unit area
    def Calcmass_area(self):
        # if self.mai1 == -1:
        #     try:
        #         self.mai = float(self.mai)
        #         self.a = float(self.a)
        #     except IndexError:
        #         raise IndexError\
        #         ('The mass applied to patty and area of the patty must be supplied the command line.')
        #     except ValueError:
        #         raise ValueError\
        #         ('The area of the rice paddy must be a real number, not "%ha"' % self.a)
        #     except ValueError:
        #         raise ValueError\
        #         ('The area of the rice paddy must be a real number, not "%ha"' % self.mai)
        #     if self.a < 0:
        #         raise ValueError\
        #         ('a=%g is a non-physical value.' % self.a)
        #     if self.mai < 0:
        #         raise ValueError\
        #         ('mai=%g is a non-physical value.' % self.mai)
        self.out_mass_area = (self.mai / self.area) * 10000
        return self.out_mass_area

    #    if a <= 0:
    #     print('The area of the rice paddy must be greater than 0 m2')


    # Water Concentration
    def Calccw(self):
        # if self.cw == -1:
        #     try:
        #         self.mai1 = float(self.mai1)
        #         self.dw = float(self.dw)
        #         self.dsed = float(self.dsed)
        #         self.osed = float(self.osed)
        #         self.pb = float(self.pb)
        #         self.kd = float(self.kd)
        #     except IndexError:
        #         raise IndexError\
        #         ('The mass of pesticide applied per unit area, water column depth,'\
        #         ' the sediment depth, porosity of sediment, the bulk density of sediment,'\
        #         'and/or the water-sediment partitioning coefficient must be supplied on'\
        #         ' the command line.')
        #     except ValueError:
        #         raise ValueError\
        #         ('The mass of pesticide applied per unit area must be a real number, '\
        #         'not "%kg/ha"' %mai1)
        #     except ValueError:
        #         raise ValueError\
        #         ('The water column depth must be a real number, not "%cm"' % self.dw)
        #     except ValueError:
        #         raise ValueError\
        #         ('The sediment depth must be a real number, not "%cm"' % self.dsed)
        #     except ValueError:
        #         raise ValueError\
        #         ('The porosity of the sediment must be a real number' % self.osed)
        #     except ValueError:
        #         raise ValueError\
        #         ('The bulk density of the sediment must be a real number, not"%kg/m3"' % self.pb)
        #     except ValueError:
        #         raise ValueError\
        #         ('The water-sediment partitioning coefficient must be a real number,'\
        #         ' not"%kg/L"' % self.kd)
        #     if self.mai1 < 0:
        #         raise ValueError\
        #         ('mai1=%g is a non-physical value.' % self.mai1)
        #     if self.dw < 0:
        #         raise ValueError\
        #         ('dw=%g is a non-physical value.' % self.dw)
        #     if self.dsed < 0:
        #         raise ValueError\
        #         ('dsed=%g is a non-physical value.' % self.dsed)
        #     if self.osed < 0:
        #         raise ValueError\
        #         ('osed=g% is a non-physical value.' % self.osed)
        #     if self.pb < 0:
        #         raise ValueError\
        #         ('pb=g% is a non-physical value.' % self.pb)
        #     if self.kd < 0:
        #         raise ValueError\
        #         ('kd=g% is a non-physical value.' % self.kd)
        self.out_cw = (self.out_mass_area / (self.dw + (self.dsed * (self.osed + (self.pb * self.Kd * 1e-5))))) * 100
        return self.out_cw
