# Benthic Parameters - USEPA OPP defaults from EXAMS
benthic_params = {
    "depth": 0.05,  # benthic depth (m)
    "porosity": 0.65,  # benthic porosity
    "bulk_density": 1,  # bulk density, dry solid mass/total vol (g/cm3)
    "froc": 0,  # benthic organic carbon fraction
    "doc": 5,  # benthic dissolved organic carbon content (mg/L)
    "bnmas": 0,  # benthic biomass intensity (g/m2)
    "d_over_dx": 1  # mass transfer coefficient for exchange between benthic and water column (m/s)
    # (can be modified later if data exists)
}
def partition_benthic(reach, runoff, runoff_mass, erosion_mass):
    from .parameters import soil, stream_channel, benthic

    try:
        reach = self.region.flow_file.fetch(reach)
        q, v, l = reach.q, reach.v, reach.l
    except AttributeError:
        return None, None, (None, None)

    mean_runoff = runoff.mean()  # m3/d
    baseflow = np.subtract(q, mean_runoff, out=np.zeros(self.i.n_dates), where=(q > mean_runoff))
    total_flow = runoff + baseflow
    mixing_cell = 40.  # meters
    cross_section = total_flow / v
    width = stream_channel.a * np.power(cross_section, stream_channel.b)
    depth = cross_section / width
    surface_area = width * l
    volume = np.array([(depth * surface_area),  # Water column
                       (benthic.depth * surface_area * benthic.porosity)])  # Benthic zone

    # Compute concentration in runoff of runoff mass and erosion mass
    runoff_conc = np.divide(runoff_mass, runoff, out=np.zeros(self.i.n_dates), where=(runoff != 0))
    daily_conc = np.divide(runoff_mass + erosion_mass, mixing_cell, out=np.zeros(self.i.n_dates),
                           where=(runoff_mass + erosion_mass > 0.0) & (mixing_cell > 0.0))

    # Divide mass loading between water column and benthic zones
    mass_input = np.vstack([runoff_mass + ((1. - soil.prben) * erosion_mass),  # Water Column
                            soil.prben * erosion_mass]).T  # Benthic
    # Partition concentration into benthic and water column concentrations
    # This needs to be cleaned up
    # Compute benthic solute holding capacity
    fw1, fw2, theta, sed_conv_factor, omega = solute_holding_capacity(depth, surface_area, self.i.koc)

    k_adj = np.array((total_flow / mixing_cell) + (self.i.deg_photolysis + self.i.deg_hydrolysis) * fw1 + \
                     (self.i.deg_wc * fw1) + self.i.deg_benthic * (1 - fw1))

    aqconc_avg_wb, daily_avg, daily_peak = \
        concentration_loop(self.i.n_dates, daily_conc, k_adj, volume,
                           mass_input, fw1, fw2, omega, theta, self.i.deg_aqueous)

    return map(lambda x: x * 1000000., (runoff_conc, aqconc_avg_wb, daily_avg, daily_peak))

@njit
def concentration_loop(n_dates, daily_concentration, k_adj, daily_volume, mass_input, fw1, fw2, omega, theta, deg_aq):
    # Beginning day aquatic concentrations, considered Peak Aqueous Daily Conc in Water Column
    daily_peak = np.zeros((2, n_dates))
    daily_avg = np.zeros((2, n_dates))
    aqconc_avg_wb = np.zeros(n_dates)

    # Reset starting values
    exp_k = np.exp(-k_adj)
    aqconc_wb = 0
    antecedent_mass = np.zeros(2)  # mn

    for day in range(daily_concentration.size):
        # Add mass input to antecedent mass
        daily_mass = antecedent_mass + mass_input[day]

        # Convert to aqueous concentrations (peak) at beginning of day
        # JCH - fw comes from solute_holding_capacity. Fraction going into each section. Should fw[0] + fw[1] = 1?
        daily_peak[0, day] = daily_mass[0] * fw1[day] / daily_volume[day, 0]
        daily_peak[1, day] = daily_mass[1] * fw2[day] / daily_volume[day, 1]

        # Compute daily average concentration in the water body - when no Benthic layer considered
        aqconc_wb += daily_concentration[day]  # initial water body concentration for current time step

        # Daily avg aq conc in water body, area under curve/t = Ci/k*(1-e^-k), NO benthic
        aqconc_avg_wb[day] = aqconc_wb / k_adj[day] * (1 - exp_k[day])

        # initial water body concentration for next time step
        aqconc_wb *= exp_k[day]

        # For simul diffeq soln: mn1,mn2,mavg1,mavg2 = new_aqconc1, new_aqconc2, aqconc_avg1[d], aqconc_avg2[d]
        # Note: aqconc_avg1 and aqconc_avg2 are outputted - Daily avg aq conc in WC and Benthic regions
        new_aqconc, wc_avg, benthic_avg = simultaneous_diffeq(k_adj[day], deg_aq, omega, theta[day], daily_peak[:, day])
        daily_avg[0, day] = wc_avg
        daily_avg[1, day] = benthic_avg

        # Masses m1 and m2 after time step, t_end
        antecedent_mass[0] = new_aqconc[0] / fw1[day] * daily_volume[day, 0]
        antecedent_mass[1] = new_aqconc[1] / fw2[day] * daily_volume[day, 1]

    return aqconc_avg_wb, daily_avg, daily_peak
@njit
def simultaneous_diffeq(gamma1, gamma2, omega, theta, daily_aq_peak):
    """
    ANALYTICAL SOLUTION FOR THE TWO SIMULTANEOUS DIFFERENTIAL EQNS:
              dm1/dt = Am1 + Bm2
              dm2/dt = Em1 + Fm2
    WITH INITIAL VALUES m1 AND m2 FOR m1 AND m2
    mn1 IS OUTPUT VALUE FOR m1 AFTER TIME T
    mn2 IS OUTPUT VALUE FOR m2 AFTER TIME T
    mavg1 IS AVERAGE VALUE OF m1 OVER TIME T
    """

    t_end = 86400.  # seconds, time step of ONE DAY
    m1, m2 = daily_aq_peak

    # Calculate constants for simultaneous_diffeq: A,B,E,F
    # This reduces the model equivalent parameters to the coefficients needed for solving simultaneous_diffeq
    a = -gamma1 - omega * theta
    b = omega * theta
    e = omega
    f = -gamma2 - omega

    af = a + f
    dif = 4 * ((f * a) - (b * e))
    bbb = np.sqrt(af * af - dif)

    root1 = (af + bbb) / 2.
    root2 = (af - bbb) / 2.

    dd = (root1 - a) / b
    ee = (root2 - a) / b
    ff = ee - dd
    x1 = (ee * m1 - m2) / ff
    y1 = (m2 - dd * m1) / ff

    # Calculate new concentrations for next step
    rt1 = root1 * t_end
    rt2 = root2 * t_end
    exrt1 = np.exp(rt1)
    exrt2 = np.exp(rt2)
    ccc = x1 * exrt1
    ddd = y1 * exrt2

    # values for m1 and m2 after time step t_end
    mn = np.zeros(2)
    mn[0] = ccc + ddd  # Water column
    mn[1] = dd * ccc + ee * ddd  # Benthic

    # AVERAGE DAILY CONCENTRATION SOLUTION: set up for daily average, but can be changed by adjusting time step
    gx = x1 / root1
    hx = y1 / root2

    term1 = gx * exrt1  # term3 = -X1/root1*exp(root1*T1)
    term2 = hx * exrt2  # term4 = -Y1/root2*exp(root2*T1
    term3 = -gx
    term4 = -hx

    mavg_wc = (term1 + term2 + term3 + term4) / t_end  # Water column
    mavg_ben = (term1 * dd + term2 * ee + term3 * dd + term4 * ee) / t_end  # Benthic

    return mn, mavg_wc, mavg_ben


def solute_holding_capacity(depth, surface_area, koc):
    """Calculates Solute Holding capacities and mass transfer between water column and benthic regions"""

    from .parameters import benthic, water_column

    # Aqueous volumes in each region
    vol1 = depth * surface_area  # total volume in water column, approximately equal to water volume alone
    vol2a = benthic.depth * surface_area  # total benthic volume
    vol2 = vol2a * benthic.porosity  # total benthic pore water volume

    # Default EXAMS conditions for partitioning
    kow = koc / .35  # DEFAULT EXAMS CONDITION ON Kow  p.35
    kpdoc1 = kow * .074  # DEFAULT RELATION IN EXAMS (LITTORAL)
    kpdoc2 = koc  # DEFAULT RELATION IN EXAMS (BENTHIC) p.16 of EXAMS 2.98 (or is it Kow*.46 ?)
    xkpb = 0.436 * kow ** .907  # DEFAULT RELATION IN EXAMS

    # mass in littoral region
    vol1a = depth[0] * surface_area  # initial volume corresponding with suspended matter reference
    m_sed_1 = water_column.sused * vol1a * .001  # SEDIMENT MASS LITTORAL
    m_bio_1 = water_column.plmas * vol1a * .001  # BIOLOGICAL MASS LITTORAL
    m_doc_1 = water_column.doc * vol1a * .001  # DOC MASS LITTORAL

    # partitioning coefficients of individual media
    kd_sed_1 = koc * water_column.froc * .001  # Kd of sediment in littoral [m3/kg]
    kd_sed_2 = koc * benthic.froc * .001  # Kd of sediment in benthic
    kd_bio = xkpb / 1000.  # Kd of biological organisms
    kd_doc_1 = kpdoc1 / 1000.  # Kd of DOC in littoral region
    kd_doc_2 = kpdoc2 / 1000.  # Kd of DOC in benthic region

    # mass in benthic region
    m_sed_2 = benthic.bulk_density * vol2a * 1000.  # as defined by EXAMS parameters m_sed_2 = BULKD/PCTWA*VOL2*100000.
    m_bio_2 = benthic.bnmas * surface_area * .001
    m_doc_2 = benthic.doc * vol2 * .001

    # solute holding capacity in regions 1 and 2
    capacity_1 = kd_sed_1 * m_sed_1 + kd_bio * m_bio_1 + kd_doc_1 * m_doc_1 + vol1
    capacity_2 = kd_sed_2 * m_sed_2 + kd_bio * m_bio_2 + kd_doc_2 * m_doc_2 + vol2

    # Fraction going to water column and benthic
    fw1 = vol1 / capacity_1  # fw1 is daily, vol1 is daily
    fw2 = vol2 / capacity_2

    theta = capacity_2 / capacity_1

    sed_conv_factor = vol2 / fw2 / m_sed_2  # converts pore water to [Total Conc normalized to sed mass]

    # Omega mass transfer - Calculates littoral to benthic mass transfer coefficient
    omega = benthic.d_over_dx / benthic.depth  # (m3/hr)/(3600 s/hr)

    return fw1, fw2, theta, sed_conv_factor, omega
