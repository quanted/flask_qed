# -*- coding: utf-8 -*-
"""
Created on Thu Nov 14 10:18:30 2013

@author: Jon F
"""
# from vvwm_parameters_transfer import *
import os
import datetime
from datetime import date

def createJulianDayList():
	


def makeSamInp(args):



	####################Start writing input file###################
	myfile = open('SAM.inp','w')                                   				#Name of input file created
	
	myfile.write(simType + "\n")												# Sim Type
	myfile.write(startDateIndex + " !Simulation Start Day Index" + "\n")		# Sim Start Date Index
	myfile.write(startJulianDay + " !Start Julian Day" + "\n")					# Start Julian Day
	myfile.write(endJulianDay + " !End Julian Day" + "\n")						# End Julian Day
	myfile.write(totalNoSimDay + " !Total Number of Simulation Days" + "\n")	# Total Number of Sim Days
	# List Julian Day sequence
	myfile.write( + "\n")
	# List of M/D/YYYY and HH:MM:SS AM/PM sequence of applications
	myfile.write( + "\n")

	myfile.write(chemical_name + " !Chemical" + "\n")							# Chemical Name
	myfile.write(noOfCrops + " !Number of Crops" + "\n")						# Number of Crops
	myfile.write(cropId + " !Crop IDs" + "\n") #??? How should this be formatted?  # Crop IDs
	myfile.write(koc + "." + " !Koc" + "\n")									# Koc
	myfile.write(soil_halflife + "." + " !Soil Half Life" + "\n")				# Soil halflife (days)
	myfile.write(noa + " !Total Number of Apps" + "\n")							# Total number of apps
	myfile.write(" " + appJulianDates + " !Application num_record" + "\n")		# Application num records list
	myfile.write(" " + appJulianDates + " !Application Julian dates" + "\n")	# Application Julian dates list
	myfile.write(" " + appRates + " !App mass kg/ha" + "\n")					# Application rates list
	myfile.write(outputType + " !Output type (1=ToxExd,2=30dMax,3=AnnPeak)" + "\n")
	myfile.write(threshold + " !Threshold (0=no threshold, >0 threshold set)" + "\n")
	myfile.write(thresholdType + " !Thres Type (1=30d,2=annual)" + "\n")
	myfile.write(outputFormat + " !Output format (1=table,2=map)" + "\n")

	myfile.close()