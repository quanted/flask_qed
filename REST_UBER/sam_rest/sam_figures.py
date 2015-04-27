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
#monthly streak data for huc
def GetSAM_MonthlyHUCStreakOutput(jobid, hucid):
	#fake
    #sam_dict = {0:0., 1:0., 2:0., 3:3.3, 4:2.4, 5:1.1,
               6:3.6, 7:2.0, 8:0., 9:0., 10:0., 11:0.}
    sam_dict = {0:[0.,0.,0.,3.3,2.4,1.1,3.6,2.0,0.,0.,0.,0.]}

    #convert returned dictionary to list
    sam_huc = sam_dict.values()

	return sam_huc

#annual streak data for huc
def GetSAM_AnnualHUCStreakOutput(jobid, hucid):
	#fake
	sam_dict = {0:0., 1:0., 2:0., 3:3.3, 4:2.4, 5:1.1, 6:3.6, 7:2.0, 8:0., 9:0., 10:0., 11:0.,
               12:0., 13:0., 14:0., 15:3.3, 16:2.4, 17:1.1, 18:3.6, 19:2.0, 20:0., 21:0., 22:0., 23:0.,
               24:0., 25:0., 26:0., 27:3.3, 28:2.4, 29:1.1}

    #convert returned dictionary to list
    sam_huc = sam_dict.values()

	return sam_huc

#monthly frequency of exceedance data for huc
def GetSAM_MonthlyHUCFreqofExceedOutput(jobid, hucid):
	#fake
	#sam_huc = [0.,0.,0.,0.04,0.05,0.08,0.02,0.,0.,0.,0.,0.]
    sam_dict = {0:0., 1:0., 2:0., 3:0.04, 4:0.05, 5:0.08,
               6:0.02, 7:0., 8:0., 9:0., 10:0., 11:0.}
    #sam_huc = [0.,0.,0.,3.3,2.4,1.1,3.6,2.0,0.,0.,0.,0.]

    #convert returned dictionary to list
    sam_huc = sam_dict.values()

	return sam_huc

#annual frequency of exceedance data for huc
def GetSAM_AnnualHUCFreqofExceedOutput(jobid, hucid):
	#fake
	sam_huc = [0.04,0.08,0.06,0.07,0.02,0.03,0.04,0.01,0.11,0.08,0.11,0.03,
               0.03,0.02,0.04,0.11,0.09,0.07,0.05,0.03,0.02,0.06,0.04,0.06,
               0.01,0.05,0.03,0.06,0.07,0.02]

	return sam_huc

#monthly streak data
def GetSAM_MonthlyArrayStreakOutput(jobid):
	#fake, change to mongoquery
	jan = rand(50)
	feb = rand(50)
	mar = rand(50)
	apr = rand(50)
	may = rand(50)
	jun = rand(50)
	jul = rand(50)
	aug = rand(50)
	sep = rand(50)
	octo = rand(50)
	nov = rand(50)
	dec = rand(50)

	sam = concatenate( (jan, feb, mar, apr, may, jun, jul, aug, sep, octo, nov, dec), 0 )
	sam.shape = (50, 12)

	return sam

#monthly streak data
def GetSAM_AnnualArrayStreakOutput(jobid):
	#fake, change to mongoquery
	yr1984 = rand(50) * 100
    yr1984 = rand(50) * 100
    yr1985 = rand(50) * 100
    yr1986 = rand(50) * 100
    yr1987 = rand(50) * 100
    yr1988 = rand(50) * 100
    yr1989 = rand(50) * 100
    yr1990 = rand(50) * 100
    yr1991 = rand(50) * 100
    yr1992 = rand(50) * 100
    yr1993 = rand(50) * 100
    yr1994 = rand(50) * 100
    yr1995 = rand(50) * 100
    yr1996 = rand(50) * 100
    yr1997 = rand(50) * 100
    yr1998 = rand(50) * 100
    yr1999 = rand(50) * 100
    yr2000 = rand(50) * 100
    yr2001 = rand(50) * 100
    yr2002 = rand(50) * 100
    yr2003 = rand(50) * 100
    yr2004 = rand(50) * 100
    yr2005 = rand(50) * 100
    yr2006 = rand(50) * 100
    yr2007 = rand(50) * 100
    yr2008 = rand(50) * 100
    yr2009 = rand(50) * 100
    yr2010 = rand(50) * 100
    yr2011 = rand(50) * 100
    yr2012 = rand(50) * 100
    yr2013 = rand(50) * 100

	sam = concatenate( (yr1984, yr1985, yr1986, yr1987, yr1988, yr1989,
                        yr1990, yr1991, yr1992, yr1993, yr1994, yr1995,
                        yr1996, yr1997, yr1998, yr1999, yr2000, yr2001,
                        yr2002, yr2003, yr2004, yr2005, yr2006, yr2007,
                        yr2008, yr2009, yr2010, yr2011, yr2012, yr2013,), 0 )
	sam.shape = (50, 30)

	return sam

#monthly frequency of exceedance data
def GetSAM_MonthlyArrayFreqofExceedOutput(jobid):
	#fake, change to mongoquery
	jan = rand(50)
	feb = rand(50)
	mar = rand(50)
	apr = rand(50)
	may = rand(50)
	jun = rand(50)
	jul = rand(50)
	aug = rand(50)
	sep = rand(50)
	octo = rand(50)
	nov = rand(50)
	dec = rand(50)

	sam = concatenate( (jan, feb, mar, apr, may, jun, jul, aug, sep, octo, nov, dec), 0 )
	sam.shape = (50, 12)

	return sam

#monthly frequency of exceedance data
def GetSAM_AnnualArrayFreqofExceedOutput(jobid):
	#fake, change to mongoquery

    yr1984 = rand(50)
    yr1984 = rand(50)
    yr1985 = rand(50)
    yr1986 = rand(50)
    yr1987 = rand(50)
    yr1988 = rand(50)
    yr1989 = rand(50)
    yr1990 = rand(50)
    yr1991 = rand(50)
    yr1992 = rand(50)
    yr1993 = rand(50)
    yr1994 = rand(50)
    yr1995 = rand(50)
    yr1996 = rand(50)
    yr1997 = rand(50)
    yr1998 = rand(50)
    yr1999 = rand(50)
    yr2000 = rand(50)
    yr2001 = rand(50)
    yr2002 = rand(50)
    yr2003 = rand(50)
    yr2004 = rand(50)
    yr2005 = rand(50)
    yr2006 = rand(50)
    yr2007 = rand(50)
    yr2008 = rand(50)
    yr2009 = rand(50)
    yr2010 = rand(50)
    yr2011 = rand(50)
    yr2012 = rand(50)
    yr2013 = rand(50)

    sam = concatenate( (yr1984, yr1985, yr1986, yr1987, yr1988, yr1989,
                        yr1990, yr1991, yr1992, yr1993, yr1994, yr1995,
                        yr1996, yr1997, yr1998, yr1999, yr2000, yr2001,
                        yr2002, yr2003, yr2004, yr2005, yr2006, yr2007,
                        yr2008, yr2009, yr2010, yr2011, yr2012, yr2013,), 0 )

    sam.shape = (50, 30)

    return sam

#all streak data
def GetSAM_MonthlyVectorStreakOutput(jobid):
	#fake, change to mongo query
	jan = rand(50) * 100
	feb = rand(50) * 100
	mar = rand(50) * 100
	apr = rand(50) * 100
	may = rand(50) * 100
	jun = rand(50) * 100
	jul = rand(50) * 100
	aug = rand(50) * 100
	sep = rand(50) * 100
	octo = rand(50) * 100
	nov = rand(50) * 100
	dec = rand(50) * 100

	sam_vector = concatenate( (jan, feb, mar, apr, may, jun, jul, aug, sep, octo, nov, dec), 0 )
    #no shape, just a vector of everything

	return sam_vector

#all streak data
def GetSAM_MonthlyVectorFreqofExceedOutput(jobid):
	#fake, change to mongo query
	jan = rand(50)
	feb = rand(50)
	mar = rand(50)
	apr = rand(50)
	may = rand(50)
	jun = rand(50)
	jul = rand(50)
	aug = rand(50)
	sep = rand(50)
	octo = rand(50)
	nov = rand(50)
	dec = rand(50)

	sam_vector = concatenate( (jan, feb, mar, apr, may, jun, jul, aug, sep, octo, nov, dec), 0 )
    #no shape, just a vector of everything

	return sam_vector

#monthly streak data
def GetSAM_AnnualVectorStreakOutput(jobid):
	#fake, change to mongoquery

    yr1984 = rand(50) * 100
    yr1984 = rand(50) * 100
    yr1985 = rand(50) * 100
    yr1986 = rand(50) * 100
    yr1987 = rand(50) * 100
    yr1988 = rand(50) * 100
    yr1989 = rand(50) * 100
    yr1990 = rand(50) * 100
    yr1991 = rand(50) * 100
    yr1992 = rand(50) * 100
    yr1993 = rand(50) * 100
    yr1994 = rand(50) * 100
    yr1995 = rand(50) * 100
    yr1996 = rand(50) * 100
    yr1997 = rand(50) * 100
    yr1998 = rand(50) * 100
    yr1999 = rand(50) * 100
    yr2000 = rand(50) * 100
    yr2001 = rand(50) * 100
    yr2002 = rand(50) * 100
    yr2003 = rand(50) * 100
    yr2004 = rand(50) * 100
    yr2005 = rand(50) * 100
    yr2006 = rand(50) * 100
    yr2007 = rand(50) * 100
    yr2008 = rand(50) * 100
    yr2009 = rand(50) * 100
    yr2010 = rand(50) * 100
    yr2011 = rand(50) * 100
    yr2012 = rand(50) * 100
    yr2013 = rand(50) * 100

    sam = concatenate( (yr1984, yr1985, yr1986, yr1987, yr1988, yr1989,
                        yr1990, yr1991, yr1992, yr1993, yr1994, yr1995,
                        yr1996, yr1997, yr1998, yr1999, yr2000, yr2001,
                        yr2002, yr2003, yr2004, yr2005, yr2006, yr2007,
                        yr2008, yr2009, yr2010, yr2011, yr2012, yr2013,), 0 )
    #no shape, just a vector of everything

    return sam

#monthly frequency of exceedance data
def GetSAM_AnnualFreqofExceedStreakOutput(jobid):
	#fake, change to mongoquery

    yr1984 = rand(50)
    yr1984 = rand(50)
    yr1985 = rand(50)
    yr1986 = rand(50)
    yr1987 = rand(50)
    yr1988 = rand(50)
    yr1989 = rand(50)
    yr1990 = rand(50)
    yr1991 = rand(50)
    yr1992 = rand(50)
    yr1993 = rand(50)
    yr1994 = rand(50)
    yr1995 = rand(50)
    yr1996 = rand(50)
    yr1997 = rand(50)
    yr1998 = rand(50)
    yr1999 = rand(50)
    yr2000 = rand(50)
    yr2001 = rand(50)
    yr2002 = rand(50)
    yr2003 = rand(50)
    yr2004 = rand(50)
    yr2005 = rand(50)
    yr2006 = rand(50)
    yr2007 = rand(50)
    yr2008 = rand(50)
    yr2009 = rand(50)
    yr2010 = rand(50)
    yr2011 = rand(50)
    yr2012 = rand(50)
    yr2013 = rand(50)

    sam = concatenate( (yr1984, yr1985, yr1986, yr1987, yr1988, yr1989,
                        yr1990, yr1991, yr1992, yr1993, yr1994, yr1995,
                        yr1996, yr1997, yr1998, yr1999, yr2000, yr2001,
                        yr2002, yr2003, yr2004, yr2005, yr2006, yr2007,
                        yr2008, yr2009, yr2010, yr2011, yr2012, yr2013,), 0 )
    #no shape, just a vector of everything

    return sam


#################################################
# generate boxplots
#################################################
## Average streak by month boxplot
def GenerateSAM_MonthStreakBoxplot(jobid):

	# get sam monthly data array of streaks
	sam_vector = GetSAM_MonthlyArrayStreakOutput(jobid)

	# Create a figure instance
	fig = plt.figure(1, figsize=(10, 6))

	# Create an axes instance
	ax = fig.add_subplot(111)
	ax1 = fig.add_subplot(111)

	# Create a boxplot
	bp = ax.boxplot(sam_vector, notch=0, sym='+', vert=1, whis=1.5, patch_artist = True)
	plt.setp(bp['boxes'], color='black')
	plt.setp(bp['whiskers'], color='black')
	plt.setp(bp['fliers'], color='red', marker='+')
	colors = ['lightblue', 'lightblue', 'lightblue', 'lightblue', 'lightblue', 'lightblue',
		 'lightblue','lightblue','lightblue','lightblue','lightblue','lightblue']
	for patch, color in zip(bp['boxes'], colors):
	    patch.set_facecolor(color)

	## Custom x-axis labels
	monthNames = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
	ax.set_xticklabels(monthNames)

	## Remove top axes and right axes ticks
	ax.get_xaxis().tick_bottom()
	ax.get_yaxis().tick_left()
	ax1.set_xlabel('Month')
	ax1.set_ylabel('Days')

    # Add a horizontal grid to the plot - light in color
	ax1.yaxis.grid(True, linestyle='-', which='major', color='lightgrey',
		      alpha=0.5)
	ax1.set_axisbelow(True)
	fig.suptitle("Monthly Average Exceedance Streak Distribution across HUCs")

    # Save the figure
    static_path = ''
    f = static_path + jobid + "_month_streak_boxplot.png"
	fig.savefig(f, bbox_inches = "tight")
	fig.canvas.set_window_title('Monthly Streak Average')
	fig.clf()

## Average streak by year boxplot
def GenerateSAM_AnnualStreakBoxplot(jobid):

	# get sam annual data array of streaks
	sam_vector = GetSAM_AnnualArrayStreakOutput(jobid)

	# Create a figure instance
	fig = plt.figure(1, figsize=(10, 6))

	# Create an axes instance
	ax = fig.add_subplot(111)
	ax1 = fig.add_subplot(111)

	# Create a boxplot
	bp = ax.boxplot(sam_vector, notch=0, sym='+', vert=1, whis=1.5, patch_artist = True)
	plt.setp(bp['boxes'], color='black')
	plt.setp(bp['whiskers'], color='black')
    locs, labels = plt.xticks()
    plt.setp(labels, rotation=90)
	plt.setp(bp['fliers'], color='red', marker='+')
    colors = ['lightblue', 'lightblue', 'lightblue', 'lightblue', 'lightblue', 'lightblue',
              'lightblue','lightblue','lightblue','lightblue','lightblue','lightblue',
              'lightblue','lightblue','lightblue','lightblue','lightblue','lightblue',
              'lightblue','lightblue','lightblue','lightblue','lightblue','lightblue',
              'lightblue','lightblue','lightblue','lightblue','lightblue','lightblue']
	for patch, color in zip(bp['boxes'], colors):
	    patch.set_facecolor(color)

	## Custom x-axis labels
	yearNames = ['1984', '1985', '1986', '1987', '1988', '1989',
                '1990', '1991', '1992', '1993', '1994', '1995',
                '1996', '1997', '1998', '1999', '2000', '2001',
                '2002', '2003', '2004', '2005', '2006', '2007',
                '2008', '2009', '2010', '2011', '2012', '2013']
	ax.set_xticklabels(yearNames)

	## Remove top axes and right axes ticks
	ax.get_xaxis().tick_bottom()
	ax.get_yaxis().tick_left()
	ax1.set_xlabel('Year')
	ax1.set_ylabel('Days')

	# Add a horizontal grid to the plot - light in color
	ax1.yaxis.grid(True, linestyle='-', which='major', color='lightgrey',
		      alpha=0.5)
	ax1.set_axisbelow(True)
	fig.suptitle("Annual Average Exceedance Streak Distribution across HUCs")

	# Save the figure
    static_path = ''
    f = static_path + jobid + "_annual_streak_boxplot.png"
	fig.savefig(f, bbox_inches = "tight")
	fig.canvas.set_window_title('Annual Streak Average')
	fig.clf()

## Average streak by month boxplot
def GenerateSAM_MonthFreqofExceedBoxplot(jobid):

	# get sam monthly data array of streaks
	sam_vector = GetSAM_MonthlyArrayFreqofExceedOutput(jobid)

	# Create a figure instance
	fig = plt.figure(1, figsize=(10, 6))

	# Create an axes instance
	ax = fig.add_subplot(111)
	ax1 = fig.add_subplot(111)

	# Create a boxplot
	bp = ax.boxplot(sam_vector, notch=0, sym='+', vert=1, whis=1.5, patch_artist = True)
	plt.setp(bp['boxes'], color='black')
	plt.setp(bp['whiskers'], color='black')
	plt.setp(bp['fliers'], color='red', marker='+')
	colors = ['lightblue', 'lightblue', 'lightblue', 'lightblue', 'lightblue', 'lightblue',
		 'lightblue','lightblue','lightblue','lightblue','lightblue','lightblue']
	for patch, color in zip(bp['boxes'], colors):
	    patch.set_facecolor(color)

	## Custom x-axis labels
	monthNames = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
	ax.set_xticklabels(monthNames)

	## Remove top axes and right axes ticks
	ax.get_xaxis().tick_bottom()
	ax.get_yaxis().tick_left()
	ax1.set_xlabel('Month')
	ax1.set_ylabel('Exceedance Proportion')

	# Add a horizontal grid to the plot - light in color
	ax1.yaxis.grid(True, linestyle='-', which='major', color='lightgrey',
		      alpha=0.5)
	ax1.set_axisbelow(True)
	fig.suptitle("Monthly Proportion of Exceedance Distribution across HUCs")

	# Save the figure
    static_path = ''
    f = static_path + jobid + "_month_exceedance_boxplot.png"
	fig.savefig(f, bbox_inches = "tight")
	fig.canvas.set_window_title('Monthly Proportion of Exceedance')
	fig.clf()

## Average streak by year boxplot
def GenerateSAM_AnnualFreqofExceedBoxplot(jobid):

	# get sam annual data array of streaks
	sam_vector = GetSAM_AnnualArrayFreqofExceedOutput(jobid)

	# Create a figure instance
	fig = plt.figure(1, figsize=(10, 6))

	# Create an axes instance
	ax = fig.add_subplot(111)
	ax1 = fig.add_subplot(111)

	# Create a boxplot
	bp = ax.boxplot(sam_vector, notch=0, sym='+', vert=1, whis=1.5, patch_artist = True)
	plt.setp(bp['boxes'], color='black')
	plt.setp(bp['whiskers'], color='black')
    locs, labels = plt.xticks()
    plt.setp(labels, rotation=90)
    plt.setp(bp['fliers'], color='red', marker='+')
    colors = ['lightblue', 'lightblue', 'lightblue', 'lightblue', 'lightblue', 'lightblue',
              'lightblue','lightblue','lightblue','lightblue','lightblue','lightblue',
              'lightblue','lightblue','lightblue','lightblue','lightblue','lightblue',
              'lightblue','lightblue','lightblue','lightblue','lightblue','lightblue',
              'lightblue','lightblue','lightblue','lightblue','lightblue','lightblue']
	for patch, color in zip(bp['boxes'], colors):
	    patch.set_facecolor(color)

	## Custom x-axis labels
	yearNames = ['1984', '1985', '1986', '1987', '1988', '1989',
                '1990', '1991', '1992', '1993', '1994', '1995',
                '1996', '1997', '1998', '1999', '2000', '2001',
                '2002', '2003', '2004', '2005', '2006', '2007',
                '2008', '2009', '2010', '2011', '2012', '2013']
	ax.set_xticklabels(yearNames)

	## Remove top axes and right axes ticks
	ax.get_xaxis().tick_bottom()
	ax.get_yaxis().tick_left()
	ax1.set_xlabel('Year')
	ax1.set_ylabel('Exceedance Proportion')

	# Add a horizontal grid to the plot - light in color
	ax1.yaxis.grid(True, linestyle='-', which='major', color='lightgrey',
		      alpha=0.5)
	ax1.set_axisbelow(True)
	fig.suptitle("Annual Proportion of Exceedance Distribution across HUCs")

	# Save the figure
    static_path = ''
    f = static_path + jobid + "_annual_exceedance_boxplot.png"
	fig.savefig(f, bbox_inches = "tight")
	fig.canvas.set_window_title('Annual Proportion of Exceedance')
	fig.clf()

#######################################################
# generate histograms
#######################################################

## Histogram of monthly streaks
def GenerateSAM_MonthStreakHistogram(jobid):

	# get sam data vector of streaks
	sam_vector = GetSAM_MonthlyVectorStreakOutput(jobid)

	# Create a second figure instance
	fig2 = plt.figure(2, figsize=(10, 6))

	# Create an axes instance
	ax_2 = fig2.add_subplot(111)
	ax1_2 = fig2.add_subplot(111)

	# Add a horizontal grid to the plot - light in color
	ax1_2.yaxis.grid(True, linestyle='-', which='major', color='lightgrey',
		      alpha=0.5)
	ax1_2.set_axisbelow(True)

	# Create a histogram
	hist_fig = ax_2.hist(sam_vector, facecolor="darkseagreen")

	## Remove top axes and right axes ticks
	ax_2.get_xaxis().tick_bottom()
	ax_2.get_yaxis().tick_left()
	ax1_2.set_xlabel('Days')
	ax1_2.set_ylabel('Frequency')

	#fig2.title('Streak Average across all Months and HUCs')
	ax_2.set_title('Streak Average across all Months and HUCs')

	# Save the figure
    static_path = ''
    f = static_path + jobid + "_month_streak_histogram.png"
    fig2.savefig(f, bbox_inches = "tight")

	fig2.clf()


## Histogram of annual streaks
def GenerateSAM_AnnualStreakHistogram(jobid):

	# get sam data vector of streaks
	sam_vector = GetSAM_AnnualVectorStreakOutput(jobid)

	# Create a second figure instance
	fig2 = plt.figure(2, figsize=(10, 6))

	# Create an axes instance
	ax_2 = fig2.add_subplot(111)
	ax1_2 = fig2.add_subplot(111)

	# Add a horizontal grid to the plot - light in color
	ax1_2.yaxis.grid(True, linestyle='-', which='major', color='lightgrey',
		      alpha=0.5)
	ax1_2.set_axisbelow(True)

	# Create a histogram
	hist_fig = ax_2.hist(sam_vector, facecolor="darkseagreen")

	## Remove top axes and right axes ticks
	ax_2.get_xaxis().tick_bottom()
	ax_2.get_yaxis().tick_left()
	ax1_2.set_xlabel('Days')
	ax1_2.set_ylabel('Frequency')

	#fig2.title('Streak Average across all Years and HUCs')
	ax_2.set_title('Streak Average across all Years and HUCs')

	# Save the figure
    static_path = ''
    f = static_path + jobid + "_annual_streak_histogram.png"
	fig2.savefig(f, bbox_inches = "tight")

	fig2.clf()

## Histogram of monthly frequency of exceedances
def GenerateSAM_MonthFreqofExceedHistogram(jobid):

	# get sam data vector of streaks
	sam_vector = GetSAM_MonthlyVectorFreqofExceedOutput(jobid)

	# Create a second figure instance
	fig2 = plt.figure(2, figsize=(10, 6))

	# Create an axes instance
	ax_2 = fig2.add_subplot(111)
	ax1_2 = fig2.add_subplot(111)

	# Add a horizontal grid to the plot - light in color
	ax1_2.yaxis.grid(True, linestyle='-', which='major', color='lightgrey',
		      alpha=0.5)
	ax1_2.set_axisbelow(True)

	# Create a histogram
	hist_fig = ax_2.hist(sam_vector, facecolor="darkseagreen")

	## Remove top axes and right axes ticks
	ax_2.get_xaxis().tick_bottom()
	ax_2.get_yaxis().tick_left()
	ax1_2.set_xlabel('Days')
	ax1_2.set_ylabel('Frequency')

	#fig2.title('Streak Average across all Months and HUCs')
	ax_2.set_title('Proportion of Exceedance across all Months and HUCs')

	# Save the figure
    static_path = ''
    f = static_path + jobid + "_month_exceedance_histogram.png"
	fig2.savefig(f, bbox_inches = "tight")

	fig2.clf()


## Histogram of annual frequency of exceedances
def GenerateSAM_AnnualFreqofExceedHistogram(jobid):

	# get sam data vector of streaks
	sam_vector = GetSAM_AnnualVectorFreqofExceedOutput(jobid)

	# Create a second figure instance
	fig2 = plt.figure(2, figsize=(10, 6))

	# Create an axes instance
	ax_2 = fig2.add_subplot(111)
	ax1_2 = fig2.add_subplot(111)

	# Add a horizontal grid to the plot - light in color
	ax1_2.yaxis.grid(True, linestyle='-', which='major', color='lightgrey',
		      alpha=0.5)
	ax1_2.set_axisbelow(True)

	# Create a histogram
	hist_fig = ax_2.hist(sam_vector, facecolor="darkseagreen")

	## Remove top axes and right axes ticks
	ax_2.get_xaxis().tick_bottom()
	ax_2.get_yaxis().tick_left()
	ax1_2.set_xlabel('Days')
	ax1_2.set_ylabel('Frequency')

	#fig2.title('Streak Average across all Years and HUCs')
	ax_2.set_title('Proportion of Exceedance across all Years and HUCs')

	# Save the figure
    static_path = ''
    f = static_path + jobid + "_annual_exceedance_histogram.png"
	fig2.savefig(f, bbox_inches = "tight")

	fig2.clf()


#########################################################
# generate huc time series
##########################################################
## huc time series for monthly average streak
def GenerateSAM_MonthStreakHUCPlot(jobid, hucid):

	# get sam streak data for a particular huc
	sam_huc = GetSAM_MonthlyHUCStreakOutput(jobid, hucid)

	#month info
	months = range(12)
	monthNames = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

	# Create a third figure instance
	fig3 = plt.figure(3, figsize=(10, 6))

	# Create an axes instance
	ax_3 = fig3.add_subplot(111)
	ax1_3 = fig3.add_subplot(111)

	#plot monthly series
	plt.plot(months, sam_huc, linestyle='-', marker='o')

	# Add a horizontal grid to the plot - light in color
	ax1_3.yaxis.grid(True, linestyle='-', which='major', color='lightgrey',
		      alpha=0.5)
	ax1_3.set_axisbelow(True)

	## Custom x-axis labels
	ax_3.set_xticklabels(monthNames)
	#set tick intervals to 12
	ax_3.locator_params(tight=True, nbins=12)
	## Remove top axes and right axes ticks
	ax_3.get_xaxis().tick_bottom()
	ax_3.get_yaxis().tick_left()
	ax1_3.set_xlabel('Month')
	ax1_3.set_ylabel('Maximum Exceedance Streak (days)')

	#title
	huc_title = "Monthly Maximimum Streak for HUC " + hucid
	ax_3.set_title(huc_title)

    # Save the figure
    static_path = ''
    f = static_path + jobid + hucid + "_month_streaks_huc.png"
	fig3.savefig(f, bbox_inches = "tight")

	fig3.clf()


## huc time series for annual average streak
def GenerateSAM_AnnualStreakHUCPlot(jobid, hucid):

	# get sam streak data for a particular huc
	sam_huc = GetSAM_AnnualHUCStreakOutput(jobid, hucid)

	#month info
	years = range(30)
	yearNames = ['1984', '1985', '1986', '1987', '1988', '1989',
                '1990', '1991', '1992', '1993', '1994', '1995',
                '1996', '1997', '1998', '1999', '2000', '2001',
                '2002', '2003', '2004', '2005', '2006', '2007',
                '2008', '2009', '2010', '2011', '2012', '2013']

	# Create a third figure instance
	fig3 = plt.figure(3, figsize=(10, 6))

	# Create an axes instance
	ax_3 = fig3.add_subplot(111)
	ax1_3 = fig3.add_subplot(111)

	#plot annual series
	plt.plot(years, sam_huc, linestyle='-', marker='o')
    locs, labels = plt.xticks()
    plt.setp(labels, rotation=90)

	# Add a horizontal grid to the plot - light in color
	ax1_3.yaxis.grid(True, linestyle='-', which='major', color='lightgrey',
		      alpha=0.5)
	ax1_3.set_axisbelow(True)

	## Custom x-axis labels
	ax_3.set_xticklabels(yearNames)
	#set tick intervals to 12
	ax_3.locator_params(tight=True, nbins=30)
	## Remove top axes and right axes ticks
	ax_3.get_xaxis().tick_bottom()
	ax_3.get_yaxis().tick_left()
	ax1_3.set_xlabel('Year')
	ax1_3.set_ylabel('Maximum Exceedance Streak (days)')

	#title
	huc_title = "Annual Maximum Streak for HUC " + hucid
	ax_3.set_title(huc_title)

    # Save the figure
    static_path = ''
    f = static_path + jobid + hucid + "_annual_streaks_huc.png"
	fig3.savefig(f, bbox_inches = "tight")

	fig3.clf()

## huc time series for monthly average streak
def GenerateSAM_MonthFreqofExceedHUCPlot(jobid, hucid):

	# get sam streak data for a particular huc
	sam_huc = GetSAM_MonthlyHUCFreqofExceedOutput(jobid, hucid)

	#month info
	months = range(12)
	monthNames = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

	# Create a third figure instance
	fig3 = plt.figure(3, figsize=(10, 6))

	# Create an axes instance
	ax_3 = fig3.add_subplot(111)
	ax1_3 = fig3.add_subplot(111)

	#plot monthly series
	plt.plot(months, sam_huc, linestyle='-', marker='o')

	# Add a horizontal grid to the plot - light in color
	ax1_3.yaxis.grid(True, linestyle='-', which='major', color='lightgrey',
		      alpha=0.5)
	ax1_3.set_axisbelow(True)

	## Custom x-axis labels
	ax_3.set_xticklabels(monthNames)
	#set tick intervals to 12
	ax_3.locator_params(tight=True, nbins=12)
	## Remove top axes and right axes ticks
	ax_3.get_xaxis().tick_bottom()
	ax_3.get_yaxis().tick_left()
	ax1_3.set_xlabel('Month')
	ax1_3.set_ylabel('Maximum Exceedance Streak (days)')

	#title
	huc_title = "Monthly Proportion of Exceedance for HUC " + hucid
	ax_3.set_title(huc_title)

    # Save the figure
    static_path = ''
    f = static_path + jobid + hucid + "_month_exceedance_huc.png"
	fig3.savefig(f, bbox_inches = "tight")

	fig3.clf()


## huc time series for annual average streak
def GenerateSAM_AnnualFreqofExceedHUCPlot(jobid, hucid):

	# get sam streak data for a particular huc
	sam_huc = GetSAM_AnnualHUCFreqofExceedOutput(jobid, hucid)

	#month info
	years = range(30)
	yearNames = ['1984', '1985', '1986', '1987', '1988', '1989',
                '1990', '1991', '1992', '1993', '1994', '1995',
                '1996', '1997', '1998', '1999', '2000', '2001',
                '2002', '2003', '2004', '2005', '2006', '2007',
                '2008', '2009', '2010', '2011', '2012', '2013']

	# Create a third figure instance
	fig3 = plt.figure(3, figsize=(10, 6))

	# Create an axes instance
	ax_3 = fig3.add_subplot(111)
	ax1_3 = fig3.add_subplot(111)

	#plot annual series
	plt.plot(years, sam_huc, linestyle='-', marker='o')
    locs, labels = plt.xticks()
    plt.setp(labels, rotation=90)

	# Add a horizontal grid to the plot - light in color
	ax1_3.yaxis.grid(True, linestyle='-', which='major', color='lightgrey',
		      alpha=0.5)
	ax1_3.set_axisbelow(True)

	## Custom x-axis labels
	ax_3.set_xticklabels(yearNames)
	#set tick intervals to 12
	ax_3.locator_params(tight=True, nbins=30)
	## Remove top axes and right axes ticks
	ax_3.get_xaxis().tick_bottom()
	ax_3.get_yaxis().tick_left()
	ax1_3.set_xlabel('Year')
	ax1_3.set_ylabel('Proportion of Exceedance')

	#title
	huc_title = "Annual Proportion of Exceedance for HUC " + hucid
	ax_3.set_title(huc_title)

    # Save the figure
    static_path = ''
    f = static_path + jobid + hucid + "_annual_exceedance_huc.png"
	fig3.savefig(f, bbox_inches = "tight")

	fig3.clf()