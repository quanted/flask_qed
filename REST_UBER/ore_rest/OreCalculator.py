from collections import OrderedDict


class OreCalculator(object):
    def __init__(self, app_rate, area_treated, unit_exp, abs_frac, bw_adult, nc_POD):
        self.app_rate = float(app_rate)
        self.area_treated = float(area_treated)
        self.unit_exp = float(unit_exp)
        self.abs_frac = float(abs_frac)
        self.bw_adult = float(bw_adult)
        self.nc_POD = float(nc_POD)

        self.exposure_conc = self.exposure_conc_calc()
        self.dose_conc = self.dose_conc_calc()
        self.moe = self.moe_calc()

    def exposure_conc_calc(self):
        return (self.unit_exp / 1000.) * self.app_rate * self.area_treated

    def dose_conc_calc(self):
        return (self.exposure_conc * self.abs_frac) / self.bw_adult

    def moe_calc(self):
        return self.nc_POD / self.dose_conc


class NonCancerInputs(object):
    def __init__(self, activity, crop_target, app_rate, app_rate_unit,
                 formulation, app_equip, app_type,
                 loc_dermal, loc_inhal, area_treated, area_treated_unit):
        """
            Shared Inputs between DermalNonCancer and InhalNonCancer classes

            This class plus DermalNonCancer and InhalNonCancer make up a row in the spreadsheet calculator
        """
        self.activity = activity
        self.formulation = formulation
        self.app_equip = app_equip
        self.app_type = app_type
        self.crop_target = crop_target
        self.app_rate = app_rate
        self.app_rate_unit = app_rate_unit
        self.area_treated = area_treated
        self.area_treated_unit = area_treated_unit
        self.loc_dermal = float(loc_dermal)
        self.loc_inhal = float(loc_inhal)


class DermalNonCancer(NonCancerInputs):
    def __init__(self, activity, crop_target, app_rate, app_rate_unit,
                 loc_dermal, loc_inhal, area_treated, area_treated_unit,
                 formulation, app_equip, app_type,
                 abs_frac, bw_adult, nc_POD,
                 unit_exp_sl_no_G, unit_exp_sl_G, unit_exp_dl_G, unit_exp_sl_G_crh, unit_exp_dl_G_crh, unit_exp_ec):

        NonCancerInputs.__init__(self, activity, crop_target, app_rate, app_rate_unit,
                                 formulation, app_equip, app_type,
                                 loc_dermal, loc_inhal, area_treated, area_treated_unit)

        self.unit_exp_sl_no_G = unit_exp_sl_no_G
        self.unit_exp_sl_G = unit_exp_sl_G
        self.unit_exp_dl_G = unit_exp_dl_G
        self.unit_exp_sl_G_crh = unit_exp_sl_G_crh
        self.unit_exp_dl_G_crh = unit_exp_dl_G_crh
        self.unit_exp_ec = unit_exp_ec

        # Dermal PPEs
        self.sl_no_G = None
        self.sl_G = None
        self.dl_G = None
        self.sl_G_crh = None
        self.dl_G_crh = None
        self.ec = None

        # Start calculations to fill out needed PPE attributes
        try:  #  try...except handles the possibility of "No Data" or "NA" in SQLite query results, which are skipped
            self.sl_no_G = OreCalculator(app_rate, area_treated, self.unit_exp_sl_no_G, abs_frac, bw_adult, nc_POD)
        except ValueError:
            self.sl_no_G = "No Data"
        #  If LOC is greater than the MOE, calculate at the next level of PPE (personal protective equipment)
        if calc_further(self.sl_no_G, self.loc_dermal):
            try:
                self.sl_G = OreCalculator(app_rate, area_treated, self.unit_exp_sl_G, abs_frac, bw_adult, nc_POD)
            except ValueError:
                self.sl_G = "No Data"
        if calc_further(self.sl_G, self.loc_dermal):
            try:
                self.dl_G = OreCalculator(app_rate, area_treated, self.unit_exp_dl_G, abs_frac, bw_adult, nc_POD)
            except ValueError:
                self.dl_G = "No Data"
        if calc_further(self.dl_G, self.loc_dermal):
            try:
                self.sl_G_crh = OreCalculator(app_rate, area_treated, self.unit_exp_sl_G_crh, abs_frac, bw_adult, nc_POD)
            except ValueError:
                self.sl_G_crh = "No Data"
        if calc_further(self.sl_G_crh, self.loc_dermal):
            try:
                self.dl_G_crh = OreCalculator(app_rate, area_treated, self.unit_exp_dl_G_crh, abs_frac, bw_adult, nc_POD)
            except ValueError:
                self.dl_G_crh = "No Data"
        if calc_further(self.dl_G_crh, self.loc_dermal):
            try:
                self.ec = OreCalculator(app_rate, area_treated, self.unit_exp_ec, abs_frac, bw_adult, nc_POD)
            except ValueError:
                self.ec = "No Data"


    def get_ppe_increasing_order(self):
        return ['sl_no_G', 'sl_G', 'dl_G', 'sl_G_crh', 'dl_G_crh', 'ec']

    def ordered_dict(self):
        ppe_order = self.get_ppe_increasing_order()
        ordered_dict = OrderedDict()
        for attr in ppe_order:
            ordered_dict[attr] = getattr(self, attr)
        for k, v in self.__dict__.items():
            if not ordered_dict.has_key(k):
                ordered_dict[k] = v

        return ordered_dict



class InhalNonCancer(NonCancerInputs):
    def __init__(self, activity, crop_target, app_rate, app_rate_unit,
                 loc_dermal, loc_inhal, area_treated, area_treated_unit,
                 formulation, app_equip, app_type,
                 abs_frac, bw_adult, nc_POD,
                 unit_exp_no_r, unit_exp_pf5_r, unit_exp_pf10_r, unit_exp_ec):

        NonCancerInputs.__init__(self, activity, crop_target, app_rate, app_rate_unit,
                                 formulation, app_equip, app_type,
                                 loc_dermal, loc_inhal, area_treated, area_treated_unit)

        self.unit_exp_no_r = unit_exp_no_r
        self.unit_exp_pf5_r = unit_exp_pf5_r
        self.unit_exp_pf10_r = unit_exp_pf10_r
        self.unit_exp_ec = unit_exp_ec

        # Inhalation PPEs
        self.no_r = None
        self.pf5_r = None
        self.pf10_r = None
        self.ec = None

        # Start calculations to fill out needed PPE attributes
        try:  #  try...except handles the possibility of "No Data" or "NA" in SQLite query results, which are skipped
            self.no_r = OreCalculator(app_rate, area_treated, self.unit_exp_no_r, abs_frac, bw_adult, nc_POD)
        except ValueError:
            self.no_r = "No Data"
        #  If LOC is greater than the MOE, calculate at the next level of PPE (personal protective equipment)
        if calc_further(self.no_r, self.loc_inhal):
            try:
                self.pf5_r = OreCalculator(app_rate, area_treated, self.unit_exp_pf5_r, abs_frac, bw_adult, nc_POD)
            except ValueError:
                self.pf5_r = "No Data"
        if calc_further(self.pf5_r, self.loc_inhal):
            try:
                self.pf10_r = OreCalculator(app_rate, area_treated, self.unit_exp_pf10_r, abs_frac, bw_adult, nc_POD)
            except ValueError:
                self.pf10_r = "No Data"
        if calc_further(self.pf10_r, self.loc_inhal):
            try:
                self.ec = OreCalculator(app_rate, area_treated, self.unit_exp_ec, abs_frac, bw_adult, nc_POD)
            except ValueError:
                self.ec = "No Data"

    def get_ppe_increasing_order(self):
        return ['no_r', 'pf5_r', 'pf10_r', 'ec']

    def ordered_dict(self):
        ppe_order = self.get_ppe_increasing_order()
        ordered_dict = OrderedDict()
        for attr in ppe_order:
            ordered_dict[attr] = getattr(self, attr)
        for k, v in self.__dict__.items():
            if not ordered_dict.has_key(k):
                ordered_dict[k] = v

        return ordered_dict


##############################################################################
#                     Module level methods
##############################################################################

def calc_further(ppe, loc):
    """
    Method determines where or not further calculations are required.  Further calculation is required when
    either the 'loc' value is greater than the 'ppe' value or when 'ppe' value contained no data and was set
    to be a String "No Data".  Otherwise, no further calculations are needed.

    :param ppe: String, None, or Class instance; Object representing the previous level of PPE used by the worker
    :param loc: float; Level of Concern
    :return: Boolean
    """
    if ppe is None:
        return False
    if type(ppe) is str:
        return True
    try:
        if loc > ppe.moe:
            return True
    except AttributeError:
        return False

def combined_dose(dose_conc_dermal, dose_conc_inhal):
    """
    Combined: Additive Dose approach

    :param dose_conc_dermal: float
    :param dose_conc_inhal: float
    :return: float
    """
    return dose_conc_dermal + dose_conc_inhal

def combined_moe(moe_dermal, moe_inhal):
    """
    Combined: 1/MOE Approach

    :param moe_dermal: float
    :param moe_inhal: float
    :return: float
    """
    return 1 / ( ( 1 / moe_dermal ) + ( 1 / moe_inhal ) )

def ari(loc_dermal, loc_inhal, moe_dermal, moe_inhal):
    """
    Aggregate Risk Index

    :param loc_dermal: float
    :param loc_inhal: float
    :param moe_dermal: float
    :param moe_inhal: float
    :return: float
    """
    return 1 / ( ( loc_dermal / moe_dermal ) + ( loc_inhal / moe_inhal ) )