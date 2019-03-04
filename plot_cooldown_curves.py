import matplotlib.pyplot as plt
import numpy as np
import matplotlib.ticker as mtick

response= raw_input("Is this code in the same directory where the input textfile is? (Y/N): ")
if response=='N':
	print "Please copy the code to the data file's directory, then try again"
	quit()
	
#Read the textfile as string data. This is helpful when one has mixed format data file
f = raw_input("Enter the name of the textfile including the extension:")

date = raw_input("Enter date of cool down test (e.g. 30 May 2018): ")
print date

data = np.genfromtxt(f, dtype=None, delimiter=',')

#Remove first row which is header, and remove the first column containing date and time  
data = data[1:, 1:]

#print data[0,:]

#Convert strings to usable float data 

data = np.asfarray(data,float)

#print data[0,:]

#Convert time from sec to min

time = (data[:,0] - data[0,0])/(3600.0) - 0.27 

print("Last time recorded in this textfile:")
print(time[len(time)-1])
print("\n")

#########################################################
# Plot canvas for cooling down and filling phase
#########################################################

fig=plt.figure()
 
ax1 = fig.add_subplot(111)

title = 'H2 cooldown '
title += date

#print "plot title:" 
#print title 

ax1.set_title(title)    
ax1.set_xlabel('Time (hr)', size=13)
ax1.set_ylabel('Temp (K)', size=13)

ax1.plot(time, data[:,3], color='r', marker='s', markersize=2.5, label='Condenser temp 1')
ax1.plot(time, data[:,4], color='y', marker='o', markersize=0.5, label='Condenser temp 2')
ax1.plot(time, data[:,5], '-b', label='Target temp')
ax1.set_xlim([0,2.8])
ax1.set_ylim([15,345])
ax1.xaxis.set_ticks(np.linspace(0, 2.8, 7))
ax1.xaxis.set_major_formatter(mtick.FormatStrFormatter('%0.1f'))

plt.grid()
leg = ax1.legend(loc=1, fontsize=12)

#Correct the inversion of level sensor's resistance in the labview code

#level_R = 1/(data[:,6]*10) 

#Plot level sensor on secondary axis

ax2 = ax1.twinx()
ax2.set_ylabel(r'Level Sensor R ($\Omega$)', size=13)
ax2.set_ylim([105, 200])
ax2.plot(time, data[:,6], '--g', label='level sensor')
ax1.set_xlim([0,2.8])
ax1.xaxis.set_ticks(np.linspace(0, 2.8, 7))
leg2 = ax2.legend(loc=2, fontsize=12)

plotname = 'Cooldown_fill_times'
plotname += date
plotname +='.png'

plt.savefig(plotname, bbox_inches='tight')
#bbox inches = tight removes the white space around the image

#########################################################
# Plot canvas for target operation phase
#########################################################

fig1=plt.figure()
 
ax3 = fig1.add_subplot(1,1,1)

title2 = 'Target Temp regulation '
title2 += date

ax3.set_title(title2)    
ax3.set_xlabel('Time (hr)', size=13)
ax3.set_ylabel('Temp (K)',size=13)

ax3.plot(time[::50], data[:,3][::50], color='r', marker='s', markersize=1.0, label='Condenser temp 1')
#ax3.plot(time, data[:,4], color='y', marker='o', markersize=0.5, label='Condenser temp 2')
ax3.plot(time[::50], data[:,5][::50], color='b', marker='s', markersize=1.0, label='Target temp')
ax3.set_xlim([3,time[len(time)-1]])
ax3.set_ylim([20.0,21.0])

x_minor_ticks = np.arange(3,time[len(time)-1],0.5)
y_minor_ticks = np.arange(20.0,21.0,0.05)

ax3.set_xticks(np.arange(3,time[len(time)-1],1))
ax3.set_yticks(np.arange(20.0,21.0,0.1))
ax3.set_xticks(x_minor_ticks, minor=True)
ax3.set_yticks(y_minor_ticks, minor=True)

# And a corresponding grid
#ax3.grid(which='both')
ax3.grid()

# If you want different settings for the grids:
#ax3.grid(which='minor', alpha=0.3)
ax3.grid(which='major', alpha=0.8)

leg = ax3.legend(loc=1, fontsize=12)

plotname1 = 'Target_temp_regulation_'
plotname1 += date
plotname1 +='.png'

plt.savefig(plotname1, bbox_inches='tight')

#bbox inches = tight removes the white space around the image

####################################################################################################################
# Plot canvas for target operation phase: compare expected temp from observed exhaust pressure with measured temp.
####################################################################################################################

fig4=plt.figure()
 
ax4 = fig4.add_subplot(111)
 
title3 = 'Target Temp Pressure Comparison '
title3 += date

ax4.set_title(title3)    
ax4.set_xlabel('Time (hr)', size=13)
ax4.set_ylabel('T (K)', size=13)

# Convert exhaust pressure to absolute value
P_abs = data[:,2] + 1.0135

#pressure as a function of temp. at the saturation curve from NIST for Hydrogen
T_expected = -0.9517*P_abs*P_abs+5.3868*P_abs+15.8624

#Plot expected condenser temperature, plot every 5th element of the time and data array
ax4.plot(time[::50], T_expected[::50], color='m', marker='s', markersize=1.0, label='Temp calc. (from exhaust P)')

#Plot measured condenser temperature, plot every 5th element of the time and data array
ax4.plot(time[::50], data[:,5][::50], color='b', marker='s', markersize=1.0, label='Target temp meas.')


ax4.set_xlim([3,time[len(time)-1]])
ax4.set_ylim([20.4, 21.4])

x_minor_ticks = np.arange(3,time[len(time)-1],0.5)
y_minor_ticks = np.arange(20.4,21.4,0.05)

ax4.set_xticks(np.arange(3,time[len(time)-1], 1))
ax4.set_yticks(np.arange(20.4,21.4,0.1))
ax4.set_xticks(x_minor_ticks, minor=True)
ax4.set_yticks(y_minor_ticks, minor=True)

ax4.grid()

# If you want different settings for the grids:
#ax4.grid(which='minor', alpha=0.3)
ax4.grid(which='major', alpha=1)

leg3 = ax4.legend(loc=1, fontsize=12)

ax5 = ax4.twinx()
ax5.set_ylabel('P (bar)', size=13)
ax5.set_ylim([.8, 1.26])
ax5.plot(time[::50], P_abs[::50], color='c', marker='s', markersize=2.0, label='Exhaust P')
ax4.set_xlim([3,time[len(time)-1]])
ax4.set_xticks(np.arange(3,time[len(time)-1], 1))

leg4 = ax5.legend(loc=2, fontsize=12)
plotname3 = 'Target_T_exhaust_P_'
plotname3 += date
plotname3 +='.png'

plt.savefig(plotname3, bbox_inches='tight')



