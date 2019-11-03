import scipy.io
import numpy as np
import matplotlib.pyplot as plt
import math
print("Introduce los valores para la escala")
mini=int(input("Valor minimo:"))
maxi=int(input("Valor maximo:"))
res=int(input("El numero de segmentos"))
exponents=np.linspace(mini,maxi,res)
print(exponents)
