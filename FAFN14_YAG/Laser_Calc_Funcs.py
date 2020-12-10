# -*- coding: utf-8 -*-
"""
Created on Thu Dec 10 17:15:14 2020
@author: Vidar
"""
import numpy as np

C = 30*10**-6 #F  
V_pump = [5,23,4,23,25,26] #kV
rate = 10        #Hz
lasing_treshold = None #kv #J

def Func_E_Cap(C,V):
    E_cap  = C*np.power(V,2)/2
    return(E_cap)

E_Cap = Func_E_Cap(C,V_pump)

dur = {'IR_nQ':[],
       'IR_Q':[],
       '532_Q':[]} 

pow_av = {'IR_nQ':[5],
          'IR_Q':[10],
          '532_Q':[33]} 

E_pulse  = {'IR_nQ':[],
            'IR_Q':[],
            '532_Q':[]} 

eff = {'IR_nQ':[],
       'IR_Q':[],
       '532_Q':[]} 

pow_peak = {'IR_nQ':[],
            'IR_Q':[],
            '532_Q':[]} 


def Func_E_(C,V):
    E_cap  = C*np.power(V,2)/2
    return(E_cap)

def Func_L_Input():
    None
