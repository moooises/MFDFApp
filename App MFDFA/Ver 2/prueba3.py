from tkinter import *
import numpy as np
import matplotlib.pyplot as plt
import numpy as np


plt.switch_backend('TkAgg')

class Aux_Window():
    def __init__(self,title):
        self.window=Tk()
        self.window.title(title)
        #self.window.protocol('WM_DELETE_WINDOW', self.close_window)
        self.c=0
        self.r=0


    def add_scale(self,label,begin,end):
        self.var=DoubleVar()
        self.var.set((end-begin)/2)    
        self.window_label=Label(self.window,text=label)
        self.window_label.grid(row=self.r,column=self.c)
        self.window_scale=Scale(self.window,from_=begin,to=end,variable=self.var,orient=HORIZONTAL,sliderlength=10,length=end/2)
        self.window_scale.grid(row=self.r+1,column=self.c)
        #self.window_spinbox=Spinbox(self.window,from_=begin,to=end)
        #self.window_spinbox.grid(row=self.r,column=self.c+1)
        self.r+=1
        

    def start_window(self):
        self.window.resizable(width=False,height=False)
        #self.window.geometry('646x650')
        self.window_button=Button(self.window,text="Send",command=self.close_window)
        self.window_button.grid(row=self.r+1,column=self.c)
        
        self.window.mainloop()

    def close_window(self):
        plt.close(1)
        #self.window.quit()



if __name__=='__main__':

    #t = np.linspace(0, 0.1,1000)
    #w = 60*2*np.pi


    #plt.figure(1)
    #plt.plot(t,np.cos(w*t))
    #plt.plot(t,np.cos(w*t-2*np.pi/3))
    #plt.plot(t,np.cos(w*t-4*np.pi/3))
    
    #plt.ion()
    #plt.pause(0.001)
    #plt.show()

    #f=Aux_Window("Prueba")
    #f.add_scale("Introduce     :",0,1024)
    #f.start_window()
    a=np.linspace(-5,4,21)
    print(a)
    print(type(a[0]))
    m=list(map(float,a))
    print(m)
    print(type(m[0]))

    a=np.linspace(-5,5,21)
    print(a)
    print(type(a[0]))
    m=list(map(float,a))
    print(m)
    print(type(m[0]))

    for x in range(1,5):
        print(x)





