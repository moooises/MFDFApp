from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from tkinter.filedialog import askopenfile
from tkinter.filedialog import askopenfilename
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.pyplot as plt_aux
import scipy.io
import math
import csv
import sys

plt.switch_backend('TkAgg')
colours=["blue","green","red","cyan","magenta","yellow","black"]

def index(q):
    #i=0
    #while round(q[i])!=0 and i!=len(q):
    #    i=i+1


    #ind=i

    q_index=[]

    for j in range(1,5): ##Change this value(5) to get more q plots
        q_index.append(j*4)

    return q_index


def Select_Scale(data,scale,q,m,qindex,noise,figure,scale_min,scale_max,scale_res):
    #probar con los arrays de numpy
    if noise=="1":
        data=np.cumsum(data-np.mean(data))



    segments=[]
    RMS=[]
    qRMS=[]
    Fq=[]
    Hq=[]
    qRegLine=[]


    for i in range(0,len(q)):
        Fq.append([])


    for ns in range(0,len(scale)):
        segments.append(math.floor(len(data)/scale[ns]))
        RMS.append([])
        Idx_start=0
        sum=int(scale[ns])
        Idx_stop=sum-1
        qRMS.append([])
        for v in range(0,segments[-1]):
            Index=range(Idx_start,Idx_stop)
            X_Idx=data[Index]
            C=np.polyfit(Index,X_Idx,m)
            fit=np.polyval(C,Index)
            RMS[ns].append(np.sqrt(np.mean((X_Idx-fit)**2)))
            Idx_start=Idx_stop+1
            Idx_stop=Idx_stop+sum


        for nq in range(0,len(q)):
            qRMS[ns]=RMS[ns]**q[nq]
            if q[nq]==0:
                i=nq
            else:
                Fq[nq].append(np.mean(qRMS[-1])**(1/q[nq]))

        sumaFq=[]
        for j in range(0,len(Fq[i-1])):
            sumaFq.append(Fq[i-1][j]+Fq[i+1][j])


        Fq[i]=[x/2 for x in sumaFq]
    

    for nq in range(0,len(q)):

        C=np.polyfit(np.log2(scale),np.log2(Fq[nq]),1)
        Hq.append(C[0])
        qRegLine.append(np.polyval(C,np.log2(scale)))


    X=np.log2(scale)

    ##Para la seleccion

    plt.figure(20)
    plt.title("One section")
    plt.xlabel('scale')
    plt.ylabel('Fq')
    i=0
    for k in qindex:
        plt.plot(X,np.log2(Fq[k]),"o",color=colours[i],label="q="+str(int(q[k])))
        plt.plot(X,qRegLine[k],color=colours[i])
        i=i+1
    #plt.xticks(X,np.linspace(scale_min,scale_max,scale_res))####
    plt.xticks(X,scale)
    #plt.yticks(,np.round(np.linspace(-1,32,20)))
    plt.legend(loc='upper center', bbox_to_anchor=(0.5, 1.00), shadow=True, ncol=4)
    plt.ion()
    plt.pause(0.001)
    plt.show()
    scale_d=scale
    scale=np.delete(scale,0)
    scale=np.delete(scale,len(scale)-1)
    scale_selector=Aux_Window("Scale Selector",scale_min,scale_max,scale,scale_d)
    s=scale_selector.ret_value_scale()
    l=scale_selector.ret_value_left_delimiter()
    r=scale_selector.ret_value_right_delimiter()
    p=scale_selector.ret_value_check()

    return float(s),float(l),float(r),p

def DFA(data,scale,m,noise,figure,scale_min,scale_max,scale_res,ind_figure,one_section):

    segments=[]
    F=[]
    RMS=[]


    if noise=="1":
        print("Tiene estructura ruido")
    else:
        print("NO")

    if figure=="1":
        if noise=="1":
            plt.subplot(4,2,1)

            plt.plot(data,label='time series')
            plt.xlabel('time')
            plt.ylabel('Amplitude')
            plt.rcParams["axes.titlesize"] = 8
            plt.title("Time serie")
            data=np.cumsum(data-np.mean(data))
            plt.plot(data,label='Random Walk')
            plt.legend()
        else:
            plt.subplot(4,2,1)

            plt.plot(data,label='time series')
            plt.xlabel('time')
            plt.ylabel('Amplitude')
            plt.rcParams["axes.titlesize"] = 8
            plt.title("Time serie")
            plt.legend()
    else:

        if ind_figure==1:
            plt.figure(1)
        
            if noise=="1":
                #if one_section==0:
                #    plt.subplot(1,2,ind_figure)

                plt.plot(data,label='time series')
                plt.xlabel('time')
                plt.ylabel('Amplitude')
                plt.rcParams["axes.titlesize"] = 8
                plt.title("Time serie")
                data=np.cumsum(data-np.mean(data))
                plt.plot(data,label='Random Walk')
                plt.legend()
            else:
                #if one_section==0:
                #    plt.subplot(1,2,ind_figure)

                plt.plot(data,label='time series')
                plt.xlabel('time')
                plt.ylabel('Amplitude')
                plt.rcParams["axes.titlesize"] = 8
                plt.title("Time serie")
                plt.legend()
        else:
            data=np.cumsum(data-np.mean(data))




    #exponents=np.linspace(math.log2(16),math.log2(1024),19)
    #scale=np.around(2**exponents,0)
    #scale=[16,32,64,128,256,512,1024]



    for ns in range(0,len(scale)):
        segments.append(math.floor(len(data)/scale[ns]))
        RMS.append([])
        Idx_start=0
        sum=int(scale[ns])
        Idx_stop=sum
        for v in range(0,segments[-1]):
            Index=range(Idx_start,Idx_stop)

            X_Idx=data[Index]

            C=np.polyfit(Index,X_Idx,m)

            fit=np.polyval(C,Index)
            RMS[ns].append(math.sqrt(np.mean((X_Idx-fit)**2)))
            Idx_start=Idx_stop+1
            Idx_stop=Idx_stop+sum
        F.append(np.sqrt(np.mean([l**2 for l in RMS[ns]])))
        
        

    X=np.log2(scale)
    Ch=np.polyfit(X,np.log2(F),1)
    H=Ch[0]
    RegLine=np.polyval(Ch,X)

    if figure=="1":
        plt.subplot(4,2,2)

        plt.xlabel('Scale')
        plt.ylabel('Overall RMS')
        plt.rcParams["axes.titlesize"] = 8
        plt.title("Overall RMS")
        plt.plot(X,RegLine,"b-",label='Multifractal time series')
        plt.plot(X,np.log2(F),"o",color="blue",label="slope H = "+str(H))
        #plt.xticks(X,np.linspace(scale_min,scale_max,scale_res))
        plt.xticks(X,scale)##Esta es nuestra autentica escala
        plt.yticks(RegLine,np.round(np.linspace(1,32,19)))
        plt.legend()
    else:
        plt.figure(2)

        if one_section==0:
            plt.subplot(1,2,ind_figure)
            plt.suptitle('Section 1                                                  Section 2', fontsize=16)

        plt.xlabel('Scale')
        plt.ylabel('Overall RMS')
        plt.rcParams["axes.titlesize"] = 8
        plt.title("Overall RMS")
        plt.plot(X,RegLine,"b-",label='Multifractal time series')
        plt.plot(X,np.log2(F),"o",color="blue",label="slope H = "+str(H))
        #plt.xticks(X,np.linspace(scale_min,scale_max,scale_res))#####
        plt.xticks(X,scale)##Esta es nuestra autentica escala
        plt.yticks(RegLine,np.round(np.linspace(1,32,19)))
        plt.legend()
    
    return H

def MFDFA(data,scale,q,m,qindex,Adjustment,noise,figure,scale_min,scale_max,scale_res,ind_figure,one_section):
    #probar con los arrays de numpy
    if noise=="1":
        data=np.cumsum(data-np.mean(data))



    segments=[]
    RMS=[]
    qRMS=[]
    Fq=[]
    Hq=[]
    qRegLine=[]


    for i in range(0,len(q)):
        Fq.append([])

    for ns in range(0,len(scale)):
        segments.append(math.floor(len(data)/scale[ns]))
        RMS.append([])
        Idx_start=0
        sum=int(scale[ns])
        Idx_stop=sum-1
        qRMS.append([])
        for v in range(0,segments[-1]):
            Index=range(Idx_start,Idx_stop)
            X_Idx=data[Index]
            C=np.polyfit(Index,X_Idx,m)
            fit=np.polyval(C,Index)
            RMS[ns].append(np.sqrt(np.mean((X_Idx-fit)**2)))
            Idx_start=Idx_stop+1
            Idx_stop=Idx_stop+sum


        for nq in range(0,len(q)):
            qRMS[ns]=RMS[ns]**q[nq]
            if q[nq]==0:
                #Fq[nq].append(np.exp(0.5*np.mean([l**2 for l in np.log(RMS[ns])])))
                i=nq
            else:
                Fq[nq].append(np.mean(qRMS[-1])**(1/q[nq]))

        sumaFq=[]
        for j in range(0,len(Fq[i-1])):
            sumaFq.append(Fq[i-1][j]+Fq[i+1][j])


        Fq[i]=[x/2 for x in sumaFq]


    for nq in range(0,len(q)):
        C=np.polyfit(np.log2(scale),np.log2(Fq[nq]),1)
        Hq.append(C[0])
        qRegLine.append(np.polyval(C,np.log2(scale)))



    X=np.log2(scale)

    
    i=0
    if figure=="1":
        plt.subplot(4,2,4)
        plt.xlabel('scale')
        plt.ylabel('Fq')
        plt.title("q-order RMS")
        for k in qindex:
            plt.plot(X,np.log2(Fq[k]),"o",color=colours[i],label=q[k])
            plt.plot(X,qRegLine[k],color=colours[i])
            i=i+1

        #plt.xticks(X,np.linspace(scale_min,scale_max,scale_res))
        plt.xticks(X,scale)
        #plt.yticks(,np.round(np.linspace(-1,32,20)))
        plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.38), shadow=True, ncol=4)   
    else:
        plt.figure(4)
        if one_section==0:
            plt.subplot(1,2,ind_figure)
            plt.suptitle('Section 1                                                  Section 2', fontsize=16)


        plt.xlabel('scale')
        plt.ylabel('Fq')
        plt.title("q-order RMS")
        for k in qindex:
            plt.plot(X,np.log2(Fq[k]),"o",color=colours[i],label=q[k])
            plt.plot(X,qRegLine[k],color=colours[i])
            i=i+1
        plt.legend(loc='upper center', bbox_to_anchor=(0.5, 1.00), shadow=True, ncol=4)
        #plt.xticks(X,np.linspace(scale_min,scale_max,scale_res))####
        plt.xticks(X,scale)
        #plt.yticks(,np.round(np.linspace(-1,32,20)))


    tq=Hq*q-1

    if figure=="1":
        plt.subplot(4,2,7)

        plt.rcParams["axes.titlesize"] = 8
        plt.title("Max Exponent tq")
        plt.xlabel('q-order')
        plt.ylabel('tq')
        plt.plot(q,tq,color="blue")
    else:
        plt.figure(7)
        if one_section==0:
            plt.subplot(1,2,ind_figure)
            plt.suptitle('Section 1                          Section 2', fontsize=16)


        plt.rcParams["axes.titlesize"] = 8
        plt.title("Max Exponent tq")
        plt.xlabel('q-order')
        plt.ylabel('tq')
        plt.plot(q,tq,color="blue")   

    hq=np.diff(tq)/(q[1]-q[0])
    Dq=(q[0:-1]*hq)-tq[0:-1]

    if figure=="1":

        plt.subplot(4,2,5)

        plt.xlabel('q-order')
        plt.ylabel('hq')
        plt.title("Tangent slope of tq")
        plt.plot(q[0:-1],hq,color="blue")

        plt.subplot(4,2,6)

        plt.xlabel('q-order')
        plt.ylabel('Dq')
        plt.title('Singularity Dimension')
        plt.plot(q[0:-1],Dq,color="blue")

        plt.subplot(4,2,8)

        plt.rcParams["axes.titlesize"] = 8
        plt.title("Multifractal spectrum of Dq and hq")
        plt.xlabel('hq')
        plt.ylabel('Dq')
        plt.plot(hq,Dq,color="blue")

        plt.subplot(4,2,3)

        plt.rcParams["axes.titlesize"] = 8
        plt.title("Hurst exponent in each q-order",)
        plt.xlabel('q-order')
        plt.ylabel('Hq')
        plt.plot(q,Hq,color="blue")
        
        plt.subplots_adjust(wspace=0.2,hspace=0.9)

        
    else:

        plt.figure(5)
        if one_section==0:
            plt.subplot(1,2,ind_figure)
            plt.suptitle('Section 1                                                  Section 2', fontsize=16)


        plt.xlabel('q-order')
        plt.ylabel('hq')
        plt.plot(q[0:-1],hq,color="blue")

        plt.figure(6)
        if one_section==0:
            plt.subplot(1,2,ind_figure)
            plt.suptitle('Section 1                                                  Section 2', fontsize=16)


        plt.xlabel('q-order')
        plt.ylabel('Dq')
        plt.plot(q[0:-1],Dq,color="blue")

        plt.figure(8)
        if one_section==0:
            plt.subplot(1,2,ind_figure)
            plt.suptitle('Section 1                                                  Section 2', fontsize=16)


        plt.rcParams["axes.titlesize"] = 8
        plt.title("Multifractal spectrum of Dq and hq")
        plt.xlabel('hq')
        plt.ylabel('Dq')
        plt.plot(hq,Dq,color="blue")

        plt.figure(3)
        if one_section==0:
            plt.subplot(1,2,ind_figure)
            plt.suptitle('Section 1                                                  Section 2', fontsize=16)


        plt.rcParams["axes.titlesize"] = 8
        plt.title("Hurst exponent in each q-order",)
        plt.xlabel('q-order')
        plt.ylabel('Hq')
        plt.plot(q,Hq,color="blue")


    return  Hq,tq,hq,Dq,Fq


def start_MFDFA(data,m,scale,q,q_index,noise,figure,scale_min,scale_max,scale_res,section,left,right,one_section):

    ind_izq=np.where(scale==left)
    ind_derch=np.where(scale==right)
    ind_sect=np.where(scale==section)

    if one_section==1:

        H=DFA(data,scale[int(ind_izq[0]):int(ind_derch[0])+1],m,noise,figure,scale_min,scale_max,scale_res,1,one_section)

        Adjustment=0
        if H<0.2:
            Adjustment-=1
        else:
            if H>1.2 and H<1.8:
                Adjustment+=1
            else:
                if H>1.8:
                    Adjustment+=2

        Hq,tq,hq,Dq,Fq=MFDFA(data,scale[int(ind_izq[0]):int(ind_derch[0])+1],q,m,q_index,Adjustment,noise,figure,scale_min,scale_max,scale_res,1,one_section)
    
    else:

        if figure=="1":
            plt.figure(num='Section 1')

        H=DFA(data,scale[int(ind_izq[0]):int(ind_sect[0])+1],m,noise,figure,scale_min,scale_max,scale_res,1,one_section)

        Adjustment=0
        if H<0.2:
            Adjustment-=1
        else:
            if H>1.2 and H<1.8:
                Adjustment+=1
            else:
                if H>1.8:
                    Adjustment+=2

        Hq,tq,hq,Dq,Fq=MFDFA(data,scale[int(ind_izq[0]):int(ind_sect[0])+1],q,m,q_index,Adjustment,noise,figure,scale_min,scale_max,scale_res,1,one_section)

   
        if figure=="1":
            plt.figure(num='Section 2')

        H=DFA(data,scale[int(ind_sect[0]):int(ind_derch[0])+1],m,noise,figure,scale_min,scale_max,scale_res,2,one_section)

        Adjustment=0
        if H<0.2:
            Adjustment-=1
        else:
            if H>1.2 and H<1.8:
                Adjustment+=1
            else:
                if H>1.8:
                    Adjustment+=2

        if figure=="1":
            plt.figure(num='Section 2')

        Hq,tq,hq,Dq,Fq=MFDFA(data,scale[int(ind_sect[0]):int(ind_derch[0])+1],q,m,q_index,Adjustment,noise,figure,scale_min,scale_max,scale_res,2,one_section)

        plt.show(block=True)
        plt.show()
    


    return Hq,tq,hq,Dq,Fq


class Aux_Window():

    def valuecheck(self,value):
        newvalue=min(self.scale_window, key=lambda x:abs(x-float(value)))
        self.window_scale.set(newvalue)

    def valuecheck_left_delimiter(self,value):
        newvalue=min(self.scale_delimiter_window, key=lambda x:abs(x-float(value)))
        self.left_delimiter_scale.set(newvalue)

    def valuecheck_right_delimiter(self,value):
        newvalue=min(self.scale_delimiter_window, key=lambda x:abs(x-float(value)))
        self.right_delimiter_scale.set(newvalue)

    def __init__(self,title,scale_min,scale_max,scale,scale_delimiter):
        self.scale_window=scale
        self.scale_delimiter_window=scale_delimiter

        self.window=Toplevel()
        self.window.title(title)
        self.window.protocol('WM_DELETE_WINDOW', self.close_window)
   
        self.window.resizable(width=False,height=False)

        self.left_delimiter_label=Label(self.window,text="Select left delimiter")
        self.left_delimiter_label.grid(row=0,column=0)
        self.left_delimiter_scale=Scale(self.window,from_=scale_min,to=scale_max,orient=HORIZONTAL,sliderlength=10,length=int(scale_max/2),command=self.valuecheck_left_delimiter)
        self.left_delimiter_scale.set(int(scale_min))
        self.left_delimiter_scale.grid(row=1,column=0)

        self.right_delimiter_label=Label(self.window,text="Select right delimiter")
        self.right_delimiter_label.grid(row=2,column=0)
        self.right_delimiter_scale=Scale(self.window,from_=scale_min,to=scale_max,orient=HORIZONTAL,sliderlength=10,length=int(scale_max/2),command=self.valuecheck_right_delimiter)
        self.right_delimiter_scale.set(int(scale_max))
        self.right_delimiter_scale.grid(row=3,column=0)


        self.window_label=Label(self.window,text="Select the value for the next regresion and the regresion value:")
        self.window_label.grid(row=4,column=0)
        self.window_scale=Scale(self.window,from_=scale_min,to=scale_max,orient=HORIZONTAL,sliderlength=10,length=int(scale_max/2),command=self.valuecheck,state=ACTIVE,takefocus=1)
        self.window_scale.set(int(scale_max/4))
        self.window_scale.grid(row=5,column=0)


        self.one_section=0

        self.window_check_figure=Checkbutton(self.window,text='One section',variable=self.one_section,command=self.click)
        self.window_check_figure.grid(row=6,column=0,sticky=W)

        self.window_button=Button(self.window,text="Send",command=self.send_data)
        self.window_button.grid(row=6,column=0)


        self.window.grid_rowconfigure(0, minsize=20)
        self.window.grid_rowconfigure(2, minsize=20)
        self.window.grid_rowconfigure(4, minsize=20)
        self.window.grid_rowconfigure(6, minsize=30)


        self.window.mainloop()

    #I don't know how to make it work like the other one, for any reason that doesn't work anymore
    def click(self):
        if self.one_section==0:
            self.one_section=1
            self.window_scale.configure(state=DISABLED,takefocus=0)
        else:
            self.window_scale.configure(state=ACTIVE,takefocus=1)
            self.one_section=0

    def close_window(self):
        #plt.close(20)# desactivada temporalmente
        self.window.quit()
        self.window.destroy()

    def send_data(self):
        l=self.left_delimiter_scale.get()
        r=self.right_delimiter_scale.get()
        s=self.window_scale.get()
        o=self.one_section
        if r<l:
            messagebox.showwarning("Warning", "Right delimiter can't be lower than left delimiter")
        elif l==r:
            messagebox.showwarning("Warning", "Left and Right delimiter can't be equal")
        elif o==0:
            if s<=l:
                messagebox.showwarning("Warning", "Section delimiter can't be at the left of the left delimiter")
            elif s>=r:
                messagebox.showwarning("Warning", "Section delimiter can't be at the right of the right delimiter")
            else:
                self.scale_value=s
                self.left_value=l
                self.right_value=r
                self.section=o
                self.window.quit()
                self.window.destroy()
        else: 
            self.scale_value=s
            self.left_value=l
            self.right_value=r
            self.section=o
            self.window.quit()
            self.window.destroy()

    def ret_value_scale(self):
        return self.scale_value

    def ret_value_left_delimiter(self):
        return self.left_value

    def ret_value_right_delimiter(self):
        return self.right_value

    def ret_value_check(self):
        return self.section
    