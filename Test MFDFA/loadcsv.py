import csv
import scipy.io
import numpy as np
import matplotlib.pyplot as plt

time=[]
cpuclock=[]
constexswitch=[]
cpumig=[]
pagefaults=[]
cycles=[]
instructions=[]
branches=[]
branchesmiss=[]

with open('data.csv') as file:
    reader=csv.reader(file, delimiter='|')
    for row in reader:
        if row[3]=="cpu-clock":
            cpuclock.append(row[1])
            time.append(float(row[0]))
        elif row[3]=="context-switches":
            constexswitch.append(float(row[1]))
        elif row[3]=="cpu-migrations":
            cpumig.append(float(row[1]))           
        elif row[3]=="page-faults":
            pagefaults.append(float(row[1]))           
        elif row[3]=="cycles":
            cycles.append(float(row[1]))           
        elif row[3]=="instructions":
            instructions.append(float(row[1]))           
        elif row[3]=="branches":
            branches.append(float(row[1]))           
        elif row[3]=="branch-misses":
            branchesmiss.append(float(row[1]))



plt.figure(1)
plt.xlabel('time')
plt.ylabel('context-switches')
plt.plot(time,constexswitch)

plt.figure(2)
plt.xlabel('time')
plt.ylabel('cpu-migrations')
plt.plot(time,cpumig)

plt.figure(3)
plt.xlabel('time')
plt.ylabel('page-faults')
plt.plot(time,pagefaults)

plt.figure(4)
plt.xlabel('time')
plt.ylabel('cycles')
plt.plot(time,cycles)

plt.figure(5)
plt.xlabel('time')
plt.ylabel('instructions')
plt.plot(time,instructions)

plt.figure(6)
plt.xlabel('time')
plt.ylabel('branches')
plt.plot(time,branches)

plt.figure(7)
plt.xlabel('time')
plt.ylabel('branch-misses')
plt.plot(time,branchesmiss)

#plt.figure(8)
#plt.xlabel('time')
#plt.ylabel('cpu-clock')
#plt.plot(time,cpuclock)

plt.legend()
plt.show()


