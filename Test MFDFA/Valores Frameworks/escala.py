import scipy.io
import numpy as np
import matplotlib.pyplot as plt
import math
print("Introduce los valores para la escala")
mini=int(input("Valor minimo:"))
maxi=int(input("Valor maximo:"))
res=int(input("El numero de segmentos"))
exponents=np.linspace(math.log2(mini),math.log2(maxi),res)
print(exponents)
scale=np.around(2**exponents,0)
print(scale)
