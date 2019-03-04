#######################################################################################
#  README
#
#  This code reads an ASCII file which contains temperature and pressure measurements
#  of an ultracold equipment, collected from 17 to 20 Dec 2018. 

#  Part 1: reads the ASCII file. 

#  Part 2: the temperature distribution over all days is plotted in a histogram, and 
#  a Gaussian fit is performed to determine the mean temperature and its stability.

#  Part 3: temperature versus time is plotted. 

#  Created by Priyashree Roy (Jan 2019)
######################################################################################
 
import matplotlib.pyplot as plt
import numpy as np
from scipy import stats #For Gaussian fit
import matplotlib.ticker as mtick

########################################################
Part 1. Read ASCII file
########################################################

response= raw_input("Is this code in the same directory where the input textfile is? (Y/N): ")
if response=='N':
	print "Please copy the code to the data file's directory, then try again"
	quit()
	
#Read the textfile as string data. This is helpful when one has mixed format data file
f = raw_input("Enter the name of the textfile including the extension:")

date = raw_input("Enter date of cool down test (e.g. 30_May_2018): ")
print date

data = np.genfromtxt(f, dtype=None, delimiter=',')

print(data.shape)
#Remove the first column containing date and time. The second column has date and time combined.  

data = data[1:, 1:]

print(data[1,:])

#Convert strings to usable float data 

data = np.asfarray(data,float)

#Convert time from sec to hr & offset by 0.25 hrs because that's when we started cooling down

time = (data[:,0] - data[0,0])/(3600.0) - 0.27 

print("Last time recorded in this textfile (Day):")
print(time[len(time)-1])
print("\n")

#########################################################
# Part 2. Plot target temperature distribution histogram
#########################################################

fig1=plt.figure()
 
ax1=fig1.add_subplot(111)

#Filter data to remove cooldown, warm up sections

temp_filter = data[:,5][(time>5.5) & (time<78)]

#Plot the data without normalizing it

nbins=20
result=plt.hist(temp_filter, range=[20.62, 20.72], color='white', edgecolor='blue', bins=nbins, histtype="step", linewidth=2)

#Find min and max of xticks so we know where we should compare 
#theoretical dist.
 
xmin, xmax = 20.62, 20.72  
lnspc = np.linspace(xmin, xmax, len(temp_filter))

# Fit normal distribution 

m, s = stats.norm.fit(temp_filter) # get mean and standard deviation  
pdf_g = stats.norm.pdf(lnspc, m, s) # now get theoretical values in our interval 

#Scale norm fit to data and plot

dx=result[1][1]-result[1][0] # this gives the width of a single bar, in Kelvin
scale=len(temp_filter)*dx

ax1.plot(lnspc, pdf_g*scale, '--r', label="Mean=%.2fK \n $\sigma$=%.2fK" %(m, s), linewidth=3) # plot it

#Title and labels

ax1.set_title('Target Temp Regulation Over 4 Days', size = 15)
ax1.set_xlabel('Temp (K)', size = 13)

ax1.set_ylim([0,28000])

#Show legend

leg = ax1.legend(loc=1, fontsize=12)

plotname1 = 'Target_T_dist_'
plotname1 += date
plotname1 +='.png'

plt.savefig(plotname1, bbox_inches='tight')

#bbox inches = tight removes the white space around the image

#########################################################
# Part 3: Plot target temperature over time
#########################################################

fig2=plt.figure()
 
ax3 = fig2.add_subplot(1,1,1)

title2 = 'Target Temp regulation '
title2 += date

ax3.set_title(title2)    
ax3.set_xlabel('Time (hr)', size=13)
ax3.set_ylabel('Temp (K)', size=13)

#Choose the data range between cool down and warm up, where target T was being regulated.

time_filter = time[(time>2) & (time<98)]
cond_T_filter = data[:,3][(time>2) & (time<98)]
target_T_filter= data[:,5][(time>2) & (time<98)]

#Since there is a lot of data, read every 5th element of each array

ax3.plot(time_filter[::200], cond_T_filter[::200], color='r', marker='s', markersize=0.5, label='Condenser temp 1')
ax3.plot(time_filter[::200], target_T_filter[::200], color='b', marker='s', markersize=0.5, label='Target temp')
ax3.set_xlim([2,98])
ax3.set_ylim([20.0,21.0])

#x_minor_ticks = np.arange(2,78,2)
y_minor_ticks = np.arange(20.0,21.0,0.05)

ax3.set_xticks(np.arange(2,98,4))
ax3.xaxis.set_major_formatter(mtick.FormatStrFormatter('%d'))
ax3.set_yticks(np.arange(20.0,21.0,0.1))
ax3.set_yticks(y_minor_ticks, minor=True)

# And a corresponding grid

ax3.grid()

# If you want different settings for the grids:

ax3.grid(which='major', alpha=1.0)

leg2 = ax3.legend(loc=1, fontsize=13)

plotname2 = 'Target_T_regulation_'
plotname2 += date
plotname2 +='.png'

#Place lines at end of each day (i.e. at 11:59:59 a.m. of each day)

plt.axvline(x=16.51, color='black', linestyle='--', linewidth=1.5)
plt.axvline(x=40.51, color='black', linestyle='--', linewidth=1.5)
plt.axvline(x=64.51, color='black', linestyle='--', linewidth=1.5)
plt.axvline(x=88.51, color='black', linestyle='--', linewidth=1.5)

#Place dates before the drawn lines

ax3.text(3,20.12,'17 Dec', fontsize=14)
ax3.text(23,20.12,'18 Dec', fontsize=14)
ax3.text(46,20.12,'19 Dec', fontsize=14)
ax3.text(70,20.12,'20 Dec', fontsize=14)

plt.savefig(plotname2, bbox_inches='tight')






