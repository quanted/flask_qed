import pandas as pd
import logging
class terrplant(object):

    def __init__(self, run_type, pd_obj, pd_obj_exp):

        # logging.info(pd_obj)

        # Inputs: Assign object attribute variables from the input Pandas DataFrame
        self.run_type = run_type
        
        self.version_terrplant = pd_obj['version_terrplant']
        self.application_rate = pd_obj['application_rate']
        self.incorporation_depth = pd_obj['incorporation_depth']
        self.runoff_fraction = pd_obj['runoff_fraction']
        self.drift_fraction = pd_obj['drift_fraction']
        self.chemical_name = pd_obj['chemical_name']
        self.pc_code = pd_obj['pc_code']
        self.use = pd_obj['use']
        self.application_method = pd_obj['application_method']
        self.application_form = pd_obj['application_form']
        self.solubility = pd_obj['solubility']
        self.ec25_nonlisted_seedling_emergence_monocot = pd_obj["ec25_nonlisted_seedling_emergence_monocot"]
        self.ec25_nonlisted_seedling_emergence_dicot = pd_obj["ec25_nonlisted_seedling_emergence_dicot"]
        self.noaec_listed_seedling_emergence_monocot = pd_obj["noaec_listed_seedling_emergence_monocot"]
        self.noaec_listed_seedling_emergence_dicot = pd_obj["noaec_listed_seedling_emergence_dicot"]
        self.ec25_nonlisted_vegetative_vigor_monocot = pd_obj["ec25_nonlisted_vegetative_vigor_monocot"]
        self.ec25_nonlisted_vegetative_vigor_dicot = pd_obj["ec25_nonlisted_vegetative_vigor_dicot"]
        self.noaec_listed_vegetative_vigor_monocot = pd_obj["noaec_listed_vegetative_vigor_monocot"]
        self.noaec_listed_vegetative_vigor_dicot = pd_obj["noaec_listed_vegetative_vigor_dicot"]


        # Outputs: Assign object attribute variables to Pandas Series
        self.out_rundry = pd.Series(name="out_rundry")
        self.out_runsemi = pd.Series(name="out_runsemi")
        self.out_totaldry = pd.Series(name="out_totaldry")
        self.out_totalsemi = pd.Series(name="out_totalsemi")
        self.out_spray = pd.Series(name="out_spray")
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


        # Now that the output member variables are defined, run the model methods
        self.run_methods()
        

        # Create DataFrame containing output value Series
        pd_obj_out = pd.DataFrame({
            'out_rundry' : self.out_rundry,
            'out_runsemi' : self.out_runsemi,
            'out_totaldry' : self.out_totaldry,
            'out_totalsemi' : self.out_totalsemi,
            'out_spray' : self.out_spray,
            'out_nms_rq_dry' : self.out_nms_rq_dry,
            'out_nms_loc_dry' : self.out_nms_loc_dry,
            'out_nms_rq_semi' : self.out_nms_rq_semi,
            'out_nms_loc_semi' : self.out_nms_loc_semi,
            'out_nms_rq_spray' : self.out_nms_rq_spray,
            'out_nms_loc_spray ' : self.out_nms_loc_spray ,
            'out_lms_rq_dry' : self.out_lms_rq_dry,
            'out_lms_loc_dry' : self.out_lms_loc_dry,
            'out_lms_rq_semi' : self.out_lms_rq_semi,
            'out_lms_loc_semi' : self.out_lms_loc_semi,
            'out_lms_rq_spray' : self.out_lms_rq_spray,
            'out_lms_loc_spray' : self.out_lms_loc_spray,
            'out_nds_rq_dry' : self.out_nds_rq_dry,
            'out_nds_loc_dry' : self.out_nds_loc_dry,
            'out_nds_rq_semi' : self.out_nds_rq_semi,
            'out_nds_loc_semi' : self.out_nds_loc_semi,
            'out_nds_rq_spray' : self.out_nds_rq_spray,
            'out_nds_loc_spray' : self.out_nds_loc_spray,
            'out_lds_rq_dry' : self.out_lds_rq_dry,
            'out_lds_loc_dry' : self.out_lds_loc_dry,
            'out_lds_rq_semi' : self.out_lds_rq_semi,
            'out_lds_loc_semi' : self.out_lds_loc_semi,
            'out_lds_rq_spray' : self.out_lds_rq_spray,
            'out_lds_loc_spray' : self.out_lds_loc_spray
        })


        # Callable from Bottle that returns JSON
        self.json = self.json(pd_obj, pd_obj_out, pd_obj_exp)      
        

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
            self.nms_rq_dry()
            self.nms_rq_semi()
            self.nms_rq_spray()
            self.lms_rq_dry()
            self.lms_rq_semi()
            self.lms_rq_spray()
            self.nds_rq_dry()
            self.nds_rq_semi()
            self.nds_rq_spray()
            self.lds_rq_dry()
            self.lds_rq_semi()
            self.lds_rq_spray()
        except TypeError:
            print "Type Error: Your variables are not set correctly."

    # EEC for runoff for dry areas
    def rundry(self):
        self.out_rundry = (self.application_rate/self.incorporation_depth) * self.runoff_fraction
        return self.out_rundry

    # EEC for runoff to semi-aquatic areas
    def runsemi(self):
        self.out_runsemi = (self.application_rate/self.incorporation_depth) * self.runoff_fraction * 10
        return self.out_runsemi

    # EEC for spray drift
    def spray(self):
        self.out_spray = self.application_rate * self.drift_fraction
        return self.out_spray

    # EEC total for dry areas
    def totaldry(self):
        self.out_totaldry = self.out_rundry + self.out_spray
        return self.out_totaldry


    # EEC total for semi-aquatic areas
    def totalsemi (self):
        self.out_totalsemi = self.out_runsemi + self.out_spray
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
        self.out_nms_rq_dry = self.out_totaldry/self.ec25_nonlisted_seedling_emergence_monocot
        return self.out_nms_rq_dry

    # Level of concern for non-listed monocot seedlings exposed to pesticide X in a dry area
    def LOCnmsdry(self):
        if self.out_nms_rq_dry >= 1.0:
            self.out_nms_loc_dry = ('The risk quotient for non-listed monocot seedlings exposed to'\
            ' the pesticide via runoff to a dry area indicates a potential risk.')
        else:
            self.out_nms_loc_dry = ('The risk quotient for non-listed monocot seedlings exposed to'\
            ' the pesticide via runoff to a dry area indicates that potential risk is minimal.'))
        return self.out_nms_loc_dry

    # Risk Quotient for NON-LISTED MONOCOT seedlings exposed to Pesticide X in a SEMI-AQUATIC area
    def nmsRQsemi(self):
        self.out_nms_rq_semi = self.out_totalsemi/self.ec25_nonlisted_seedling_emergence_monocot
        return self.out_nms_rq_semi

    # Level of concern for non-listed monocot seedlings exposed to pesticide X in a semi-aquatic area
    def LOCnmssemi(self):
        if self.out_nms_rq_semi >= 1.0:
            self.out_nms_loc_semi = ('The risk quotient for non-listed monocot seedlings exposed to'\
            ' the pesticide via runoff to a semi-aquatic area indicates a potential risk.')
        else:
            self.out_nms_loc_semi = ('The risk quotient for non-listed monocot seedlings exposed to the'\
            ' pesticide via runoff to a semi-aquatic area indicates that potential risk is minimal.')
        return self.out_nms_loc_semi


    # Risk Quotient for NON-LISTED MONOCOT seedlings exposed to Pesticide X via SPRAY drift
    def nmsRQspray(self):
        self.out_nms_rq_spray = self.out_spray/self.ec25_nonlisted_seedling_emergence_monocot
        return self.out_nms_rq_spray

    # Level of concern for non-listed monocot seedlings exposed to pesticide via spray drift
    def LOCnmsspray(self):
        if self.out_nms_rq_spray >= 1.0:
            self.out_nms_loc_spray = ('The risk quotient for non-listed monocot seedlings exposed to'\
        ' the pesticide via spray drift indicates a potential risk.')
        else:
            self.out_nms_loc_spray = ('The risk quotient for non-listed monocot seedlings exposed to the'\
        ' pesticide via spray drift indicates that potential risk is minimal.')
        return self.out_nms_loc_spray


    # Risk Quotient for LISTED MONOCOT seedlings exposed to Pesticide X in a DRY areas
    def lmsRQdry(self):
        self.out_lms_rq_dry = self.out_totaldry/self.ec25_nonlisted_seedling_emergence_dicot
        return self.out_lms_rq_dry

    # Level of concern for listed monocot seedlings exposed to pesticide
    #  via runoff in a dry area
    def LOClmsdry(self):
        if self.out_lms_rq_dry >= 1.0:
            self.out_lms_loc_dry = ('The risk quotient for listed monocot seedlings exposed to'\
            ' the pesticide via runoff to a dry area indicates a potential risk.')
        else:
            self.out_lms_loc_dry = ('The risk quotient for listed monocot seedlings exposed to the'\
            ' pesticide via runoff to a dry area indicates that potential risk is minimal.')
        return self.out_lms_loc_dry


    # Risk Quotient for LISTED MONOCOT seedlings exposed to Pesticide X in a SEMI-AQUATIC area
    def lmsRQsemi(self):
        self.out_lms_rq_semi = self.out_totalsemi/self.ec25_nonlisted_seedling_emergence_dicot
        return self.out_lms_rq_semi

    # Level of concern for listed monocot seedlings exposed to pesticide X in semi-aquatic areas
    def LOClmssemi(self):
        if self.out_lms_rq_semi >= 1.0:
            self.out_lms_loc_semi = ('The risk quotient for listed monocot seedlings exposed to'\
            ' the pesticide via runoff to a semi-aquatic area indicates a potential risk.')
        else:
            self.out_lms_loc_semi = ('The risk quotient for listed monocot seedlings exposed to the'\
            ' pesticide via runoff to a semi-aquatic area indicates that potential risk is minimal.')
        return self.out_lms_loc_semi


    # Risk Quotient for LISTED MONOCOT seedlings exposed to Pesticide X via SPRAY drift
    def lmsRQspray(self):
        self.out_lms_rq_spray = self.out_spray/self.ec25_nonlisted_seedling_emergence_dicot
        return self.out_lms_rq_spray

    # Level of concern for listed monocot seedlings exposed to pesticide X via spray drift
    def LOClmsspray(self):
        if self.out_lms_rq_spray >= 1.0:
            self.out_lms_loc_spray = ('The risk quotient for listed monocot seedlings exposed to'\
            ' the pesticide via spray drift indicates a potential risk.')
        else:
            self.out_lms_loc_spray = ('The risk quotient for listed monocot seedlings exposed to the'\
            ' pesticide via spray drift indicates that potential risk is minimal.')
        return self.out_lms_loc_spray


    # Risk Quotient for NON-LISTED DICOT seedlings exposed to Pesticide X in DRY areas
    def ndsRQdry(self):
        self.out_nds_rq_dry = self.out_totaldry/self.noaec_listed_seedling_emergence_monocot
        return self.out_nds_rq_dry

    # Level of concern for non-listed dicot seedlings exposed to pesticide X in dry areas
    def LOCndsdry(self):
        if self.out_nds_rq_dry >= 1.0:
            self.out_nds_loc_dry = ('The risk quotient for non-listed monocot seedlings exposed to'\
            ' the pesticide via runoff to dry areas indicates a potential risk.')
        else:
            self.out_nds_loc_dry = ('The risk quotient for non-listed monocot seedlings exposed to the'\
            ' pesticide via runoff to dry areas indicates that potential risk is minimal.')
        return self.out_nds_loc_dry


    # Risk Quotient for NON-LISTED DICOT seedlings exposed to Pesticide X in SEMI-AQUATIC areas
    def ndsRQsemi(self):
        self.out_nds_rq_semi = self.out_totalsemi/self.noaec_listed_seedling_emergence_monocot
        return self.out_nds_rq_semi

    # Level of concern for non-listed dicot seedlings exposed to pesticide X in semi-aquatic areas
    def LOCndssemi(self):)
        if self.out_nds_rq_semi >= 1.0:
            self.out_nds_loc_semi = ('The risk quotient for non-listed monocot seedlings exposed to'\
            ' the pesticide via runoff to semi-aquatic areas indicates a potential risk.')
        else:
            self.out_nds_loc_semi = ('The risk quotient for non-listed monocot seedlings exposed to the'\
            ' pesticide via runoff to semi-aquatic areas indicates that potential risk is minimal.')
        return self.out_nds_loc_semi

    # Risk Quotient for NON-LISTED DICOT seedlings exposed to Pesticide X via SPRAY drift
    def ndsRQspray(self):
        self.out_nds_rq_spray = self.out_spray/self.noaec_listed_seedling_emergence_monocot
        return self.out_nds_rq_spray

    # Level of concern for non-listed dicot seedlings exposed to pesticide X via spray drift
    def LOCndsspray(self):
        if self.out_nds_rq_spray >= 1.0:
            self.out_nds_loc_semi = ('The risk quotient for non-listed monocot seedlings exposed to'\
            ' the pesticide via spray drift indicates a potential risk.')
        else:
            self.out_nds_loc_semi = ('The risk quotient for non-listed monocot seedlings exposed to the'\
            ' pesticide via spray drift indicates that potential risk is minimal.')
        return self.out_nds_loc_semi

    # Risk Quotient for LISTED DICOT seedlings exposed to Pesticide X in DRY areas
    def ldsRQdry(self):
        self.out_lds_rq_dry = self.out_totaldry/self.noaec_listed_seedling_emergence_dicot
        return self.out_lds_rq_dry

    # Level of concern for listed dicot seedlings exposed to pesticideX in dry areas
    def LOCldsdry(self):
        if self.out_lds_rq_dry >= 1.0:
            self.out_lds_loc_dry = ('The risk quotient for listed monocot seedlings exposed to'\
            ' the pesticide via runoff to dry areas indicates a potential risk.')
        else:
            self.out_lds_loc_dry = ('The risk quotient for listed monocot seedlings exposed to the'\
            ' pesticide via runoff to dry areas indicates that potential risk is minimal.')
        return self.out_lds_loc_dry

    # Risk Quotient for LISTED DICOT seedlings exposed to Pesticide X in SEMI-AQUATIC areas
    def ldsRQsemi(self):
        self.out_lds_rq_semi = self.out_totalsemi/self.noaec_listed_seedling_emergence_dicot
        return self.out_lds_rq_semi

    # Level of concern for listed dicot seedlings exposed to pesticide X in dry areas
    def LOCldssemi(self):
        if self.out_lds_rq_semi >= 1.0:
            self.out_lds_loc_semi = ('The risk quotient for listed monocot seedlings exposed to'\
            ' the pesticide via runoff to semi-aquatic areas indicates a potential risk.')
        else:
            self.out_lds_loc_semi = ('The risk quotient for listed monocot seedlings exposed to the'\
            ' pesticide via runoff to semi-aquatic areas indicates that potential risk is minimal.')
        return self.out_lds_loc_semi

    # Risk Quotient for LISTED DICOT seedlings exposed to Pesticide X via SPRAY drift
    def ldsRQspray(self):
        self.out_lds_rq_spray = self.out_spray/self.noaec_listed_seedling_emergence_dicot
        return self.out_lds_rq_spray

    # Level of concern for listed dicot seedlings exposed to pesticide X via spray drift
    def LOCldsspray(self):)
        if self.out_lds_rq_spray >= 1.0:
            self.out_lds_loc_spray = ('The risk quotient for listed monocot seedlings exposed to'\
            ' the pesticide via spray drift indicates a potential risk.')
        else:
            self.out_lds_loc_spray = ('The risk quotient for listed monocot seedlings exposed to the'\
            ' pesticide via spray drift indicates that potential risk is minimal.')
        return self.out_lds_loc_spray
