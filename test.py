import pandas as pd
import datetime as dt
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import minimize
from ctypes import CFUNCTYPE
import sys 
import json

file1path = sys.argv[1]
file2path = sys.argv[2]
# district = sys.argv[3]
file3path = sys.argv[3]

def calculate_onsite_emission(file1path, file2path,file3path):

        #unit capital cost of each system
    C = {"Solar":3000, "BESS":1500, "HVO":1}       # $/kW,  $/Kwh

    #Emission Factors
    #EF = {"Solar":0.04, "Diesel":2.692, "HVO":0.195, "Fuel oil":2.96,  "Wood":0.06}   #kgCO2e/kWh, kgCO2e/l, kgCO2e/l, kgCO2e/l, kgCO2e/kg
    EF = {"Solar":0.04, "Diesel":2.692, "HVO":0.195, "Fuel oil":0.28,  "Wood":0.06}   
        #kgCO2e/kWh,   kgCO2e/l,        kgCO2e/l,     kgCO2e/kWh,     kgCO2e/kg

    # 1kWh = 3.6 MJ
    Rs_USD = 320    # 1 USD = 320 LKR
        # Read input files
    GridEF_df = pd.read_excel(r"C:\Users\wnspi\OneDrive\Desktop\myNode\FYP\files\Marginal Emission Factors.xlsx")
    Elec_df = pd.read_excel(file1path)
    # dis = district.strip()
    # dis = district.capitalize()

    #Solar1kWp_df = pd.read_excel(r"C:\Users\wnspi\OneDrive\Desktop\myNode\FYP\files\Monthly district solar average for 1kWp in kWh.xlsx",sheet_name = dis)

    # N_build = int(buildings.strip())
    # roof_sizes=[];
    # for i in range(N_build):
    #     L = float(input("Building -%i, roof length(m): " %(i+1)).strip())
    #     W = float(input("Building -%i, roof width(m): " %(i+1)).strip())
    #     roof_sizes.append([L,W])
    #roof_area = float(area.strip()) #m^2

    

    Steam_demand = pd.read_excel(file2path)
    diesel_consump = pd.read_excel(file3path)


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

    Grid_EM = Grid_EM_df.sum().sum() #Total Grid emission for the year



    # Req_battery_cap = (Consump_dis.max())/DoD/eff 
    diesel_CV = 36.9  #MJ/l
    HVO_CV = 34.4     #MJ/l
    diesel_emission = EF["Diesel"] * diesel_consump.iloc[:12,1].sum()

    #if totally replaced by HVO
    # Annual_HVO_req = diesel_consump * diesel_CV / HVO_CV    #liters
    # HVO_emission = Annual_HVO_req * EF["HVO"]

    Steam_kg_TO_kwh = 0.7147

    # Efficiency of fuel oil- burnt boiler
    eff_oil = 0.85
    # Efficiency of biomass boiler
    eff_bio = 0.8

    # Calorific value of wood in MJ/kg
    Cal_wood = 14.7       
    # Calorific value of wood in MJ/L
    Cal_oil = 39.21

    # price of 1liter of fuel oil
    oil_1L = 330
    # price of 1kf of wood
    wood_1kg = 14

    Steam_kWh = Steam_demand["Steam (kg)"].sum() * Steam_kg_TO_kwh
    Fuel_oil_EM = Steam_kWh /eff_oil * EF["Fuel oil"]

    # #if Fuel oil boiler is totally replaced bt biomass
    # Biomass_Boi_size = Steam_demand["Steam (kg)"].max()

    # Biomass_EM = Steam_kWh * EF["Wood"]*3.6/(Cal_wood * eff_bio)

    Total_EM = Grid_EM + diesel_emission + Fuel_oil_EM
    #return Grid_EM,diesel_emission,Fuel_oil_EM,Total_EM

    
    return json.dumps({
        'Grid_EM': round(Grid_EM,2),
        'diesel_emission': round(diesel_emission,2),
        'Fuel_oil_EM': round(Fuel_oil_EM,2),
        'Total_EM': round(Total_EM,2)
    })


# Grid_EM , diesel_emission , Fuel_oil_EM,Total_EM = calculate_onsite_emission(file1path, file2path, district, area, diesel)
em_output=calculate_onsite_emission(file1path, file2path, file3path)
print(em_output)

