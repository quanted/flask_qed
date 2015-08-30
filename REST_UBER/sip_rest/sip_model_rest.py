# -*- coding: utf-8 -*-

import numpy as np
import pandas as pd
import logging
from functools import wraps
import time

def timefn(fn):
    @wraps(fn)
    def measure_time(*args, **kwargs):
        t1 = time.time()
        result = fn(*args, **kwargs)
        t2 = time.time()
        logging.info(t1)
        logging.info(t2)
        print("sip_model_rest.py@timefn: " + fn.func_name + " took " + 
            "{:.6f}".format(t2-t1) + " seconds")
        return result
    return measure_time


class sip(object):
    @timefn
    def __init__(self, run_type, pd_obj, pd_obj_exp):
        # run_type can be single, batch or qaqc
        self.run_type = run_type

        # Inputs: Assign object attribute variables from the input Pandas DataFrame
        self.chemical_name = pd_obj['chemical_name']
        self.solubility = pd_obj['solubility']
        # try:
        #     self.species_tested_bird = pd_obj['species_tested_bird']  
        # except:
        #     self.species_tested_bird = None
        self.bodyweight_tested_bird = pd_obj['bodyweight_tested_bird']
        self.ld50_avian_water = pd_obj['ld50_avian_water']   
        self.noaec_quail = pd_obj['noaec_quail']
        self.noaec_duck = pd_obj['noaec_duck']
        self.noaec_bird_other_1 = pd_obj['noaec_bird_other_1']
        self.noaec_bird_other_2 = pd_obj['noaec_bird_other_2']
        # self.ld50_species_tested_mammal = pd_obj['ld50_species_tested_mammal']
        self.bodyweight_tested_mammal = pd_obj['bodyweight_tested_mammal'] 
        self.ld50_mammal_water = pd_obj['ld50_mammal_water']
        self.noael_mammal_water = pd_obj['noael_mammal_water']
        self.mineau_scaling_factor = pd_obj['mineau_scaling_factor']

        self.bodyweight_assessed_bird = 20.
        self.bodyweight_assessed_mammal = 1000.


        # Outputs: Assign object attribute variables to Pandas Series
        self.fw_bird_out = pd.Series(name = "fw_bird_out")
        self.fw_mamm_out = pd.Series(name = "fw_mamm_out")
        self.dose_bird_out = pd.Series(name = "dose_bird_out")
        self.dose_mamm_out = pd.Series(name = "dose_mamm_out")
        self.at_bird_out = pd.Series(name = "at_bird_out")
        self.at_mamm_out = pd.Series(name = "at_mamm_out")
        self.fi_bird_out = pd.Series(name = "fi_bird_out")
        self.det_out = pd.Series(name = "det_out")
        self.act_out = pd.Series(name = "act_out")
        self.acute_bird_out = pd.Series(name = "acute_bird_out")
        self.acuconb_out = pd.Series(name = "acuconb_out")
        self.acute_mamm_out = pd.Series(name = "acute_mamm_out")
        self.acuconm_out = pd.Series(name = "acuconm_out")
        self.chron_bird_out = pd.Series(name = "chron_bird_out")
        self.chronconb_out = pd.Series(name = "chronconb_out")
        self.chron_mamm_out = pd.Series(name = "chron_mamm_out")
        self.chronconm_out = pd.Series(name = "chronconm_out")

        # Execute model methods
        self.run_methods()

        # Create DataFrame containing output value Series
        pd_obj_out = pd.DataFrame({
            'fw_bird_out' : self.fw_bird_out,
            'fw_mamm_out' : self.fw_mamm_out,
            'dose_bird_out' : self.dose_bird_out,
            'dose_mamm_out' : self.dose_mamm_out,
            'at_bird_out' : self.at_bird_out,
            'at_mamm_out' : self.at_mamm_out,
            'fi_bird_out' : self.fi_bird_out,
            'det_out' : self.det_out,
            'act_out' : self.act_out,
            'acute_bird_out' : self.acute_bird_out,
            'acuconb_out' : self.acuconb_out,
            'acute_mamm_out' : self.acute_mamm_out,
            'acuconm_out' : self.acuconm_out,
            'chron_bird_out' : self.chron_bird_out,
            'chronconb_out' : self.chronconb_out,
            'chron_mamm_out' : self.chron_mamm_out,
            'chronconm_out' : self.chronconm_out
        })

        # Callable from Bottle that returns JSON
        self.json = self.json(pd_obj, pd_obj_out, pd_obj_exp)

    @timefn
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


    # Begin model methods
    @timefn
    def run_methods(self):
        self.fw_bird()
        self.fw_mamm()
        self.dose_bird()
        self.dose_mamm()
        self.at_bird()
        self.at_mamm()
        self.det()
        self.act()
        self.acute_bird()
        self.acuconb()
        self.acute_mamm()
        self.acuconm()
        self.chron_bird()
        self.chronconb()
        self.chron_mamm()
        self.chronconm()

    @timefn
    def fw_bird(self):
        """
        For birds, the daily water intake rate is calculated using the equation below. 
        This equation is representative of passerine birds, which represent the majority 
        of bird species visiting agricultural areas and which have higher daily water flux 
        requirements than other birds.  As a result, the equations represent the most 
        conservative estimate of pesticide concentrations in water. The resulting daily 
        water intake rate for the 20 g bird is 0.0162 L.

            Flux(water) = (1.180 * BW^0.874) / 1000

            where: BW = 20 g
        """
        # if self.fw_bird_out == -1:
        #     try:
        #         self.bodyweight_assessed_bird = float(self.bodyweight_assessed_bird)
        #     except IndexError:
        #         raise IndexError\
        #         ('The body weight of the bird must be supplied on the command line.')
        #     except ValueError:
        #         raise ValueError\
        #         ('The body weight of the bird must be a real number, not "%g"' % self.bodyweight_assessed_bird)
        #     if self.bodyweight_assessed_bird < 0:
        #         raise ValueError\
        #         ('self.bodyweight_assessed_bird=%g is a non-physical value.' % self.bodyweight_assessed_bird)
        
        # self.fw_bird_out = (1.180 * (self.bodyweight_assessed_bird**0.874))/1000.0
        """
        Using fixed value to correctly handle floating point decimals as compared to spreadsheet implementation
        """
        self.fw_bird_out = 0.0162
        return self.fw_bird_out

    # Daily water intake rate for mammals
    @timefn
    def fw_mamm(self):
        """
        For mammals, the daily water intake rate is calculated using the equation below. 
        This equation is representative of eutherian herbivore mammals, which have higher 
        daily water flux requirements compared to other mammals that visit agricultural areas. 
        The only equation that would generate higher estimates of daily water flux corresponds 
        to marsupial carnivores, which are not considered to be representative of the majority 
        of mammals that visit agricultural areas.  The resulting daily water intake rate for a 
        1000 g mammal is 0.172 L. 

            Flux(water) = (0.708 * BW^0.795) / 1000

            where: BW = 1000 g
        """
        # if self.fw_mamm_out == -1:
        #     try:
        #         self.bodyweight_assessed_mammal = float(self.bodyweight_assessed_mammal)
        #     except IndexError:
        #         raise IndexError\
        #         ('The body weight of the mammal must be supplied on the command line.')
        #     except ValueError:
        #         raise ValueError\
        #         ('The body weight of the mammal must be a real number, not "%g"' % self.bodyweight_assessed_mammal)
        #     if self.bodyweight_assessed_mammal < 0:
        #         raise ValueError\
        #         ('self.bodyweight_assessed_mammal=%g is a non-physical value.' % self.bodyweight_assessed_mammal)
        
        # self.fw_mamm_out = (0.708 * (self.bodyweight_assessed_mammal**0.795))/1000.0
        """
        Using fixed value to correctly handle floating point decimals as compared to spreadsheet implementation
        """
        self.fw_mamm_out = 0.172
        return self.fw_mamm_out

    # Upper bound estimate of exposure for birds
    @timefn
    def dose_bird(self):
        """
        The model calculates the upper bound estimate of exposure in drinking water 
        (dose-based; units in mg/kg-bw) by multiplying the daily water intake rate (L) 
        by the chemical solubility (mg/L) and then dividing by the body weight (in kg) 
        of the assessed animal (See equation below). In cases where water characteristics 
        (e.g., pH) influence the solubility of a chemical in water, the user should select 
        the highest available water solubility for use in SIP.

            Dose = (Flux(water) * solubility) / BW

            where: BW = body weight (kg) of the assessed bird (e.g. mallard duck, bobtail quail, other)
        """
        # if self.dose_bird_out == -1:
        #     try:
        #         self.fw_bird_out = float(self.fw_bird_out)
        #         self.solubility = float(self.solubility)
        #         self.bodyweight_assessed_bird = float(self.bodyweight_assessed_bird)
        #     except IndexError:
        #         raise IndexError\
        #         ('The daily water intake for birds, chemical solubility, and/or'\
        #         ' the body weight of the bird must be supplied on the command line.')
        #     except ValueError:
        #         raise ValueError\
        #         ('The daily water intake for birds must be a real number, '\
        #         'not "%L"' %self.fw_bird)
        #     except ValueError:
        #         raise ValueError\
        #         ('The chemical solubility must be a real number, not "%mg/L"' %self.solubility)
        #     except ValueError:
        #         raise ValueError\
        #         ('The body weight of the bird must be a real number, not "%g"' %self.bodyweight_assessed_bird)
        #     except ZeroDivisionError:
        #         raise ZeroDivisionError\
        #         ('The body weight of the bird must non-zero.')
        #     if self.fw_bird_out < 0:
        #         raise ValueError\
        #         ('fw_bird=%g is a non-physical value.' % self.fw_bird_out)
        #     if self.solubility < 0:
        #         raise ValueError\
        #         ('solubility=%g is a non-physical value.' % self.solubility)
        #     if self.bodyweight_assessed_bird < 0:
        #         raise ValueError\
        #         ('self.bodyweight_assessed_bird=%g is a non-physical value.' % self.bodyweight_assessed_bird)
        self.dose_bird_out = (self.fw_bird_out * self.solubility)/(self.bodyweight_assessed_bird / 1000.)
        return self.dose_bird_out


    # Upper bound estimate of exposure for mammals
    @timefn
    def dose_mamm(self):
        """
        The model calculates the upper bound estimate of exposure in drinking water 
        (dose-based; units in mg/kg-bw) by multiplying the daily water intake rate (L) 
        by the chemical solubility (mg/L) and then dividing by the body weight (in kg) 
        of the assessed animal (See equation below). In cases where water characteristics 
        (e.g., pH) influence the solubility of a chemical in water, the user should select 
        the highest available water solubility for use in SIP.

            Dose = (Flux(water) * solubility) / BW

            where: BW = body weight (kg) of the assessed animal (e.g. laboratory rat, other)
        """
        # if self.dose_mamm_out == -1:
        #     try:
        #         self.fw_mamm_out = float(self.fw_mamm_out)
        #         self.solubility = float(self.solubility)
        #         self.bodyweight_assessed_mammal = float(self.bodyweight_assessed_mammal)
        #     except IndexError:
        #         raise IndexError\
        #         ('The daily water intake for mammals, chemical solubility, and/or'\
        #         ' the body weight of the mammal must be supplied on the command line.')
        #     except ValueError:
        #         raise ValueError\
        #         ('The daily water intake for mammals must be a real number, '\
        #         'not "%L"' %self.fw_mamm)
        #     except ValueError:
        #         raise ValueError\
        #         ('The chemical solubility must be a real number, not "%mg/L"' %self.solubility)
        #     except ValueError:
        #         raise ValueError\
        #         ('The body weight of the mammal must be a real number, not "%g"' %self.bodyweight_assessed_mammal)
        #     except ZeroDivisionError:
        #         raise ZeroDivisionError\
        #         ('The body weight of the mammal must non-zero.')
        #     if self.fw_bird_out < 0:
        #         raise ValueError\
        #         ('fw_mamm=%g is a non-physical value.' % self.fw_mamm_out)
        #     if self.solubility < 0:
        #         raise ValueError\
        #         ('solubility=%g is a non-physical value.' % self.solubility)
        #     if self.bodyweight_assessed_mammal < 0:
        #         raise ValueError\
        #         ('self.bodyweight_assessed_mammal=%g is a non-physical value.' % self.bodyweight_assessed_mammal)
        self.dose_mamm_out = (self.fw_mamm_out * self.solubility)/(self.bodyweight_assessed_mammal / 1000.)
        return self.dose_mamm_out

    # Acute adjusted toxicity value for birds
    @timefn
    def at_bird(self):
        """
        LD50 values for mammals and birds are adjusted using the same approach employed 
        by T-REX (USEPA 2008). These equations are provided below. In these equations, 
        AT = adjusted toxicity value (mg/kg-bw); LD50 = endpoint reported by toxicity study 
        (mg/kg-bw); TW = body weight of tested animal (350g rat, 1580g mallard duck, 178 g 
        Northern bobwhite quail or weight defined by the model user for an alternative species); 

        AT = LD50* (AW / TW)^(x-1)

        where: 
            AW = body weight of assessed animal (g)
            x = Mineau scaling factor.  Chemical specific values for x may be located in the 
            worksheet titled "Mineau scaling factors." If no chemical specific data are available, 
            the default value of 1.15 should be used for this parameter. 
        """
        # if self.at_bird_out == -1:
        #     try:
        #         self.ld50_avian_water = float(self.ld50_avian_water)
        #         self.bodyweight_assessed_bird = float(self.bodyweight_assessed_bird)
        #         self.bodyweight_tested_bird = float(self.bodyweight_tested_bird)
        #         self.mineau_scaling_factor = float(self.mineau_scaling_factor)
        #     except IndexError:
        #         raise IndexError\
        #         ('The lethal dose, body weight of assessed bird, body weight'\
        #         ' of tested bird, and/or the mineau_scaling_factor scaling factor must be'\
        #         'supplied the command line.')
        #     except ValueError:
        #         raise ValueError\
        #         ('The mineau_scaling_factor scaling factor must be a real number' %self.mineau_scaling_factor)
        #     except ValueError:
        #         raise ValueError\
        #         ('The lethal dose must be a real number, not "%mg/kg"' %self.ld50_avian_water)
        #     except ValueError:
        #         raise ValueError\
        #         ('The body weight of assessed bird must be a real number, not "%g"' %self.bodyweight_assessed_bird)
        #     except ValueError:
        #         raise ValueError\
        #         ('The body weight of tested bird must be a real number, not "%g"' %self.bodyweight_tested_bird)
        #     except ZeroDivisionError:
        #         raise ZeroDivisionError\
        #         ('The body weight of tested bird must be non-zero.')
        #     if self.ld50_avian_water < 0:
        #         raise ValueError\
        #         ('ld50_avian_water=%g is a non-physical value.' % self.ld50_avian_water)
        #     if self.bodyweight_assessed_bird < 0:
        #         raise ValueError\
        #         ('bodyweight_assessed_bird=%g is a non-physical value.' % self.bodyweight_assessed_bird)
        #     if self.bodyweight_tested_bird < 0:
        #         raise ValueError\
        #         ('bodyweight_tested_bird=%g is a non-physical value.' % self.bodyweight_tested_bird)
        logging.info(self.bodyweight_tested_bird)
        self.at_bird_out = (self.ld50_avian_water) * ((self.bodyweight_assessed_bird / self.bodyweight_tested_bird)**(self.mineau_scaling_factor - 1.))
        return self.at_bird_out

    # Acute adjusted toxicity value for mammals
    @timefn
    def at_mamm(self):
        """
        LD50 values for mammals and birds are adjusted using the same approach employed 
        by T-REX (USEPA 2008). These equations are provided below. In these equations, 
        AT = adjusted toxicity value (mg/kg-bw); LD50 = endpoint reported by toxicity study 
        (mg/kg-bw); TW = body weight of tested animal (350g rat, 1580g mallard duck, 178 g 
        Northern bobwhite quail or weight defined by the model user for an alternative species); 

        AT = LD50* (TW / AW)^0.25

        where: 
            AW = body weight of assessed animal (g)
            x = Mineau scaling factor.  Chemical specific values for x may be located in the 
            worksheet titled "Mineau scaling factors." If no chemical specific data are available, 
            the default value of 1.15 should be used for this parameter. 
        """
        # if self.at_mamm_out == -1:
        #     try:
        #         self.ld50_mammal_water = float(self.ld50_mammal_water)
        #         self.bodyweight_assessed_mammal = float(self.bodyweight_assessed_mammal)
        #         self.bodyweight_tested_mammal = float(self.bodyweight_tested_mammal)
        #     except TypeError:
        #         raise TypeError\
        #         ('Either ld50_mammal_water, bodyweight_assessed_mammal or bodyweight_tested_mammal equals None and therefor this function cannot be run.')
        #     except IndexError:
        #         raise IndexError\
        #         ('The lethal dose, body weight of assessed mammal, and/or body weight'\
        #         ' of tested mammal, must be supplied the command line.')
        #     except ValueError:
        #         raise ValueError\
        #         ('The lethal dose must be a real number, not "%mg/kg"' %self.ld50_mammal_water)
        #     except ValueError:
        #         raise ValueError\
        #         ('The body weight of assessed mammal must be a real number, not "%g"' %self.bodyweight_assessed_mammal)
        #     except ValueError:
        #         raise ValueError\
        #         ('The body weight of tested mammal must be a real number, not "%g"' %self.bodyweight_tested_mammal)
        #     except ZeroDivisionError:
        #         raise ZeroDivisionError\
        #         ('The body weight of tested mammal must be non-zero.')
        #     if self.ld50_mammal_water < 0:
        #         raise ValueError\
        #         ('ld50_mammal_water=%g is a non-physical value.' % self.ld50_mammal_water)
        #     if self.bodyweight_assessed_mammal < 0:
        #         raise ValueError\
        #         ('bodyweight_assessed_mammal=%g is a non-physical value.' % self.bodyweight_assessed_mammal)
        #     if self.bodyweight_tested_mammal < 0:
        #         raise ValueError\
        #         ('bodyweight_tested_mammal=%g is a non-physical value.' % self.bodyweight_tested_mammal)
        self.at_mamm_out = (self.ld50_mammal_water) * ((self.bodyweight_tested_mammal / self.bodyweight_assessed_mammal)**0.25)
        return self.at_mamm_out


    # Adjusted chronic toxicity values for birds

    # FI = Food Intake Rate
    @timefn
    def fi_bird(self, bw_grams):
        """
        Daily Food Intake Rate:

        Chronic avian toxicity studies produce endpoints based on concentration in food, not dose. 
        The endpoint is a No Observed Adverse Effects Concentration (NOAEC) that is assumed to be 
        relevant to all birds, regardless of body weight.  In order to convert a reported avian 
        NOAEC (mg/kg-diet) value to a dose equivalent toxicity value for the assessed animal, 
        the daily food (dry) intake of the test bird is considered. The daily food intake rate 
        (FI; units in kg-food) of the test bird is calculated using the equation below.

        FI = 0.0582 * BW^0.651

        where:
            BW = body weight in kg (USEPA 1993). This equation corresponds to a daily food intake 
            rate for all birds, which generates a lower food intake rate compared to passerines. 
            The equation is more conservative because it results in a lower dose-equivalent toxicity value. 
        """
        # if self.fi_bird_out == -1:
        #     try:
        #         self.bodyweight_tested_bird = float(self.bodyweight_tested_bird)
        #     except IndexError:
        #         raise IndexError\
        #         ('The body weight of the bird must be supplied the command line.')
        #     except ValueError:
        #         raise ValueError\
        #         ('The body weight must be a real number, not "%kg"' %self.bodyweight_tested_bird)
        #     if self.bodyweight_tested_bird < 0:
        #         raise ValueError\
        #         ('self.bodyweight_tested_bird=%g is a non-physical value.' % self.bodyweight_tested_bird)
        self.fi_bird_out = 0.0582 * ((bw_grams / 1000.)**0.651)
        return self.fi_bird_out

    # Dose-equivalent chronic toxicity value for birds
    @timefn
    def det(self):
        """
        Dose Equiv. Toxicity:

        The FI value (kg-diet) is multiplied by the reported NOAEC (mg/kg-diet) and then divided by 
        the test animal's body weight to derive the dose-equivalent chronic toxicity value (mg/kg-bw):

        Dose Equiv. Toxicity = (NOAEC * FI) / BW

        NOTE: The user enters the lowest available NOAEC for the mallard duck, for the bobwhite quail, 
        and for any other test species. The model calculates the dose equivalent toxicity values for 
        all of the modeled values (Cells F20-24 and results worksheet) and then selects the lowest dose 
        equivalent toxicity value to represent the chronic toxicity of the chemical to birds.
        """
        # if self.det_out == -1:
        #     try:
        #         self.noael_avian_water = float(self.noael_avian_water)
        #         self.fi_bird_out = float(self.fi_bird_out)
        #         self.bodyweight_tested_bird = float(self.bodyweight_tested_bird)
        #     except IndexError:
        #         raise IndexError\
        #         ('The no observed adverse effects concentration, daily food intake'\
        #         ' rate for birds, and/or body weight of the bird must be supplied the'\
        #         ' command line.')
        #     except ValueError:
        #         raise ValueError\
        #         ('The NOAEC must be a real number, not "%mg/kg"' % self.noael_avian_water)
        #     except ValueError:
        #         raise ValueError\
        #         ('The dialy food intake rate for birds must be a real number,'\
        #         ' not "%kg"' % self.fi_bird_out)
        #     except ValueError:
        #         raise ValueError\
        #         ('The body weight of the bird must be a real number, not "%kg"' % self.bodyweight_tested_bird)
        #     except ZeroDivisionError:
        #         raise ZeroDivisionError\
        #         ('The body weight of the bird must be non-zero.')
        #     if self.noael_avian_water < 0:
        #         raise ValueError\
        #         ('noael_avian_water=%g is a non-physical value.' % self.noael_avian_water)
        #     if self.fi_bird_out < 0:
        #         raise ValueError\
        #         ('fi_bird=%g is a non-physical value.' % self.fi_bird_out)
        #     if self.bodyweight_tested_bird < 0:
        #         raise ValueError\
        #         ('self.bodyweight_tested_bird=%g is a non-physical value.' % self.bodyweight_tested_bird)


        # Create method Series for each potential NOAEC value
        det_quail = pd.Series(name="det_quail")
        det_duck = pd.Series(name="det_duck")
        det_other_1 = pd.Series(name="det_other_1")
        det_other_2 = pd.Series(name="det_other_2")

        try:
            # Body weight of bobtail quail is 178 g
            det_quail = (self.noaec_quail * self.fi_bird(178.)) / (178. / 1000.)    
        except:
            det_quail = None

        try:
            # Body weight of mallard duck is 1580 g
            det_duck = (self.noaec_duck * self.fi_bird(1580.)) / (1580. / 1000.)           
        except:
            det_duck = None

        try:
            det_other_1 = (self.noaec_bird_other_1 * self.fi_bird(self.bodyweight_bird_other_1)) / (self.bodyweight_bird_other_1 / 1000.)           
        except:
            det_other_1 = None

        try:
            det_other_2 = (self.noaec_bird_other_2 * self.fi_bird(self.bodyweight_bird_other_1)) / (self.bodyweight_bird_other_1 / 1000.)           
        except:
            det_other_2 = None

        # Create DataFrame containing method Series created above
        df_noaec = pd.DataFrame({
            'det_quail' : det_quail,
            'det_duck' : det_duck,
            'det_other_1' : det_other_1,
            'det_other_2' : det_other_2
        })

        # Create a Series of the minimum values for each row/model run of the above DataFrame
        self.det_out = df_noaec.min(axis=1, numeric_only=True)

        logging.info(df_noaec)
        logging.info(self.det_out)
        return self.det_out

    # Adjusted chronic toxicty value for mammals
    @timefn
    def act(self):
        """
        SIP relies upon the No Observed Adverse Effects Level (NOAEL; mg/kg-bw) from a chronic mammalian study. 
        If only a NOAEC value (in mg/kg-diet) is available, the model user should divide the NOAEC by 20 to 
        determine the equivalent chronic daily dose. This approach is consistent with that of T-REX, which 
        relies upon the standard FDA lab rat conversion. (USEPA 2008). Mammalian NOAEL values are adjusted 
        using the same approach employed by T-REX (USEPA 2008). The equation for mammals is provided below 
        (variables are defined above). 

        AT = NOAEL * (TW / AW)^0.25
        """
        # if self.act_out == -1:
        #     try:
        #         self.noael_mammal_water = float(self.noael_mammal_water)
        #         self.bodyweight_tested_mammal = float(self.bodyweight_tested_mammal)
        #         self.bodyweight_assessed_mammal = float(self.bodyweight_assessed_mammal)
        #     except IndexError:
        #         raise IndexError\
        #         ('The no observed adverse effects level, body weight of the tested'\
        #         ' mammal, and/or body weight of assessed mammal must be supplied the'\
        #         ' command line.')
        #     except ValueError:
        #         raise ValueError\
        #         ('The NOAEL must be a real number, not "%mg/kg"' % self.noael_mammal_water)
        #     except ValueError:
        #         raise ValueError\
        #         ('The body weight of the tested mammal must be a real number,'\
        #         ' not "%kg"' % self.bodyweight_tested_mammal)
        #     except ValueError:
        #         raise ValueError\
        #         ('The body weight of the assessed mammal must be a real number,'\
        #         ' not "%kg"' % self.bodyweight_assessed_mammal)
        #     except ZeroDivisionError:
        #         raise ZeroDivisionError\
        #         ('The body weight of the assessed mammal must be non-zero.')
        #     if self.noael_mammal_water < 0:
        #         raise ValueError\
        #         ('noael_mammal_water=%g is a non-physical value.' % self.noael_mammal_water)
        #     if self.bodyweight_tested_mammal < 0:
        #         raise ValueError\
        #         ('bodyweight_tested_mammal=%g is a non-physical value.' % self.bodyweight_tested_mammal)
        #     if self.bodyweight_assessed_mammal < 0:
        #         raise ValueError\
        #         ('bodyweight_assessed_mammal=%g is a non-physical value.' % self.bodyweight_assessed_mammal)
        self.act_out = (self.noael_mammal_water) * ((self.bodyweight_tested_mammal / self.bodyweight_assessed_mammal)**0.25)
        return self.act_out
        #   MAMMILIAN:  If only a NOAEC value (in mg/kg-diet) is available, the model user should divide the NOAEC by 20 to determine the equivalent chronic daily dose (NOAEL)
    # ---- Is drinking water a concern?

    # Acute exposures for birds

    @timefn
    def acute_bird(self):
        """
        For acute exposures, if the ratio of the upper bound dose to the adjusted LD50 value is <0.1, 
        the risk assessor can conclude that pesticide exposure to mammals or birds through drinking 
        water by itself is not an exposure route of concern. If the ratio of the upper bound dose to 
        the adjusted LD50 value is ≥ 0.1, the risk assessor can conclude that pesticide exposure to 
        mammals or birds through drinking water by itself is an exposure route of concern.
        """
        # if self.acute_bird_out == -1:
        #     try:
        #         self.dose_bird_out = float(self.dose_bird_out)
        #         self.at_bird_out = float(self.at_bird_out)
        #     except IndexError:
        #         raise IndexError\
        #         ('The upper bound estimate of exposure for birds, and/or the adjusted'\
        #         ' toxicity value for birds must be supplied the command line.')
        #     except ValueError:
        #         raise ValueError\
        #         ('The upper bound estimate of exposure for birds must be a real'\
        #         ' number, not "%mg/kg"' % self.dose_bird_out)
        #     except ValueError:
        #         raise ValueError\
        #         ('The adjusted toxicity value for birds must be a real number,'\
        #         ' not "%mg/kg"' % self.at_bird_out)
        #     except ZeroDivisionError:
        #         raise ZeroDivisionError\
        #         ('The adjusted toxicity value for birds must be non-zero.')
        #     if self.dose_bird_out < 0:
        #         raise ValueError\
        #         ('dose_bird=%g is a non-physical value.' % self.dose_bird_out)
        #     if self.at_bird_out < 0:
        #         raise ValueError\
        #         ('at_bird=%g is a non-physical value.' % self.at_bird_out)
        self.acute_bird_out = self.dose_bird_out / self.at_bird_out
        return self.acute_bird_out

    @timefn
    def acuconb(self):
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
        boolean = self.acute_bird_out < 0.1
        self.acuconb_out = boolean.map(lambda x: 
            'Drinking water exposure alone is NOT a potential concern for birds' if x == True 
            else 'Exposure through drinking water alone is a potential concern for birds')
             
        return self.acuconb_out

    # Acute exposures for mammals
    @timefn
    def acute_mamm(self):
        """
        For acute exposures, if the ratio of the upper bound dose to the adjusted LD50 value is <0.1, 
        the risk assessor can conclude that pesticide exposure to mammals or birds through drinking 
        water by itself is not an exposure route of concern. If the ratio of the upper bound dose to 
        the adjusted LD50 value is ≥ 0.1, the risk assessor can conclude that pesticide exposure to 
        mammals or birds through drinking water by itself is an exposure route of concern.
        """
        # if self.acute_mamm_out == -1:
        #     try:
        #         self.dose_mamm_out = float(self.dose_mamm_out)
        #         self.at_mamm_out = float(self.at_mamm_out)
        #     except IndexError:
        #         raise IndexError\
        #         ('The upper bound estimate of exposure for mammals, and/or the adjusted'\
        #         ' toxicity value for mammals must be supplied the command line.')
        #     except ValueError:
        #         raise ValueError\
        #         ('The upper bound estimate of exposure for mammals must be a real'\
        #         ' number, not "%mg/kg"' % self.dose_mamm_out)
        #     except ValueError:
        #         raise ValueError\
        #         ('The adjusted toxicity value for mammals must be a real number,'\
        #         ' not "%mg/kg"' % self.at_mamm_out)
        #     except ZeroDivisionError:
        #         raise ZeroDivisionError\
        #         ('The adjusted toxicity value for mammals must be non-zero.')
        #     if self.dose_mamm_out < 0:
        #         raise ValueError\
        #         ('dose_mamm=%g is a non-physical value.' % self.dose_mamm_out)
        #     if self.at_mamm_out < 0:
        #         raise ValueError\
        #         ('at_mamm=%g is a non-physical value.' % self.at_mamm_out)
        self.acute_mamm_out = self.dose_mamm_out / self.at_mamm_out
        return self.acute_mamm_out

    @timefn
    def acuconm(self):
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
        boolean = self.acute_mamm_out < 0.1
        self.acuconm_out = boolean.map(lambda x: 
            'Drinking water exposure alone is NOT a potential concern for mammals' if x == True 
            else 'Exposure through drinking water alone is a potential concern for mammals')
        return self.acuconm_out

    # Chronic Exposures for birds
    @timefn
    def chron_bird(self):
        """
        For chronic exposures, if the ratio of the upper bound dose to the adjusted chronic 
        toxicity value is <1, the risk assessor can conclude that pesticide exposure to mammals 
        or birds through drinking water by itself is not an exposure route of concern. If the 
        ratio of the upper bound dose to the adjusted chronic toxicity value is ≥1, the risk 
        assessor can conclude that pesticide exposure to mammals or birds through drinking water 
        by itself is an exposure route of concern.
        """
        # if self.chron_bird_out == -1:
        #     try:
        #         self.dose_bird_out = float(self.dose_bird_out)
        #         self.det_out = float(self.det_out)
        #     except TypeError:
        #         raise TypeError\
        #         ('Either dose_bird or det equals None and therefor this function cannot be run.')
        #     except IndexError:
        #         raise IndexError\
        #         ('The upper bound estimate of exposure for birds, and/or the dose-'\
        #         'equivalent chronic toxicity value for birds must be supplied the'\
        #         ' command line.')
        #     except ValueError:
        #         raise ValueError\
        #         ('The upper bound estimate of exposure for birds must be a real'\
        #         ' number, not "%mg/kg"' % self.dose_bird_out)
        #     except ValueError:
        #         raise ValueError\
        #         ('The dose-equivalent chronic toxicity value for birds must be a real'\
        #         ' number, not "%mg/kg"' % self.det_out)
        #     except ZeroDivisionError:
        #         raise ZeroDivisionError\
        #         ('The dose-equivalent chronic toxicity value for birds must be non-zero.')
        #     if self.dose_bird_out < 0:
        #         raise ValueError\
        #         ('dose_bird=%g is a non-physical value.' % self.dose_bird_out)
        #     if self.det_out < 0:
        #         raise ValueError\
        #         ('det=%g is a non-physical value.' % self.det_out)
        self.chron_bird_out = self.dose_bird_out / self.det_out
        return self.chron_bird_out

    @timefn
    def chronconb(self):
        """
        Message stating whether or not a risk is present
        """
        # if self.chronconb_out == -1:
        #     if self.chron_bird_out == None:
        #         raise ValueError\
        #         ('chron_bird variable equals None and therefor this function cannot be run.')
        #     if self.chron_bird_out < 1:
        #         self.chronconb_out = ('Drinking water exposure alone is NOT a potential concern for birds')
        #     else:
        #         self.chronconb_out = ('Exposure through drinking water alone is a potential concern for birds')
        boolean = self.chron_bird_out < 1
        self.chronconb_out = boolean.map(lambda x: 
            'Drinking water exposure alone is NOT a potential concern for birds' if x == True 
            else 'Exposure through drinking water alone is a potential concern for birds')
        return self.chronconb_out

    # Chronic exposures for mammals
    @timefn
    def chron_mamm(self):
        """
        For chronic exposures, if the ratio of the upper bound dose to the adjusted chronic 
        toxicity value is <1, the risk assessor can conclude that pesticide exposure to mammals 
        or birds through drinking water by itself is not an exposure route of concern. If the 
        ratio of the upper bound dose to the adjusted chronic toxicity value is ≥1, the risk 
        assessor can conclude that pesticide exposure to mammals or birds through drinking water 
        by itself is an exposure route of concern.
        """
        # if self.chron_mamm_out == -1:
        #     try:
        #         self.dose_mamm_out = float(self.dose_mamm_out)
        #         self.act_out = float(self.act_out)
        #     except IndexError:
        #         raise IndexError\
        #         ('The upper bound estimate of exposure for mammals, and/or the'\
        #         ' adjusted chronic toxicity value for mammals must be supplied the'\
        #         ' command line.')
        #     except ValueError:
        #         raise ValueError\
        #         ('The upper bound estimate of exposure for mammals must be a real'\
        #         ' number, not "%mg/kg"' % self.dose_mamm_out)
        #     except ValueError:
        #         raise ValueError\
        #         ('The adjusted chronic toxicity value for mammals must be a real'\
        #         ' number, not "%mg/kg"' % self.act_out)
        #     except ZeroDivisionError:
        #         raise ZeroDivisionError\
        #         ('The adjusted chronic toxicity value for mammals must be non-zero.')
        #     if self.dose_mamm_out < 0:
        #         raise ValueError\
        #         ('dose_mamm=%g is a non-physical value.' % self.dose_mamm_out)
        #     if self.act_out < 0:
        #         raise ValueError\
        #         ('act=%g is a non-physical value.' % self.act_out)
        self.chron_mamm_out = self.dose_mamm_out / self.act_out
        return self.chron_mamm_out
    @timefn
    def chronconm(self):
        """
        Message stating whether or not a risk is present
        """
        # if self.chronconm_out == -1:
        #     if self.chron_mamm_out == None:
        #         raise ValueError\
        #         ('chron_mamm variable equals None and therefor this function cannot be run.')
        #     if self.chron_mamm_out < 1:
        #         self.chronconm_out = ('Drinking water exposure alone is NOT a potential concern for mammals')
        #     else:
        #         self.chronconm_out = ('Exposure through drinking water alone is a potential concern for mammals')
        boolean = self.chron_mamm_out < 1
        self.chronconm_out = boolean.map(lambda x: 
            'Drinking water exposure alone is NOT a potential concern for mammals' if x == True 
            else 'Exposure through drinking water alone is a potential concern for mammals')
        return self.chronconm_out
