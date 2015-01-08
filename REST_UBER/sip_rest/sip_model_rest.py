
class sip(object):
    def __init__(self, chemical_name, bodyweight_tested_bird, bodyweight_quail, bodyweight_duck, bodyweight_bird_other, 
                    bodyweight_rat, bodyweight_tested_mammal_other, species_tested_bird, species_tested_mammal, 
                    bodyweight_tested_mammal, solubility, ld50_avian_water, ld50_mammal_water, bodyweight_assessed_bird, 
                    mineau_scaling_factor, bodyweight_assessed_mammal, noael_avian_water, noael_mammal_water):
        
        self.chemical_name = chemical_name
        self.solubility = solubility

        self.species_tested_bird = species_tested_bird
        self.bodyweight_tested_bird = bodyweight_tested_bird
        self.bodyweight_quail = bodyweight_quail
        self.bodyweight_duck = bodyweight_duck
        self.bodyweight_bird_other = bodyweight_bird_other
        self.bodyweight_assessed_bird = bodyweight_assessed_bird        
        self.ld50_avian_water = ld50_avian_water
        self.noael_avian_water = noael_avian_water

        self.species_tested_mammal = species_tested_mammal
        self.bodyweight_tested_mammal = bodyweight_tested_mammal        
        self.bodyweight_rat = bodyweight_rat
        self.bodyweight_tested_mammal_other = bodyweight_tested_mammal_other
        self.bodyweight_assessed_mammal = bodyweight_assessed_mammal
        self.ld50_mammal_water = ld50_mammal_water        
        self.noael_mammal_water = noael_mammal_water

        self.mineau_scaling_factor = mineau_scaling_factor

        #Result variables
        self.fw_bird_out = -1
        self.fw_mamm_out = -1
        self.dose_bird_out = -1
        self.dose_mamm_out = -1
        self.at_bird_out = -1
        self.at_mamm_out = -1
        self.fi_bird_out = -1
        self.det_out = -1
        self.act_out = -1
        self.acute_bird_out = -1
        self.acuconb_out = -1
        self.acute_mamm_out = -1
        self.acuconm_out = -1
        self.chron_bird_out = -1
        self.chronconb_out = -1
        self.chron_mamm_out = -1
        self.chronconm_out = -1
        self.run_methods()

    def run_methods(self):
        self.fw_bird()
        self.fw_mamm()
        self.dose_bird()
        self.dose_mamm()
        self.at_bird()
        self.at_mamm()
        self.fi_bird()
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

    def fw_bird(self):
        if self.fw_bird_out == -1:
            try:
                self.bodyweight_assessed_bird = float(self.bodyweight_assessed_bird)
            except IndexError:
                raise IndexError\
                ('The body weight of the bird must be supplied on the command line.')
            except ValueError:
                raise ValueError\
                ('The body weight of the bird must be a real number, not "%g"' % self.bodyweight_assessed_bird)
            if self.bodyweight_assessed_bird < 0:
                raise ValueError\
                ('self.bodyweight_assessed_bird=%g is a non-physical value.' % self.bodyweight_assessed_bird)
            self.fw_bird_out = (1.180 * (self.bodyweight_assessed_bird**0.874))/1000.0
        return self.fw_bird_out

    # Daily water intake rate for mammals

    def fw_mamm(self):
        if self.fw_mamm_out == -1:
            try:
                self.bodyweight_assessed_mammal = float(self.bodyweight_assessed_mammal)
            except IndexError:
                raise IndexError\
                ('The body weight of the mammal must be supplied on the command line.')
            except ValueError:
                raise ValueError\
                ('The body weight of the mammal must be a real number, not "%g"' % self.bodyweight_assessed_mammal)
            if self.bodyweight_assessed_mammal < 0:
                raise ValueError\
                ('self.bodyweight_assessed_mammal=%g is a non-physical value.' % self.bodyweight_assessed_mammal)
            self.fw_mamm_out = (0.708 * (self.bodyweight_assessed_mammal**0.795))/1000.0
        return self.fw_mamm_out

    # Upper bound estimate of exposure for birds

    def dose_bird(self):
        if self.dose_bird_out == -1:
            try:
                self.fw_bird_out = float(self.fw_bird_out)
                self.solubility = float(self.solubility)
                self.bodyweight_assessed_bird = float(self.bodyweight_assessed_bird)
            except IndexError:
                raise IndexError\
                ('The daily water intake for birds, chemical solubility, and/or'\
                ' the body weight of the bird must be supplied on the command line.')
            except ValueError:
                raise ValueError\
                ('The daily water intake for birds must be a real number, '\
                'not "%L"' %self.fw_bird)
            except ValueError:
                raise ValueError\
                ('The chemical solubility must be a real number, not "%mg/L"' %self.solubility)
            except ValueError:
                raise ValueError\
                ('The body weight of the bird must be a real number, not "%g"' %self.bodyweight_assessed_bird)
            except ZeroDivisionError:
                raise ZeroDivisionError\
                ('The body weight of the bird must non-zero.')
            if self.fw_bird_out < 0:
                raise ValueError\
                ('fw_bird=%g is a non-physical value.' % self.fw_bird_out)
            if self.solubility < 0:
                raise ValueError\
                ('solubility=%g is a non-physical value.' % self.solubility)
            if self.bodyweight_assessed_bird < 0:
                raise ValueError\
                ('self.bodyweight_assessed_bird=%g is a non-physical value.' % self.bodyweight_assessed_bird)
            self.dose_bird_out = (self.fw_bird_out * self.solubility)/(self.bodyweight_assessed_bird / 1000)
        return self.dose_bird_out


    # Upper bound estimate of exposure for mammals

    def dose_mamm(self):
        if self.dose_mamm_out == -1:
            try:
                self.fw_mamm_out = float(self.fw_mamm_out)
                self.solubility = float(self.solubility)
                self.bodyweight_assessed_mammal = float(self.bodyweight_assessed_mammal)
            except IndexError:
                raise IndexError\
                ('The daily water intake for mammals, chemical solubility, and/or'\
                ' the body weight of the mammal must be supplied on the command line.')
            except ValueError:
                raise ValueError\
                ('The daily water intake for mammals must be a real number, '\
                'not "%L"' %self.fw_mamm)
            except ValueError:
                raise ValueError\
                ('The chemical solubility must be a real number, not "%mg/L"' %self.solubility)
            except ValueError:
                raise ValueError\
                ('The body weight of the mammal must be a real number, not "%g"' %self.bodyweight_assessed_mammal)
            except ZeroDivisionError:
                raise ZeroDivisionError\
                ('The body weight of the mammal must non-zero.')
            if self.fw_bird_out < 0:
                raise ValueError\
                ('fw_mamm=%g is a non-physical value.' % self.fw_mamm_out)
            if self.solubility < 0:
                raise ValueError\
                ('solubility=%g is a non-physical value.' % self.solubility)
            if self.bodyweight_assessed_mammal < 0:
                raise ValueError\
                ('self.bodyweight_assessed_mammal=%g is a non-physical value.' % self.bodyweight_assessed_mammal)
            self.dose_mamm_out = (self.fw_mamm_out * self.solubility)/(self.bodyweight_assessed_mammal / 1000)
        return self.dose_mamm_out

    # Acute adjusted toxicity value for birds

    def at_bird(self):
        if self.at_bird_out == -1:
            try:
                self.ld50_avian_water = float(self.ld50_avian_water)
                self.bodyweight_assessed_bird = float(self.bodyweight_assessed_bird)
                self.bodyweight_tested_bird = float(self.bodyweight_tested_bird)
                self.mineau_scaling_factor = float(self.mineau_scaling_factor)
            except IndexError:
                raise IndexError\
                ('The lethal dose, body weight of assessed bird, body weight'\
                ' of tested bird, and/or the mineau_scaling_factor scaling factor must be'\
                'supplied the command line.')
            except ValueError:
                raise ValueError\
                ('The mineau_scaling_factor scaling factor must be a real number' %self.mineau_scaling_factor)
            except ValueError:
                raise ValueError\
                ('The lethal dose must be a real number, not "%mg/kg"' %self.ld50_avian_water)
            except ValueError:
                raise ValueError\
                ('The body weight of assessed bird must be a real number, not "%g"' %self.bodyweight_assessed_bird)
            except ValueError:
                raise ValueError\
                ('The body weight of tested bird must be a real number, not "%g"' %self.bodyweight_tested_bird)
            except ZeroDivisionError:
                raise ZeroDivisionError\
                ('The body weight of tested bird must be non-zero.')
            if self.ld50_avian_water < 0:
                raise ValueError\
                ('ld50_avian_water=%g is a non-physical value.' % self.ld50_avian_water)
            if self.bodyweight_assessed_bird < 0:
                raise ValueError\
                ('bodyweight_assessed_bird=%g is a non-physical value.' % self.bodyweight_assessed_bird)
            if self.bodyweight_tested_bird < 0:
                raise ValueError\
                ('bodyweight_tested_bird=%g is a non-physical value.' % self.bodyweight_tested_bird)
            self.at_bird_out = (self.ld50_avian_water) * ((self.bodyweight_assessed_bird/self.bodyweight_tested_bird)**(self.mineau_scaling_factor-1))
        return self.at_bird_out

    # Acute adjusted toxicity value for mammals

    def at_mamm(self):
        if self.at_mamm_out == -1:
            try:
                self.ld50_mammal_water = float(self.ld50_mammal_water)
                self.bodyweight_assessed_mammal = float(self.bodyweight_assessed_mammal)
                self.bodyweight_tested_mammal = float(self.bodyweight_tested_mammal)
            except TypeError:
                raise TypeError\
                ('Either ld50_mammal_water, bodyweight_assessed_mammal or bodyweight_tested_mammal equals None and therefor this function cannot be run.')
            except IndexError:
                raise IndexError\
                ('The lethal dose, body weight of assessed mammal, and/or body weight'\
                ' of tested mammal, must be supplied the command line.')
            except ValueError:
                raise ValueError\
                ('The lethal dose must be a real number, not "%mg/kg"' %self.ld50_mammal_water)
            except ValueError:
                raise ValueError\
                ('The body weight of assessed mammal must be a real number, not "%g"' %self.bodyweight_assessed_mammal)
            except ValueError:
                raise ValueError\
                ('The body weight of tested mammal must be a real number, not "%g"' %self.bodyweight_tested_mammal)
            except ZeroDivisionError:
                raise ZeroDivisionError\
                ('The body weight of tested mammal must be non-zero.')
            if self.ld50_mammal_water < 0:
                raise ValueError\
                ('ld50_mammal_water=%g is a non-physical value.' % self.ld50_mammal_water)
            if self.bodyweight_assessed_mammal < 0:
                raise ValueError\
                ('bodyweight_assessed_mammal=%g is a non-physical value.' % self.bodyweight_assessed_mammal)
            if self.bodyweight_tested_mammal < 0:
                raise ValueError\
                ('bodyweight_tested_mammal=%g is a non-physical value.' % self.bodyweight_tested_mammal)
            self.at_mamm_out = (self.ld50_mammal_water) * ((self.bodyweight_tested_mammal/self.bodyweight_assessed_mammal)**0.25)
        return self.at_mamm_out


    # Adjusted chronic toxicity values for birds

    # FI = Food Intake Rate

    def fi_bird(self):
        if self.fi_bird_out == -1:
            try:
                self.bodyweight_tested_bird = float(self.bodyweight_tested_bird)
            except IndexError:
                raise IndexError\
                ('The body weight of the bird must be supplied the command line.')
            except ValueError:
                raise ValueError\
                ('The body weight must be a real number, not "%kg"' %self.bodyweight_tested_bird)
            if self.bodyweight_tested_bird < 0:
                raise ValueError\
                ('self.bodyweight_tested_bird=%g is a non-physical value.' % self.bodyweight_tested_bird)
            self.fi_bird_out = 0.0582 * ((self.bodyweight_tested_bird / 1000)**0.651)
        return self.fi_bird_out

    # Dose-equivalent chronic toxicity value for birds

    def det(self):
        if self.det_out == -1:
            try:
                self.noael_avian_water = float(self.noael_avian_water)
                self.fi_bird_out = float(self.fi_bird_out)
                self.bodyweight_tested_bird = float(self.bodyweight_tested_bird)
            except IndexError:
                raise IndexError\
                ('The no observed adverse effects concentration, daily food intake'\
                ' rate for birds, and/or body weight of the bird must be supplied the'\
                ' command line.')
            except ValueError:
                raise ValueError\
                ('The NOAEC must be a real number, not "%mg/kg"' % self.noael_avian_water)
            except ValueError:
                raise ValueError\
                ('The dialy food intake rate for birds must be a real number,'\
                ' not "%kg"' % self.fi_bird_out)
            except ValueError:
                raise ValueError\
                ('The body weight of the bird must be a real number, not "%kg"' % self.bodyweight_tested_bird)
            except ZeroDivisionError:
                raise ZeroDivisionError\
                ('The body weight of the bird must be non-zero.')
            if self.noael_avian_water < 0:
                raise ValueError\
                ('noael_avian_water=%g is a non-physical value.' % self.noael_avian_water)
            if self.fi_bird_out < 0:
                raise ValueError\
                ('fi_bird=%g is a non-physical value.' % self.fi_bird_out)
            if self.bodyweight_tested_bird < 0:
                raise ValueError\
                ('self.bodyweight_tested_bird=%g is a non-physical value.' % self.bodyweight_tested_bird)
            self.det_out = (self.noael_avian_water * self.fi_bird_out) / (self.bodyweight_tested_bird / 1000)
        return self.det_out

    # Adjusted chronic toxicty value for mammals

    def act(self):
        if self.act_out == -1:
            try:
                self.noael_mammal_water = float(self.noael_mammal_water)
                self.bodyweight_tested_mammal = float(self.bodyweight_tested_mammal)
                self.bodyweight_assessed_mammal = float(self.bodyweight_assessed_mammal)
            except IndexError:
                raise IndexError\
                ('The no observed adverse effects level, body weight of the tested'\
                ' mammal, and/or body weight of assessed mammal must be supplied the'\
                ' command line.')
            except ValueError:
                raise ValueError\
                ('The NOAEL must be a real number, not "%mg/kg"' % self.noael_mammal_water)
            except ValueError:
                raise ValueError\
                ('The body weight of the tested mammal must be a real number,'\
                ' not "%kg"' % self.bodyweight_tested_mammal)
            except ValueError:
                raise ValueError\
                ('The body weight of the assessed mammal must be a real number,'\
                ' not "%kg"' % self.bodyweight_assessed_mammal)
            except ZeroDivisionError:
                raise ZeroDivisionError\
                ('The body weight of the assessed mammal must be non-zero.')
            if self.noael_mammal_water < 0:
                raise ValueError\
                ('noael_mammal_water=%g is a non-physical value.' % self.noael_mammal_water)
            if self.bodyweight_tested_mammal < 0:
                raise ValueError\
                ('bodyweight_tested_mammal=%g is a non-physical value.' % self.bodyweight_tested_mammal)
            if self.bodyweight_assessed_mammal < 0:
                raise ValueError\
                ('bodyweight_assessed_mammal=%g is a non-physical value.' % self.bodyweight_assessed_mammal)
            self.act_out = (self.noael_mammal_water) * ((self.bodyweight_tested_mammal/self.bodyweight_assessed_mammal)**0.25)
        return self.act_out
        #   MAMMILIAN:  If only a NOAEC value (in mg/kg-diet) is available, the model user should divide the NOAEC by 20 to determine the equivalent chronic daily dose (NOAEL)
    # ---- Is drinking water a concern?

    # Acute exposures for birds


    def acute_bird(self):
        if self.acute_bird_out == -1:
            try:
                self.dose_bird_out = float(self.dose_bird_out)
                self.at_bird_out = float(self.at_bird_out)
            except IndexError:
                raise IndexError\
                ('The upper bound estimate of exposure for birds, and/or the adjusted'\
                ' toxicity value for birds must be supplied the command line.')
            except ValueError:
                raise ValueError\
                ('The upper bound estimate of exposure for birds must be a real'\
                ' number, not "%mg/kg"' % self.dose_bird_out)
            except ValueError:
                raise ValueError\
                ('The adjusted toxicity value for birds must be a real number,'\
                ' not "%mg/kg"' % self.at_bird_out)
            except ZeroDivisionError:
                raise ZeroDivisionError\
                ('The adjusted toxicity value for birds must be non-zero.')
            if self.dose_bird_out < 0:
                raise ValueError\
                ('dose_bird=%g is a non-physical value.' % self.dose_bird_out)
            if self.at_bird_out < 0:
                raise ValueError\
                ('at_bird=%g is a non-physical value.' % self.at_bird_out)
            self.acute_bird_out = self.dose_bird_out/self.at_bird_out
        return self.acute_bird_out


    def acuconb(self):
        if self.acuconb_out == -1:
            if self.acute_bird_out == None:
                raise ValueError\
                ('acute_bird variable equals None and therefor this function cannot be run.')
            if self.acute_bird_out < 0.1:
                self.acuconb_out = ('Drinking water exposure alone is NOT a potential concern for birds')
            else:
                self.acuconb_out = ('Exposure through drinking water alone is a potential concern for birds')
        return self.acuconb_out

    # Acute exposures for mammals

    def acute_mamm(self):
        if self.acute_mamm_out == -1:
            try:
                self.dose_mamm_out = float(self.dose_mamm_out)
                self.at_mamm_out = float(self.at_mamm_out)
            except IndexError:
                raise IndexError\
                ('The upper bound estimate of exposure for mammals, and/or the adjusted'\
                ' toxicity value for mammals must be supplied the command line.')
            except ValueError:
                raise ValueError\
                ('The upper bound estimate of exposure for mammals must be a real'\
                ' number, not "%mg/kg"' % self.dose_mamm_out)
            except ValueError:
                raise ValueError\
                ('The adjusted toxicity value for mammals must be a real number,'\
                ' not "%mg/kg"' % self.at_mamm_out)
            except ZeroDivisionError:
                raise ZeroDivisionError\
                ('The adjusted toxicity value for mammals must be non-zero.')
            if self.dose_mamm_out < 0:
                raise ValueError\
                ('dose_mamm=%g is a non-physical value.' % self.dose_mamm_out)
            if self.at_mamm_out < 0:
                raise ValueError\
                ('at_mamm=%g is a non-physical value.' % self.at_mamm_out)
            self.acute_mamm_out = self.dose_mamm_out/self.at_mamm_out
        return self.acute_mamm_out

    def acuconm(self):
        if self.acuconm_out == -1:
            if self.acute_mamm_out == None:
                raise ValueError\
                ('acute_mamm variable equals None and therefor this function cannot be run.')
            if self.acute_mamm_out < 0.1:
                self.acuconm_out = ('Drinking water exposure alone is NOT a potential concern for mammals')
            else:
                self.acuconm_out = ('Exposure through drinking water alone is a potential concern for mammals')
            return self.acuconm_out
        return self.acuconm_out

    # Chronic Exposures for birds

    def chron_bird(self):
        if self.chron_bird_out == -1:
            try:
                self.dose_bird_out = float(self.dose_bird_out)
                self.det_out = float(self.det_out)
            except TypeError:
                raise TypeError\
                ('Either dose_bird or det equals None and therefor this function cannot be run.')
            except IndexError:
                raise IndexError\
                ('The upper bound estimate of exposure for birds, and/or the dose-'\
                'equivalent chronic toxicity value for birds must be supplied the'\
                ' command line.')
            except ValueError:
                raise ValueError\
                ('The upper bound estimate of exposure for birds must be a real'\
                ' number, not "%mg/kg"' % self.dose_bird_out)
            except ValueError:
                raise ValueError\
                ('The dose-equivalent chronic toxicity value for birds must be a real'\
                ' number, not "%mg/kg"' % self.det_out)
            except ZeroDivisionError:
                raise ZeroDivisionError\
                ('The dose-equivalent chronic toxicity value for birds must be non-zero.')
            if self.dose_bird_out < 0:
                raise ValueError\
                ('dose_bird=%g is a non-physical value.' % self.dose_bird_out)
            if self.det_out < 0:
                raise ValueError\
                ('det=%g is a non-physical value.' % self.det_out)
            self.chron_bird_out = self.dose_bird_out/self.det_out
        return self.chron_bird_out


    def chronconb(self):
        if self.chronconb_out == -1:
            if self.chron_bird_out == None:
                raise ValueError\
                ('chron_bird variable equals None and therefor this function cannot be run.')
            if self.chron_bird_out < 1:
                self.chronconb_out = ('Drinking water exposure alone is NOT a potential concern for birds')
            else:
                self.chronconb_out = ('Exposure through drinking water alone is a potential concern for birds')
        return self.chronconb_out

    # Chronic exposures for mammals

    def chron_mamm(self):
        if self.chron_mamm_out == -1:
            try:
                self.dose_mamm_out = float(self.dose_mamm_out)
                self.act_out = float(self.act_out)
            except IndexError:
                raise IndexError\
                ('The upper bound estimate of exposure for mammals, and/or the'\
                ' adjusted chronic toxicity value for mammals must be supplied the'\
                ' command line.')
            except ValueError:
                raise ValueError\
                ('The upper bound estimate of exposure for mammals must be a real'\
                ' number, not "%mg/kg"' % self.dose_mamm_out)
            except ValueError:
                raise ValueError\
                ('The adjusted chronic toxicity value for mammals must be a real'\
                ' number, not "%mg/kg"' % self.act_out)
            except ZeroDivisionError:
                raise ZeroDivisionError\
                ('The adjusted chronic toxicity value for mammals must be non-zero.')
            if self.dose_mamm_out < 0:
                raise ValueError\
                ('dose_mamm=%g is a non-physical value.' % self.dose_mamm_out)
            if self.act_out < 0:
                raise ValueError\
                ('act=%g is a non-physical value.' % self.act_out)
            self.chron_mamm_out = self.dose_mamm_out/self.act_out
        return self.chron_mamm_out

    def chronconm(self):
        if self.chronconm_out == -1:
            if self.chron_mamm_out == None:
                raise ValueError\
                ('chron_mamm variable equals None and therefor this function cannot be run.')
            if self.chron_mamm_out < 1:
                self.chronconm_out = ('Drinking water exposure alone is NOT a potential concern for mammals')
            else:
                self.chronconm_out = ('Exposure through drinking water alone is a potential concern for mammals')
        return self.chronconm_out
