# -*- coding: utf-8 -*-
"""
Created on Thu Dec 10 17:15:14 2020

@author: Vidar
"""

C    = 30*10**-6 #F  

rate = 10        #Hz

dur_IR_nQ = None

dur_IR_Q = None

dur_532_Q = None

V_pump = [5,23,4,23,25,26]

def Func_E_Cap(C,V):
    E_cap  = C*V**2/2
    return(E_cap)

E_Cap = Func_E_Cap(C,V_pump)

def Func_L_Input():
    None