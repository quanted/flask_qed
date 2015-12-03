# -*- coding: utf-8 -*-
from __future__ import division
import pandas as pd
import logging


class terrplant(object):
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
        logging.info("1")
        self.populate_input_properties()
        logging.info("2")
        self.create_output_properties()
        logging.info("3")
        self.run_methods()
        logging.info("4")
        self.create_output_dataframe()
        # Callable from Bottle that returns JSON
        logging.info("5")
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

    # Begin model methods
    def run_methods(self):
        try:
            self.rundry()
            self.runsemi()
            self.spray()
            self.totaldry()
            self.totalsemi()
            self.minnmsspray()
            self.minlmsspray()
            self.minndsspray()
            self.minldsspray()
            self.nmsRQdry()
            self.LOCnmsdry()
            self.nmsRQsemi()
            self.LOCnmssemi()
            self.nmsRQspray()
            self.LOCnmsspray()
            self.lmsRQdry()
            self.LOClmsdry()
            self.lmsRQsemi()
            self.LOClmssemi()
            self.lmsRQspray()
            self.LOClmsspray()
            self.ndsRQdry()
            self.LOCndsdry()
            self.ndsRQsemi()
            self.LOCndssemi()
            self.ndsRQspray()
            self.LOCndsspray()
            self.ldsRQdry()
            self.LOCldsdry()
            self.ldsRQsemi()
            self.LOCldssemi()
            self.ldsRQspray()
            self.LOCldsspray()
        except TypeError:
            print "Type Error: Your variables are not set correctly."

    def create_output_dataframe(self):
        # Create DataFrame containing output value Series
        pd_obj_out = pd.DataFrame({
            "out_rundry": self.out_rundry,
            "out_runsemi": self.out_runsemi,
            "out_totaldry": self.out_totaldry,
            "out_totalsemi": self.out_totalsemi,
            "out_spray": self.out_spray,
            "out_min_nms_spray": self.out_min_nms_spray,
            "out_min_lms_spray": self.out_min_lms_spray,
            "out_min_nds_spray": self.out_min_nds_spray,
            "out_min_lds_spray": self.out_min_lds_spray,
            "out_nms_rq_dry": self.out_nms_rq_dry,
            "out_nms_loc_dry": self.out_nms_loc_dry,
            "out_nms_rq_semi": self.out_nms_rq_semi,
            "out_nms_loc_semi": self.out_nms_loc_semi,
            "out_nms_rq_spray": self.out_nms_rq_spray,
            "out_nms_loc_spray": self.out_nms_loc_spray,
            "out_lms_rq_dry": self.out_lms_rq_dry,
            "out_lms_loc_dry": self.out_lms_loc_dry,
            "out_lms_rq_semi": self.out_lms_rq_semi,
            "out_lms_loc_semi": self.out_lms_loc_semi,
            "out_lms_rq_spray": self.out_lms_rq_spray,
            "out_lms_loc_spray": self.out_lms_loc_spray,
            "out_nds_rq_dry": self.out_nds_rq_dry,
            "out_nds_loc_dry": self.out_nds_loc_dry,
            "out_nds_rq_semi": self.out_nds_rq_semi,
            "out_nds_loc_semi": self.out_nds_loc_semi,
            "out_nds_rq_spray": self.out_nds_rq_spray,
            "out_nds_loc_spray": self.out_nds_loc_spray,
            "out_lds_rq_dry": self.out_lds_rq_dry,
            "out_lds_loc_dry": self.out_lds_loc_dry,
            "out_lds_rq_semi": self.out_lds_rq_semi,
            "out_lds_loc_semi": self.out_lds_loc_semi,
            "out_lds_rq_spray": self.out_lds_rq_spray,
            "out_lds_loc_spray": self.out_lds_loc_spray
        })

        # create pandas properties for acceptance testing
        logging.info("here is the output object")
        logging.info(pd_obj_out)
        self.pd_obj_out = pd_obj_out

    def create_output_properties(self):
        # Outputs: Assign object attribute variables to Pandas Series
        self.out_rundry = pd.Series(name="out_rundry")
        self.out_runsemi = pd.Series(name="out_runsemi")
        self.out_totaldry = pd.Series(name="out_totaldry")
        self.out_totalsemi = pd.Series(name="out_totalsemi")
        self.out_spray = pd.Series(name="out_spray")
        self.out_min_nms_spray = pd.Series(name="out_min_nms_spray")
        self.out_min_lms_spray = pd.Series(name="out_min_lms_spray")
        self.out_min_nds_spray = pd.Series(name="out_min_nds_spray")
        self.out_min_lds_spray = pd.Series(name="out_min_lds_spray")
        self.out_nms_rq_dry = pd.Series(name="out_nms_rq_dry")
        self.out_nms_loc_dry = pd.Series(name="out_nms_loc_dry")
        self.out_nms_rq_semi = pd.Series(name="out_nms_rq_semi")
        self.out_nms_loc_semi = pd.Series(name="out_nms_loc_semi")
        self.out_nms_rq_spray = pd.Series(name="out_nms_rq_spray")
        self.out_nms_loc_spray = pd.Series(name="out_nms_loc_spray")
        self.out_lms_rq_dry = pd.Series(name="out_lms_rq_dry")
        self.out_lms_loc_dry = pd.Series(name="out_lms_loc_dry")
        self.out_lms_rq_semi = pd.Series(name="out_lms_rq_semi")
        self.out_lms_loc_semi = pd.Series(name="out_lms_loc_semi")
        self.out_lms_rq_spray = pd.Series(name="out_lms_rq_spray")
        self.out_lms_loc_spray = pd.Series(name="out_lms_loc_spray")
        self.out_nds_rq_dry = pd.Series(name="out_nds_rq_dry")
        self.out_nds_loc_dry = pd.Series(name="out_nds_loc_dry")
        self.out_nds_rq_semi = pd.Series(name="out_nds_rq_semi")
        self.out_nds_loc_semi = pd.Series(name="out_nds_loc_semi")
        self.out_nds_rq_spray = pd.Series(name="out_nds_rq_spray")
        self.out_nds_loc_spray = pd.Series(name="out_nds_loc_spray")
        self.out_lds_rq_dry = pd.Series(name="out_lds_rq_dry")
        self.out_lds_loc_dry = pd.Series(name="out_lds_loc_dry")
        self.out_lds_rq_semi = pd.Series(name="out_lds_rq_semi")
        self.out_lds_loc_semi = pd.Series(name="out_lds_loc_semi")
        self.out_lds_rq_spray = pd.Series(name="out_lds_rq_spray")
        self.out_lds_loc_spray = pd.Series(name="out_lds_loc_spray")

    def populate_input_properties(self):
        # Inputs: Assign object attribute variables from the input Pandas Dataframe
        self.version_terrplant = self.pd_obj["version_terrplant"]
        self.application_rate = self.pd_obj["application_rate"]
        self.incorporation_depth = self.pd_obj["incorporation_depth"]
        self.runoff_fraction = self.pd_obj["runoff_fraction"]
        self.drift_fraction = self.pd_obj["drift_fraction"]
        self.chemical_name = self.pd_obj["chemical_name"]
        self.pc_code = self.pd_obj["pc_code"]
        self.use = self.pd_obj["use"]
        self.application_method = self.pd_obj["application_method"]
        self.application_form = self.pd_obj["application_form"]
        self.solubility = self.pd_obj["solubility"]
        self.ec25_nonlisted_seedling_emergence_monocot = self.pd_obj["ec25_nonlisted_seedling_emergence_monocot"]
        self.ec25_nonlisted_seedling_emergence_dicot = self.pd_obj["ec25_nonlisted_seedling_emergence_dicot"]
        self.noaec_listed_seedling_emergence_monocot = self.pd_obj["noaec_listed_seedling_emergence_monocot"]
        self.noaec_listed_seedling_emergence_dicot = self.pd_obj["noaec_listed_seedling_emergence_dicot"]
        self.ec25_nonlisted_vegetative_vigor_monocot = self.pd_obj["ec25_nonlisted_vegetative_vigor_monocot"]
        self.ec25_nonlisted_vegetative_vigor_dicot = self.pd_obj["ec25_nonlisted_vegetative_vigor_dicot"]
        self.noaec_listed_vegetative_vigor_monocot = self.pd_obj["noaec_listed_vegetative_vigor_monocot"]
        self.noaec_listed_vegetative_vigor_dicot = self.pd_obj["noaec_listed_vegetative_vigor_dicot"]

    # EEC for runoff for dry areas
    def rundry(self):
        # try:
        #     self.application_rate = float(self.application_rate)
        #     self.incorporation_depth = float(self.incorporation_depth)
        #     self.runoff_fraction = float(self.runoff_fraction)
        # except ZeroDivisionError:
        #     raise ZeroDivisionError\
        #     ('The incorporation_depth must be non-zero.')
        # except IndexError:
        #     raise IndexError\
        #     ('The application rate, incorporation_depth, and/or runoff fraction must be supplied on the command line. ')
        # except ValueError:
        #     raise ValueError\
        #     ('The application rate, incorporation_depth, and/or runoff fraction must be a real number')
        # except TypeError:
        #     raise TypeError\
        #     ('The application rate, incorporation_depth, and/or runoff fraction must be an integer or string')
        # if self.application_rate < 0:
        #     raise ValueError\
        #     ('application_rate must be positive.')
        # if self.incorporation_depth == 0:
        #     raise ZeroDivisionError\
        #     ('incorporation_depth must not equal zero.')
        # if self.incorporation_depth < 0:
        #     raise ValueError\
        #     ('incorporation_depth must be positive.')
        # if self.runoff_fraction < 0:
        #     raise ValueError\
        #     ('runoff_fraction must be positive.')
        # if self.out_rundry == -1:
        self.out_rundry = (self.application_rate / self.incorporation_depth) * self.runoff_fraction
        logging.info(self.out_rundry)
        return self.out_rundry

    # EEC for runoff to semi-aquatic areas
    def runsemi(self):
        # try:
        #     self.application_rate = float(self.application_rate)
        #     self.incorporation_depth = float(self.incorporation_depth)
        #     self.runoff_fraction = float(self.runoff_fraction)
        # except ZeroDivisionError:
        #     raise ZeroDivisionError\
        #     ('The incorporation_depth must be non-zero.')
        # except IndexError:
        #     raise IndexError\
        #     ('The application rate, incorporation_depth, and/or runoff fraction must be supplied on the command line. ')
        # except ValueError:
        #     raise ValueError\
        #     ('The application rate, incorporation_depth, and/or runoff fraction must be a real number')
        # if self.application_rate < 0:
        #     raise ValueError\
        #     ('application_rate must be positive.')
        # if self.incorporation_depth == 0:
        #     raise ZeroDivisionError\
        #     ('incorporation_depth must not equal zero.')
        # if self.incorporation_depth < 0:
        #     raise ValueError\
        #     ('incorporation_depth must be positive.')
        # if self.runoff_fraction < 0:
        #     raise ValueError\
        #     ('runoff_fraction must be positive.')
        # if self.out_runsemi == -1:
        self.out_runsemi = (self.application_rate / self.incorporation_depth) * self.runoff_fraction * 10
        logging.info("runsemi")
        logging.info(self.out_runsemi)
        return self.out_runsemi

    # EEC for spray drift
    def spray(self):
        # try:
        #     self.application_rate = float(self.application_rate)
        #     self.drift_fraction = float(self.drift_fraction)
        # except ZeroDivisionError:
        #     raise ZeroDivisionError\
        #     ('The incorporation_depth must be non-zero.')
        # except IndexError:
        #     raise IndexError\
        #     ('The application rate, incorporation_depth, and/or runoff fraction must be supplied on the command line. ')
        # except ValueError:
        #     raise ValueError\
        #     ('The application rate, incorporation_depth, and/or runoff fraction must be a real number')
        # if self.application_rate < 0:
        #     raise ValueError\
        #     ('application_rate must be positive.')
        # if self.drift_fraction < 0:
        #     raise ValueError\
        #     ('drift_fraction must be positive.')
        # if self.out_spray == -1:
        self.out_spray = self.application_rate * self.drift_fraction
        logging.info("spray")
        logging.info(self.out_spray)
        return self.out_spray

    # EEC total for dry areas
    def totaldry(self):
        # if self.out_totaldry == -1:
        #     try:
        #         if self.out_rundry == -1:
        #             self.rundry()
        #         if self.out_spray == -1:
        #             self.spray()
        #         if self.out_rundry == None or self.out_spray == None:
        #             raise ValueError\
        #             ('Either the rundry or spray variables equals None and therefor this function cannot be run.')
        self.out_totaldry = self.out_rundry + self.out_spray
        # except ZeroDivisionError:
        #     raise ZeroDivisionError\
        #     ('The incorporation_depth must be non-zero.')
        logging.info("totaldry")
        logging.info(self.out_totaldry)
        return self.out_totaldry

    # EEC total for semi-aquatic areas
    def totalsemi(self):
        # if self.out_totalsemi == -1:
        #     try:
        #         if self.out_runsemi == -1:
        #             self.runsemi()
        #         if self.out_spray == -1:
        #             self.spray()
        #         if self.out_runsemi == None or self.out_spray == None:
        #             raise ValueError\
        #             ('Either the runsemi or spray variables equals None and therefor this function cannot be run.')
        self.out_totalsemi = self.out_runsemi + self.out_spray
        # except ZeroDivisionError:
        #     raise ZeroDivisionError\
        #     ('The incorporation_depth must be non-zero.')
        logging.info("totalsemi")
        logging.info(self.out_totalsemi)
        return self.out_totalsemi

    # ec25 --> non-listed species
    # noaec --> listed species

    # ALL USER INPUTS

    # ec25 (Non-listed) Monocot Seedling (ec25_nonlisted_seedling_emergence_monocot)
    # noaec (Listed) Monocot Seedling (ec25_nonlisted_seedling_emergence_dicot)
    # ec25 (Non-listed) Dicot Seedling (noaec_listed_seedling_emergence_monocot)
    # noaec (Listed) Dicot Seedling (noaec_listed_seedling_emergence_dicot)
    # ec25 (Non-listed) Monocot Vegetative (ec25_nonlisted_vegetative_vigor_monocot)
    # noaec (Listed) Monocot Vegetative (ec25_nonlisted_vegetative_vigor_dicot)
    # ec25 (Non-listed) Dicot Vegetative (noaec_listed_vegetative_vigor_monocot)
    # noaec (Listed) Dicot Vegetative (noaec_listed_vegetative_vigor_dicot)


    # Risk Quotient for NON-LISTED MONOCOT seedlings exposed to Pesticide X in a DRY area

    def nmsRQdry(self):
        # if self.out_nms_rq_dry == -1:
        #     try:
        #         self.ec25_nonlisted_seedling_emergence_monocot = float(self.ec25_nonlisted_seedling_emergence_monocot)
        #         self.out_totaldry = float(self.out_totaldry)
        #     except ValueError:
        #         raise ValueError\
        #         ('The application rate, incorporation_depth, and/or runoff fraction must be a real number')
        #     except TypeError:
        #         raise TypeError\
        #         ('totaldry equals None and therefor this function cannot be run.')
        #     except IndexError:
        #         raise IndexError\
        #         ('The total amount of runoff and spray to semi-aquatic areas be supplied on the command line. ')
        #     except ZeroDivisionError:
        #         raise ZeroDivisionError\
        #         ('The incorporation_depth must be non-zero.')
        #     if self.ec25_nonlisted_seedling_emergence_monocot < 0:
        #         raise ValueError\
        #         ('ec25_nonlisted_seedling_emergence_monocot=%g is a non-physical value' %self.ec25_nonlisted_seedling_emergence_monocot)
        #     if self.out_totaldry == -1:
        #         self.totaldry()
        #     if self.out_totaldry == None:
        #         raise ValueError\
        #         ('Either the out_totaldry variable equals None and therefor this function cannot be run.')
        self.out_nms_rq_dry = self.out_totaldry / self.ec25_nonlisted_seedling_emergence_monocot
        logging.info("nmsRQdry")
        logging.info(self.out_nms_rq_dry)
        return self.out_nms_rq_dry

    # Level of concern for non-listed monocot seedlings exposed to pesticide X in a dry area

    def LOCnmsdry(self):
        # if self.out_nms_loc_dry == '':
        # try:
        #     if self.out_nms_rq_dry == -1:
        #         try:
        #             self.nmsRQdry()
        #         except TypeError:
        #             raise TypeError\
        #             ('totaldry equals None and therefor this function cannot be run.')
        # if self.out_nms_rq_dry == None:
        #     raise ValueError\
        #     ('nmsRQdry variable equals None and therefor this function cannot be run.')
        # elif self.out_nms_rq_dry >= 1.0:
        # if self.out_nms_rq_dry >= 1.0:
        #     self.out_nms_loc_dry = ('The risk quotient for non-listed monocot seedlings exposed to the pesticide via runoff to dry areas indicates a potential risk.')
        # else:
        #     self.out_nms_loc_dry = ('The risk quotient for non-listed monocot seedlings exposed to the pesticide via runoff to dry areas indicates that potential risk is minimal.')
        exceed_boolean = self.out_nms_rq_dry >= 1.0
        self.out_nms_loc_dry = exceed_boolean.map(lambda x:
                                                  'The risk quotient for non-listed monocot seedlings exposed to the pesticide via runoff to dry areas indicates a potential risk.' if x == True
                                                  else 'The risk quotient for non-listed monocot seedlings exposed to the pesticide via runoff to dry areas indicates that potential risk is minimal.')
        # except ZeroDivisionError:
        #     raise ZeroDivisionError\
        #     ('The incorporation_depth must be non-zero.')
        logging.info("LOCnmsdry")
        logging.info(self.out_nms_loc_dry)
        return self.out_nms_loc_dry

    # Risk Quotient for NON-LISTED MONOCOT seedlings exposed to Pesticide X in a SEMI-AQUATIC area

    def nmsRQsemi(self):
        # if self.out_nms_rq_semi == -1:
        #     try:
        #         self.ec25_nonlisted_seedling_emergence_monocot = float(self.ec25_nonlisted_seedling_emergence_monocot)
        #         self.out_totalsemi = float(self.out_totalsemi)
        #     except ValueError:
        #         raise ValueError\
        #         ('The application rate, incorporation_depth, and/or runoff fraction must be a real number')             
        #     except TypeError:
        #         raise TypeError\
        #         ('totaldry equals None and therefor this function cannot be run.')
        #     except IndexError:
        #         raise IndexError\
        #         ('The total amount of runoff and spray to semi-aquatic areas be supplied on the command line. ')
        #     except ZeroDivisionError:
        #         raise ZeroDivisionError\
        #         ('The incorporation_depth must be non-zero.')
        #     if self.ec25_nonlisted_seedling_emergence_monocot < 0:
        #         raise ValueError\
        #         ('ec25_nonlisted_seedling_emergence_monocot=%g is a non-physical value' %self.ec25_nonlisted_seedling_emergence_monocot)   
        #     if self.out_totalsemi == -1:
        #         self.totalsemi()
        #     if self.out_totalsemi == None:
        #         raise ValueError\
        #         ('Either the out_totaldry variable equals None and therefor this function cannot be run.')
        self.out_nms_rq_semi = self.out_totalsemi / self.ec25_nonlisted_seedling_emergence_monocot
        logging.info("nmsRQsemi")
        logging.info(self.out_nms_rq_semi)
        return self.out_nms_rq_semi

    # Level of concern for non-listed monocot seedlings exposed to pesticide X in a semi-aquatic area
    def LOCnmssemi(self):
        # if self.out_nms_loc_semi == '':
        #     if self.out_nms_rq_semi == -1:
        #         try:
        #             self.nmsRQsemi()
        #         except TypeError:
        #             raise TypeError\
        #             ('totaldry equals None and therefor this function cannot be run.')
        #     if self.out_nms_rq_semi == None:
        #         raise ValueError\
        #         ('nmsRQsemi variable equals None and therefor this function cannot be run.')
        # if self.out_nms_rq_semi >= 1.0:
        #     self.out_nms_loc_semi = ('The risk quotient for non-listed monocot seedlings exposed to'\
        #     ' the pesticide via runoff to semi-aquatic areas indicates a potential risk.')
        # else:
        #     self.out_nms_loc_semi = ('The risk quotient for non-listed monocot seedlings exposed to the'\
        #     ' pesticide via runoff to semi-aquatic areas indicates that potential risk is minimal.')
        exceed_boolean = self.out_nms_rq_semi >= 1.0
        self.out_nms_loc_semi = exceed_boolean.map(lambda x:
                                                   'The risk quotient for non-listed monocot seedlings exposed to the pesticide via runoff to semi-aquatic areas indicates a potential risk.' if x == True
                                                   else 'The risk quotient for non-listed monocot seedlings exposed to the pesticide via runoff to semi-aquatic areas indicates that potential risk is minimal.')
        logging.info("LOCnmssemi")
        logging.info(self.out_nms_loc_semi)
        return self.out_nms_loc_semi

    # Risk Quotient for NON-LISTED MONOCOT seedlings exposed to Pesticide X via SPRAY drift
    def nmsRQspray(self):
        # if self.out_nms_rq_spray == -1:
        #     try:
        #         self.ec25_nonlisted_seedling_emergence_monocot = float(self.ec25_nonlisted_seedling_emergence_monocot)
        #         self.out_spray = float(self.out_spray)
        #     except TypeError:
        #         raise TypeError\
        #         ('EEC for spray drift equals None and therefor this function cannot be run.')
        #     except IndexError:
        #         raise IndexError\
        #         ('The EEC for spray drift needs to be supplied on the command line. ')
        #     except ZeroDivisionError:
        #         raise ZeroDivisionError\
        #         ('The incorporation_depth must be non-zero.')
        #     if self.ec25_nonlisted_seedling_emergence_monocot < 0:
        #         raise ValueError\
        #         ('ec25_nonlisted_seedling_emergence_monocot=%g is a non-physical value' %self.ec25_nonlisted_seedling_emergence_monocot)   
        #     if self.out_spray == -1:
        #         self.spray()
        #     if self.out_spray == None:
        #         raise ValueError\
        #         ('Either the out_spray variable equals None and therefor this function cannot be run.')
        # li = [self.ec25_nonlisted_vegetative_vigor_monocot, self.ec25_nonlisted_seedling_emergence_monocot]

        # m = pd.Series([min(li, key=lambda x:float(x))])
        self.out_nms_rq_spray = self.out_spray / self.out_min_nms_spray
        logging.info("nmsRQspray")
        logging.info(self.out_nms_rq_spray)
        return self.out_nms_rq_spray

    # Level of concern for non-listed monocot seedlings exposed to pesticide via spray drift
    def LOCnmsspray(self):
        # if self.out_nms_loc_spray == '':
        #     if self.out_nms_rq_spray == -1:
        #         try:
        #             self.nmsRQspray()
        #         except TypeError:
        #             raise TypeError\
        #             ('totaldry equals None and therefor this function cannot be run.')
        #     if self.out_nms_rq_spray == None:
        #         raise ValueError\
        #         ('out_nms_rq_spray variable equals None and therefor this function cannot be run.')
        # if self.out_nms_rq_spray >= 1.0:
        #     self.out_nms_loc_spray = ('The risk quotient for non-listed monocot seedlings exposed to'\
        # ' the pesticide via spray drift indicates a potential risk.')
        # else:
        #     self.out_nms_loc_spray = ('The risk quotient for non-listed monocot seedlings exposed to the'\
        # ' pesticide via spray drift indicates that potential risk is minimal.')
        exceed_boolean = self.out_nms_rq_spray >= 1.0
        self.out_nms_loc_spray = exceed_boolean.map(lambda x:
                                                    'The risk quotient for non-listed monocot seedlings exposed to the pesticide via spray drift indicates a potential risk.' if x == True
                                                    else 'The risk quotient for non-listed monocot seedlings exposed to the pesticide via spray drift indicates that potential risk is minimal.')
        logging.info("LOCnmsspray")
        logging.info(self.out_nms_loc_spray)
        return self.out_nms_loc_spray

    # Risk Quotient for LISTED MONOCOT seedlings exposed to Pesticide X in a DRY areas
    def lmsRQdry(self):
        # if self.out_lms_rq_dry == -1:
        #     try:
        #         self.ec25_nonlisted_seedling_emergence_dicot = float(self.ec25_nonlisted_seedling_emergence_dicot)
        #         self.out_totaldry = float(self.out_totaldry)
        #     except TypeError:
        #         raise TypeError\
        #         ('totaldry equals None and therefor this function cannot be run.')
        #     except IndexError:
        #         raise IndexError\
        #         ('The total amount of runoff and spray to dry areas needs to be supplied on the command line. ')
        #     except ValueError:
        #         raise ValueError\
        #         ('The total amount of runoff and spray to dry areas must be a real number,'\
        #         ' not "%lbs ai/A"' %self.out_totaldry)
        #     except ZeroDivisionError:
        #         raise ZeroDivisionError\
        #         ('The incorporation_depth must be non-zero.')
        #     if self.ec25_nonlisted_seedling_emergence_dicot < 0:
        #         raise ValueError\
        #         ('ec25_nonlisted_seedling_emergence_dicot=%g is a non-physical value' %self.ec25_nonlisted_seedling_emergence_dicot)   
        #     if self.out_totaldry == -1:
        #         self.totaldry()
        #     if self.out_totaldry == None:
        #         raise ValueError\
        #         ('Either the out_spray variable equals None and therefor this function cannot be run.')
        self.out_lms_rq_dry = self.out_totaldry / self.noaec_listed_seedling_emergence_monocot
        logging.info("lmsRQdry")
        logging.info(self.out_lms_rq_dry)
        return self.out_lms_rq_dry

    # Level of concern for listed monocot seedlings exposed to pesticide
    #  via runoff in a dry area
    def LOClmsdry(self):
        # if self.out_lms_loc_dry == '':
        #     if self.out_lms_rq_dry == -1:
        #         try:
        #             self.lmsRQdry()
        #         except TypeError:
        #             raise TypeError\
        #             ('totaldry equals None and therefor this function cannot be run.')
        #     if self.out_lms_rq_dry == None:
        #         raise ValueError\
        #         ('out_lms_rq_dry variable equals None and therefor this function cannot be run.')
        # if self.out_lms_rq_dry >= 1.0:
        #     self.out_lms_loc_dry = ('The risk quotient for listed monocot seedlings exposed to'\
        #     ' the pesticide via runoff to dry areas indicates a potential risk.')
        # else:
        #     self.out_lms_loc_dry = ('The risk quotient for listed monocot seedlings exposed to the'\
        #     ' pesticide via runoff to dry areas indicates that potential risk is minimal.')
        exceed_boolean = self.out_lms_rq_dry >= 1.0
        self.out_lms_loc_dry = exceed_boolean.map(lambda x:
                                                  'The risk quotient for listed monocot seedlings exposed to the pesticide via runoff to dry areas indicates a potential risk.' if x == True
                                                  else 'The risk quotient for listed monocot seedlings exposed to the pesticide via runoff to dry areas indicates that potential risk is minimal.')
        logging.info("LOClmsdry")
        logging.info(self.out_lms_loc_dry)
        return self.out_lms_loc_dry

    # Risk Quotient for LISTED MONOCOT seedlings exposed to Pesticide X in a SEMI-AQUATIC area
    def lmsRQsemi(self):
        # if self.out_lms_rq_semi == -1:
        #     try:
        #         self.ec25_nonlisted_seedling_emergence_dicot = float(self.ec25_nonlisted_seedling_emergence_dicot)
        #         self.out_totalsemi = float(self.out_totalsemi)
        #     except TypeError:
        #         raise TypeError\
        #         ('totaldry equals None and therefor this function cannot be run.')
        #     except IndexError:
        #         raise IndexError\
        #         ('The total amount of runoff and spray to semi-aquatic areas needs to be supplied on the command line. ')
        #     except ValueError:
        #         raise ValueError\
        #         ('The total amount of runoff and spray to semi-aquatic areas must be a real number,'\
        #         ' not "%lbs ai/A"' %self.out_totalsemi)
        #     except ZeroDivisionError:
        #         raise ZeroDivisionError\
        #         ('The incorporation_depth must be non-zero.')
        #     if self.ec25_nonlisted_seedling_emergence_dicot < 0:
        #         raise ValueError\
        #         ('ec25_nonlisted_seedling_emergence_monocot=%g is a non-physical value' %self.ec25_nonlisted_seedling_emergence_dicot)   
        #     if self.out_totalsemi == -1:
        #         self.totalsemi()
        #     if self.out_totalsemi == None:
        #         raise ValueError\
        #         ('Either the out_totalsemi variable equals None and therefor this function cannot be run.')
        self.out_lms_rq_semi = self.out_totalsemi / self.noaec_listed_seedling_emergence_monocot
        logging.info("lmsRQsemi")
        logging.info(self.out_lms_rq_semi)
        return self.out_lms_rq_semi

    # Level of concern for listed monocot seedlings exposed to pesticide X in semi-aquatic areas
    def LOClmssemi(self):
        # if self.out_lms_loc_semi == '':
        #     if self.out_lms_rq_semi == -1:
        #         try:
        #             self.lmsRQsemi()
        #         except TypeError:
        #             raise TypeError\
        #             ('totaldry equals None and therefor this function cannot be run.')
        #     if self.out_lms_rq_semi == None:
        #         raise ValueError\
        #         ('lmsRQsemi variable equals None and therefor this function cannot be run.')
        # if self.out_lms_rq_semi >= 1.0:
        #     self.out_lms_loc_semi = ('The risk quotient for listed monocot seedlings exposed to'\
        #     ' the pesticide via runoff to semi-aquatic areas indicates a potential risk.')
        # else:
        #     self.out_lms_loc_semi = ('The risk quotient for listed monocot seedlings exposed to the'\
        #     ' pesticide via runoff to semi-aquatic areas indicates that potential risk is minimal.')
        exceed_boolean = self.out_lms_rq_semi >= 1.0
        self.out_lms_loc_semi = exceed_boolean.map(lambda x:
                                                   'The risk quotient for listed monocot seedlings exposed to the pesticide via runoff to semi-aquatic areas indicates a potential risk.' if x == True
                                                   else 'The risk quotient for listed monocot seedlings exposed to the pesticide via runoff to semi-aquatic areas indicates that potential risk is minimal.')
        logging.info("LOClmssemi")
        logging.info(self.out_lms_loc_semi)
        return self.out_lms_loc_semi

    # Risk Quotient for LISTED MONOCOT seedlings exposed to Pesticide X via SPRAY drift
    def lmsRQspray(self):
        # if self.out_lms_rq_spray == -1:
        #     try:
        #         self.ec25_nonlisted_seedling_emergence_dicot = float(self.ec25_nonlisted_seedling_emergence_dicot)
        #         self.out_spray = float(self.out_spray)
        #     except TypeError:
        #         raise TypeError\
        #         ('out_spray equals None and therefor this function cannot be run.')
        #     except IndexError:
        #         raise IndexError\
        #         ('The amount of spray drift exposure needs to be supplied on the command line. ')
        #     except ValueError:
        #         raise ValueError\
        #         ('The amount of spray drift exposure must be a real number, not "%lbs ai/A"' %out_spray)
        #     except ZeroDivisionError:
        #         raise ZeroDivisionError\
        #         ('The incorporation_depth must be non-zero.')
        #     if self.ec25_nonlisted_seedling_emergence_dicot < 0:
        #         raise ValueError\
        #         ('ec25_nonlisted_seedling_emergence_monocot=%g is a non-physical value' %self.ec25_nonlisted_seedling_emergence_dicot)  
        #     if self.out_spray == -1:
        #         self.spray()
        #     if self.out_spray == None:
        #         raise ValueError\
        #         ('The out_spray variable equals None and therefor this function cannot be run.')
        self.out_lms_rq_spray = self.out_spray / self.out_min_lms_spray
        logging.info("lmsRQspray")
        logging.info(self.out_lms_rq_spray)
        return self.out_lms_rq_spray

    # Level of concern for listed monocot seedlings exposed to pesticide X via spray drift
    def LOClmsspray(self):
        # if self.out_lms_loc_spray == '':
        #     if self.out_lms_rq_spray == -1:
        #         try:
        #             self.lmsRQspray()
        #         except TypeError:
        #             raise TypeError\
        #             ('totaldry equals None and therefor this function cannot be run.')
        #     if self.out_lms_rq_spray == None:
        #         raise ValueError\
        #         ('lmsRQspray variable equals None and therefor this function cannot be run.')
        # if self.out_lms_rq_spray >= 1.0:
        #     self.out_lms_loc_spray = ('The risk quotient for listed monocot seedlings exposed to'\
        #     ' the pesticide via spray drift indicates a potential risk.')
        # else:
        #     self.out_lms_loc_spray = ('The risk quotient for listed monocot seedlings exposed to the'\
        #     ' pesticide via spray drift indicates that potential risk is minimal.')
        exceed_boolean = self.out_lms_rq_spray >= 1.0
        self.out_lms_loc_spray = exceed_boolean.map(lambda x:
                                                    'The risk quotient for listed monocot seedlings exposed to the pesticide via spray drift indicates a potential risk.' if x == True
                                                    else 'The risk quotient for listed monocot seedlings exposed to the pesticide via spray drift indicates that potential risk is minimal.')
        logging.info("LOClmsspray")
        logging.info(self.out_lms_loc_spray)
        return self.out_lms_loc_spray

    # Risk Quotient for NON-LISTED DICOT seedlings exposed to Pesticide X in DRY areas
    def ndsRQdry(self):
        # if self.out_nds_rq_dry == -1:
        #     try:
        #         self.noaec_listed_seedling_emergence_monocot = float(self.noaec_listed_seedling_emergence_monocot)
        #         self.out_totaldry = float(self.out_totaldry)
        #     except TypeError:
        #         raise TypeError\
        #         ('out_totaldry equals None and therefor this function cannot be run.')
        #     except IndexError:
        #         raise IndexError\
        #         ('The amount of runoff and spray to dry areas needs to be supplied on the command line. ')
        #     except ValueError:
        #         raise ValueError\
        #         ('The total amount of runoff and spray to dry areas must be a real number, not "%lbs ai/A"' %out_totaldry)
        #     except ZeroDivisionError:
        #         raise ZeroDivisionError\
        #         ('The incorporation_depth must be non-zero.')
        #     if self.noaec_listed_seedling_emergence_monocot < 0:
        #         raise ValueError\
        #         ('noaec_listed_seedling_emergence_monocot=%g is a non-physical value' %self.noaec_listed_seedling_emergence_monocot)  
        #     if self.out_totaldry == -1:
        #         self.totaldry()
        #     if self.out_totaldry == None:
        #         raise ValueError\
        #         ('The out_totaldry variable equals None and therefor this function cannot be run.')
        self.out_nds_rq_dry = self.out_totaldry / self.ec25_nonlisted_seedling_emergence_dicot
        logging.info("ndsRQdry")
        logging.info(self.out_nds_rq_dry)
        return self.out_nds_rq_dry

    # Level of concern for non-listed dicot seedlings exposed to pesticide X in dry areas
    def LOCndsdry(self):
        # if self.out_nds_loc_dry == '':
        #     if self.out_nds_rq_dry == -1:
        #         try:
        #             self.ndsRQdry()
        #         except TypeError:
        #             raise TypeError\
        #             ('totaldry equals None and therefor this function cannot be run.')
        #     if self.out_nds_rq_dry == None:
        #         raise ValueError\
        #         ('out_nds_rq_dry variable equals None and therefor this function cannot be run.')
        # if self.out_nds_rq_dry >= 1.0:
        #     self.out_nds_loc_dry = ('The risk quotient for non-listed monocot seedlings exposed to'\
        #     ' the pesticide via runoff to dry areas indicates a potential risk.')
        # else:
        #     self.out_nds_loc_dry = ('The risk quotient for non-listed monocot seedlings exposed to the'\
        #     ' pesticide via runoff to dry areas indicates that potential risk is minimal.')
        exceed_boolean = self.out_nds_rq_dry >= 1.0
        self.out_nds_loc_dry = exceed_boolean.map(lambda x:
                                                  'The risk quotient for non-listed dicot seedlings exposed to the pesticide via runoff to dry areas indicates a potential risk.' if x == True
                                                  else 'The risk quotient for non-listed dicot seedlings exposed to the pesticide via runoff to dry areas indicates that potential risk is minimal.')
        logging.info("LOCndsdry")
        logging.info(self.out_nds_loc_dry)
        return self.out_nds_loc_dry

    # Risk Quotient for NON-LISTED DICOT seedlings exposed to Pesticide X in SEMI-AQUATIC areas
    def ndsRQsemi(self):
        # if self.out_nds_rq_semi == -1:
        #     try:
        #         self.noaec_listed_seedling_emergence_monocot = float(self.noaec_listed_seedling_emergence_monocot)
        #         self.out_totalsemi = float(self.out_totalsemi)
        #     except TypeError:
        #         raise TypeError\
        #         ('out_totalsemi equals None and therefor this function cannot be run.')
        #     except IndexError:
        #         raise IndexError\
        #         ('The total amount of runoff and spray to semi-aquatic areas needs to be supplied on the command line. ')
        #     except ValueError:
        #         raise ValueError\
        #         ('The total amount of runoff and spray to semi-aquatic areas must be a real number, not "%lbs ai/A"' %out_totaldry)
        #     except ZeroDivisionError:
        #         raise ZeroDivisionError\
        #         ('The incorporation_depth must be non-zero.')
        #     if self.noaec_listed_seedling_emergence_monocot < 0:
        #         raise ValueError\
        #         ('noaec_listed_seedling_emergence_monocot=%g is a non-physical value' %self.noaec_listed_seedling_emergence_monocot)  
        #     if self.out_totaldry == -1:
        #         self.totalsemi()
        #     if self.out_totaldry == None:
        #         raise ValueError\
        #         ('The out_totalsemi variable equals None and therefor this function cannot be run.')
        self.out_nds_rq_semi = self.out_totalsemi / self.ec25_nonlisted_seedling_emergence_dicot
        logging.info("ndsRQsemi")
        logging.info(self.out_nds_rq_semi)
        return self.out_nds_rq_semi

    # Level of concern for non-listed dicot seedlings exposed to pesticide X in semi-aquatic areas
    def LOCndssemi(self):
        # if self.out_nds_loc_semi == '':
        #     if self.out_nds_rq_semi == -1:
        #         try:
        #             self.ndsRQsemi()
        #         except TypeError:
        #             raise TypeError\
        #             ('totaldry equals None and therefor this function cannot be run.')
        #     if self.out_nds_rq_semi == None:
        #         raise ValueError\
        #         ('out_nds_rq_semi variable equals None and therefor this function cannot be run.')
        # if self.out_nds_rq_semi >= 1.0:
        #     self.out_nds_loc_semi = ('The risk quotient for non-listed monocot seedlings exposed to'\
        #     ' the pesticide via runoff to semi-aquatic areas indicates a potential risk.')
        # else:
        #     self.out_nds_loc_semi = ('The risk quotient for non-listed monocot seedlings exposed to the'\
        #     ' pesticide via runoff to semi-aquatic areas indicates that potential risk is minimal.')
        exceed_boolean = self.out_nds_rq_semi >= 1.0
        self.out_nds_loc_semi = exceed_boolean.map(lambda x:
                                                   'The risk quotient for non-listed dicot seedlings exposed to the pesticide via runoff to semi-aquatic areas indicates a potential risk.' if x == True
                                                   else 'The risk quotient for non-listed dicot seedlings exposed to the pesticide via runoff to semi-aquatic areas indicates that potential risk is minimal.')
        logging.info("LOCndssemi")
        logging.info(self.out_nds_loc_semi)
        return self.out_nds_loc_semi

    # Risk Quotient for NON-LISTED DICOT seedlings exposed to Pesticide X via SPRAY drift
    def ndsRQspray(self):
        # if self.out_nds_rq_spray == -1:
        #     try:
        #         self.noaec_listed_seedling_emergence_monocot = float(self.noaec_listed_seedling_emergence_monocot)
        #         self.out_spray = float(self.out_spray)
        #     except TypeError:
        #         raise TypeError\
        #         ('out_spray equals None and therefor this function cannot be run.')
        #     except IndexError:
        #         raise IndexError\
        #         ('The the amount of spray drift exposure needs to be supplied on the command line. ')
        #     except ValueError:
        #         raise ValueError\
        #         ('The the amount of spray drift exposure areas must be a real number, not "%lbs ai/A"' %out_spray)
        #     except ZeroDivisionError:
        #         raise ZeroDivisionError\
        #         ('The incorporation_depth must be non-zero.')
        #     if self.noaec_listed_seedling_emergence_monocot < 0:
        #         raise ValueError\
        #         ('noaec_listed_seedling_emergence_monocot=%g is a non-physical value' %self.noaec_listed_seedling_emergence_monocot)
        #     if self.out_spray == -1:
        #         self.spray()
        #     if self.out_spray == None:
        #         raise ValueError\
        #         ('The out_spray variable equals None and therefor this function cannot be run.')
        self.out_nds_rq_spray = self.out_spray / self.out_min_nds_spray
        logging.info("ndsRQspray")
        logging.info(self.out_nds_rq_spray)
        return self.out_nds_rq_spray

    # Level of concern for non-listed dicot seedlings exposed to pesticide X via spray drift
    def LOCndsspray(self):
        # if self.out_nds_loc_semi == '':
        #     if self.out_nds_rq_spray == -1:
        #         try:
        #             self.ndsRQspray()
        #         except TypeError:
        #             raise TypeError\
        #             ('totaldry equals None and therefor this function cannot be run.')
        #     if self.out_nds_rq_spray == None:
        #         raise ValueError\
        #         ('out_nds_rq_spray variable equals None and therefor this function cannot be run.')
        # if self.out_nds_rq_spray >= 1.0:
        #     self.out_nds_loc_semi = ('The risk quotient for non-listed monocot seedlings exposed to'\
        #     ' the pesticide via spray drift indicates a potential risk.')
        # else:
        #     self.out_nds_loc_semi = ('The risk quotient for non-listed monocot seedlings exposed to the'\
        #     ' pesticide via spray drift indicates that potential risk is minimal.')
        exceed_boolean = self.out_nds_rq_spray >= 1.0
        self.out_nds_loc_spray = exceed_boolean.map(lambda x:
                                                    'The risk quotient for non-listed dicot seedlings exposed to the pesticide via spray drift indicates a potential risk.' if x == True
                                                    else 'The risk quotient for non-listed dicot seedlings exposed to the pesticide via spray drift indicates that potential risk is minimal.')
        logging.info("LOCndsspray")
        logging.info(self.out_nds_loc_spray)
        return self.out_nds_loc_spray

    # Risk Quotient for LISTED DICOT seedlings exposed to Pesticide X in DRY areas
    def ldsRQdry(self):
        # if self.out_lds_rq_dry == -1:
        #     try:
        #         self.noaec_listed_seedling_emergence_dicot = float(self.noaec_listed_seedling_emergence_dicot)
        #         self.out_totaldry = float(self.out_totaldry)
        #     except TypeError:
        #         raise TypeError\
        #         ('out_totaldry equals None and therefor this function cannot be run.')
        #     except IndexError:
        #         raise IndexError\
        #         ('The total amount of runoff and spray to dry areas needs to be supplied on the command line. ')
        #     except ValueError:
        #         raise ValueError\
        #         ('The total amount of runoff and spray to dry areas must be a real number, not "%lbs ai/A"' %out_totaldry)
        #     except ZeroDivisionError:
        #         raise ZeroDivisionError\
        #         ('The incorporation_depth must be non-zero.')
        #     if self.noaec_listed_seedling_emergence_dicot < 0:
        #         raise ValueError\
        #         ('noaec_listed_seedling_emergence_dicot=%g is a non-physical value' %self.noaec_listed_seedling_emergence_dicot)
        #     if self.out_totaldry == -1:
        #         self.totaldry()
        #     if self.out_totaldry == None:
        #         raise ValueError\
        #         ('The out_totaldry variable equals None and therefor this function cannot be run.')
        self.out_lds_rq_dry = self.out_totaldry / self.noaec_listed_seedling_emergence_dicot
        logging.info("ldsRQdry")
        logging.info(self.out_lds_rq_dry)
        return self.out_lds_rq_dry

    # Level of concern for listed dicot seedlings exposed to pesticideX in dry areas
    def LOCldsdry(self):
        # if self.out_lds_loc_dry == '':
        #     if self.out_lds_rq_dry == -1:
        #         try:
        #             self.ldsRQdry()
        #         except TypeError:
        #             raise TypeError\
        #             ('totaldry equals None and therefor this function cannot be run.')
        #     if self.out_lds_rq_dry == None:
        #         raise ValueError\
        #         ('out_lds_rq_dry variable equals None and therefor this function cannot be run.')
        # if self.out_lds_rq_dry >= 1.0:
        #     self.out_lds_loc_dry = ('The risk quotient for listed monocot seedlings exposed to'\
        #     ' the pesticide via runoff to dry areas indicates a potential risk.')
        # else:
        #     self.out_lds_loc_dry = ('The risk quotient for listed monocot seedlings exposed to the'\
        #     ' pesticide via runoff to dry areas indicates that potential risk is minimal.')
        exceed_boolean = self.out_lds_rq_dry >= 1.0
        self.out_lds_loc_dry = exceed_boolean.map(lambda x:
                                                  'The risk quotient for listed dicot seedlings exposed to the pesticide via runoff to dry areas indicates a potential risk.' if x == True
                                                  else 'The risk quotient for listed dicot seedlings exposed to the pesticide via runoff to dry areas indicates that potential risk is minimal.')
        logging.info("LOCldsdry")
        logging.info(self.out_lds_loc_dry)
        return self.out_lds_loc_dry

    # Risk Quotient for LISTED DICOT seedlings exposed to Pesticide X in SEMI-AQUATIC areas
    def ldsRQsemi(self):
        # if self.out_lds_rq_semi == -1:
        #     try:
        #         self.noaec_listed_seedling_emergence_dicot = float(self.noaec_listed_seedling_emergence_dicot)
        #         self.out_totalsemi = float(self.out_totalsemi)
        #     except TypeError:
        #         raise TypeError\
        #         ('out_totalsemi equals None and therefor this function cannot be run.')
        #     except IndexError:
        #         raise IndexError\
        #         ('The total amount of runoff and spray to semi-aquatic areas needs to be supplied on the command line. ')
        #     except ValueError:
        #         raise ValueError\
        #         ('The total amount of runoff and spray to semi-aquatic areas must be a real number, not "%lbs ai/A"' %totaldry)
        #     except ZeroDivisionError:
        #         raise ZeroDivisionError\
        #         ('The incorporation_depth must be non-zero.')
        #     if self.noaec_listed_seedling_emergence_dicot < 0:
        #         raise ValueError\
        #         ('noaec_listed_seedling_emergence_dicot=%g is a non-physical value' %self.noaec_listed_seedling_emergence_dicot)
        #     if self.out_totalsemi == -1:
        #         self.totalsemi()
        #     if self.out_totalsemi == None:
        #         raise ValueError\
        #         ('The out_totalsemi variable equals None and therefor this function cannot be run.')
        self.out_lds_rq_semi = self.out_totalsemi / self.noaec_listed_seedling_emergence_dicot
        logging.info("ldsRQsemi")
        logging.info(self.out_lds_rq_semi)
        return self.out_lds_rq_semi

    # Level of concern for listed dicot seedlings exposed to pesticide X in dry areas
    def LOCldssemi(self):
        # if self.out_lds_loc_semi == '':
        #     if self.out_lds_rq_semi == -1:
        #         try:
        #             self.ldsRQsemi()
        #         except TypeError:
        #             raise TypeError\
        #             ('totaldry equals None and therefor this function cannot be run.')
        #     if self.out_lds_rq_semi == None:
        #         raise ValueError\
        #         ('out_lds_rq_semi variable equals None and therefor this function cannot be run.')
        # if self.out_lds_rq_semi >= 1.0:
        #     self.out_lds_loc_semi = ('The risk quotient for listed monocot seedlings exposed to'\
        #     ' the pesticide via runoff to semi-aquatic areas indicates a potential risk.')
        # else:
        #     self.out_lds_loc_semi = ('The risk quotient for listed monocot seedlings exposed to the'\
        #     ' pesticide via runoff to semi-aquatic areas indicates that potential risk is minimal.')
        exceed_boolean = self.out_lds_rq_semi >= 1.0
        self.out_lds_loc_semi = exceed_boolean.map(lambda x:
                                                   'The risk quotient for listed dicot seedlings exposed to the pesticide via runoff to semi-aquatic areas indicates a potential risk.' if x == True
                                                   else 'The risk quotient for listed dicot seedlings exposed to the pesticide via runoff to semi-aquatic areas indicates that potential risk is minimal.')
        logging.info("LOCldssemi")
        logging.info(self.out_lds_loc_semi)
        return self.out_lds_loc_semi

    # Risk Quotient for LISTED DICOT seedlings exposed to Pesticide X via SPRAY drift
    def ldsRQspray(self):
        # if self.out_lds_rq_spray == -1:
        #     try:
        #         self.noaec_listed_seedling_emergence_dicot = float(self.noaec_listed_seedling_emergence_dicot)
        #         self.out_spray = float(self.out_spray)
        #     except TypeError:
        #         raise TypeError\
        #         ('out_spray equals None and therefor this function cannot be run.')
        #     except IndexError:
        #         raise IndexError\
        #         ('The amount of spray drift exposure needs to be supplied on the command line. ')
        #     except ValueError:
        #         raise ValueError\
        #         ('The amount of spray drift exposure must be a real number, not "%lbs ai/A"' %out_spray)
        #     except ZeroDivisionError:
        #         raise ZeroDivisionError\
        #         ('The incorporation_depth must be non-zero.')
        #     if self.noaec_listed_seedling_emergence_dicot < 0:
        #         raise ValueError\
        #         ('noaec_listed_seedling_emergence_dicot=%g is a non-physical value' %self.noaec_listed_seedling_emergence_dicot)
        #     if self.out_spray == -1:
        #         self.spray()
        #     if self.out_spray == None:
        #         raise ValueError\
        #         ('The out_spray variable equals None and therefor this function cannot be run.')
        self.out_lds_rq_spray = self.out_spray / self.out_min_lds_spray
        logging.info("ldsRQspray")
        logging.info(self.out_lds_rq_spray)
        return self.out_lds_rq_spray

    # Level of concern for listed dicot seedlings exposed to pesticide X via spray drift
    def LOCldsspray(self):
        # if self.out_lds_loc_spray == '':
        #     if self.out_lds_rq_spray == -1:
        #         try:
        #             self.ldsRQspray()
        #         except TypeError:
        #             raise TypeError\
        #             ('totaldry equals None and therefor this function cannot be run.')
        #     if self.out_lds_rq_spray == None:
        #         raise ValueError\
        #         ('out_lds_rq_spray variable equals None and therefor this function cannot be run.')
        # if self.out_lds_rq_spray >= 1.0:
        #     self.out_lds_loc_spray = ('The risk quotient for listed monocot seedlings exposed to'\
        #     ' the pesticide via spray drift indicates a potential risk.')
        # else:
        #     self.out_lds_loc_spray = ('The risk quotient for listed monocot seedlings exposed to the'\
        #     ' pesticide via spray drift indicates that potential risk is minimal.')
        exceed_boolean = self.out_lds_rq_spray >= 1.0
        self.out_lds_loc_spray = exceed_boolean.map(lambda x:
                                                    'The risk quotient for listed dicot seedlings exposed to the pesticide via spray drift indicates a potential risk.' if x == True
                                                    else 'The risk quotient for listed dicot seedlings exposed to the pesticide via spray drift indicates that potential risk is minimal.')
        logging.info("LOCldsspray")
        logging.info(self.out_lds_loc_spray)
        return self.out_lds_loc_spray

    def minnmsspray(self):
        # determine minimum toxicity concentration used for RQ spray drift values
        # non-listed monocot EC25 and NOAEC
        s1 = pd.Series(self.ec25_nonlisted_seedling_emergence_monocot, name='seedling')
        s2 = pd.Series(self.ec25_nonlisted_vegetative_vigor_monocot, name='vegetative')
        df = pd.concat([s1, s2], axis=1)
        self.out_min_nms_spray = pd.DataFrame.min(df, axis=1)
        logging.info("minnmsspray")
        logging.info(self.out_min_nms_spray)
        return self.out_min_nms_spray

    def minlmsspray(self):
        # determine minimum toxicity concentration used for RQ spray drift values
        # listed monocot EC25 and NOAEC
        s1 = pd.Series(self.noaec_listed_seedling_emergence_monocot, name='seedling')
        s2 = pd.Series(self.noaec_listed_vegetative_vigor_monocot, name='vegetative')
        df = pd.concat([s1, s2], axis=1)
        self.out_min_lms_spray = pd.DataFrame.min(df, axis=1)
        logging.info("minlmsspray")
        logging.info(self.out_min_lms_spray)
        return self.out_min_lms_spray

    def minndsspray(self):
        # determine minimum toxicity concentration used for RQ spray drift values
        # non-listed dicot EC25 and NOAEC
        s1 = pd.Series(self.ec25_nonlisted_seedling_emergence_dicot, name='seedling')
        s2 = pd.Series(self.ec25_nonlisted_vegetative_vigor_dicot, name='vegetative')
        df = pd.concat([s1, s2], axis=1)
        self.out_min_nds_spray = pd.DataFrame.min(df, axis=1)
        logging.info("minndsspray")
        logging.info(self.out_min_nds_spray)
        return self.out_min_nds_spray

    def minldsspray(self):
        # determine minimum toxicity concentration used for RQ spray drift values
        # listed dicot EC25 and NOAEC
        s1 = pd.Series(self.noaec_listed_seedling_emergence_dicot, name='seedling')
        s2 = pd.Series(self.noaec_listed_vegetative_vigor_dicot, name='vegetative')
        df = pd.concat([s1, s2], axis=1)
        self.out_min_lds_spray = pd.DataFrame.min(df, axis=1)
        logging.info("minldsspray")
        logging.info(self.out_min_lds_spray)
        return self.out_min_lds_spray
