r=[7,7.7,7.9,8.1,8.3,8.4,8.5,8.5,8.6]
t2=[]
t3=[]
for i in range(9):
    t2.append(round((r[i] / 7) * (235 + 30) - 235,2))
    t3.append(round(t2[i]-30,2))

print(t2)
print(t3)
