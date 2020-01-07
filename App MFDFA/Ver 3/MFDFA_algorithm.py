from tkinter import *
from tkinter import ttk
from tkinter.filedialog import askopenfile
from tkinter.filedialog import askopenfilename
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure

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

    #plt.figure(20)
    #plt.title("One section")
    #plt.xlabel('scale')
    #plt.ylabel('Fq')
    
    
    scale_selector=Aux_Window("Scale Selector",X,Fq,qRegLine,q,qindex,scale)
    #s=scale_selector.ret_value_scale()
    #l=scale_selector.ret_value_left_delimiter()
    #r=scale_selector.ret_value_right_delimiter()
    #p=scale_selector.ret_value_check()

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
    def search_point(self,data,X,min,max,center):

        r=max
        l=min
        found=False

        distance1=math.sqrt(pow(data-X[center],2))
        i=0
        while l<r and i<100:

            c1=int((center+l)/2)
            c2=int((r+center)/2)


            d1=math.sqrt(pow(data-X[c1],2))
            d2=math.sqrt(pow(data-X[c2],2))


            if d1<d2:
                distance2=d1
                r=center
                center=c1
                

         
                
            else:
                distance2=d2    
                l=center
                center=c2

            if distance1<distance2:
                p=center
                
            distance1=distance2
            i=i+1

        return X[center]



    
    def open_info(self):
        self.info_active=True
        self.raiz_info=Toplevel()
        self.raiz_info.title('Info')
        self.info_text=Text(self.raiz_info)
        self.info_text.insert('1.0','Information about input parameters\n')
        self.info_text.insert(END,'\n\nDelimiters:\nThey are use to select the range of data to analyse.\nThe left select the left interval and the right the right interval. The range   selected is the one that is between these two delimiters.')
        self.info_text.insert(END,'\nThe section delimiter select the limit between the two section of the data.     Each section will be analyze separetly.\n\nThis deceisions can be made observing the figure.') 
        self.info_text.insert(END,"\nIn case you want just one section check the one section mark")
        self.info_text.configure(state=DISABLED)
        self.info_text.pack(side=TOP,fill=BOTH,expand=1)
        self.info_button=Button(self.raiz_info,text='Close',command=self.close_info)
        self.info_button.pack(side=BOTTOM)
        self.raiz_info.geometry('646x230')
        self.raiz_info.resizable(width=False,height=False)


        #self.raiz_info.update()
        #print(self.raiz_info.winfo_geometry())
        self.raiz_info.protocol('WM_DELETE_WINDOW', self.close_info)
        self.raiz_info.mainloop()


    def close_info(self):
        self.raiz_info.destroy()


    def left_del(self,event):
        if event.button==1:
            if self.left_bool:
                i=-1
                while self.a.lines[i].get_label()!="left":
                    print(self.a.lines[i].get_label())
                    i-=1
                self.a.lines[i].remove()
                    

            p=self.search_point(event.xdata,self.x_Axis,0,len(self.x_Axis),self.center)

            self.line_left=self.a.axvline(x=p,color="red",label="left")
            print('%s click: button=%d, x=%d, y=%d, xdata=%f, ydata=%f' %
                    ('double' if event.dblclick else 'single', event.button,
                    event.x, event.y, event.xdata, event.ydata))
            self.canvas.draw()
            self.left_bool=True
            self.deep_left=0



            print("largo")
            print(len(self.a.lines))

    def right_del(self,event):
        if event.button==3:
            if self.right_bool:
                i=-1
                while self.a.lines[i].get_label()!="right":
                    print(self.a.lines[i].get_label())
                    i-=1
                self.a.lines[i].remove()

            p=self.search_point(event.xdata,self.x_Axis,0,len(self.x_Axis),self.center)

            self.line_right=self.a.axvline(x=p,color="blue",label="right")
            print('%s click: button=%d, x=%d, y=%d, xdata=%f, ydata=%f' %
                    ('double' if event.dblclick else 'single', event.button,
                    event.x, event.y, event.xdata, event.ydata))
            self.canvas.draw()
            self.right_bool=True
            self.deep_right=0

            print("largo")
            print(len(self.a.lines))

    def section(self,event):
        if event.button==2:
            if self.section_bool:
                i=-1
                while self.a.lines[i].get_label()!="section":
                    print(self.a.lines[i].get_label())
                    i-=1
                self.a.lines[i].remove()

            p=self.search_point(event.xdata,self.x_Axis,0,len(self.x_Axis),self.center)

            self.line_section=self.a.axvline(x=p,color="green",label="section")
            print('%s click: button=%d, x=%d, y=%d, xdata=%f, ydata=%f' %
                    ('double' if event.dblclick else 'single', event.button,
                    event.x, event.y, event.xdata, event.ydata))
            self.canvas.draw()
            self.section_bool=True
            self.deep_section=0
    
            print("largo")
            print(len(self.a.lines))
    

    def __init__(self,title,X,Fq,qRegLine,q,qindex,scale):
        self.left_bool=False
        self.right_bool=False
        self.section_bool=False

        self.x_Axis=X#needed for axvline
        self.center=int(len(X)/2)

        self.window=Toplevel()
        self.window.title(title)
        self.window.protocol('WM_DELETE_WINDOW', self.close_window)
   
        self.window.resizable(width=True,height=True)

        self.menubar=Menu(self.window)
        self.menubar.config(bg='grey90')
        self.menubar.add_command(label='Info',command=self.open_info)
        self.window.config(menu=self.menubar)

        self.f=Figure(dpi=100)
        self.a=self.f.add_subplot(111)

        i=0
        for k in qindex:
            self.a.plot(X,np.log2(Fq[k]),"o",color=colours[i],label="q="+str(int(q[k])))
            self.a.plot(X,qRegLine[k],color=colours[i])
            i=i+1
        #plt.xticks(X,np.linspace(scale_min,scale_max,scale_res))####
        #a.xticks(X,scale)
        #plt.yticks(,np.round(np.linspace(-1,32,20)))
        self.a.legend(loc='upper center', bbox_to_anchor=(0.5, 1.00), shadow=True, ncol=4)
        #a.ion()
        #a.pause(0.001)

        print(X)
        print(len(X))

        self.canvas=FigureCanvasTkAgg(self.f,master=self.window)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(side=BOTTOM,fill=BOTH,expand=True)
        toolbar=NavigationToolbar2Tk(self.canvas,self.window)
        toolbar.update()
        self.canvas._tkcanvas.pack(side=TOP,fill=BOTH,expand=True)

        cid1=self.f.canvas.mpl_connect('button_press_event',self.left_del)
        cid2=self.f.canvas.mpl_connect('button_press_event',self.right_del)
        cid3=self.f.canvas.mpl_connect('button_press_event',self.section)




        self.window.mainloop()

    #I don't know how to make it work like the other one, for any reason that doesn't work anymore

    def close_window(self):
        self.window.quit()
        self.window.destroy()  
        sys.exit()

    