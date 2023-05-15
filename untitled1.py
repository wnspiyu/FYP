import pandas as pd
import datetime as dt
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import minimize
from ctypes import CFUNCTYPE
#import openpyxl  # work from excel workbook
import numpy_financial as npf
import math

#Emission Factors
#EF = {"Solar":0.04, "Diesel":2.692, "HVO":0.195, "Fuel oil":2.96,  "Wood":0.06}   #kgCO2e/kWh, kgCO2e/l, kgCO2e/l, kgCO2e/l, kgCO2e/kg
EF = {"Solar":0, "Diesel":2.692, "HVO":0.195, "Fuel oil":0.28,  "Wood":0.007}   
      #kgCO2e/kWh,   kgCO2e/l,        kgCO2e/l,     kgCO2e/kWh,     kgCO2e/kg

# 1kWh = 3.6 MJ
Rs_USD = 320    # 1 USD = 320 LKR


#####################################################################################################################################
#                                 USER INPUTS                         
#####################################################################################################################################
Elec_df = pd.read_excel('/content/gdrive/My Drive/FYP/Hirdaramini Data Reading/Scaled data from Imported electricity- dan.xlsx')

district = input("Enter Your District: ").strip()
district = district.capitalize()

N_build = int(input("Number of buildings available with solarPV mounting capability: ").strip())
roof_sizes=[];
for i in range(N_build):
    L = float(input("Building -%i, roof length(m): " %(i+1)).strip())
    W = float(input("Building -%i, roof width(m): " %(i+1)).strip())
    roof_sizes.append([L,W])

Diesel_cosumption_df = pd.read_excel('/content/gdrive/My Drive/FYP/Hirdaramini Data Reading/Monthly Diesel consumption Data.xlsx')

Steam_demand = pd.read_excel('/content/gdrive/My Drive/FYP/Hirdaramini Data Reading/Scaled steam demand data.xlsx')

#####################################################################################################################################
#                                 DATABASE                       
#####################################################################################################################################
GridEF_df = pd.read_excel('/content/gdrive/MyDrive/FYP/Hirdaramini Data Reading/Marginal Emission Factors.xlsx')
Solar1kWp_df = pd.read_excel('/content/gdrive/My Drive/FYP/Hirdaramini Data Reading/Monthly district solar average for 1kWp in kWh.xlsx',sheet_name = district)

#####################################################################################################################################
#                                 Grid Emission Calculation                         
#####################################################################################################################################

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

#####################################################################################################################################
#                                 Solar Emission from a 1kW Solar PV system                         
#####################################################################################################################################

col_names=list(range(24))
EmReductionSolar1kW_df = pd.DataFrame(columns = col_names)
m1 = 4  #time interval changing factor (1/4h to 1h)
cols = 24 #for hourly data

for i in range(cols):
  EmReductionSolar1kW_df.iloc[:,i] = GridEF_df.iloc[:,m1*i:m1*i+m1].mean(axis=1)#take average of adjacent groups of 4 columns

EmReductionSolar1kW_df = EmReductionSolar1kW_df - EF["Solar"]

#Find the days for each month and multiply net emission factor by solar generation for each month
year = 2021
for i in range(365):
  date_object = dt.date(year, 1, 1) + dt.timedelta(i)
  month_number = date_object.month # get the month number from the datetime object
  EmReductionSolar1kW_df.iloc[i,:] = (EmReductionSolar1kW_df.iloc[i,:].multiply(Solar1kWp_df.iloc[:24,month_number].T))/1000 
  #for each day for each hour (gridEF-solarEF)xHourlySolarGeneration
  #/1000 -> Wh generation data to kWh

#---------------------------------------------------------------------
EmReductionSolar1kW = EmReductionSolar1kW_df.sum().sum()
#---------------------------------------------------------------------

#####################################################################################################################################
#            Solar PV system Upper bound Calculation considering available rooftop area                         
#####################################################################################################################################

panel_sum = 0
l = 2.279   #m      panel length
w = 1.134  #m      panel width
panel_cap = 550 #wp
#number of panels required
for i in roof_sizes:
    L = i[0]        #roof length
    W = i[1]        #roof width

    c1 = 0.5        #clearence between 8x8 panel sets for both directions
    c2 = 0.02       #clearence between two panels in the width direction (for T clamps)
    columns = int(8*(L-c1)/(8*l + c1))
    rows = int(8*(W-c1)/(8*(w + c2) + c1))
    panel_sum += columns * rows

#---------------------------------------------------------------------
max_DC_capacity = panel_sum * panel_cap/1000 #kW
#---------------------------------------------------------------------


#EmAfterMaxSolar = Grid_EM - EmReductionSolar1kW * max_DC_capacity
#print("Minimum Emission, achievable by %0.2f kW Solar PV system alone = %f" %(max_DC_capacity,EmAfterMaxSolar) )


#####################################################################################################################################
#            BESS                         
#####################################################################################################################################

DoD = 0.8   #Recommended depth of discharge for Li-ion Batteries 
eff = 0.95  #Efficiency of BESS 

#-------------------Charging Interval------------------------------------
m1 = 18*2                    #18:6PM   *2:to half hourly intervals
n1 = round( (18+2+1/2)*2 )   #+2.5:8.30PM   *2:to half hourly intervals

#-------------------Discharging Interval---------------------------------
m2 = 7*2                    #7:7AM   *2:to half hourly intervals
n2 = round( (7+3+1/2)*2 )   #+3.5h:10.30AM   *2:to half hourly intervals


EF_ch = New_GridEF_df.iloc[:,m1:n1].mean(axis=1)        #Charging interval avg EF for 365 days
EF_dis = New_GridEF_df.iloc[:,m2:n2].mean(axis=1)       #Discharging interval avg EF for 365 days
Consump_dis = New_Elec_df.iloc[:,m2:n2].sum(axis=1)     #Discharging interval electricity consumption for 365 days
max_power = New_Elec_df.iloc[:,m2:n2].max().max()

BatteryEM = ((EF_ch/eff - EF_dis).multiply(Consump_dis)).sum()  #Negative Emission 

Req_battery_cap = (Consump_dis.max())/DoD/eff  #Oversized
#print("Required Battery Capacity for maximum emission reduction = %f kWh" % Req_battery_cap)
#print("Emission reduction from BESS = %f kgCO2" %BatteryEM)


#####################################################################################################################################
#                               Diesel Generator                      
#####################################################################################################################################

diesel_consump = Diesel_cosumption_df.iloc[:12,1].sum() #annual diesel consumption

diesel_CV = 36.9  #MJ/l
HVO_CV = 34.4     #MJ/l
diesel_emission = EF["Diesel"] * diesel_consump

#if totally replaced by HVO
Annual_HVO_req = diesel_consump * diesel_CV / HVO_CV    #liters
HVO_emission = Annual_HVO_req * EF["HVO"]

#print("Maximum HVO capacity = %f l" % Annual_HVO_req)

#####################################################################################################################################
#            BOILER                       
#####################################################################################################################################
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


#####################################################################################################################################
#            COST FUNCTION                      
#####################################################################################################################################

r = 0.1
#district = input("Enter the district: ").strip()

# Annual solar generation potential of each district
DISTRICT = ['COLOMBO', 'GAMPAHA', 'KALUTHARA', 'GALLE', 'MATARA', 'HAMBANTHOTA', 'AMPARA', 'BATTICALOA', 'TRINCOMALEE', 'MULLAITIVE', 'JAFFNA', 'KILINOCHCHI', 'MANNAR', 'VAVNIYA', 'PUTTALAM', 'KURUNAGALA', 'ANURADHAPURA', 'POLONNARUWA', 'MATALE', 'KANDY', 'NUWARA ELIYA', 'KEGALLE', 'RATNAPURA', 'BADULLA', 'MONARAGALA'];
Solar_Gen = [1512.047, 1453.854, 1463.566, 1510.533, 1561.024, 1552.867 , 1484.226, 1542.362, 1523.683, 1529.024, 1521.172, 1522.26, 1583.638, 1491.192, 1524.986, 1429.35, 1483.562, 1499.308, 1377.517, 1417.402, 1318.484, 1419.132, 1381.223, 1446.717, 1464.645]

district = district.upper()
for i in range(len(DISTRICT)):
  if district == DISTRICT[i]:
    n=i
    break
Annual_gen = Solar_Gen[n]
# print(Annual_gen)

# import data list of cost data of PV system from csv file
df1 = pd.read_excel('/content/gdrive/My Drive/FYP/Hirdaramini Data Reading/LevelizeCost.xlsx',sheet_name= 'PVsystem')

# Cashflow of PV system
# Cost for 20 years
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

# Calculate the benefit of PV system
for k in range(21):
  if k==0:
    # Initial year take as 0
    PV_benefit.append(0)
    PV_sell_benefit.append(0)
    PV_CO2_benefit.append(0)

  else:
    # Assume solar tariff method as net plus which means sell all the solar units to the CEB
    # Carbon pricing has taken as $12.7/MT
    # system degredation take as 0.4%
    Sum1 = Annual_gen* ((1-0.004)**(k-1)) 
    PV_sell_benefit.append(Sum1)
    Sum2 = PV_GHG * 0.0127 * ((1-0.004)**(k-1))
    PV_CO2_benefit.append(Sum2)

    PV_benefit.append(PV_Tariff *Sum1 + Sum2)

# Calculate cost and cashflow of the PV system
for j in range (21):
  Sum_cost = PV_CC[j] + PV_R[j]
  Sum_OM  = PV_OM1[j] + PV_OM2[j]
  PV_cost.append(Sum_cost)
  PV_OM.append(Sum_OM)
  CF = PV_benefit[j]-Sum_cost
  PV_CF.append(float(CF))


# Define a function to call cashflows of BESS and Boiler systems 
def Cashflows(filename):

    # import data list of cost data of Boiler system from csv file
    df = pd.read_excel('/content/gdrive/My Drive/FYP/Hirdaramini Data Reading/LevelizeCost.xlsx',sheet_name = filename)

    # Cashflow of Boiler system
    # Cost for 20 years
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


#######         Benefit and fuel cost of BESS system for 1kWh           ######
#_____________________________________________________________________________


Bat_Dis_benefit = []        # Benefit from charging and discharging batttery
Bat_CO2_benefit = []        # Benefit from CO2 charge saving

# Unit price of electricity tariff when discharging is Rs.37/=
# Unit price of electricity tariff when charging is Rs.40/=
Dis_price = 37/Rs_USD
cha_price = 40/Rs_USD
Bat_Deg = 0.00292

for k1 in range(21):
      if k1==0:
        Bat_Dis_benefit.append(0)
        Bat_CO2_benefit.append(0)

      else:
        # Assume revenue come from CO2 charge reduction + saving cost of imported electricity
        # Carbon pricing has taken as $12.7/MT
        Sum1 = (Dis_price - cha_price) * ((1 - Bat_Deg)**(k1-1))
        Bat_Dis_benefit.append(Sum1)

        # Assume revenue come from CO2 charge reduction + saving cost of imported electricity
        # Carbon pricing has taken as $12.7/MT
        Sum2 = 0.0127*((1 - Bat_Deg)**(k1-1))
        Bat_CO2_benefit.append(Sum2)
        


#######       Benefit and fuel cost of Boiler system for 1kWh           ######
#_____________________________________________________________________________

Boi_benefit = []

# Fuel oil price for making 1kWh of energy in boiler is Rs.30.294 = Price of 1L * 3.6/Calorific value
# Wood price for making 1kWh of energy in boiler is Rs.45/=
oil_price = oil_1L* 3.6/(Cal_oil * Rs_USD * eff_oil)
wood_price = wood_1kg* 3.6/(Cal_wood * Rs_USD * eff_bio)
Boi_Deg = 0.00292

for k2 in range(21):
      if k2==0:
        Boi_benefit.append(0)
      else:
        # Assume revenue come from CO2 charge reduction + saving cost of using wood over fuel oil
        # Carbon pricing has taken as $12.7/MT
        Sum = (oil_price - wood_price)*((1-Boi_Deg)**(k2-1)) + (EF["Fuel oil"]/eff_oil - EF["Wood"]*3.6/Cal_wood / eff_bio) *0.0127*((1-Boi_Deg)**(k2-1))
        Boi_benefit.append(Sum)


#######             Benefit and fuel cost of Diesel generator system for 1kWh             ######
#_____________________________________________________________________________


Gen_CF = []

# Diesel price for making 1kWh of energy in boiler is Rs.420/=, $ 1.3
# Hydrotreated Vegetable Oil(HVO) price for making 1kWh of energy in boiler is $1.13

Diesel_price = 1.106                      # price for generating 1 kWh
HVO_price = 1.13
Annual_HVO_CF = ( Diesel_price * HVO_CV/diesel_CV - HVO_price) + (EF["Diesel"]*HVO_CV/diesel_CV - EF["HVO"])*0.0127

Gen_CF = [Annual_HVO_CF]*20
Gen_CF.insert(0,0)




# NPV for 1kW PV system
PV_npv = npf.npv(r, PV_CF)
# NPV of O&M cost of PV system
PV_OM_npv = npf.npv(r, PV_OM)
# NPV of capital cost for 1kW of BESS
Bat_cost_npv = npf.npv(r, Bat_cost)
# NPV of benefit for 1 kWh of BESS
Bat_Dis_benefit_npv = npf.npv(r, Bat_Dis_benefit)               # NPV of benefit of charging and discharging duration
Bat_CO2_benefit_npv = npf.npv(r, Bat_CO2_benefit)               # NPV of benefit of CO2 charge saving
# NPV of capital cost for 1kW of biomass boiler
Boi_cost_npv = npf.npv(r, Boi_cost)
# NPV of benefit for 1 kWh of biomass boiler
Boi_benefit_npv = npf.npv(r, Boi_benefit)
# NPV of replacing diesel oil from HVO fuel
DG_npv = npf.npv(r, Gen_CF)


#####################################################################################################################################
#                               Cost Function                     
#####################################################################################################################################
Steam_kg_TO_kwh = 0.7147

def objective(x):

  SolarPV_NPV = x[0] * PV_npv - ( PV_OM_npv if round(x[0]) > 0.0 else 0)

  Battery_consump = (Consump_dis.apply(lambda i:x[1] if x[1] < i else i)) #Battery energy usage for each day * 365
  BatteryEM =  (-(EF_ch/eff - EF_dis).multiply(Battery_consump)).sum()      #Annual emission reduction
  Annual_consump = Battery_consump.sum()

  BESS_cost = - (x[1]/(DoD * eff)) * Bat_cost_npv + Annual_consump * Bat_Dis_benefit_npv + BatteryEM * Bat_CO2_benefit_npv

  #Boiler
  Annual_Total_Steam_demand = Steam_demand["Steam (kg)"].sum() #steam kg
  Biomass_steam_supply = Steam_demand["Steam (kg)"].apply(lambda i:x[3] if x[3] < i else i)     #hourly steam data in kg
  #x[3] =  boiler capacity in steam kg/h
  Annual_Biomass_steam_supply = (Biomass_steam_supply.sum()) * Steam_kg_TO_kwh    #Annual energy consumption from biomass boiler in kWh

  Boiler_NPV = - x[3] * Steam_kg_TO_kwh * Boi_cost_npv + Annual_Biomass_steam_supply * Boi_benefit_npv

  NPV = SolarPV_NPV + BESS_cost + DG_npv * x[2] + Boiler_NPV 

  return -NPV

####################################################################################################################################
#        Print and Visualize Current System and Maximum Emission reduction data
####################################################################################################################################

Total_EM = Grid_EM + diesel_emission + Fuel_oil_EM

print("\n--- Emissions of the Current Energy System ---")

print("Grid Emission = %.2f kgCO2e" % Grid_EM)
print("Diesel Generator Emission = %.2f kgCO2e" % diesel_emission)
print("Boiler Emission = %.2f kgCO2e" % Fuel_oil_EM)
print("Total Onsite Emission = %.2f kgCO2e" % Total_EM)
print("\n")

fig1 = plt.figure(figsize=(8, 6))
Y1 = np.array([Grid_EM, diesel_emission, Fuel_oil_EM])
mylabels = ["Grid", "Diesel Generator", "Boiler"]
myexplode = [0, 0, 0]   # To give space between parts

plt.pie(Y1, labels = mylabels,autopct='%1.1f%%', explode = myexplode, shadow = True)
plt.title('Annual Onsite Emission from the Current System')
plt.show() 

#System sizes for maximum emission reduction
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

# Maximum emission reduction from each alternative
Solar_EM_Red = EmReductionSolar1kW * max_DC_capacity
BESS_EM_Red = - BatteryEM
GreenDiesel_EM_Red = diesel_emission - HVO_emission
Biomass_EM_Red = Fuel_oil_EM - Biomass_EM

print("\n")

fig2 = plt.figure(figsize=(8, 6))
plt.title("Maximum Annual Emission Reduction from alternatives")
X2 = np.array(["Solar PV", "BESS", "Green Diesel DG", "Biomass Boiler", "Total System"])
Y2 = np.array( [Solar_EM_Red, BESS_EM_Red, GreenDiesel_EM_Red, Biomass_EM_Red, sum([Solar_EM_Red, BESS_EM_Red, GreenDiesel_EM_Red, Biomass_EM_Red]) ])

# Add text labels to the bars (show values on the bars)
for i in range(len(X2)):
    plt.text(i, Y2[i], str(round(Y2[i],2)), ha='center', va='bottom')

plt.ylabel("Emission(kgCO2e)")
plt.xlabel("Alternatives")
plt.bar(X2, Y2, color = "#4CAF50")
plt.show()

# Cost analysis for maximum emission reduction
x0 = [max_DC_capacity, 0, 0, 0]
x1 = [0, Req_battery_cap*DoD*eff, 0, 0]
x2 = [0, 0, Annual_HVO_req, 0 ]
x3 = [0, 0, 0, Biomass_Boi_size]

fig3 = plt.figure(figsize=(8, 6))
plt.title("Net Present Value for systems")
X3 = np.array(["Solar PV", "BESS", "Green Diesel DG", "Biomass Boiler", "Total System"])
Y3 = np.array([-objective(x0), -objective(x1), -objective(x2), -objective(x3), sum([-objective(x0), -objective(x1), -objective(x2), -objective(x3)])])

# Add text labels to the bars (show values on the bars)
for i in range(len(X3)):
    plt.text(i, Y3[i], str(round(Y3[i],2)), ha='center', va='bottom')

plt.ylabel("NPV ($)")
plt.xlabel("Alternatives")
plt.bar(X3, Y3, color = "red")
plt.show()

print("\n")
print("Possible Minimum Onsite Emission after alternatives = %.2f kgCO2e" %(Grid_EM - EmReductionSolar1kW * max_DC_capacity + BatteryEM + HVO_emission + Biomass_EM ))

#####################################################################################################################################
#                               Emission Function                        
#####################################################################################################################################

EmTarget = float(input("Enter the desired emission target in kgCO2e = ").strip())
def constraint1(x):
  #__________________________________________________________________________
  #For BESS

  Battery_consump = Consump_dis.apply(lambda i:x[1] if x[1] < i else i)
  #Battery supply daily consumption for the discharging interval, to a max of its dischargable capacity

  BatteryEM = ((EF_ch/eff - EF_dis).multiply(Battery_consump)).sum()  #negative -> emission reduction


  #__________________________________________________________________________
 #For Biomass boiler

  Annual_Total_Steam_demand = Steam_demand["Steam (kg)"].sum() #steam kg

  Biomass_steam_supply = Steam_demand["Steam (kg)"].apply(lambda i:x[3] if x[3] < i else i)     #hourly steam data in kg
  #x[3] =  boiler capacity in steam kg/h
  Annual_Biomass_steam_supply = (Biomass_steam_supply.sum()) * Steam_kg_TO_kwh     #Annual energy consumption from biomass boiler in kWh

  BoilerEM_red = (EF["Fuel oil"]/eff_oil - EF["Wood"]*3.6/Cal_wood / eff_bio) * Annual_Biomass_steam_supply
 
  
  #__________________________________________________________________________
 

  ###############################################################################
  #For DG by HVO
  DG_EM_Reduc = x[2] * ( HVO_CV / diesel_CV * EF["Diesel"] - EF["HVO"])

  return EmTarget - (Total_EM - EmReductionSolar1kW * x[0] + BatteryEM - DG_EM_Reduc - BoilerEM_red)  # >= 0k



#####################################################################################################################################
#                               Optimization with SLSQP                        
#####################################################################################################################################

# initial guesses
n = 4
x0 = np.zeros(n)
#x0[0] = max_DC_capacity/2
x0[0] = 0.0
x0[1] = 0.0
x0[2] = 0.0
x0[3] = 0.0

# optimize
b0 = (0, max_DC_capacity)
b1 = (0, Consump_dis.max())
b2 = (0, diesel_consump * diesel_CV / HVO_CV)
b3 = (0,Steam_demand["Steam (kg)"].max())
bnds = (b0, b1, b2, b3)
con1 = {'type': 'ineq', 'fun': constraint1}
cons = ([con1])
solution = minimize(objective,x0,method='SLSQP',bounds=bnds,constraints=cons)
x = solution.x

#####################################################################################################################################
#                                System Sizing                       
#####################################################################################################################################


#_______________________________________________________________________________
## SOLAR SYSTEM
Tstc = 25 #Standard test condition temperature
Tmax = 39.5+25
Tmin = 14.4

# Select panel type as JASolar 550W panel
Eff = 0.213                   #Panel efficiency
P_panel = 550                 #Rated maximum power of a panel
Voc_panel = 49.9              #open circuit voltage
Vmp_panel = 41.96             #Maximum power voltage
Coef_T_Voc = -0.00275         #Temperature coeffient of Voc
Coef_T_Pmp = -0.0035          #Temperature coeffient of Pmp


#Select inverter type as Huawei SUN2000
#SUN2000 60kW
Voc_60 = 1100                 #Maximum input voltage
Vmp_60 =200                  #MPPT Operating Voltage Range
N_mppt = 6

#SUN2000 100kW
Voc_100 = 1100                #Maximum input voltage
Vmp_100 =200                 #MPPT Operating Voltage Range
N_mppt = 10

# Inverter sizing / panel sizing
def PVsizing(P_PV):

  N_panel = math.ceil(P_PV*1000/P_panel)

  #Consider AC capacity equal to DC capacity of the system

  #Inverter sizing
  #Consider two option of inverter capacity 100kW & 60kW
  # First find no. of 100kW size inverters

  N_100kW = (P_PV // 100)                #No. of 100kW inverters
  N_60kW = 0

  #Remaining power after sizing 100kW inverter
  P_remain = P_PV % 100

  #P_remain less than 20kW, it is not required an another inverter because 100kW inverter can oversize upto 120kW.
  #P_remain between 60kW & 72kW, it is not required an another inverter because 60kW inverter can oversize upto 72kW.
  if 72 >= P_remain > 20:
    #Number of 60kW size inverter
    N_60kW = 1

  elif P_remain > 72:
    N_100kW =+ 1

  return N_panel, P_PV, N_100kW, N_60kW


def stringsizing(Inv_type):

  if Inv_type == 100 or Inv_type == 60 :

      #Maximum number of panels for a string
      #Voc of string < Voc Inverter

      #Voc of the panel may change for ambient temperature
      Cor_Voc = Voc_panel * (1 + Coef_T_Voc * (Tmin - Tstc))    #Corrected Voc of panel
      #Maximum number of panel for a string
      N_max = Voc_100 // Cor_Voc

      #Minimum number of panels for a string
      #minimum Vmpp of Inverter < Vmpp of string

      #Vmp of the panel may change for ambient temperature
      Cor_Vmp = Vmp_panel * (1 + Coef_T_Pmp * (Tmax - Tstc))    #Corrected Vmp of panel
      #Minimum number of panel for a string
      N_min = (Vmp_100 // Cor_Vmp) + 1

      return N_max, N_min



#BESS
Battery_Cap = 100 #Ah
Battery_Volt = 12 #V
BESS_size = x[1]/DoD/eff
default_sys_voltage = 48 #V

if BESS_size==0:
  Series_con = 0

else:
  Series_con = default_sys_voltage/Battery_Volt
Parallel_con = math.ceil(BESS_size*1000/(default_sys_voltage*Battery_Cap)) #math ceil


#####################################################################################################################################
#                               Display New Energy System                        
#####################################################################################################################################

#####       GHG Emission Reduction from each new System

fig4 = plt.figure(figsize=(8, 6))
plt.title("GHG Emission Reduction for New System")
X4 = np.array(["Solar PV", "BESS", "Green Diesel DG", "Biomass Boiler", "Total System"])

Ea = (constraint1([x[0],0,0,0]) - EmTarget + Total_EM)  
Eb = (constraint1([0,x[1],0,0]) - EmTarget + Total_EM) 
Ec = (constraint1([0,0,x[2],0]) - EmTarget + Total_EM) 
Ed = (constraint1([0,0,0,x[3]]) - EmTarget + Total_EM) 

Y4 = np.array([Ea,Eb,Ec,Ed,sum([Ea,Eb,Ec,Ed])])
#y = np.array([ GHGReduc ([x[0],0,0,0]),GHGReduc ([0,x[1],0,0]), GHGReduc ([0,0,x[2],0]), GHGReduc ([0,0,0,x[3]]),sum([ GHGReduc ([x[0],0,0,0]),GHGReduc ([0,x[1],0,0]),GHGReduc ([0,0,x[2],0]),GHGReduc ([0,0,0,x[3]]) ]) ])

# Add text labels to the bars (show values on the bars)
for i in range(len(X4)):
    plt.text(i, Y4[i], str(round(Y4[i],2)), ha='center', va='bottom')

plt.ylabel("GHG Emission (kgCO2e)")
plt.xlabel("Alternatives")
plt.bar(X4, Y4, color = "#4CAF50")
plt.show()

#####       GHG Emission of the new System

fig6 = plt.figure(figsize=(8, 6))
plt.title("GHG Emission of the New System")
X6 = np.array(["Electricity", "Diesel Generator", "Boiler", "Total System"])

#New emissions
E_elec = Grid_EM - (constraint1([x[0],x[1],0,0]) - EmTarget + Total_EM) 
E_DG = diesel_emission - (constraint1([0,0,x[2],0]) - EmTarget + Total_EM) 
E_Boi = Fuel_oil_EM - (constraint1([0,0,0,x[3]]) - EmTarget + Total_EM) 
E_Total = Total_EM - (constraint1([x[0],x[1],x[2],x[3]]) - EmTarget + Total_EM)