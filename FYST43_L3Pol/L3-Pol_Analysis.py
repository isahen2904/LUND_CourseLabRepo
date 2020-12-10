# -*- coding: utf-8 -*-
"""
Created on Wed Oct 16 02:22:14 2019

@author: DeltaMod
"""
import numpy as np
import os 
from scipy import signal
import matplotlib.pyplot as plt
plt.rcParams['figure.figsize'] = (7, 5)
plt.rcParams['figure.dpi']     = 150


Dpath = os.getcwd()+'\\oct-14\\'
Names = os.listdir(Dpath)
DList = [Dpath+file for file in os.listdir(Dpath) if file.endswith(".txt")]

Dat      = []
for Name in range(len(DList)): 
    with open(DList[Name],'r') as Fop:
        datastr = Fop.read()
        datalist = datastr.split("\n")
        rowsplit = [datalist[n].split(',') for n in range(len(datalist))]
        elemlist = [s for s in rowsplit if len(s) == 3] 

    Dat.append(np.array([(float(elemlist[n][1]),float(elemlist[n][2])) for n in range(len(elemlist))]) )
#Index 4->13 is crystal rotations 0:5:45
d     = 10**-3*np.array([0.24, 1.00, 3.00, 9.02]) #Originally in mm => 10^3 microns

Dat2    = [signal.savgol_filter(Dat[n][:,1], 51, 10) for n in range(len(Dat))] #We smooth out all signals, since they were pretty rough
PLoc    = [signal.find_peaks(abs(Dat2[n]-max(Dat2[n])),width=20) for n in range(len(Dat))]      #We use a peak finder to determine the indices of all valleys
PLoc[3] = signal.find_peaks(Dat2[3],width=5,prominence=9)    #We use a peak finder to determine the indices of all valleys

NSel   = [5,13,21]
NMod   = [NSel[n] - NSel[0] for n in range(len(NSel))]
WRange = Dat[3][:,0]*10**-9
biflam = [Dat[3][PLoc[3][0][NSel[n]],0]*10**-9 for n in range(len(NSel))]
a = 3


D1 = d[a]*(1/(biflam[1]**2) - 1/(biflam[0]**2)); D2 = d[a]*(1/(biflam[2]**2)-1/(biflam[0]**2))

meq = ((biflam[2]-biflam[0])/(2*D2)+(biflam[0]-biflam[1])/(2*D1) - (biflam[2]*NMod[2])/D2+(biflam[1]*NMod[1])/D1)/((biflam[1]-biflam[0])/(D1)+(biflam[0]-biflam[2])/(D2))
Beq  = ((2*meq + 1)*(0.5*(biflam[1]-biflam[0]))-biflam[1]*NMod[1])/(d[a]*(1/(biflam[1]**2)-1/(biflam[0]**2))) 
Beq2 = ((2*meq + 1)*(0.5*(biflam[2]-biflam[1]))-biflam[2]*NMod[2])/(d[a]*(1/(biflam[2]**2)-1/(biflam[0]**2))) 
Aeq = (2*meq+1)*biflam[0]/(2*d[a]) - Beq/(biflam[0]**2) #

Test0 = (2*d[a]*(Aeq+Beq/(biflam[0]**2))/(biflam[0]) - 1)/2
Test1 = (2*d[a]*(Aeq+Beq/(biflam[1]**2))/(biflam[1]) - 1 + 2*NMod[1])/2
Test2 = (2*d[a]*(Aeq+Beq/(biflam[2]**2))/(biflam[2]) - 1 + 2*NMod[2])/2

#%% Alternate solution using np linalg:
MA = np.array([[1,1/(biflam[0]**2),-biflam[0]/d[a]], 
               [1,1/(biflam[1]**2),-biflam[1]/d[a]], 
               [1,1/(biflam[2]**2),-biflam[2]/d[a]]])
MB = np.array([[biflam[0]/(2*d[a])],
               [biflam[1]/(2*d[a])-(NMod[1]*biflam[1])/(d[a])],
               [biflam[2]/(2*d[a])-(NMod[2]*biflam[2])/(d[a])]])
ABXSolve = np.linalg.solve(MA, MB)
print(ABXSolve)

#%% Birefringeance Stuff
Deltn = []
ABTest = True

for i in range(0,len(PLoc[3][0])):
    if ABTest == False:
        Deltn.append((2*(ABXSolve[2]-i))*(Dat[3][PLoc[3][0][i],0]*10**-9)/(2*d[a]))
    if ABTest == True:
        Deltn.append((ABXSolve[0]+ABXSolve[1]/(Dat[3][PLoc[3][0][i],0]*10**-9)**2))
DELTN = [Deltn[0]-Deltn[i] for i in range(1,len(Deltn))]
fig0 = plt.figure(0)
ax = fig0.gca()
#ax.plot(Dat[3][PLoc[3][0],0],Deltn)
ax.plot(Dat[3][PLoc[3][0][1:],0],DELTN)
plt.xlabel('Wavelength [nm]')
plt.ylabel('$\Delta$ n')
plt.grid()

fig1 = plt.figure(1)
fig1.clf()
ax = fig1.gca()
for m in range(3,4): 
    m = 3
    ax.plot(Dat[m][:,0]*10**-9,Dat[m][:,1]) 
    ax.scatter(Dat[m][PLoc[m][0],0]*10**-9,Dat[m][PLoc[m][0],1])
    ax.scatter(biflam,Dat[m][PLoc[m][0][NSel],1])
plt.grid()
plt.autoscale(enable=True,tight=True)
plt.xlabel('Wavelength [m]')
plt.ylabel('Intensity [a.u]')
#%% Optical Activity Stuff:

fig3 = plt.figure(3)
fig3.clf()
ax = fig3.gca()
for n in range(4,14): 
    ax.plot(Dat[n][:,0],Dat[n][:,1])
    ax.plot(Dat[n][:,0],Dat2[n][:])
    
for n in range(4,14):
    ax.scatter(Dat[n][PLoc[n][0],0],Dat[n][PLoc[n][0],1])
plt.xlabel('Wavelength [m]')
plt.ylabel('Intensity [a.u]')
beta  = np.array([0, 5, 10, 15, 20, 25, 30, 35, 40, 45])
lambd = [10**-9*Dat[n][PLoc[n][0][-1],0] for n in range(4,14)]
plt.grid()
plt.autoscale(enable=True,tight=True) 
#beta = delta/2 = \pi/\lambda_0 * d * Dn
Dn = [beta[n]*lambd[n]/(d[3]*np.pi) for n in range(len(beta))]    

fig4 = plt.figure(4)
fig4.clf()
ax = fig4.gca()
for n in range(4,14): 
    ax.plot(lambd,Dn)
plt.grid()
plt.xlabel('Wavelength [m]')
plt.ylabel('$\Delta$ n ')
plt.autoscale(enable=True,tight=True)

fig4 = plt.figure(5)
fig4.clf()
ax = fig4.gca()
for n in range(4,14): 
    ax.plot(lambd,beta)
plt.grid()
plt.xlabel('Wavelength[m] ')
plt.ylabel('$Beta$')
plt.autoscale(enable=True,tight=True)