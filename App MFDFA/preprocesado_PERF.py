from tkinter.filedialog import askopenfilename
import csv
import os

#n=input("Select the number of parameters:")
n=8
i=0
data=[]
names=[]
time=[]
name=True

while i<n:
    data.append([])
    i=i+1
i=0

file=askopenfilename()
if file is not None and file.endswith('.csv'):            
    path=file
    print(path)

    with open(path) as file:
        reader=csv.reader(file,delimiter='|')
        for row in reader:
            if i==n:
                i=0
                name=False
            if i==0:
                time.append(float(row[0]))

            if i!=0:#Esto por el tema de cpu-clock a float
                if name:
                    names.append(row[3])
                data[i].append(float(row[1]))
            i=i+1

    #create the individuals files

    i=1
    while path[-i]!='/':
        if path[-i]=='.':
            j=i
        i=i+1
    name=path[-i+1:-j]

    print(len(names))
    print(len(data))

    os.mkdir("Data_csv")

    for n in range(0,len(names)): 
        with open("Data_csv/"+name+"_"+names[n]+".csv","w+") as f:
            f.write(str(data[n+1]))
    with open("Data_csv/"+name+"_time.csv",'w+') as f:
        f.write(str(time))

else:
    print("Warning: This app only support .csv files")#write on text widget