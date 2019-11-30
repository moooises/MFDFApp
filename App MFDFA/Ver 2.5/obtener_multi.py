import scipy.io

data_r= scipy.io.loadmat('fractaldata.mat')
multifractal=data_r['multifractal']
type(multifractal)

print(multifractal)
#data=list(map(float,data_r))

data=multifractal.tolist()

MyFile=open('multifractal_paper.dat','w')
for element in data:
    MyFile.write(str(element[0]))
    MyFile.write("\n")
MyFile.close()