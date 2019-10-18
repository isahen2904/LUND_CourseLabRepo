# -*- coding: utf-8 -*-
"""
Created on Wed Oct 16 02:22:14 2019

@author: DeltaMod
"""
import numpy as np
import os 
from scipy import signal
import matplotlib.pyplot as plt
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

Dat2 = [signal.savgol_filter(Dat[n][:,1], 51, 3) for n in range(len(Dat))] #We smooth out all signals, since they were pretty rough
PLoc = [signal.find_peaks(Dat2[n],width=20) for n in range(len(Dat))]      #We use a peak finder to determine the indices of all peaks
for n in range(4,12): 
    plt.plot(Dat[n][:,0],Dat2[n][:])
    plt.plot(Dat[n][:,0],Dat[n][:,1])
    
for n in range(4,12):
    plt.scatter(Dat[n][PLoc[n][0],0],Dat[n][PLoc[n][0],1])