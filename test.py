import pandas as pd
import datetime as dt
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import minimize
from ctypes import CFUNCTYPE
import sys 
import json
import ast

file1path = sys.argv[1]
file2path = sys.argv[2]
file3path = sys.argv[3]
buildings = sys.argv[4]
dimensions = sys.argv[5]
district = sys.argv[6]
dimensions=ast.literal_eval(dimensions)
district = district.strip()
district = district.capitalize()

def calculate_onsite_emission(file1path, file2path,file3path,buildings,dimensions,district):

        #unit capital cost of each system
    C = {"Solar":3000, "BESS":1500, "HVO":1}       # $/kW,  $/Kwh

    
    EF = {"Solar":0, "Diesel":2.692, "HVO":0.195, "Fuel oil":0.28,  "Wood":0.007}   
        #kgCO2e/kWh,   kgCO2e/l,        kgCO2e/l,     kgCO2e/kWh,     kgCO2e/kg

    # 1kWh = 3.6 MJ
    Rs_USD = 320    # 1 USD = 320 LKR
        # Read input files
    GridEF_df = pd.read_excel(r"C:\Users\wnspi\OneDrive\Desktop\myNode\FYP\files\Marginal Emission Factors.xlsx")
    Elec_df = pd.read_excel(file1path)
    # dis = district.strip()
    # dis = district.capitalize()

    Solar1kWp_df = pd.read_excel(r"C:\Users\wnspi\OneDrive\Desktop\myNode\FYP\files\Monthly district solar average for 1kWp in kWh.xlsx",sheet_name = district)

    # df1 = pd.read_excel(r"C:\Users\wnspi\OneDrive\Desktop\myNode\FYP\files\LevelizeCost.xlsx",sheet_name= 'PVsystem')

    
    Steam_demand = pd.read_excel(file2path)
    Diesel_cosumption_df = pd.read_excel(file3path)


    col_names=list(range(48))
    New_GridEF_df = pd.DataFrame(columns = col_names)
    New_Elec_df = pd.DataFrame(columns = col_names)
    col_names=list(range(24))
    EmReductionSolar1kW_df = pd.DataFrame(columns = col_names)
    m1 = 4  #time interval changing factor (1/4h to 1h)
    cols = 24 #for hourly data
    for i in range(cols):
        EmReductionSolar1kW_df.iloc[:,i] = GridEF_df.iloc[:,m1*i:m1*i+m1].mean(axis=1)

    EmReductionSolar1kW_df = EmReductionSolar1kW_df - EF["Solar"]
    year = 2021
    for i in range(365):
        date_object = dt.date(year, 1, 1) + dt.timedelta(i)
        month_number = date_object.month
        EmReductionSolar1kW_df.iloc[i,:] = (EmReductionSolar1kW_df.iloc[i,:].multiply(Solar1kWp_df.iloc[:24,month_number].T))/1000 
    EmReductionSolar1kW = EmReductionSolar1kW_df.sum().sum()

    panel_sum = 0
    l = 2.279   #m      panel length
    w = 1.134  #m      panel width
    panel_cap = 550 #wp
    #number of panels required
    for i in dimensions:
        L = i[1]        #roof length
        W = i[0]        #roof width

        c1 = 0.5        #clearence between 8x8 panel sets for both directions
        c2 = 0.02       #clearence between two panels in the width direction (for T clamps)
        columns = int(8*(L-c1)/(8*l + c1))
        rows = int(8*(W-c1)/(8*(w + c2) + c1))
        panel_sum += columns * rows
    max_DC_capacity = panel_sum * panel_cap/1000

    m1 = 2  #time interval changing factor for grid ef (2= 15min to 30 min)
    m2 = 1  #time interval changing factor for elec consumption (No change)
    cols = 48 #for half hourly data
    for i in range(cols):
        New_GridEF_df.iloc[:,i] = GridEF_df.iloc[:,m1*i:m1*i+m1].mean(axis=1)#take average of adjacent groups of 4 columns

    for i in range(cols):
        New_Elec_df.iloc[:,i] = Elec_df.iloc[:,m2*i:m2*i+m2].mean(axis=1)  #take average of adjacent groups of 4 columns

    Grid_EM_df = New_GridEF_df.multiply(New_Elec_df) #quater hourly emission in kgCO2e

    Grid_EM = Grid_EM_df.sum().sum() #Total Grid emission for the year


    diesel_consump = Diesel_cosumption_df.iloc[:12,1].sum()
    # Req_battery_cap = (Consump_dis.max())/DoD/eff 
    diesel_CV = 36.9  #MJ/l
    HVO_CV = 34.4     #MJ/l
    diesel_emission = EF["Diesel"] * diesel_consump

    #if totally replaced by HVO
    Annual_HVO_req = diesel_consump* diesel_CV / HVO_CV    #liters
    HVO_emission = Annual_HVO_req * EF["HVO"]

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

    #if Fuel oil boiler is totally replaced bt biomass
    Biomass_Boi_size = Steam_demand["Steam (kg)"].max()

    Biomass_EM = Steam_kWh * EF["Wood"]*3.6/(Cal_wood * eff_bio)

    DoD = 0.8   #Recommended depth of discharge for Li-ion Batteries 
    eff = 0.95  #Efficiency of BESS 
    m1 = 18*2                    #18:6PM   *2:to half hourly intervals
    n1 = round( (18+2+1/2)*2 )   #+2.5:8.30PM   *2:to half hourly 
    m2 = 7*2                    #7:7AM   *2:to half hourly intervals
    n2 = round( (7+3+1/2)*2 )   #+3.5h:10.30AM   *2:to half hourly 
    EF_ch = New_GridEF_df.iloc[:,m1:n1].mean(axis=1)        #Charging 
    EF_dis = New_GridEF_df.iloc[:,m2:n2].mean(axis=1)       #Discharging 
    Consump_dis = New_Elec_df.iloc[:,m2:n2].sum(axis=1)     #Discharging 
    max_power = New_Elec_df.iloc[:,m2:n2].max().max()
    BatteryEM = ((EF_ch/eff - EF_dis).multiply(Consump_dis)).sum()

    
    Solar_EM_Red = EmReductionSolar1kW * max_DC_capacity
    BESS_EM_Red = - BatteryEM
    GreenDiesel_EM_Red = diesel_emission - HVO_emission
    Biomass_EM_Red = Fuel_oil_EM - Biomass_EM

    Total_EM = Grid_EM + diesel_emission + Fuel_oil_EM
    Total_max_EM_Red=Solar_EM_Red+BESS_EM_Red+GreenDiesel_EM_Red+Biomass_EM_Red
    Remaining=Total_EM-Total_max_EM_Red
    #return Grid_EM,diesel_emission,Fuel_oil_EM,Total_EM
    buildings=int(buildings)
    district=district

    Grid_EM_daily_df = Grid_EM_df.sum(axis=1)
    Grid_EM_daily_df = pd.DataFrame({'Emissions': Grid_EM_daily_df})
    # Create a new column for month
    Grid_EM_daily_df['Month'] = pd.DatetimeIndex(pd.date_range(start='2022-01-01', end='2022-12-31', freq='D')).month
    # Group the DataFrame by month and sum the emissions for each month
    monthly_sum_elec = Grid_EM_daily_df.groupby('Month')['Emissions'].sum().values
    monthly_sum_elec=list(monthly_sum_elec)

    diesel_cosump_data = np.array(Diesel_cosumption_df.iloc[:12,1].values)
    diesel_cosump_data=diesel_cosump_data.tolist()

    Steam_EM = pd.DataFrame({'Steam (kg)': Steam_demand["Steam (kg)"] * Steam_kg_TO_kwh /eff_oil * EF["Fuel oil"]})
    # Create a new column for month
    Steam_EM['Month'] = pd.DatetimeIndex(pd.date_range(start='2022-01-01 00:00:00', end='2022-12-31 23:00:00', freq='H')).month
    monthly_sum_boiler = Steam_EM.groupby('Month')["Steam (kg)"].sum().values
    monthly_sum_boiler=list(monthly_sum_boiler)
    
    return json.dumps({
        'Grid_EM': round(Grid_EM,2),
        'diesel_emission': round(diesel_emission,2),
        'Fuel_oil_EM': round(Fuel_oil_EM,2),
        'Total_EM': round(Total_EM,2),
        'Solar_EM_Red': round(Solar_EM_Red,2),
        'BESS_EM_Red': round(BESS_EM_Red,2),
        'GreenDiesel_EM_Red': round(GreenDiesel_EM_Red,2),
        'Biomass_EM_Red': round(Biomass_EM_Red,2),
        'Total_max_EM_Red': round(Total_max_EM_Red,2),
        'Remaining':round(Remaining,2),
        'buildings':buildings,
        'dimensions': dimensions,
        'district':district,
        'max_DC_capacity':max_DC_capacity,
        'EmReductionSolar1kW':EmReductionSolar1kW,
        'monthly_sum_elec':monthly_sum_elec,
        'diesel_cosump_data':diesel_cosump_data,
        'monthly_sum_boiler':monthly_sum_boiler     
    })



em_output=calculate_onsite_emission(file1path, file2path, file3path,buildings,dimensions,district)
print(em_output)

