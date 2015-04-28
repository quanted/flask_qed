# coding: utf-8

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pylab import *
## agg backend is used to create plot as a .png file
#mpl.use('agg')


#############################
# get data
##############################


##################################
#monthly streak data for huc
#need a dictionary with a single huc as a key and
#12 monthly values in a list as the value
def GetSAM_MonthlyHUCStreakOutput(jobid, hucid):
	#fake
    sam_dict = {0:[0.,0.,0.,3.3,2.4,1.1,3.6,2.0,0.,0.,0.,0.]}

    #actual mongo query

    #get values from dictionary- return the list
    sam_huc = sam_dict.values()

	return sam_huc

#annual streak data for huc
#need a dictionary with a single huc as a key and
#30 annual values in a list as the value
def GetSAM_AnnualHUCStreakOutput(jobid, hucid):
	#fake
    sam_dict = {0:[0.,0.,0.,3.3,2.4,1.1,3.6,2.0,0.,0.,0.,0.,
                   0.,0.,0.,3.3,2.4,1.1,3.6,2.0,0.,0.,0.,0.,
                   0.,0.,0.,3.3,2.4,1.1]}

    #actual mongo query

    #get values from dictionary- return the list
    sam_huc = sam_dict.values()

	return sam_huc

#monthly frequency of exceedance data for huc
def GetSAM_MonthlyHUCFreqofExceedOutput(jobid, hucid):
	#fake
    sam_dict =  {0:[0.,0.,0.,0.03,0.05,0.05,0.04,0.02,0.,0.,0.,0.]}

    #actual mongo query

    #get values from dictionary- return the list
    sam_huc = sam_dict.values()

	return sam_huc

#annual frequency of exceedance data for huc
def GetSAM_AnnualHUCFreqofExceedOutput(jobid, hucid):
	#fake
	sam_huc = {0:[0.04,0.08,0.06,0.07,0.02,0.03,0.04,0.01,0.11,0.08,0.11,0.03,
               0.03,0.02,0.04,0.11,0.09,0.07,0.05,0.03,0.02,0.06,0.04,0.06,
               0.01,0.05,0.03,0.06,0.07,0.02]}

    #actual mongo query

    #get values from dictionary- return the list
    sam_huc = sam_dict.values()

	return sam_huc
############################################


############################################
#get data as 2-d array for boxplots
#monthly streak data
def GetSAM_MonthlyArrayStreakOutput(jobid):
	# fake, change to mongoquery
    #rand produces a numpy array but the mongo call returns a dictionary of lists
    huc01 = rand(12).tolist()
	huc02 = rand(12).tolist()
	huc03 = rand(12).tolist()
	huc04 = rand(12).tolist()
	huc05 = rand(12).tolist()
	huc06 = rand(12).tolist()
	huc07 = rand(12).tolist()
	huc08 = rand(12).tolist()
	huc09 = rand(12).tolist()
	huc10 = rand(12).tolist()

    sam_dict = {0:huc01,1:huc02,2:huc03,3:huc04,4:huc05,5:huc06,6:huc07,7:huc08,8:huc09,9:huc10}

    #actual mongo query


    #convert dictionary to numpy array using pandas dataframe
    sam = pd.DataFrame.from_dict(sam_dict, orient="index").as_matrix()

	return sam

#annual streak data
def GetSAM_AnnualArrayStreakOutput(jobid):
	#fake, change to mongoquery
    huc01 = rand(30).tolist()
	huc02 = rand(30).tolist()
	huc03 = rand(30).tolist()
	huc04 = rand(30).tolist()
	huc05 = rand(30).tolist()
	huc06 = rand(30).tolist()
	huc07 = rand(30).tolist()
	huc08 = rand(30).tolist()
	huc09 = rand(30).tolist()
	huc10 = rand(30).tolist()
    sam_dict = {0:huc01,1:huc02,2:huc03,3:huc04,4:huc05,5:huc06,6:huc07,7:huc08,8:huc09,9:huc10}

    #actual mongo query

    #convert dictionary to numpy array using pandas dataframe
    sam = pd.DataFrame.from_dict(sam_dict, orient="index").as_matrix()

	return sam

#monthly frequency of exceedance data
def GetSAM_MonthlyArrayFreqofExceedOutput(jobid):
	# fake, change to mongoquery
    #rand produces a numpy array but the mongo call returns a dictionary of lists
    huc01 = rand(12).tolist()
	huc02 = rand(12).tolist()
	huc03 = rand(12).tolist()
	huc04 = rand(12).tolist()
	huc05 = rand(12).tolist()
	huc06 = rand(12).tolist()
	huc07 = rand(12).tolist()
	huc08 = rand(12).tolist()
	huc09 = rand(12).tolist()
	huc10 = rand(12).tolist()

    sam_dict = {0:huc01,1:huc02,2:huc03,3:huc04,4:huc05,5:huc06,6:huc07,7:huc08,8:huc09,9:huc10}

    #actual mongo query


    #convert dictionary to numpy array using pandas dataframe
    sam = pd.DataFrame.from_dict(sam_dict, orient="index").as_matrix()

	return sam

#annual frequency of exceedance data
def GetSAM_AnnualArrayFreqofExceedOutput(jobid):
	#fake, change to mongoquery
    huc01 = rand(30).tolist()
	huc02 = rand(30).tolist()
	huc03 = rand(30).tolist()
	huc04 = rand(30).tolist()
	huc05 = rand(30).tolist()
	huc06 = rand(30).tolist()
	huc07 = rand(30).tolist()
	huc08 = rand(30).tolist()
	huc09 = rand(30).tolist()
	huc10 = rand(30).tolist()
    sam_dict = {0:huc01,1:huc02,2:huc03,3:huc04,4:huc05,5:huc06,6:huc07,7:huc08,8:huc09,9:huc10}

    #actual mongo query

    #convert dictionary to numpy array using pandas dataframe
    sam = pd.DataFrame.from_dict(sam_dict, orient="index").as_matrix()

    return sam
############################################

############################################
#get all data as 1-d vector for histograms
#all streak data - monthly
def GetSAM_MonthlyVectorStreakOutput(jobid):
	# fake, change to mongoquery
    #rand produces a numpy array
    huc01 = rand(12).tolist()
	huc02 = rand(12).tolist()
	huc03 = rand(12).tolist()
	huc04 = rand(12).tolist()
	huc05 = rand(12).tolist()
	huc06 = rand(12).tolist()
	huc07 = rand(12).tolist()
	huc08 = rand(12).tolist()
	huc09 = rand(12).tolist()
	huc10 = rand(12).tolist()

    sam_dict = {0:huc01,1:huc02,2:huc03,3:huc04,4:huc05,5:huc06,6:huc07,7:huc08,8:huc09,9:huc10}

    #actual mongo query


    #convert dictionary to 2-d numpy array using pandas dataframe
    sam_matrix = pd.DataFrame.from_dict(sam_dict, orient="index").as_matrix()
    #numpy to stack arrays horizontally
    sam_vector = np.hstack(sam_matrix)

	return sam_vector

#all streak data - monthly
def GetSAM_MonthlyVectorFreqofExceedOutput(jobid):
	# fake, change to mongoquery
    #rand produces a numpy array
    huc01 = rand(12).tolist()
	huc02 = rand(12).tolist()
	huc03 = rand(12).tolist()
	huc04 = rand(12).tolist()
	huc05 = rand(12).tolist()
	huc06 = rand(12).tolist()
	huc07 = rand(12).tolist()
	huc08 = rand(12).tolist()
	huc09 = rand(12).tolist()
	huc10 = rand(12).tolist()

    sam_dict = {0:huc01,1:huc02,2:huc03,3:huc04,4:huc05,5:huc06,6:huc07,7:huc08,8:huc09,9:huc10}

    #actual mongo query


    #convert dictionary to 2-d numpy array using pandas dataframe
    sam_matrix = pd.DataFrame.from_dict(sam_dict, orient="index").as_matrix()
    #numpy to stack arrays horizontally
    sam_vector = np.hstack(sam_matrix)

	return sam_vector

#monthly streak data - annual
def GetSAM_AnnualVectorStreakOutput(jobid):
	# fake, change to mongoquery
    #rand produces a numpy array
    huc01 = rand(30).tolist()
	huc02 = rand(30).tolist()
	huc03 = rand(30).tolist()
	huc04 = rand(30).tolist()
	huc05 = rand(30).tolist()
	huc06 = rand(30).tolist()
	huc07 = rand(30).tolist()
	huc08 = rand(30).tolist()
	huc09 = rand(30).tolist()
	huc10 = rand(30).tolist()

    sam_dict = {0:huc01,1:huc02,2:huc03,3:huc04,4:huc05,5:huc06,6:huc07,7:huc08,8:huc09,9:huc10}

    #actual mongo query


    #convert dictionary to 2-d numpy array using pandas dataframe
    sam_matrix = pd.DataFrame.from_dict(sam_dict, orient="index").as_matrix()
    #numpy to stack arrays horizontally
    sam_vector = np.hstack(sam_matrix)

	return sam_vector

#frequency of exceedance data - annual
def GetSAM_AnnualFreqofExceedStreakOutput(jobid):
	# fake, change to mongoquery
    #rand produces a numpy array
    huc01 = rand(30).tolist()
	huc02 = rand(30).tolist()
	huc03 = rand(30).tolist()
	huc04 = rand(30).tolist()
	huc05 = rand(30).tolist()
	huc06 = rand(30).tolist()
	huc07 = rand(30).tolist()
	huc08 = rand(30).tolist()
	huc09 = rand(30).tolist()
	huc10 = rand(30).tolist()

    sam_dict = {0:huc01,1:huc02,2:huc03,3:huc04,4:huc05,5:huc06,6:huc07,7:huc08,8:huc09,9:huc10}

    #actual mongo query


    #convert dictionary to 2-d numpy array using pandas dataframe
    sam_matrix = pd.DataFrame.from_dict(sam_dict, orient="index").as_matrix()
    #numpy to stack arrays horizontally
    sam_vector = np.hstack(sam_matrix)

	return sam_vector
############################################

