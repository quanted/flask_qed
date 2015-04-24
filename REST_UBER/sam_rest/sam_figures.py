# coding: utf-8

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pylab import *
## agg backend is used to create plot as a .png file
#mpl.use('agg')

#streak data for huc
def GetSAM_HUCStreakOutput(mongokey, hucid):
	#fake
	sam_huc = [0.,0.,0.,3.3,2.4,1.1,3.6,2.0,0.,0.,0.,0.]

	return sam_huc

#monthly streak data
def GetSAM_MonthlyStreakOutput(self, mongokey):
	#fake, change to mongoquery
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

	sam = concatenate( (jan, feb, mar, apr, may, jun, jul, aug, sep, octo, nov, dec), 0 )
	sam.shape = (50, 12)

	return sam

#all streak data
def GetSAM_AllStreakOutput(self, mongokey):
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

	return sam_vector

## figure 1
def GenerateSAM_StreakBoxplot(self, mongokey):

	# get sam monthly data array of streaks
	sam_vector = GetSAM_MonthlyStreakOutput(mongokey)

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
	fig.savefig("streak_boxplot.png", bbox_inches = "tight")
	fig.canvas.set_window_title('Monthly Streak Average')
	fig.clf()


## figure 2
def GenerateSAM_StreakHistogram(self, mongokey):

	# get sam data vector of streaks
	sam_vector = GetSAM_AllStreakOutput(mongokey)

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
	fig2.savefig("streak_histogram.png", bbox_inches = "tight")

	fig2.clf()

## figure 3
def GenerateSAM_HUCPlot(self, mongokey, hucid):

	# get sam streak data for a particular huc
	sam_huc = GetSAM_HUCStreakOutput(mongokey, hucid)

	#month info
	months = [0,1,2,3,4,5,6,7,8,9,10,11]
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

	fig3.savefig("streaks_huc.png", bbox_inches = "tight")

	fig3.clf()