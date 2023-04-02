import pandas as pd
import datetime as dt
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import minimize
from ctypes import CFUNCTYPE
import sys 

file1_path = sys.argv[1]
file2_path = sys.argv[2]
def calculate_grid_emission_factors(file1_path, file2_path,district,area,diesel):
    C = {"Solar":3000, "BESS":1500, "HVO":1}       
    EF = {"Solar":0.04, "Diesel":2.692, "HVO":0.195, "Fuel oil":0.28,  "Wood":0.06}   
    Rs_USD = 320    
    GridEF_df = pd.read_excel("C:\Users\wnspi\OneDrive\Desktop\myNode\files\Marginal Emission Factors.xlsx")
    Elec_df = pd.read_excel(file1_path)
    dis = district.strip()
    dis = district.capitalize()
    Solar1kWp_df = pd.read_excel("C:\Users\wnspi\OneDrive\Desktop\myNode\files\Monthly district solar average for 1kWp in kWh.xlsx",sheet_name = dis)
    roof_area = float(area.strip()) 
    diesel_consump = float(diesel)
    Steam_demand = pd.read_excel(file2_path)
    col_names=list(range(48))
    New_GridEF_df = pd.DataFrame(columns = col_names)
    New_Elec_df = pd.DataFrame(columns = col_names)
    m1 = 2  
    m2 = 1  
    cols = 48 
    for i in range(cols):
        New_GridEF_df.iloc[:,i] = GridEF_df.iloc[:,m1*i:m1*i+m1].mean(axis=1)
    for i in range(cols):
        New_Elec_df.iloc[:,i] = Elec_df.iloc[:,m2*i:m2*i+m2].mean(axis=1)  
    Grid_EM_df = New_GridEF_df.multiply(New_Elec_df) 
    Grid_EM = Grid_EM_df.sum().sum() 

    col_names=list(range(24))
    EmReductionSolar1kW_df = pd.DataFrame(columns = col_names)
    m1 = 4 
    cols = 24 

    for i in range(cols):
        EmReductionSolar1kW_df.iloc[:,i] = GridEF_df.iloc[:,m1*i:m1*i+m1].mean(axis=1)

    EmReductionSolar1kW_df = EmReductionSolar1kW_df - EF["Solar"]

    year = 2021
    for i in range(365):
        date_object = dt.date(year, 1, 1) + dt.timedelta(i)
        month_number = date_object.month 
        EmReductionSolar1kW_df.iloc[i,:] = (EmReductionSolar1kW_df.iloc[i,:].multiply(Solar1kWp_df.iloc[:24,month_number].T))/1000 
    EmReductionSolar1kW = EmReductionSolar1kW_df.sum().sum()

    l = 2.279   
    w = 1.134  
    panel_cap = 550 

    panel_sum = roof_area//(l*w)
    max_DC_capacity = panel_sum * panel_cap/1000 

    diesel_CV = 36.9  
    HVO_CV = 34.4     
    diesel_emission = EF["Diesel"] * diesel_consump

    Annual_HVO_req = diesel_consump * diesel_CV / HVO_CV   
    HVO_emission = Annual_HVO_req * EF["HVO"]

    Steam_kg_TO_kwh = 0.7147
    eff_oil = 0.85
    eff_bio = 0.8
    Cal_wood = 14.7       
    Cal_oil = 39.21
    oil_1L = 330
    wood_1kg = 14

    Steam_kWh = Steam_demand["Steam (kg)"].sum() * Steam_kg_TO_kwh
    Fuel_oil_EM = Steam_kWh /eff_oil * EF["Fuel oil"]

    Biomass_Boi_size = Steam_demand["Steam (kg)"].max()

    Biomass_EM = Steam_kWh * EF["Wood"]*3.6/(Cal_wood * eff_bio)

    Total_EM = Grid_EM + diesel_emission + Fuel_oil_EM
    return Total_EM


print(calculate_grid_emission_factors(file1_path, file2_path,))
