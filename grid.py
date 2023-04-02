import pandas as pd
import datetime as dt
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import minimize

#unit capital cost of each system
C = {"Solar":3000, "BESS":1500}       # $/kW  $/Kwh
#Emission Factors(kgCO2e/kWh)
EF = {"Solar":0.04}

#Grid Emission Calculation                         

GridEF_df = pd.read_excel('C:/FYP/myNode/files/Marginal Emission Factors.xlsx')
Elec_df = pd.read_excel('C:/FYP/myNode/files/Scaled data from Imported electricity- dan.xlsx')

col_names=list(range(48))
New_GridEF_df = pd.DataFrame(columns = col_names)
New_Elec_df = pd.DataFrame(columns = col_names)

m1 = 2  #time interval changing factor for grid ef (2= 15min to 30 min)
m2 = 1  #time interval changing factor for elec consumption (No change)
cols = 48 #for half hourly data

for i in range(cols):
  New_GridEF_df.iloc[:,i] = GridEF_df.iloc[:,m1*i:m1*i+m1].mean(axis=1)#take average of adjacent groups of 4 columns

for i in range(cols):
  New_Elec_df.iloc[:,i] = Elec_df.iloc[:,m2*i:m2*i+m2].mean(axis=1)  #take average of adjacent groups of 4 columns

Grid_EM_df = New_GridEF_df.multiply(New_Elec_df) #quater hourly emission in kgCO2e

#---------------------------------------------------------------------
Grid_EM = Grid_EM_df.sum().sum() #Total Grid emission for the year
#---------------------------------------------------------------------
print("Grid Emission = %f kgCO2" %Grid_EM)


