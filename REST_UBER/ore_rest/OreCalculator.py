from __future__ import division
from collections import OrderedDict
import logging


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
    def __init__(self, activity, crop_target, app_rate, app_rate_unit, crop_name,
                 formulation, app_equip, app_type, abs_frac, bw_adult, nc_POD,
                 loc_dermal, loc_inhal, area_treated, area_treated_unit, active_ingredient):
        """
            Shared Inputs between DermalNonCancer and InhalNonCancer classes

            This class plus DermalNonCancer and InhalNonCancer make up a row in the spreadsheet calculator
        """
        self.activity = activity
        self.formulation = formulation
        self.app_equip = app_equip
        self.app_type = app_type
        self.crop_target = crop_target
        self.crop_name = crop_name
        self.app_rate = app_rate
        self.app_rate_unit = app_rate_unit
        self.area_treated = area_treated
        self.area_treated_unit = area_treated_unit
        self.loc_dermal = float(loc_dermal)
        self.loc_inhal = float(loc_inhal)
        self.abs_frac = abs_frac
        self.bw_adult = bw_adult
        self.nc_POD = nc_POD
        self.active_ingredient = active_ingredient

    def calc_ppe(self, unit_exp):
        #  try...except handles the possibility of "No Data" or "NA" in SQLite query results, which are skipped
        try:
            return OreCalculator(self.app_rate, self.area_treated, unit_exp, self.abs_frac, self.bw_adult, self.nc_POD)
        except ValueError:
            return "No Data"

    def calc_further(self, ppe, loc):
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

    def ordered_dict(self, ppe_order):
        ordered_dict = OrderedDict()
        for attr in ppe_order:
            ordered_dict[attr] = getattr(self, attr)
        for k, v in self.__dict__.items():
            if not ordered_dict.has_key(k):
                ordered_dict[k] = v

        return ordered_dict


class DermalNonCancer(NonCancerInputs):
    def __init__(self, activity, crop_target, app_rate, app_rate_unit, crop_name,
                 loc_dermal, loc_inhal, area_treated, area_treated_unit, active_ingredient,
                 formulation, app_equip, app_type, abs_frac, bw_adult, nc_POD,
                 unit_exp_sl_no_G, unit_exp_sl_G, unit_exp_dl_G, unit_exp_sl_G_crh, unit_exp_dl_G_crh, unit_exp_ec):

        NonCancerInputs.__init__(self, activity, crop_target, app_rate, app_rate_unit, crop_name,
                                 formulation, app_equip, app_type, abs_frac, bw_adult, nc_POD,
                                 loc_dermal, loc_inhal, area_treated, area_treated_unit, active_ingredient)

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

        """
            Remove this auto-inited methods; call from _rest_model module explicitly
        """
        self.calc_not_combined()

    def calc_sl_no_G(self):
        self.sl_no_G = self.calc_ppe(self.unit_exp_sl_no_G)

    def calc_sl_G(self):
        self.sl_G = self.calc_ppe(self.unit_exp_sl_G)

    def calc_dl_G(self):
        self.dl_G = self.calc_ppe(self.unit_exp_dl_G)

    def calc_sl_G_crh(self):
        self.sl_G_crh = self.calc_ppe(self.unit_exp_sl_G_crh)

    def calc_dl_G_crh(self):
        self.dl_G_crh = self.calc_ppe(self.unit_exp_dl_G_crh)

    def calc_ec(self):
        self.ec = self.calc_ppe(self.unit_exp_ec)

    def calc_not_combined(self):
        self.combined = False

        # Start calculations to fill out needed PPE attributes
        self.calc_sl_no_G()
        if self.calc_further(self.sl_no_G, self.loc_dermal):
            self.calc_sl_G()
        if self.calc_further(self.sl_G, self.loc_dermal):
            self.calc_dl_G()
        if self.calc_further(self.dl_G, self.loc_dermal):
            self.calc_sl_G_crh()
        if self.calc_further(self.sl_G_crh, self.loc_dermal):
            self.calc_dl_G_crh()
        if self.calc_further(self.dl_G_crh, self.loc_dermal):
            self.calc_ec()

    def get_ppe_increasing_order(self):
        return ('sl_no_G', 'sl_G', 'dl_G', 'sl_G_crh', 'dl_G_crh', 'ec')

    def get_ppe_in_use(self):

        ppe_in_use = []
        for ppe in self.get_ppe_increasing_order():
            if isinstance(getattr(self, ppe), OreCalculator):
                ppe_in_use.append(ppe)

        return ppe_in_use


class InhalNonCancer(NonCancerInputs):
    def __init__(self, activity, crop_target, app_rate, app_rate_unit, crop_name,
                 loc_dermal, loc_inhal, area_treated, area_treated_unit, active_ingredient,
                 formulation, app_equip, app_type, abs_frac, bw_adult, nc_POD,
                 unit_exp_no_r, unit_exp_pf5_r, unit_exp_pf10_r, unit_exp_ec):

        NonCancerInputs.__init__(self, activity, crop_target, app_rate, app_rate_unit, crop_name,
                                 formulation, app_equip, app_type, abs_frac, bw_adult, nc_POD,
                                 loc_dermal, loc_inhal, area_treated, area_treated_unit, active_ingredient)

        self.unit_exp_no_r = unit_exp_no_r
        self.unit_exp_pf5_r = unit_exp_pf5_r
        self.unit_exp_pf10_r = unit_exp_pf10_r
        self.unit_exp_ec = unit_exp_ec

        # Inhalation PPEs
        self.no_r = None
        self.pf5_r = None
        self.pf10_r = None
        self.ec = None

        """
            Remove this auto-inited methods; call from _rest_model module explicitly
        """
        self.calc_not_combined()

    def calc_no_r(self):
        self.no_r = self.calc_ppe(self.unit_exp_no_r)

    def calc_pf5_r(self):
        self.pf5_r = self.calc_ppe(self.unit_exp_pf5_r)

    def calc_pf10_r(self):
        self.pf10_r = self.calc_ppe(self.unit_exp_pf10_r)

    def calc_ec(self):
        self.ec = self.calc_ppe(self.unit_exp_ec)

    def calc_not_combined(self):
        self.combined = 'Not Combined'

        # Start calculations to fill out needed PPE attributes
        self.calc_no_r()
        if self.calc_further(self.no_r, self.loc_inhal):
            self.calc_pf5_r()
        if self.calc_further(self.pf5_r, self.loc_inhal):
            self.calc_pf10_r()
        if self.calc_further(self.pf10_r, self.loc_inhal):
            self.calc_ec()

    def get_ppe_increasing_order(self):
        return ('no_r', 'pf5_r', 'pf10_r', 'ec')

    def get_ppe_in_use(self):

        ppe_in_use = []
        for ppe in self.get_ppe_increasing_order():
            if isinstance(getattr(self, ppe), OreCalculator):
                ppe_in_use.append(ppe)

        return ppe_in_use


##############################################################################
#                     Combined Calculations
##############################################################################
#  Combined: Additive Dose & 1/MOE Approaches:
#    - Calc a "Total MOE" using the sum of the Dermal & Inhalation
#      dose concentrations for each "row" in output table
#        -  Dermal & Inhalation dose concentrations can be different
#           for each of these calculations depending on their individual
#           MOEs.
#    - The calculations continue (adding more rows to output table) until
#      the "Total MOE" is greater than the LOC.
#        - Does this mean for Combined Dose calculations there can only
#          be 1 LOC (dermal and inhalation having the same LOC)?
#            - Yes, if LOCs are different, the ARI method must be used...
#    - These approaches require dermal & inhalation to have same LOC
#
#  ARI (Aggregate Risk Index) Approach:
#   - Required approach if dermal & inhalation have different LOCs
#   - Does ARI value affect the number of rows in the output table?
#     Or is it a just reported, and the dermal and inhalation MOEs still
#     determine when to stop further calculations (MOE > LOC)?
#       - Value of ARIs are small compared to LOCs in example document.
##############################################################################
##############################################################################

class CombinedDose(object):
    def __init__(self, dermal, inhal):

        self.dermal = dermal
        self.inhal = inhal

        self.ppe_in_use = map(None, self.dermal.get_ppe_in_use(),
                              self.inhal.get_ppe_in_use())  # merge dermal & inhal lists
        print self.ppe_in_use

    def moe_calc_additive_dose(self, nc_POD, dose_conc_combined):
        return float(nc_POD) / dose_conc_combined

    def moe_calc_one_over_moe(self, moe_dermal, moe_inhal):
        return 1 / ((1 / moe_dermal) + (1 / moe_inhal))

    def ari_calc(self, loc_dermal, loc_inhal, moe_dermal, moe_inhal):
        return 1 / ((loc_dermal / moe_dermal) + (loc_inhal / moe_inhal))

    def additive_dose(self):
        self.combined = 'MOE'
        self.combined_moe = []
        self.approach = "Total MOE = NOAEL (mg/kg/day) / (Dermal Dose + Inhalation Dose)"

        i = 0
        for ppe_dermal, ppe_inhal in self.ppe_in_use:
            """
            self.ppe_in_use will have None values if the dermal.get_ppe_in_use() & inhal.get_ppe_in_use()
            lists are different lengths.  The try..except blocks here will replace None values with
            last valid dose conc. value for use in the Combined MOE calculation
            """
            try:  # Try to set dermal dose conc. to current ppe
                conc_d = getattr(self.dermal, ppe_dermal).dose_conc
                last_dermal_conc = conc_d
            except TypeError, e:  # if try fails, use previous valid dermal dose conc.
                logging.exception(e)
                conc_d = last_dermal_conc
            try:  # Try to set inhal dose conc. to current ppe
                conc_i = getattr(self.inhal, ppe_inhal).dose_conc
                last_inhal_conc = conc_i
            except TypeError, e:  # if try fails, use previous valid inhal dose conc.
                logging.exception(e)
                conc_i = last_inhal_conc

            combo_moe = self.moe_calc_additive_dose(self.dermal.nc_POD, conc_d + conc_i)  # run Combined MOE calculation
            self.combined_moe.append(combo_moe)

            i += 1

        print self.combined_moe
        return {'combined': self.combined, 'combined_list': self.combined_moe, 'combined_approach': self.approach}

    def one_over_moe(self):
        self.combined = 'MOE'
        self.combined_moe = []
        self.approach = "Total MOE = (1 / Dermal MOE) + (1 / Inhalation MOE)"

        i = 0
        for ppe_dermal, ppe_inhal in self.ppe_in_use:
            """
            self.ppe_in_use will have None values if the dermal.get_ppe_in_use() & inhal.get_ppe_in_use()
            lists are different lengths.  The try..except blocks here will replace None values with
            last valid dose conc. value for use in the Combined MOE calculation
            """
            try:  # Try to set dermal dose conc. to current ppe
                moe_d = getattr(self.dermal, ppe_dermal).moe
                last_dermal_moe = moe_d
            except TypeError, e:  # if try fails, use previous valid dermal dose conc.
                logging.exception(e)
                moe_d = last_dermal_moe
            try:  # Try to set inhal dose conc. to current ppe
                moe_i = getattr(self.inhal, ppe_inhal).moe
                last_inhal_moe = moe_i
            except TypeError, e:  # if try fails, use previous valid inhal dose conc.
                logging.exception(e)
                moe_i = last_inhal_moe

            combo_moe = self.moe_calc_one_over_moe(moe_d, moe_i)  # run Combined MOE calculation
            self.combined_moe.append(combo_moe)

            i += 1

        print self.combined_moe
        return {'combined': self.combined, 'combined_list': self.combined_moe, 'combined_approach': self.approach}

    def ari(self):
        self.combined = 'ARI'
        self.combined_moe = []
        self.approach = "ARI = Aggregate Risk Index = 1 / [(Dermal LOC / Dermal MOE) + (Inhalation LOC / Inhalation MOE)]"

        loc_d = self.dermal.loc_dermal
        loc_i = self.inhal.loc_inhal

        i = 0
        for ppe_dermal, ppe_inhal in self.ppe_in_use:
            """
            self.ppe_in_use will have None values if the dermal.get_ppe_in_use() & inhal.get_ppe_in_use()
            lists are different lengths.  The try..except blocks here will replace None values with
            last valid dose conc. value for use in the Combined MOE calculation
            """
            try:  # Try to set dermal dose conc. to current ppe
                moe_d = getattr(self.dermal, ppe_dermal).moe
                last_dermal_moe = moe_d
            except TypeError, e:  # if try fails, use previous valid dermal dose conc.
                logging.exception(e)
                moe_d = last_dermal_moe
            try:  # Try to set inhal dose conc. to current ppe
                moe_i = getattr(self.inhal, ppe_inhal).moe
                last_inhal_moe = moe_i
            except TypeError, e:  # if try fails, use previous valid inhal dose conc.
                logging.exception(e)
                moe_i = last_inhal_moe

            combo_moe = self.ari_calc(loc_d, loc_i, moe_d, moe_i)  # run Combined MOE calculation
            self.combined_moe.append(combo_moe)

            i += 1

        print self.combined_moe
        return {'combined': self.combined, 'combined_list': self.combined_moe, 'combined_approach': self.approach}
