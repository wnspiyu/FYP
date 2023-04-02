DoD = 0.8   #Recommended depth of discharge for Li-ion Batteries 
# eff = 0.95  #Efficiency of BESS 

# #-------------------Charging Interval------------------------------------
# m1 = 18*2                    #18:6PM   *2:to half hourly intervals
# n1 = round( (18+2+1/2)*2 )   #+2.5:8.30PM   *2:to half hourly intervals

# #-------------------Discharging Interval---------------------------------
# m2 = 7*2                    #7:7AM   *2:to half hourly intervals
# n2 = round( (7+3+1/2)*2 )   #+3.5h:10.30AM   *2:to half hourly intervals


# EF_ch = New_GridEF_df.iloc[:,m1:n1].mean(axis=1)        #Charging interval avg EF for 365 days
# EF_dis = New_GridEF_df.iloc[:,m2:n2].mean(axis=1)       #Discharging interval avg EF for 365 days
# Consump_dis = New_Elec_df.iloc[:,m2:n2].sum(axis=1)     #Discharging interval electricity consumption for 365 days
# max_power = New_Elec_df.iloc[:,m2:n2].max().max()

# BatteryEM = ((EF_ch/eff - EF_dis).multiply(Consump_dis)).sum()  #Negative Emission 


# Req_battery_cap = (Consump_dis.max())/DoD/eff 