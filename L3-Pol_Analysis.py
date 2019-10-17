# -*- coding: utf-8 -*-
"""
Created on Wed Oct 16 02:22:14 2019

@author: DeltaMod
"""
import numpy as np
import os 
import matplotlib.pyplot as plt
Dpath = os.getcwd()+'\\oct-14\\'
DList = [Dpath+file for file in os.listdir(Dpath) if file.endswith(".txt")]

Dat      = []
for Name in range(len(DList)): 
    with open(DList[Name],'r') as Fop:
        datastr = Fop.read()
        datalist = datastr.split("\n")
        rowsplit = [datalist[n].split(',') for n in range(len(datalist))]
        elemlist = [s for s in rowsplit if len(s) == 3] 

    Dat.append(np.array([(float(elemlist[n][1]),float(elemlist[n][2])) for n in range(len(elemlist))]) )
for n in range(len(Dat)):    
    plt.plot(Dat[n][:,0],Dat[n][:,1])