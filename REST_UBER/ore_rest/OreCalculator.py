


class OreCalculator(object):
    def __init__(self, app_rate, area_treated, unit_exp, abs_frac_st, bw_adult, nc_POD_st):
        self.app_rate = app_rate
        self.area_treated = area_treated
        self.unit_exp = unit_exp
        self.abs_frac_st = abs_frac_st
        self.bw_adult = bw_adult
        self.nc_POD_st = nc_POD_st

        self.exposure_conc = self.exposure_conc_calc()
        self.dose_conc = self.dose_conc_calc()
        self.moe = self.moe_calc()

    def exposure_conc_calc(self):
        return (self.unit_exp / 1000.) * self.app_rate * self.area_treated

    def dose_conc_calc(self):
        return (self.exposure_conc * self.abs_frac_st) / self.bw_adult

    def moe_calc(self):
        return self.nc_POD_st / self.dose_conc




def moe_combined(moe_dermal, moe_inhal):
    return 1 / ( ( 1 / moe_dermal ) + ( 1 / moe_inhal ) )

def ari(loc_dermal, loc_inhal, moe_dermal, moe_inhal):
    return 1 / ( ( loc_dermal / moe_dermal ) + ( loc_inhal / moe_inhal ) )