import numpy as np
import matplotlib.pyplot as plt

fig,ax =plt.subplots(2,2)
x = np.linspace(0,8,1000)
ax[0,0].plot(x,np.sin(x),'g') #row=0, col=0
ax[1,0].plot(x,np.tan(x),'k') #row=1, col=0
ax[0,1].plot(range(100),'b') #row=0, col=1
ax[1,1].plot(x,np.cos(x),'r') #row=1, col=1
plt.show()