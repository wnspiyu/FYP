import numpy as np
import matplotlib.pyplot as plt

Zo = 200    
Rs = 0              
RL = 400       
l = 100000         
vel = 300000000        
k = 1                
T = 0.008            
V = 1             

n = 1000             

if RL + Zo != 0:
    a_r = (RL - Zo) / (RL + Zo)
else:
    # Handle the zero denominator appropriately
    a_r = 0

if Rs + Zo != 0:
    a_s = (Rs - Zo) / (Rs + Zo)
else:
    # Handle the zero denominator appropriately
    a_s = 0

times = np.linspace(0, T, n)
Vr_array = []
t1 = []
Vs_array = []
t2 = []

T1 = l / vel            
m = int(np.ceil(T / T1) + 1)  


for i in times:
    Vr = 0

    if i <= T1:
        t1.append(i)
        Vr_array.append(0)

    for j in range(3, m, 2):
        if i > T1:
            Vr = Vr + V * (k*(j-2)) * ((a_r * a_s)*((j-3)/2)) * (1 + a_r)
            if i < j * T1:
                t1.append(i)
                Vr_array.append(Vr)
                break


for i in times:
    Vs = V

    if i <= 2 * T1:
        t2.append(i)
        Vs_array.append(V)

    for j in range(4, m, 2):
        if i > 2 * T1:
            Vs = Vs + V * (k*(j-2)) * (a_r[j//2-1]) * (a_s[j//2-2]) * (1 + a_s)
            if i < j * T1:
                t2.append(i)
                Vs_array.append(Vs)
                break


plt.figure()
plt.plot(t2, Vs_array)
plt.xlabel("time (s)")
plt.ylabel("Sending Voltage (V)")
plt.title("Sending Voltage Vs time")

plt.figure()
plt.plot(t1, Vr_array)
plt.xlabel("time (s)")
plt.ylabel("Receiving Voltage (V)")
plt.title("Receiving Voltage Vs time")

plt.show()
