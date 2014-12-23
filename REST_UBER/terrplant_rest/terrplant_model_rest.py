
class terrplant(object):
    def __init__(self, version_terrplant, run_type, application_rate, incorporation_depth, runoff_fraction, 
                    drift_fraction, ec25_nonlisted_seedling_emergence_monocot, ec25_nonlisted_seedling_emergence_dicot, 
                    noaec_listed_seedling_emergence_monocot, noaec_listed_seedling_emergence_dicot, 
                    chemical_name, pc_code, use, application_method, application_form, solubility):
        self.version_terrplant = version_terrplant
        self.run_type = run_type
        self.application_rate = application_rate
        self.incorporation_depth = incorporation_depth
        self.runoff_fraction = runoff_fraction
        self.drift_fraction = drift_fraction
        self.ec25_nonlisted_seedling_emergence_monocot = ec25_nonlisted_seedling_emergence_monocot
        self.ec25_nonlisted_seedling_emergence_dicot = ec25_nonlisted_seedling_emergence_dicot
        self.noaec_listed_seedling_emergence_monocot = noaec_listed_seedling_emergence_monocot
        self.noaec_listed_seedling_emergence_dicot = noaec_listed_seedling_emergence_dicot
        self.chemical_name = chemical_name
        self.pc_code = pc_code
        self.use = use
        self.application_method = application_method
        self.application_form = application_form
        self.solubility = solubility

        #Result variables
        self.rundry_results = -1
        self.runsemi_results = -1
        self.totaldry_results = -1
        self.totalsemi_results = -1
        self.spray_results = -1
        self.nms_rq_dry_results = -1
        self.LOCnmsdry_results = ''
        self.nms_rq_semi_results = -1
        self.LOCnmssemi_results = ''
        self.nms_rq_spray_results = -1
        self.LOCnmsspray_results = ''
        self.lms_rq_dry_results = -1
        self.LOClmsdry_results = ''
        self.lms_rq_semi_results = -1
        self.LOClmssemi_results = ''
        self.lms_rq_spray_results = -1
        self.LOClmsspray_results = ''
        self.nds_rq_dry_results = -1
        self.LOCndsdry_results = ''
        self.nds_rq_semi_results = -1
        self.LOCndssemi_results = ''
        self.nds_rq_spray_results = -1
        self.LOCndsspray_results = ''
        self.lds_rq_dry_results = -1
        self.LOCldsdry_results = ''
        self.lds_rq_semi_results = -1
        self.LOCldssemi_results = ''
        self.lds_rq_spray_results = -1
        self.LOCldsspray_results = ''

        self.rundry_results_expected = -1
        self.runsemi_results_expected = -1
        self.spray_results_expected = -1
        self.totaldry_results_expected = -1
        self.totalsemi_results_expected = -1
        self.nms_rq_dry_results_expected = -1
        self.nms_rq_semi_results_expected = -1
        self.nms_rq_spray_results_expected = -1
        self.lms_rq_dry_results_expected = -1
        self.lms_rq_semi_results_expected = -1
        self.lms_rq_spray_results_expected = -1
        self.nds_rq_dry_results_expected = -1
        self.nds_rq_semi_results_expected = -1
        self.nds_rq_spray_results_expected = -1
        self.lds_rq_dry_results_expected = -1
        self.lds_rq_semi_results_expected = -1
        self.lds_rq_spray_results_expected = -1
        self.run_methods()

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
        try:
            self.application_rate = float(self.application_rate)
            self.incorporation_depth = float(self.incorporation_depth)
            self.runoff_fraction = float(self.runoff_fraction)
        except ZeroDivisionError:
            raise ZeroDivisionError\
            ('The incorporation_depth must be non-zero.')
        except IndexError:
            raise IndexError\
            ('The application rate, incorporation_depth, and/or runoff fraction must be supplied on the command line. ')
        except ValueError:
            raise ValueError\
            ('The application rate, incorporation_depth, and/or runoff fraction must be a real number')
        except TypeError:
            raise TypeError\
            ('The application rate, incorporation_depth, and/or runoff fraction must be an integer or string')
        if self.application_rate < 0:
            raise ValueError\
            ('application_rate must be positive.')
        if self.incorporation_depth == 0:
            raise ZeroDivisionError\
            ('incorporation_depth must not equal zero.')
        if self.incorporation_depth < 0:
            raise ValueError\
            ('incorporation_depth must be positive.')
        if self.runoff_fraction < 0:
            raise ValueError\
            ('runoff_fraction must be positive.')
        if self.rundry_results == -1:
            self.rundry_results = (self.application_rate/self.incorporation_depth) * self.runoff_fraction
        return self.rundry_results

    # EEC for runoff to semi-aquatic areas
    def runsemi(self):
        try:
            self.application_rate = float(self.application_rate)
            self.incorporation_depth = float(self.incorporation_depth)
            self.runoff_fraction = float(self.runoff_fraction)
        except ZeroDivisionError:
            raise ZeroDivisionError\
            ('The incorporation_depth must be non-zero.')
        except IndexError:
            raise IndexError\
            ('The application rate, incorporation_depth, and/or runoff fraction must be supplied on the command line. ')
        except ValueError:
            raise ValueError\
            ('The application rate, incorporation_depth, and/or runoff fraction must be a real number')
        if self.application_rate < 0:
            raise ValueError\
            ('application_rate must be positive.')
        if self.incorporation_depth == 0:
            raise ZeroDivisionError\
            ('incorporation_depth must not equal zero.')
        if self.incorporation_depth < 0:
            raise ValueError\
            ('incorporation_depth must be positive.')
        if self.runoff_fraction < 0:
            raise ValueError\
            ('runoff_fraction must be positive.')
        if self.runsemi_results == -1:
            self.runsemi_results = (self.application_rate/self.incorporation_depth) * self.runoff_fraction * 10
        return self.runsemi_results

    # EEC for spray drift
    def spray(self):
        try:
            self.application_rate = float(self.application_rate)
            self.drift_fraction = float(self.drift_fraction)
        except ZeroDivisionError:
            raise ZeroDivisionError\
            ('The incorporation_depth must be non-zero.')
        except IndexError:
            raise IndexError\
            ('The application rate, incorporation_depth, and/or runoff fraction must be supplied on the command line. ')
        except ValueError:
            raise ValueError\
            ('The application rate, incorporation_depth, and/or runoff fraction must be a real number')
        if self.application_rate < 0:
            raise ValueError\
            ('application_rate must be positive.')
        if self.drift_fraction < 0:
            raise ValueError\
            ('drift_fraction must be positive.')
        if self.spray_results == -1:
            self.spray_results = self.application_rate * self.drift_fraction
        return self.spray_results

    # EEC total for dry areas
    def totaldry(self):
        if self.totaldry_results == -1:
            try:
                if self.rundry_results == -1:
                    self.rundry()
                if self.spray_results == -1:
                    self.spray()
                if self.rundry_results == None or self.spray_results == None:
                    raise ValueError\
                    ('Either the rundry or spray variables equals None and therefor this function cannot be run.')
                self.totaldry_results = self.rundry_results + self.spray_results
            except ZeroDivisionError:
                raise ZeroDivisionError\
                ('The incorporation_depth must be non-zero.')
        return self.totaldry_results


    # EEC total for semi-aquatic areas
    def totalsemi (self):
        if self.totalsemi_results == -1:
            try:
                if self.runsemi_results == -1:
                    self.runsemi()
                if self.spray_results == -1:
                    self.spray()
                if self.runsemi_results == None or self.spray_results == None:
                    raise ValueError\
                    ('Either the runsemi or spray variables equals None and therefor this function cannot be run.')
                self.totalsemi_results = self.runsemi_results + self.spray_results
            except ZeroDivisionError:
                raise ZeroDivisionError\
                ('The incorporation_depth must be non-zero.')
        return self.totalsemi_results


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

    def nms_rq_dry(self):
        if self.nms_rq_dry_results == -1:
            try:
                self.ec25_nonlisted_seedling_emergence_monocot = float(self.ec25_nonlisted_seedling_emergence_monocot)
                self.totaldry_results = float(self.totaldry_results)
            except ValueError:
                raise ValueError\
                ('The application rate, incorporation_depth, and/or runoff fraction must be a real number')
            except TypeError:
                raise TypeError\
                ('totaldry equals None and therefor this function cannot be run.')
            except IndexError:
                raise IndexError\
                ('The total amount of runoff and spray to semi-aquatic areas be supplied on the command line. ')
            except ZeroDivisionError:
                raise ZeroDivisionError\
                ('The incorporation_depth must be non-zero.')
            if self.ec25_nonlisted_seedling_emergence_monocot < 0:
                raise ValueError\
                ('ec25_nonlisted_seedling_emergence_monocot=%g is a non-physical value' %self.ec25_nonlisted_seedling_emergence_monocot)
            if self.totaldry_results == -1:
                self.totaldry()
            if self.totaldry_results == None:
                raise ValueError\
                ('Either the totaldry_results variable equals None and therefor this function cannot be run.')
            self.nms_rq_dry_results = self.totaldry_results/self.ec25_nonlisted_seedling_emergence_monocot
        return self.nms_rq_dry_results


    # Level of concern for non-listed monocot seedlings exposed to pesticide X in a dry area

    def LOCnmsdry(self):
        if self.LOCnmsdry_results == '':
            try:
                if self.nms_rq_dry_results == -1:
                    try:
                        self.nms_rq_dry()
                    except TypeError:
                        raise TypeError\
                        ('totaldry equals None and therefor this function cannot be run.')
                if self.nms_rq_dry_results == None:
                    raise ValueError\
                    ('nms_rq_dry variable equals None and therefor this function cannot be run.')
                elif self.nms_rq_dry_results >= 1.0:
                    self.LOCnmsdry_results = ('The risk quotient for non-listed monocot seedlings exposed to'\
                    ' the pesticide via runoff to a dry area indicates a potential risk.')
                else:
                    self.LOCnmsdry_results = ('The risk quotient for non-listed monocot seedlings exposed to'\
                    ' the pesticide via runoff to a dry area indicates that potential risk is minimal.')
            except ZeroDivisionError:
                raise ZeroDivisionError\
                ('The incorporation_depth must be non-zero.')
        return self.LOCnmsdry_results

    # Risk Quotient for NON-LISTED MONOCOT seedlings exposed to Pesticide X in a SEMI-AQUATIC area

    def nms_rq_semi(self):
        if self.nms_rq_semi_results == -1:
            try:
                self.ec25_nonlisted_seedling_emergence_monocot = float(self.ec25_nonlisted_seedling_emergence_monocot)
                self.totalsemi_results = float(self.totalsemi_results)
            except ValueError:
                raise ValueError\
                ('The application rate, incorporation_depth, and/or runoff fraction must be a real number')             
            except TypeError:
                raise TypeError\
                ('totaldry equals None and therefor this function cannot be run.')
            except IndexError:
                raise IndexError\
                ('The total amount of runoff and spray to semi-aquatic areas be supplied on the command line. ')
            except ZeroDivisionError:
                raise ZeroDivisionError\
                ('The incorporation_depth must be non-zero.')
            if self.ec25_nonlisted_seedling_emergence_monocot < 0:
                raise ValueError\
                ('ec25_nonlisted_seedling_emergence_monocot=%g is a non-physical value' %self.ec25_nonlisted_seedling_emergence_monocot)   
            if self.totalsemi_results == -1:
                self.totalsemi()
            if self.totalsemi_results == None:
                raise ValueError\
                ('Either the totaldry_results variable equals None and therefor this function cannot be run.')
            self.nms_rq_semi_results = self.totalsemi_results/self.ec25_nonlisted_seedling_emergence_monocot
        return self.nms_rq_semi_results

    # Level of concern for non-listed monocot seedlings exposed to pesticide X in a semi-aquatic area
    def LOCnmssemi(self):
        if self.LOCnmssemi_results == '':
            if self.nms_rq_semi_results == -1:
                try:
                    self.nms_rq_semi()
                except TypeError:
                    raise TypeError\
                    ('totaldry equals None and therefor this function cannot be run.')
            if self.nms_rq_semi_results == None:
                raise ValueError\
                ('nms_rq_semi variable equals None and therefor this function cannot be run.')
            if self.nms_rq_semi_results >= 1.0:
                self.LOCnmssemi_results = ('The risk quotient for non-listed monocot seedlings exposed to'\
            ' the pesticide via runoff to a semi-aquatic area indicates a potential risk.')
            else:
                self.LOCnmssemi_results = ('The risk quotient for non-listed monocot seedlings exposed to the'\
            ' pesticide via runoff to a semi-aquatic area indicates that potential risk is minimal.')
        return self.LOCnmssemi_results


    # Risk Quotient for NON-LISTED MONOCOT seedlings exposed to Pesticide X via SPRAY drift
    def nms_rq_spray(self):
        if self.nms_rq_spray_results == -1:
            try:
                self.ec25_nonlisted_seedling_emergence_monocot = float(self.ec25_nonlisted_seedling_emergence_monocot)
                self.spray_results = float(self.spray_results)
            except TypeError:
                raise TypeError\
                ('EEC for spray drift equals None and therefor this function cannot be run.')
            except IndexError:
                raise IndexError\
                ('The EEC for spray drift needs to be supplied on the command line. ')
            except ZeroDivisionError:
                raise ZeroDivisionError\
                ('The incorporation_depth must be non-zero.')
            if self.ec25_nonlisted_seedling_emergence_monocot < 0:
                raise ValueError\
                ('ec25_nonlisted_seedling_emergence_monocot=%g is a non-physical value' %self.ec25_nonlisted_seedling_emergence_monocot)   
            if self.spray_results == -1:
                self.spray()
            if self.spray_results == None:
                raise ValueError\
                ('Either the spray_results variable equals None and therefor this function cannot be run.')
            self.nms_rq_spray_results = self.spray_results/self.ec25_nonlisted_seedling_emergence_monocot
        return self.nms_rq_spray_results

    # Level of concern for non-listed monocot seedlings exposed to pesticide via spray drift
    def LOCnmsspray(self):
        if self.LOCnmsspray_results == '':
            if self.nms_rq_spray_results == -1:
                try:
                    self.nms_rq_spray()
                except TypeError:
                    raise TypeError\
                    ('totaldry equals None and therefor this function cannot be run.')
            if self.nms_rq_spray_results == None:
                raise ValueError\
                ('nms_rq_spray_results variable equals None and therefor this function cannot be run.')
            if self.nms_rq_spray_results >= 1.0:
                self.LOCnmsspray_results = ('The risk quotient for non-listed monocot seedlings exposed to'\
            ' the pesticide via spray drift indicates a potential risk.')
            else:
                self.LOCnmsspray_results = ('The risk quotient for non-listed monocot seedlings exposed to the'\
            ' pesticide via spray drift indicates that potential risk is minimal.')
        return self.LOCnmsspray_results


    # Risk Quotient for LISTED MONOCOT seedlings exposed to Pesticide X in a DRY areas
    def lms_rq_dry(self):
        if self.lms_rq_dry_results == -1:
            try:
                self.ec25_nonlisted_seedling_emergence_dicot = float(self.ec25_nonlisted_seedling_emergence_dicot)
                self.totaldry_results = float(self.totaldry_results)
            except TypeError:
                raise TypeError\
                ('totaldry equals None and therefor this function cannot be run.')
            except IndexError:
                raise IndexError\
                ('The total amount of runoff and spray to dry areas needs to be supplied on the command line. ')
            except ValueError:
                raise ValueError\
                ('The total amount of runoff and spray to dry areas must be a real number,'\
                ' not "%lbs ai/A"' %self.totaldry_results)
            except ZeroDivisionError:
                raise ZeroDivisionError\
                ('The incorporation_depth must be non-zero.')
            if self.ec25_nonlisted_seedling_emergence_dicot < 0:
                raise ValueError\
                ('ec25_nonlisted_seedling_emergence_dicot=%g is a non-physical value' %self.ec25_nonlisted_seedling_emergence_dicot)   
            if self.totaldry_results == -1:
                self.totaldry()
            if self.totaldry_results == None:
                raise ValueError\
                ('Either the spray_results variable equals None and therefor this function cannot be run.')
            self.lms_rq_dry_results = self.totaldry_results/self.ec25_nonlisted_seedling_emergence_dicot
        return self.lms_rq_dry_results

    # Level of concern for listed monocot seedlings exposed to pesticide
    #  via runoff in a dry area
    def LOClmsdry(self):
        if self.LOClmsdry_results == '':
            if self.lms_rq_dry_results == -1:
                try:
                    self.lms_rq_dry()
                except TypeError:
                    raise TypeError\
                    ('totaldry equals None and therefor this function cannot be run.')
            if self.lms_rq_dry_results == None:
                raise ValueError\
                ('lms_rq_dry_results variable equals None and therefor this function cannot be run.')
            if self.lms_rq_dry_results >= 1.0:
                self.LOClmsdry_results = ('The risk quotient for listed monocot seedlings exposed to'\
            ' the pesticide via runoff to a dry area indicates a potential risk.')
            else:
                self.LOClmsdry_results = ('The risk quotient for listed monocot seedlings exposed to the'\
            ' pesticide via runoff to a dry area indicates that potential risk is minimal.')
        return self.LOClmsdry_results


    # Risk Quotient for LISTED MONOCOT seedlings exposed to Pesticide X in a SEMI-AQUATIC area
    def lms_rq_semi(self):
        if self.lms_rq_semi_results == -1:
            try:
                self.ec25_nonlisted_seedling_emergence_dicot = float(self.ec25_nonlisted_seedling_emergence_dicot)
                self.totalsemi_results = float(self.totalsemi_results)
            except TypeError:
                raise TypeError\
                ('totaldry equals None and therefor this function cannot be run.')
            except IndexError:
                raise IndexError\
                ('The total amount of runoff and spray to semi-aquatic areas needs to be supplied on the command line. ')
            except ValueError:
                raise ValueError\
                ('The total amount of runoff and spray to semi-aquatic areas must be a real number,'\
                ' not "%lbs ai/A"' %self.totalsemi_results)
            except ZeroDivisionError:
                raise ZeroDivisionError\
                ('The incorporation_depth must be non-zero.')
            if self.ec25_nonlisted_seedling_emergence_dicot < 0:
                raise ValueError\
                ('ec25_nonlisted_seedling_emergence_monocot=%g is a non-physical value' %self.ec25_nonlisted_seedling_emergence_dicot)   
            if self.totalsemi_results == -1:
                self.totalsemi()
            if self.totalsemi_results == None:
                raise ValueError\
                ('Either the totalsemi_results variable equals None and therefor this function cannot be run.')
            self.lms_rq_semi_results = self.totalsemi_results/self.ec25_nonlisted_seedling_emergence_dicot
        return self.lms_rq_semi_results

    # Level of concern for listed monocot seedlings exposed to pesticide X in semi-aquatic areas
    def LOClmssemi(self):
        if self.LOClmssemi_results == '':
            if self.lms_rq_semi_results == -1:
                try:
                    self.lms_rq_semi()
                except TypeError:
                    raise TypeError\
                    ('totaldry equals None and therefor this function cannot be run.')
            if self.lms_rq_semi_results == None:
                raise ValueError\
                ('lms_rq_semi variable equals None and therefor this function cannot be run.')
            if self.lms_rq_semi_results >= 1.0:
                self.LOClmssemi_results = ('The risk quotient for listed monocot seedlings exposed to'\
            ' the pesticide via runoff to a semi-aquatic area indicates a potential risk.')
            else:
                self.LOClmssemi_results = ('The risk quotient for listed monocot seedlings exposed to the'\
            ' pesticide via runoff to a semi-aquatic area indicates that potential risk is minimal.')
        return self.LOClmssemi_results


    # Risk Quotient for LISTED MONOCOT seedlings exposed to Pesticide X via SPRAY drift
    def lms_rq_spray(self):
        if self.lms_rq_spray_results == -1:
            try:
                self.ec25_nonlisted_seedling_emergence_dicot = float(self.ec25_nonlisted_seedling_emergence_dicot)
                self.spray_results = float(self.spray_results)
            except TypeError:
                raise TypeError\
                ('spray_results equals None and therefor this function cannot be run.')
            except IndexError:
                raise IndexError\
                ('The amount of spray drift exposure needs to be supplied on the command line. ')
            except ValueError:
                raise ValueError\
                ('The amount of spray drift exposure must be a real number, not "%lbs ai/A"' %spray_results)
            except ZeroDivisionError:
                raise ZeroDivisionError\
                ('The incorporation_depth must be non-zero.')
            if self.ec25_nonlisted_seedling_emergence_dicot < 0:
                raise ValueError\
                ('ec25_nonlisted_seedling_emergence_monocot=%g is a non-physical value' %self.ec25_nonlisted_seedling_emergence_dicot)  
            if self.spray_results == -1:
                self.spray()
            if self.spray_results == None:
                raise ValueError\
                ('The spray_results variable equals None and therefor this function cannot be run.')
            self.lms_rq_spray_results = self.spray_results/self.ec25_nonlisted_seedling_emergence_dicot
        return self.lms_rq_spray_results

    # Level of concern for listed monocot seedlings exposed to pesticide X via spray drift
    def LOClmsspray(self):
        if self.LOClmsspray_results == '':
            if self.lms_rq_spray_results == -1:
                try:
                    self.lms_rq_spray()
                except TypeError:
                    raise TypeError\
                    ('totaldry equals None and therefor this function cannot be run.')
            if self.lms_rq_spray_results == None:
                raise ValueError\
                ('lms_rq_spray variable equals None and therefor this function cannot be run.')
            if self.lms_rq_spray_results >= 1.0:
                self.LOClmsspray_results = ('The risk quotient for listed monocot seedlings exposed to'\
            ' the pesticide via spray drift indicates a potential risk.')
            else:
                self.LOClmsspray_results = ('The risk quotient for listed monocot seedlings exposed to the'\
            ' pesticide via spray drift indicates that potential risk is minimal.')
        return self.LOClmsspray_results


    # Risk Quotient for NON-LISTED DICOT seedlings exposed to Pesticide X in DRY areas
    def nds_rq_dry(self):
        if self.nds_rq_dry_results == -1:
            try:
                self.noaec_listed_seedling_emergence_monocot = float(self.noaec_listed_seedling_emergence_monocot)
                self.totaldry_results = float(self.totaldry_results)
            except TypeError:
                raise TypeError\
                ('totaldry_results equals None and therefor this function cannot be run.')
            except IndexError:
                raise IndexError\
                ('The amount of runoff and spray to dry areas needs to be supplied on the command line. ')
            except ValueError:
                raise ValueError\
                ('The total amount of runoff and spray to dry areas must be a real number, not "%lbs ai/A"' %totaldry_results)
            except ZeroDivisionError:
                raise ZeroDivisionError\
                ('The incorporation_depth must be non-zero.')
            if self.noaec_listed_seedling_emergence_monocot < 0:
                raise ValueError\
                ('noaec_listed_seedling_emergence_monocot=%g is a non-physical value' %self.noaec_listed_seedling_emergence_monocot)  
            if self.totaldry_results == -1:
                self.totaldry()
            if self.totaldry_results == None:
                raise ValueError\
                ('The totaldry_results variable equals None and therefor this function cannot be run.')
            self.nds_rq_dry_results = self.totaldry_results/self.noaec_listed_seedling_emergence_monocot
        return self.nds_rq_dry_results

    # Level of concern for non-listed dicot seedlings exposed to pesticide X in dry areas
    def LOCndsdry(self):
        if self.LOCndsdry_results == '':
            if self.nds_rq_dry_results == -1:
                try:
                    self.nds_rq_dry()
                except TypeError:
                    raise TypeError\
                    ('totaldry equals None and therefor this function cannot be run.')
            if self.nds_rq_dry_results == None:
                raise ValueError\
                ('nds_rq_dry_results variable equals None and therefor this function cannot be run.')
            if self.nds_rq_dry_results >= 1.0:
                self.LOCndsdry_results = ('The risk quotient for non-listed monocot seedlings exposed to'\
            ' the pesticide via runoff to dry areas indicates a potential risk.')
            else:
                self.LOCndsdry_results = ('The risk quotient for non-listed monocot seedlings exposed to the'\
            ' pesticide via runoff to dry areas indicates that potential risk is minimal.')
        return self.LOCndsdry_results


    # Risk Quotient for NON-LISTED DICOT seedlings exposed to Pesticide X in SEMI-AQUATIC areas
    def nds_rq_semi(self):
        if self.nds_rq_semi_results == -1:
            try:
                self.noaec_listed_seedling_emergence_monocot = float(self.noaec_listed_seedling_emergence_monocot)
                self.totalsemi_results = float(self.totalsemi_results)
            except TypeError:
                raise TypeError\
                ('totalsemi_results equals None and therefor this function cannot be run.')
            except IndexError:
                raise IndexError\
                ('The total amount of runoff and spray to semi-aquatic areas needs to be supplied on the command line. ')
            except ValueError:
                raise ValueError\
                ('The total amount of runoff and spray to semi-aquatic areas must be a real number, not "%lbs ai/A"' %totaldry_results)
            except ZeroDivisionError:
                raise ZeroDivisionError\
                ('The incorporation_depth must be non-zero.')
            if self.noaec_listed_seedling_emergence_monocot < 0:
                raise ValueError\
                ('noaec_listed_seedling_emergence_monocot=%g is a non-physical value' %self.noaec_listed_seedling_emergence_monocot)  
            if self.totaldry_results == -1:
                self.totalsemi()
            if self.totaldry_results == None:
                raise ValueError\
                ('The totalsemi_results variable equals None and therefor this function cannot be run.')
            self.nds_rq_semi_results = self.totalsemi_results/self.noaec_listed_seedling_emergence_monocot
        return self.nds_rq_semi_results

    # Level of concern for non-listed dicot seedlings exposed to pesticide X in semi-aquatic areas
    def LOCndssemi(self):
        if self.LOCndssemi_results == '':
            if self.nds_rq_semi_results == -1:
                try:
                    self.nds_rq_semi()
                except TypeError:
                    raise TypeError\
                    ('totaldry equals None and therefor this function cannot be run.')
            if self.nds_rq_semi_results == None:
                raise ValueError\
                ('nds_rq_semi_results variable equals None and therefor this function cannot be run.')
            if self.nds_rq_semi_results >= 1.0:
                self.LOCndssemi_results = ('The risk quotient for non-listed monocot seedlings exposed to'\
            ' the pesticide via runoff to semi-aquatic areas indicates a potential risk.')
            else:
                self.LOCndssemi_results = ('The risk quotient for non-listed monocot seedlings exposed to the'\
            ' pesticide via runoff to semi-aquatic areas indicates that potential risk is minimal.')
        return self.LOCndssemi_results

    # Risk Quotient for NON-LISTED DICOT seedlings exposed to Pesticide X via SPRAY drift
    def nds_rq_spray(self):
        if self.nds_rq_spray_results == -1:
            try:
                self.noaec_listed_seedling_emergence_monocot = float(self.noaec_listed_seedling_emergence_monocot)
                self.spray_results = float(self.spray_results)
            except TypeError:
                raise TypeError\
                ('spray_results equals None and therefor this function cannot be run.')
            except IndexError:
                raise IndexError\
                ('The the amount of spray drift exposure needs to be supplied on the command line. ')
            except ValueError:
                raise ValueError\
                ('The the amount of spray drift exposure areas must be a real number, not "%lbs ai/A"' %spray_results)
            except ZeroDivisionError:
                raise ZeroDivisionError\
                ('The incorporation_depth must be non-zero.')
            if self.noaec_listed_seedling_emergence_monocot < 0:
                raise ValueError\
                ('noaec_listed_seedling_emergence_monocot=%g is a non-physical value' %self.noaec_listed_seedling_emergence_monocot)
            if self.spray_results == -1:
                self.spray()
            if self.spray_results == None:
                raise ValueError\
                ('The spray_results variable equals None and therefor this function cannot be run.')
            self.nds_rq_spray_results = self.spray_results/self.noaec_listed_seedling_emergence_monocot
        return self.nds_rq_spray_results

    # Level of concern for non-listed dicot seedlings exposed to pesticide X via spray drift
    def LOCndsspray(self):
        if self.LOCndssemi_results == '':
            if self.nds_rq_spray_results == -1:
                try:
                    self.nds_rq_spray()
                except TypeError:
                    raise TypeError\
                    ('totaldry equals None and therefor this function cannot be run.')
            if self.nds_rq_spray_results == None:
                raise ValueError\
                ('nds_rq_spray_results variable equals None and therefor this function cannot be run.')
            if self.nds_rq_spray_results >= 1.0:
                self.LOCndssemi_results = ('The risk quotient for non-listed monocot seedlings exposed to'\
            ' the pesticide via spray drift indicates a potential risk.')
            else:
                self.LOCndssemi_results = ('The risk quotient for non-listed monocot seedlings exposed to the'\
            ' pesticide via spray drift indicates that potential risk is minimal.')
        return self.LOCndssemi_results

    # Risk Quotient for LISTED DICOT seedlings exposed to Pesticide X in DRY areas
    def lds_rq_dry(self):
        if self.lds_rq_dry_results == -1:
            try:
                self.noaec_listed_seedling_emergence_dicot = float(self.noaec_listed_seedling_emergence_dicot)
                self.totaldry_results = float(self.totaldry_results)
            except TypeError:
                raise TypeError\
                ('totaldry_results equals None and therefor this function cannot be run.')
            except IndexError:
                raise IndexError\
                ('The total amount of runoff and spray to dry areas needs to be supplied on the command line. ')
            except ValueError:
                raise ValueError\
                ('The total amount of runoff and spray to dry areas must be a real number, not "%lbs ai/A"' %totaldry_results)
            except ZeroDivisionError:
                raise ZeroDivisionError\
                ('The incorporation_depth must be non-zero.')
            if self.noaec_listed_seedling_emergence_dicot < 0:
                raise ValueError\
                ('noaec_listed_seedling_emergence_dicot=%g is a non-physical value' %self.noaec_listed_seedling_emergence_dicot)
            if self.totaldry_results == -1:
                self.totaldry()
            if self.totaldry_results == None:
                raise ValueError\
                ('The totaldry_results variable equals None and therefor this function cannot be run.')
            self.lds_rq_dry_results = self.totaldry_results/self.noaec_listed_seedling_emergence_dicot
        return self.lds_rq_dry_results

    # Level of concern for listed dicot seedlings exposed to pesticideX in dry areas
    def LOCldsdry(self):
        if self.LOCldsdry_results == '':
            if self.lds_rq_dry_results == -1:
                try:
                    self.lds_rq_dry()
                except TypeError:
                    raise TypeError\
                    ('totaldry equals None and therefor this function cannot be run.')
            if self.lds_rq_dry_results == None:
                raise ValueError\
                ('lds_rq_dry_results variable equals None and therefor this function cannot be run.')
            if self.lds_rq_dry_results >= 1.0:
                self.LOCldsdry_results = ('The risk quotient for listed monocot seedlings exposed to'\
            ' the pesticide via runoff to dry areas indicates a potential risk.')
            else:
                self.LOCldsdry_results = ('The risk quotient for listed monocot seedlings exposed to the'\
            ' pesticide via runoff to dry areas indicates that potential risk is minimal.')
        return self.LOCldsdry_results

    # Risk Quotient for LISTED DICOT seedlings exposed to Pesticide X in SEMI-AQUATIC areas
    def lds_rq_semi(self):
        if self.lds_rq_semi_results == -1:
            try:
                self.noaec_listed_seedling_emergence_dicot = float(self.noaec_listed_seedling_emergence_dicot)
                self.totalsemi_results = float(self.totalsemi_results)
            except TypeError:
                raise TypeError\
                ('totalsemi_results equals None and therefor this function cannot be run.')
            except IndexError:
                raise IndexError\
                ('The total amount of runoff and spray to semi-aquatic areas needs to be supplied on the command line. ')
            except ValueError:
                raise ValueError\
                ('The total amount of runoff and spray to semi-aquatic areas must be a real number, not "%lbs ai/A"' %totaldry)
            except ZeroDivisionError:
                raise ZeroDivisionError\
                ('The incorporation_depth must be non-zero.')
            if self.noaec_listed_seedling_emergence_dicot < 0:
                raise ValueError\
                ('noaec_listed_seedling_emergence_dicot=%g is a non-physical value' %self.noaec_listed_seedling_emergence_dicot)
            if self.totalsemi_results == -1:
                self.totalsemi()
            if self.totalsemi_results == None:
                raise ValueError\
                ('The totalsemi_results variable equals None and therefor this function cannot be run.')
            self.lds_rq_semi_results = self.totalsemi_results/self.noaec_listed_seedling_emergence_dicot
        return self.lds_rq_semi_results

    # Level of concern for listed dicot seedlings exposed to pesticide X in dry areas
    def LOCldssemi(self):
        if self.LOCldssemi_results == '':
            if self.lds_rq_semi_results == -1:
                try:
                    self.lds_rq_semi()
                except TypeError:
                    raise TypeError\
                    ('totaldry equals None and therefor this function cannot be run.')
            if self.lds_rq_semi_results == None:
                raise ValueError\
                ('lds_rq_semi_results variable equals None and therefor this function cannot be run.')
            if self.lds_rq_semi_results >= 1.0:
                self.LOCldssemi_results = ('The risk quotient for listed monocot seedlings exposed to'\
            ' the pesticide via runoff to semi-aquatic areas indicates a potential risk.')
            else:
                self.LOCldssemi_results = ('The risk quotient for listed monocot seedlings exposed to the'\
            ' pesticide via runoff to semi-aquatic areas indicates that potential risk is minimal.')
        return self.LOCldssemi_results

    # Risk Quotient for LISTED DICOT seedlings exposed to Pesticide X via SPRAY drift
    def lds_rq_spray(self):
        if self.lds_rq_spray_results == -1:
            try:
                self.noaec_listed_seedling_emergence_dicot = float(self.noaec_listed_seedling_emergence_dicot)
                self.spray_results = float(self.spray_results)
            except TypeError:
                raise TypeError\
                ('spray_results equals None and therefor this function cannot be run.')
            except IndexError:
                raise IndexError\
                ('The amount of spray drift exposure needs to be supplied on the command line. ')
            except ValueError:
                raise ValueError\
                ('The amount of spray drift exposure must be a real number, not "%lbs ai/A"' %spray_results)
            except ZeroDivisionError:
                raise ZeroDivisionError\
                ('The incorporation_depth must be non-zero.')
            if self.noaec_listed_seedling_emergence_dicot < 0:
                raise ValueError\
                ('noaec_listed_seedling_emergence_dicot=%g is a non-physical value' %self.noaec_listed_seedling_emergence_dicot)
            if self.spray_results == -1:
                self.spray()
            if self.spray_results == None:
                raise ValueError\
                ('The spray_results variable equals None and therefor this function cannot be run.')
            self.lds_rq_spray_results = self.spray_results/self.noaec_listed_seedling_emergence_dicot
        return self.lds_rq_spray_results

    # Level of concern for listed dicot seedlings exposed to pesticide X via spray drift
    def LOCldsspray(self):
        if self.LOCldsspray_results == '':
            if self.lds_rq_spray_results == -1:
                try:
                    self.lds_rq_spray()
                except TypeError:
                    raise TypeError\
                    ('totaldry equals None and therefor this function cannot be run.')
            if self.lds_rq_spray_results == None:
                raise ValueError\
                ('lds_rq_spray_results variable equals None and therefor this function cannot be run.')
            if self.lds_rq_spray_results >= 1.0:
                self.LOCldsspray_results = ('The risk quotient for listed monocot seedlings exposed to'\
            ' the pesticide via spray drift indicates a potential risk.')
            else:
                self.LOCldsspray_results = ('The risk quotient for listed monocot seedlings exposed to the'\
            ' pesticide via spray drift indicates that potential risk is minimal.')
        return self.LOCldsspray_results


