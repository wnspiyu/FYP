import pandas as pd
import datetime as dt
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import minimize
from ctypes import CFUNCTYPE
import numpy_financial as npf
import math
import sys 
import json
import ast

target=sys.argv[1]
dimensions=sys.argv[2]
district = sys.argv[3]

dimensions=ast.literal_eval(dimensions)
target=int(target)
sys.stderr = sys.stdout

def optimization(target,dimensions,district):
    dis = district.strip()
    dis = district.capitalize()
    roof_sizes=dimensions
    C = {"Solar":3000, "BESS":1500, "HVO":1} 
    EF = {"Solar":0.04, "Diesel":2.692, "HVO":0.195, "Fuel oil":0.28,  "Wood":0.06}
    Rs_USD = 320 
    Total_EM=138113.12
    GridEF_df = pd.read_excel(r"C:\Users\wnspi\OneDrive\Desktop\myNode\FYP\files\Marginal Emission Factors.xlsx")
    Solar1kWp_df = pd.read_excel(r"C:\Users\wnspi\OneDrive\Desktop\myNode\FYP\files\Monthly district solar average for 1kWp in kWh.xlsx",sheet_name = dis)
    Diesel_cosumption_df=pd.read_excel(r"C:\Users\wnspi\OneDrive\Desktop\myNode\FYP\uploads\Monthly Diesel consumption Data.xlsx")
    Steam_demand = pd.read_excel(r"C:\Users\wnspi\OneDrive\Desktop\myNode\FYP\uploads\Scaled steam demand data.xlsx")
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
    for i in roof_sizes:
        L = i[1]        #roof length
        W = i[0]        #roof width
        c1 = 0.5        #clearence between 8x8 panel sets for both directions
        c2 = 0.02       #clearence between two panels in the width direction (for T clamps)
        columns = int(8*(L-c1)/(8*l + c1))
        rows = int(8*(W-c1)/(8*(w + c2) + c1))
        panel_sum += columns * rows
    max_DC_capacity = panel_sum * panel_cap/1000 #kW
    DoD = 0.8   #Recommended depth of discharge for Li-ion Batteries 
    eff = 0.95  #Efficiency of BESS 
    m1 = 18*2                    #18:6PM   *2:to half hourly intervals
    n1 = round( (18+2+1/2)*2 )   #+2.5:8.30PM   *2:to half hourly intervals
    m2 = 7*2                    #7:7AM   *2:to half hourly intervals
    n2 = round( (7+3+1/2)*2 )   #+3.5h:10.30AM   *2:to half hourly intervals
    EF_ch = New_GridEF_df.iloc[:,m1:n1].mean(axis=1)        #Charging interval avg EF for 365 days
    EF_dis = New_GridEF_df.iloc[:,m2:n2].mean(axis=1)       #Discharging interval avg EF for 365 days
    Consump_dis = New_Elec_df.iloc[:,m2:n2].sum(axis=1)     #Discharging interval electricity consumption for 365 days
    max_power = New_Elec_df.iloc[:,m2:n2].max().max()
    BatteryEM = ((EF_ch/eff - EF_dis).multiply(Consump_dis)).sum()  #Negative Emission 
    Req_battery_cap = (Consump_dis.max())/DoD/eff  #Oversized
    diesel_consump = Diesel_cosumption_df.iloc[:12,1].sum() #annual diesel consumption
    diesel_CV = 36.9  #MJ/l
    HVO_CV = 34.4     #MJ/l
    diesel_emission = EF["Diesel"] * diesel_consump
    Annual_HVO_req = diesel_consump * diesel_CV / HVO_CV    #liters
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
    r = 0.1
    district = district
    DISTRICT = ['COLOMBO', 'GAMPAHA', 'KALUTHARA', 'GALLE', 'MATARA', 'HAMBANTHOTA', 'AMPARA', 'BATTICALOA', 'TRINCOMALEE', 'MULLAITIVE', 'JAFFNA', 'KILINOCHCHI', 'MANNAR', 'VAVNIYA', 'PUTTALAM', 'KURUNAGALA', 'ANURADHAPURA', 'POLONNARUWA', 'MATALE', 'KANDY', 'NUWARA ELIYA', 'KEGALLE', 'RATNAPURA', 'BADULLA', 'MONARAGALA'];
    Solar_Gen = [1512.047, 1453.854, 1463.566, 1510.533, 1561.024, 1552.867 , 1484.226, 1542.362, 1523.683, 1529.024, 1521.172, 1522.26, 1583.638, 1491.192, 1524.986, 1429.35, 1483.562, 1499.308, 1377.517, 1417.402, 1318.484, 1419.132, 1381.223, 1446.717, 1464.645]
    district = district.upper()
    for i in range(len(DISTRICT)):
        if district == DISTRICT[i]:
            n=i
        break
    Annual_gen = Solar_Gen[n]
    df1 = pd.read_excel(r"C:\Users\wnspi\OneDrive\Desktop\myNode\FYP\files\LevelizeCost.xlsx",sheet_name= 'PVsystem')
    PV_CC = list(df1.CC)          # Capital cost
    PV_OM1 = list(df1.OM1)        # O&M cost fro tirst two years
    PV_OM2 = list(df1.OM2)        # O&M cost for other years
    PV_R = list(df1.Rplacement)   # Inverter replacement cost
    PV_Tariff = 34.5/Rs_USD
    PV_GHG = EmReductionSolar1kW
    PV_cost = []
    PV_OM = []
    PV_sell_benefit = []
    PV_CO2_benefit = []
    PV_benefit = []
    PV_CF = []
    for k in range(21):
        if k==0:
        # Initial year take as 0
            PV_benefit.append(0)
            PV_sell_benefit.append(0)
            PV_CO2_benefit.append(0)
        else:
            Sum1 = Annual_gen* ((1-0.004)**(k-1)) 
            PV_sell_benefit.append(Sum1)
            Sum2 = PV_GHG * 0.0127 * ((1-0.004)**(k-1))
            PV_CO2_benefit.append(Sum2)
            PV_benefit.append(PV_Tariff *Sum1 + Sum2)
    for j in range (21):
        Sum_cost = PV_CC[j] + PV_R[j]
        Sum_OM  = PV_OM1[j] + PV_OM2[j]
        PV_cost.append(Sum_cost)
        PV_OM.append(Sum_OM)
        CF = PV_benefit[j]-Sum_cost
        PV_CF.append(float(CF))
    def Cashflows(filename):
        df = pd.read_excel(r"C:\Users\wnspi\OneDrive\Desktop\myNode\FYP\uploads\LevelizeCost.xlsx",sheet_name = filename)
        CC = list(df.CC)
        OM1 = list(df.OM1)
        OM2 = list(df.OM2)
        R = list(df.Rplacement)
        cost = []
        for j in range (21):
            Sum_cost = CC[j] + OM1[j] + OM2[j] + R[j]
            cost.append(Sum_cost)
        return cost
    Bat_cost = Cashflows('BatterySystem')
    Boi_cost = Cashflows('BiomassBoiler')
    Bat_Dis_benefit = []        # Benefit from charging and discharging batttery
    Bat_CO2_benefit = []        # Benefit from CO2 charge saving
    Dis_price = 37/Rs_USD
    cha_price = 40/Rs_USD
    Bat_Deg = 0.00292
    for k1 in range(21):
        if k1==0:
            Bat_Dis_benefit.append(0)
            Bat_CO2_benefit.append(0)
        else:
            Sum1 = (Dis_price - cha_price) * ((1 - Bat_Deg)**(k1-1))
            Bat_Dis_benefit.append(Sum1)       
            Sum2 = 0.0127*((1 - Bat_Deg)**(k1-1))
            Bat_CO2_benefit.append(Sum2)
    Boi_benefit = []
    oil_price = oil_1L* 3.6/(Cal_oil * Rs_USD * eff_oil)
    wood_price = wood_1kg* 3.6/(Cal_wood * Rs_USD * eff_bio)
    Boi_Deg = 0.00292
    for k2 in range(21):
        if k2==0:
            Boi_benefit.append(0)
        else:        
            Sum = (oil_price - wood_price)*((1-Boi_Deg)**(k2-1)) + (EF["Fuel oil"]/eff_oil - EF["Wood"]*3.6/Cal_wood / eff_bio) *0.0127*((1-Boi_Deg)**(k2-1))
            Boi_benefit.append(Sum)
    Gen_CF = []
    Diesel_price = 1.106                      # price for generating 1 kW
    HVO_price = 1.13
    Annual_HVO_CF = ( Diesel_price * HVO_CV/diesel_CV - HVO_price) + (EF["Diesel"]*HVO_CV/diesel_CV - EF["HVO"])*0.0127
    Gen_CF = [Annual_HVO_CF]*20
    Gen_CF.insert(0,0)
    PV_npv = npf.npv(r, PV_CF)
    PV_OM_npv = npf.npv(r, PV_OM)
    Bat_cost_npv = npf.npv(r, Bat_cost)
    Bat_Dis_benefit_npv = npf.npv(r, Bat_Dis_benefit)               # NPV of benefit of charging and discharging duration
    Bat_CO2_benefit_npv = npf.npv(r, Bat_CO2_benefit)               # NPV of benefit of CO2 charge saving
    Boi_cost_npv = npf.npv(r, Boi_cost)
    Boi_benefit_npv = npf.npv(r, Boi_benefit)
    DG_npv = npf.npv(r, Gen_CF)
    Steam_kg_TO_kwh = 0.7147
    def objective(x):
        SolarPV_NPV = x[0] * PV_npv - ( PV_OM_npv if round(x[0]) > 0.0 else 0)
        Battery_consump = (Consump_dis.apply(lambda i:x[1] if x[1] < i else i)) #Battery energy usage for each day * 365
        BatteryEM =  (-(EF_ch/eff - EF_dis).multiply(Battery_consump)).sum()      #Annual emission reduction
        Annual_consump = Battery_consump.sum()
        BESS_cost = - (x[1]/(DoD * eff)) * Bat_cost_npv + Annual_consump * Bat_Dis_benefit_npv + BatteryEM * Bat_CO2_benefit_npv
        Annual_Total_Steam_demand = Steam_demand["Steam (kg)"].sum() #steam kg
        Biomass_steam_supply = Steam_demand["Steam (kg)"].apply(lambda i:x[3] if x[3] < i else i)     #hourly steam data in kg
        #x[3] =  boiler capacity in steam kg/h
        Annual_Biomass_steam_supply = (Biomass_steam_supply.sum()) * Steam_kg_TO_kwh    #Annual energy consumption from biomass boiler in kWh
        Boiler_NPV = - x[3] * Steam_kg_TO_kwh * Boi_cost_npv + Annual_Biomass_steam_supply * Boi_benefit_npv
        NPV = SolarPV_NPV + BESS_cost + DG_npv * x[2] + Boiler_NPV 
        return -NPV
    print("\n\n--- Minimum system requirements for maximum emission reduction ---\n")
    print("PV System: ")
    print("Solar panel specification\n  Brand: JA Solar\n  Type: JAM72S30-550/MR/1500V \n  Dimensions: 2279mm X 1134mm\n  Rated Maximum Power: 550W")   
    print("  Datasheet: https://www.eeusolar.com/pdf/JAM72S30-525-550-MR.pdf")   
    print("No. of panels = %i" %(panel_sum))
    print("DC capacity for Solar PV = %.2f kW" % max_DC_capacity)
    print("\n")
    print("Battery Energy Storage System:")
    print("Battery specification:")
    print("  Brand:Mastervolt")
    print("  Type: MLI Ultra 12/1250")   #Dimensions: 2279mm X 1134mm\n  Rated Maximum Power Power: 550W")  ")
    print("  Dimensions: 330mm x 173mm x 210mm")
    print("  Nominal Battery Voltage: 12V")
    print("  Nominal Battery Capacity: 100Ah")
    print("  Datasheet: https://www.mastervolt.com/products/li-ion/mli-ultra-12-1250/pdf/") 
    print("Recommended Depth of Discharge = %.1f" % DoD)
    print("Battery Capacity = %.2f kWh" % Req_battery_cap)
    #print("Minimum Power Rating = %.2f kW" %max_power)
    print("\n")
    print("Diesel Generator Fuel:")
    print("Recommended Low Carbon Technology: Full replacement of Diesel by Green Diesel (HVO)")
    print("Annual Green Diesel Fuel Capacity = %.2f l" % Annual_HVO_req)
    print("\n")
    print("Steam Boiler:")
    print("Recommended Low Carbon Technology: Full replacement of oil boiler by biomass boiler ")
    print("Biomass Boiler Size = %.2f steam kg/h" %Biomass_Boi_size)
    print("\n")
    Solar_EM_Red = EmReductionSolar1kW * max_DC_capacity
    BESS_EM_Red = - BatteryEM
    GreenDiesel_EM_Red = diesel_emission - HVO_emission
    Biomass_EM_Red = Fuel_oil_EM - Biomass_EM
    print("\n")
    EmTarget = target
    def constraint1(x):
        Battery_consump = Consump_dis.apply(lambda i:x[1] if x[1] < i else i)
        BatteryEM = ((EF_ch/eff - EF_dis).multiply(Battery_consump)).sum()  #negative -> emission reduction
        Annual_Total_Steam_demand = Steam_demand["Steam (kg)"].sum() #steam kg
        Biomass_steam_supply = Steam_demand["Steam (kg)"].apply(lambda i:x[3] if x[3] < i else i)     #hourly steam data in kg
        Annual_Biomass_steam_supply = (Biomass_steam_supply.sum()) * Steam_kg_TO_kwh     #Annual energy consumption from biomass boiler in kWh
        BoilerEM_red = (EF["Fuel oil"]/eff_oil - EF["Wood"]*3.6/Cal_wood / eff_bio) * Annual_Biomass_steam_supply
        DG_EM_Reduc = x[2] * ( HVO_CV / diesel_CV * EF["Diesel"] - EF["HVO"])
        return EmTarget - (Total_EM - EmReductionSolar1kW * x[0] + BatteryEM - DG_EM_Reduc - BoilerEM_red)  # >= 0k
    n = 4
    x0 = np.zeros(n)
    #x0[0] = max_DC_capacity/2
    x0[0] = 0.0
    x0[1] = 0.0
    x0[2] = 0.0
    x0[3] = 0.0
    b0 = (0, max_DC_capacity)
    b1 = (0, Consump_dis.max())
    b2 = (0, diesel_consump * diesel_CV / HVO_CV)
    b3 = (0,Steam_demand["Steam (kg)"].max())
    bnds = (b0, b1, b2, b3)
    con1 = {'type': 'ineq', 'fun': constraint1}
    cons = ([con1])
    solution = minimize(objective,x0,method='SLSQP',bounds=bnds,constraints=cons)
    x = solution.x
    Tstc = 25 #Standard test condition temperature
    Tmax = 39.5+25
    Tmin = 14.4
    Eff = 0.213                   #Panel efficiency
    P_panel = 550                 #Rated maximum power of a panel
    Voc_panel = 49.9              #open circuit voltage
    Vmp_panel = 41.96             #Maximum power voltage
    Coef_T_Voc = -0.00275         #Temperature coeffient of Voc
    Coef_T_Pmp = -0.0035          #Temperature coeffient of Pmp
    Voc_60 = 1100                 #Maximum input voltage
    Vmp_60 =200                  #MPPT Operating Voltage Range
    N_mppt = 6
    Voc_100 = 1100                #Maximum input voltage
    Vmp_100 =200                 #MPPT Operating Voltage Range
    N_mppt = 10
    def PVsizing(P_PV):
        N_panel = math.ceil(P_PV*1000/P_panel)
        N_100kW = (P_PV // 100)                #No. of 100kW inverters
        N_60kW = 0
        P_remain = P_PV % 100
        if 72 >= P_remain > 20:
            N_60kW = 1
        elif P_remain > 72:
            N_100kW =+ 1
        return N_panel, P_PV, N_100kW, N_60kW
    def stringsizing(Inv_type):
        if Inv_type == 100 or Inv_type == 60 :
            Cor_Voc = Voc_panel * (1 + Coef_T_Voc * (Tmin - Tstc))    #Corrected Voc of panel
            N_max = Voc_100 // Cor_Voc
            Cor_Vmp = Vmp_panel * (1 + Coef_T_Pmp * (Tmax - Tstc))    #Corrected Vmp of panel
            N_min = (Vmp_100 // Cor_Vmp) + 1
            return N_max, N_min
    Battery_Cap = 100 #Ah
    Battery_Volt = 12 #V
    BESS_size = x[1]/DoD/eff
    default_sys_voltage = 48 #V
    if BESS_size==0:
        Series_con = 0
    else:
        Series_con = default_sys_voltage/Battery_Volt
    Parallel_con = math.ceil(BESS_size*1000/(default_sys_voltage*Battery_Cap)) #math ceil
    print("\n-- Suggested sytem for desired emission reduction --")
    print("DC capacity for Solar PV = %.2f kW" % x[0])
    print("Battery Capacity: %.2f kWh" % (x[1]/DoD/eff) )
    print("Annual HVO fuel requirement: %.2f l" % x[2])
    print("Biomass Boiler Capacity: %.2f steam kg/h" % x[3])
    print("\n")
    print("Solar system Sizing:")
    N_panel,P_PV,N_100kW,N_60kW = PVsizing(x[0])
    print('PV system capacity: ',P_PV)
    print('PV system generated energy: ',P_PV*Annual_gen)
    print('No. of solar panel: ',N_panel)
    print('No. of 100kW inverters: ',N_100kW)
    print('No. of 60kW inverters: ',N_60kW)
    N_max, N_min = stringsizing(100)
    print('Maximum number of panel for a string: ',N_max)
    print('Minimum number of panel for a string: ',N_min)
    print("\n")
    practical_BESS_size = (Battery_Volt * Series_con) * (Battery_Cap * Parallel_con)
    print("BESS Sizing:")
    print("  BESS Voltage = %i" % default_sys_voltage)
    print("  No of batteries in Series per string = %i" %Series_con)
    print("  No of strings in parallel = %i" %Parallel_con)
    print("  Battery Bank Capacity = %.2f Ah" %(practical_BESS_size/default_sys_voltage))
    print("\n-- For suggested system --")
    print('NPV: $%.2f ' %(-objective(x)))
    print("New Emission: %.2f kgCO2e" % -(constraint1(x)-EmTarget))   #determined according to constraint function output
    print("\n")
    Battery_consump = (Consump_dis.apply(lambda i:x[1] if x[1] < i else i))   #Battery energy usage for each day * 365
    BatteryEM = (-(EF_ch/eff - EF_dis).multiply(Battery_consump)).sum()       #Annual emission
    Annual_consump = Battery_consump.sum()
    Annual_Total_Steam_demand = Steam_demand["Steam (kg)"].sum() #steam kg
    Biomass_steam_supply = Steam_demand["Steam (kg)"].apply(lambda i:x[3] if x[3] < i else i)     #hourly steam data in kg
    Annual_Biomass_steam_supply = (Biomass_steam_supply.sum())*0.7147     #Annual energy consumption from biomass boiler in kWh
    PV = x[0]             # PV capacity kW
    PV_GHG = EmReductionSolar1kW
    Battery = x[1] /DoD / eff        # Battery capacity in kWh
    HVO_DG = x[2]         # Annual HVO requirment in litres
    Boiler = x[3] * Steam_kg_TO_kwh        # Biomass Boiler capacity kWh 
    PV_Tariff = 34.5/Rs_USD
    PV_constant = PV * PV_Tariff
    PVf_sell_benefit = [num * PV_constant for num in PV_sell_benefit]
    PVf_CO2_benefit = [num * PV for num in PV_CO2_benefit]
    PVf_benefit = np.add(PVf_sell_benefit,PVf_CO2_benefit)
    PVf_NOOM_cost = [num * PV for num in PV_cost]
    PVf_cost = np.add(PVf_NOOM_cost,PV_OM)
    PVf_CF = np.subtract(PVf_benefit,PVf_cost)
    Batf_cost = [num * Battery for num in Bat_cost]
    Batf_Dis_benefit = [num * Annual_consump for num in Bat_Dis_benefit]
    Batf_CO2_benefit = [num * BatteryEM for num in Bat_CO2_benefit]
    Batf_benefit = np.add(Batf_Dis_benefit,Batf_CO2_benefit)
    Batf_CF = np.subtract(Batf_benefit,Batf_cost)
    Boif_cost = [num * Boiler for num in Boi_cost]
    Boif_benefit = [num * Annual_Biomass_steam_supply for num in Boi_benefit]
    Boiff_CF = np.subtract(Boif_benefit,Boif_cost)
    Genf_CF = [num * HVO_DG for num in Gen_CF]
    SYS_COST = []
    SYS_BENEFIT = []
    SYS_CF = []
    for z in range(21):
        cost = PVf_cost[z] + Batf_cost[z] + Boif_cost[z]
        benifit = PVf_benefit[z] + Batf_benefit[z] + Boif_benefit[z] + Genf_CF[z]
        cf = benifit - cost
        SYS_COST.append(cost)
        SYS_BENEFIT.append(benifit)
        SYS_CF.append(float(cf))
    irr = npf.irr(SYS_CF)
    npv = npf.npv(0.1, SYS_CF)
    CUM_CF = []
    for l in range(21):
        if l==0:
            CUM_CF.append(SYS_CF[l])
        else:
            Sum = CUM_CF[l-1] + SYS_CF[l]
            CUM_CF.append(Sum)
    for m in range (21):
        if  CUM_CF[m] >= 0 :
            PPB = m
            break
        else:
            PPB = 0
    Cap_cost_arrays = np.array([PVf_cost, Batf_cost, Boif_cost])
    SYS_Capcost = np.sum(Cap_cost_arrays[:,0])
    print('Capital cost of the overall energy system: $ %.2f ' %SYS_Capcost)
    print('IRR of the overall energy system: %.2f' %(irr*100))
    print('NPV of the overall energy system: $ %.2f ' %npv)
    print("Payback Period of the overall energy system: %i Y" %PPB)

finall=optimization(target,dimensions,district)
print(type(finall))