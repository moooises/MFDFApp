from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from tkinter.filedialog import askopenfile
from tkinter.filedialog import askopenfilename
from tkinter.filedialog import asksaveasfile 
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.font_manager import FontProperties
from matplotlib.figure import Figure
import matplotlib as mpl
import matplotlib.ticker as ticker

import numpy as np
import matplotlib.pyplot as plt
import scipy.io
import math
import csv
import sys
import random


plt.switch_backend('TkAgg')
colours=["blue","green","red","cyan","magenta","yellow","black","purple","aqua","springgreen","gold","silver","mediumblue","hotpink","deeppink","peru","skyblue","firebrick","saddlebrown","tomato","linen","cadetblue","chocolate"]



#def index(q):
    #i=0
    #while round(q[i])!=0 and i!=len(q):
    #    i=i+1


    #ind=i

 #   q_index=[]

  #  for j in range(1,5): ##Change this value(5) to get more q plots
   #     q_index.append(j*4)

    #return q_index


def Select_Scale(data,scale,q,m,noise,figure,scale_min,scale_max,scale_res,lines):
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
        suma=int(scale[ns])
        Idx_stop=suma-1
        qRMS.append([])
        for v in range(0,segments[-1]):
            Index=range(Idx_start,Idx_stop)
            X_Idx=data[Index]
            C=np.polyfit(Index,X_Idx,m)
            fit=np.polyval(C,Index)
            RMS[ns].append(np.sqrt(np.mean((X_Idx-fit)**2)))
            Idx_start=Idx_stop+1
            Idx_stop=Idx_stop+suma

        i=-1
        for nq in range(0,len(q)):
            qRMS[ns]=RMS[ns]**q[nq]
            if q[nq]==0:
                i=nq
            else:
                Fq[nq].append(np.mean(qRMS[-1])**(1/q[nq]))

        if i!=-1: # EN caso de que en q no haya un 0
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
    print("All good")

    print("fq len")
    print(len(Fq))
    print("q")
    print(len(q))


    scale_selector=Aux_Window("Select data to analyse",X,Fq,qRegLine,q,scale,lines)
    l=scale_selector.ret_value_left_delimiter()
    r=scale_selector.ret_value_right_delimiter()
    s=scale_selector.ret_value_section()
    c=scale_selector.closed()

    return l,r,s,c

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
        suma=int(scale[ns])
        Idx_stop=suma
        for v in range(0,segments[-1]):
            Index=range(Idx_start,Idx_stop)

            X_Idx=data[Index]

            C=np.polyfit(Index,X_Idx,m)

            fit=np.polyval(C,Index)
            RMS[ns].append(math.sqrt(np.mean((X_Idx-fit)**2)))
            Idx_start=Idx_stop+1
            Idx_stop=Idx_stop+suma
        F.append(np.sqrt(np.mean([l**2 for l in RMS[ns]])))
        
        

    X=np.log2(scale)
    Ch=np.polyfit(X,np.log2(F),1)
    H=Ch[0]
    RegLine=np.polyval(Ch,X)
    plt.locator_params(nbins=3)

    if figure=="1":
        plt.subplot(4,2,2)

        plt.xlabel('Scale')
        plt.ylabel('Overall RMS')
        plt.rcParams["axes.titlesize"] = 8
        plt.plot(X,RegLine,"b-",label='Multifractal time series')
        plt.plot(X,np.log2(F),"o",color="blue",label="slope H = "+str(H))
        #plt.xticks(X,np.linspace(scale_min,scale_max,scale_res))

        plt.xticks(X,scale,fontsize=9,rotation=45)##Esta es nuestra autentica escala
        F_round=np.round(F,1)
        plt.yticks(RegLine,F_round)

        a=plt.gca()

        if len(scale)>=40:
            step=int((len(scale)/40))+1
            i=0
            for n, label in enumerate(a.xaxis.get_ticklabels()):
                if i % step != 0:
                    label.set_visible(False)
                i+=1

        if len(F_round)>=8:
            step=int((len(F_round)/8))+1
            i=0
            for n, label in enumerate(a.yaxis.get_ticklabels()):
                if i % step != 0:
                    label.set_visible(False)
                i+=1

        plt.title("Overall RMS",loc='right')
        plt.legend(loc='lower left', ncol=6,bbox_to_anchor= (0.0, 1.01), borderaxespad=0, frameon=False)
    else:
        plt.figure(2)

        #plt.xticks(np.arange(min(scale),max(scale)+1,5))
        #plt.yticks(np.arange(min(np.round(np.linspace(1,32,19))),max(np.round(np.linspace(1,32,19)))+1,5))

        #plt.gca().locator_params(axis='both',nbins=2)

        if one_section==0:
            plt.subplot(1,2,ind_figure)
            plt.suptitle('Section 1                                                  Section 2', fontsize=16)

        plt.xlabel('Scale')
        plt.ylabel('Overall RMS')
        plt.rcParams["axes.titlesize"] = 8
        plt.plot(X,RegLine,"b-",label='Multifractal time series')
        plt.plot(X,np.log2(F),"o",color="blue",label="slope H = "+str(H))
        #plt.xticks(X,np.linspace(scale_min,scale_max,scale_res))#####
        plt.xticks(X,scale,rotation=45)##Esta es nuestra autentica escala
        F_round=np.round(F,1)
        plt.yticks(RegLine,F_round)
        plt.title("Overall RMS",loc='right')
        plt.legend(loc='lower left', bbox_to_anchor= (0.0, 1.01), ncol=4, borderaxespad=0, frameon=False) 

        a=plt.gca()
        if len(scale)>=80:
            step=int((len(scale)/80))+1
            i=0
            for n, label in enumerate(a.xaxis.get_ticklabels()):
                if i % step != 0:
                    label.set_visible(False)
                i+=1

        if len(F_round)>=40:
            step=int((len(F_round)/40))+1
            i=0
            for n, label in enumerate(a.yaxis.get_ticklabels()):
                if i % step != 0:
                    label.set_visible(False)
                i+=1
   
    return H

def MFDFA(data,scale,q,m,Adjustment,noise,figure,scale_min,scale_max,scale_res,ind_figure,one_section,lines):
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
        suma=int(scale[ns])
        Idx_stop=suma-1
        qRMS.append([])
        for v in range(0,segments[-1]):
            Index=range(Idx_start,Idx_stop)
            X_Idx=data[Index]
            C=np.polyfit(Index,X_Idx,m)
            fit=np.polyval(C,Index)
            RMS[ns].append(np.sqrt(np.mean((X_Idx-fit)**2)))
            Idx_start=Idx_stop+1
            Idx_stop=Idx_stop+suma

        i=-1
        for nq in range(0,len(q)):
            qRMS[ns]=RMS[ns]**q[nq]
            if q[nq]==0:
                #Fq[nq].append(np.exp(0.5*np.mean([l**2 for l in np.log(RMS[ns])])))
                i=nq
            else:
                Fq[nq].append(np.mean(qRMS[-1])**(1/q[nq]))

        if i!=-1:
            sumaFq=[]
            for j in range(0,len(Fq[i-1])):
                sumaFq.append(Fq[i-1][j]+Fq[i+1][j])

            Fq[i]=[x/2 for x in sumaFq]


    for nq in range(0,len(q)):
        C=np.polyfit(np.log2(scale),np.log2(Fq[nq]),1)
        Hq.append(C[0])
        qRegLine.append(np.polyval(C,np.log2(scale)))



    X=np.log2(scale)
    Y1=[]
    Y2=[]

    for k in range(0,len(q)):
        Y1.append([])
        Y1[-1]=np.log2(Fq[k])
        Y2.append([])
        Y2[-1]=qRegLine[k]

    i=0
    if figure=="1":
        plt.subplot(4,2,4)
        plt.xlabel('scale')
        plt.ylabel('Fq')
        for k in range(0,len(lines)):
            plt.plot(X,np.log2(Fq[lines[k]]),"o",color=colours[i],label="q="+str(q[lines[k]]))
            plt.plot(X,qRegLine[lines[k]],color=colours[i])
            i=i+1

        #plt.xticks(X,np.linspace(scale_min,scale_max,scale_res))
        plt.xticks(X,scale,fontsize=9,rotation=45)
        #plt.yticks(,np.round(np.linspace(-1,32,20)))

        a=plt.gca()
        if len(scale)>=40:
            step=int((len(scale)/40))+1
            i=0
            for n, label in enumerate(a.xaxis.get_ticklabels()):
                if i % step != 0:
                    label.set_visible(False)
                i+=1

        plt.title("q-order RMS",loc='right')
        plt.legend(loc='lower left', bbox_to_anchor= (0.0, 1.01), ncol=4, borderaxespad=0, frameon=False)

    else:
        plt.figure(4)
        if one_section==0:
            plt.subplot(1,2,ind_figure)
            plt.suptitle('Section 1                                                  Section 2', fontsize=16)


        plt.xlabel('scale')
        plt.ylabel('Fq')
        for k in range(0,len(lines)):
            plt.plot(X,np.log2(Fq[lines[k]]),"o",color=colours[i],label="q="+str(q[lines[k]]))
            plt.plot(X,qRegLine[lines[k]],color=colours[i])
            i=i+1



        plt.legend(loc='lower left', bbox_to_anchor= (0.0, 1.01), ncol=4, borderaxespad=0, frameon=False)
        #plt.xticks(X,np.linspace(scale_min,scale_max,scale_res))####
        plt.xticks(X,scale,rotation=45)
        #plt.yticks(,np.round(np.linspace(-1,32,20)))
        a=plt.gca()
        if len(scale)>=80:
            step=int((len(scale)/80))+1
            i=0
            for n, label in enumerate(a.xaxis.get_ticklabels()):
                if i % step != 0:
                    label.set_visible(False)
                i+=1
    #Calculo de RMSE

    RMSE=[]
    for i in range(0,len(q)):
        aux=[]
        for j in range(0,len(Y1[0])):
            aux.append(math.pow(Y2[i][j]-Y1[i][j],2))
        RMSE.append(math.sqrt(sum(aux)/len(Y1)))


    R2=[]
    for i in range(0,len(Y1)):
        aux1=[]
        aux2=[]
        Y1_m=sum(Y1[i])/len(Y1[i])
        for j in range(0,len(Y1[0])):
            aux2.append(math.pow(Y2[i][j]-Y1_m,2))
            aux1.append(math.pow(Y1[i][j]-Y1_m,2))
        R2.append((sum(aux2)/len(aux2))/(sum(aux1)/len(aux1)))


    mu=[]
    for i in range(0,len(q)):
        mu.append(Hq[i])
    q=np.array(q)
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
        
        plt.subplots_adjust(wspace=0.2,hspace=1.3)
        #plt.tight_layout(h_pad=0.9, w_pad=0.2 )
        
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


    return  Hq,tq,hq,Dq,Fq,mu,R2,RMSE


def start_MFDFA(data,m,scale,q,noise,figure,scale_min,scale_max,scale_res,l,r,s,lines):

    if s==-1:
        
        if l==-1:
            l=0
        if r==-1:
            r=len(scale)
        else:
            r+=1
        

        H=DFA(data,scale[l:r],m,noise,figure,scale_min,scale_max,scale_res,1,1)
     
        Adjustment=0
        if H<0.2:
            Adjustment-=1
        else:
            if H>1.2 and H<1.8:
                Adjustment+=1
            else:
                if H>1.8:
                    Adjustment+=2

        Hq,tq,hq,Dq,Fq,mu,R2,RMSE=MFDFA(data,scale[l:r],q,m,Adjustment,noise,figure,scale_min,scale_max,scale_res,1,1,lines)

        
        #Create_table("Results",q,mu,R2,RMSE)

    else:

        if l==-1:
            l=0
        if r==-1:
            r=len(scale)
        else:
            r+=1

        if figure=="1":
            plt.figure(num='Section 1')

        H=DFA(data,scale[l:s+1],m,noise,figure,scale_min,scale_max,scale_res,1,0)

        Adjustment=0
        if H<0.2:
            Adjustment-=1
        else:
            if H>1.2 and H<1.8:
                Adjustment+=1
            else:
                if H>1.8:
                    Adjustment+=2

        Hq,tq,hq,Dq,Fq,mu,R2,RMSE=MFDFA(data,scale[l:s+1],q,m,Adjustment,noise,figure,scale_min,scale_max,scale_res,1,0,lines)

   
        if figure=="1":
            plt.figure(num='Section 2')

        H=DFA(data,scale[s:r],m,noise,figure,scale_min,scale_max,scale_res,2,0)

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

        Hq,tq,hq,Dq,Fq,mu,R2,RMSE=MFDFA(data,scale[s:r],q,m,Adjustment,noise,figure,scale_min,scale_max,scale_res,2,0,lines)
    
    return Hq,tq,hq,Dq,Fq


def Create_table(title,q,mu,R2,RMSE):
    Result_Table(title,q,mu,R2,RMSE)

class Result_Table():

    def __init__(self,title,q,mu,R2,RMSE):
        self.window_table=Toplevel()
        #self.frame=Frame(self.window_table)
        #self.frame.grid(row=0,column=0,columnspan=2,sticky='nsew')
        self.window_table.resizable(width=True,height=True)
        self.window_table.title(title)

        self.window_table.protocol('WM_DELETE_WINDOW', self.close_window)


        columns_name=('q','\u03BC','R\u00b2','RMSE')

        self.tree=ttk.Treeview(self.window_table,columns=columns_name,show='headings',height=len(q)+1)
        self.tree.grid(row=0,column=0,sticky='nsew')
        for col in columns_name:
            self.tree.heading(col,text=col,anchor='center')
            self.tree.column(col,anchor='center')


        for i in range(0,len(q)+1):
            if i==len(q):
                self.tree.insert("","end",values=("Min R\u00b2","Max RMSE",min(R2),max(RMSE)),tag=i)
            else:
                self.tree.insert("","end",values=(q[i],mu[i],R2[i],RMSE[i]),tag=i)

        self.tree.tag_configure(len(q),background='grey90')
        

        self.button_txt=Button(self.window_table,text="Save data",command=self.save)
        self.button_txt.grid(row=1,column=0,sticky='nsew')

    


        self.window_table.grid_columnconfigure(0, weight=1)
        self.window_table.grid_rowconfigure(0, weight=1)
        self.window_table.grid_columnconfigure(1, weight=1)



        self.window_table.update()

    def save(self):
        
        files = [('All Files', '*.*'),('Data Document', '*.dat'),('Text Document', '*.txt'),('CSV Document', '*.csv')]
        try:
            file_path=asksaveasfile(filetypes=files, defaultextension=files)
  
            with open(file_path.name,"w+") as file:
                for line in self.tree.get_children():
                    for value in self.tree.item(line)['values']:
                        print(str(value))
                        file.write(str(value)+"|")
                    file.write('\n')
        except:
            print("Prepare exception")

    def close_window(self):
        self.window_table.destroy()  





class Aux_Window():
    def search_point(self,data,X,min,max,center):

        r=max
        l=min
        distance1=math.sqrt(pow(data-X[center],2))
        i=0
        while l<r and i<10000:

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

            #if distance1<distance2:
                #p=center
                
            distance1=distance2
            i=i+1

        return center,X[center]

    
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
        if event.button==1 and not self.section_var.get():

            self.left_index,p=self.search_point(event.xdata,self.x_Axis,0,len(self.x_Axis),self.center)
    
            if self.left_bool:
                i=-1
                while self.a.lines[i].get_label()!="left":
                    i-=1
                self.a.lines[i].remove()

            if self.left_pre!=p:
                self.line_left=self.a.axvline(x=p,color="red",label="left")
                self.left_pre=p
                self.left_bool=True
            else:
                self.left_bool=False
                self.left_pre=-1

            #print('%s click: button=%d, x=%d, y=%d, xdata=%f, ydata=%f' %
            #        ('double' if event.dblclick else 'single', event.button,
            #        event.x, event.y, event.xdata, event.ydata))
            self.canvas.draw()

    def right_del(self,event):
        if event.button==3 and not self.section_var.get():

            self.right_index,p=self.search_point(event.xdata,self.x_Axis,0,len(self.x_Axis),self.center)

            if self.right_bool:
                i=-1
                while self.a.lines[i].get_label()!="right":
                    i-=1
                self.a.lines[i].remove()

            if self.right_pre!=p:
                self.line_right=self.a.axvline(x=p,color="blue",label="right")
                self.right_pre=p
                self.right_bool=True
            else:
                self.right_bool=False
                self.right_pre=-1

            #print('%s click: button=%d, x=%d, y=%d, xdata=%f, ydata=%f' %
            #        ('double' if event.dblclick else 'single', event.button,
            #        event.x, event.y, event.xdata, event.ydata))
            self.canvas.draw()

    def section(self,event):
        if event.button==2 or self.section_var.get():

            self.section_index,p=self.search_point(event.xdata,self.x_Axis,0,len(self.x_Axis),self.center)

            if self.section_bool:
                i=-1
                while self.a.lines[i].get_label()!="section":
                    i-=1
                self.a.lines[i].remove()

            if self.section_pre!=p:
                self.line_section=self.a.axvline(x=p,color="green",label="section")
                self.section_pre=p
                self.section_bool=True
            else:
                self.section_bool=False
                self.section_pre=-1


            #print('%s click: button=%d, x=%d, y=%d, xdata=%f, ydata=%f' %
            #        ('double' if event.dblclick else 'single', event.button,
            #        event.x, event.y, event.xdata, event.ydata))
            self.canvas.draw()
    
    def reset_line(self):
        if self.left_bool:
            self.a.lines[-1].remove()
            self.left_bool=False
            self.left_index=-1

        if self.right_bool:
            self.a.lines[-1].remove()
            self.right_bool=False
            self.right_index=-1

        if self.section_bool:    
            self.a.lines[-1].remove()
            self.section_bool=False
            self.section_index=-1


        self.canvas.draw()



    def __init__(self,title,X,Fq,qRegLine,q,scale,lines):
        self.left_bool=False
        self.right_bool=False
        self.section_bool=False

        self.section_index=-1
        self.left_index=-1
        self.right_index=-1
        self.section_closed=False

        self.section_pre=-1
        self.left_pre=-1
        self.right_pre=-1

        self.x_Axis=X#needed for axvline
        self.center=int(len(X)/2)

        self.window=Toplevel()
        self.window.grab_set()
        self.window.title(title)
        self.window.protocol('WM_DELETE_WINDOW', self.close_window)
   
        self.window.resizable(width=True,height=True)

        self.menubar=Menu(self.window)
        self.menubar.config(bg='grey90')
        self.menubar.add_command(label='Info',command=self.open_info)
        self.window.config(menu=self.menubar)
        #self.a.locator_params(nbins=2)

        self.f=Figure(dpi=100)
        self.a=self.f.add_subplot(111)

        i=0
        for k in range(0,len(lines)):
            self.a.plot(X,np.log2(Fq[lines[k]]),"o",color=colours[i],label="q="+str(q[lines[k]]))
            self.a.plot(X,qRegLine[lines[k]],color=colours[i])
            i=i+1

        print("X")
        print(X)
        print("scale")
        print(scale)
  
        self.a.set_xticks(X, minor=False)
        self.a.set_xticklabels(scale,fontdict=None,minor=False,rotation=45)
        #self.a.locator_params(tight=True,nbins=4)
        if len(scale)>=80:
            step=int((len(scale)/80))+1
            i=0
            for n, label in enumerate(self.a.xaxis.get_ticklabels()):
                if i % step != 0:
                    label.set_visible(False)
                i+=1


        #fontP = FontProperties()
        #fontP.set_size('small')
        self.a.set_title("q-order RMS",loc='right')
        self.a.legend(loc='lower left', bbox_to_anchor= (0.0, 1.01), ncol=4, borderaxespad=0, frameon=True)
        #self.a.legend(loc='upper center', bbox_to_anchor=(0.5, 1.00), shadow=True, ncol=4)
        #a.ion()
        #a.pause(0.001)

       

        self.a.tick_params(axis='x', which='major', labelsize=10)
        self.a.tick_params(axis='y', which='major', labelsize=10)

        self.canvas=FigureCanvasTkAgg(self.f,master=self.window)
        self.canvas.draw()
        self.canvas.get_tk_widget().grid(row=0,column=0,columnspan=3,sticky='nsew')

        #self.canvas.get_tk_widget().grid_columnconfigure(0, weight=1)
        #self.canvas.get_tk_widget().grid_rowconfigure(0, weight=1)

        #self.canvas.get_tk_widget().pack(side=BOTTOM,fill=BOTH,expand=True)
        self.frame_toolbar=Frame(master=self.window)
        self.frame_toolbar.grid(row=1,column=0,columnspan=3,sticky='nsew')

        #self.frame_toolbar.grid_columnconfigure(0, weight=1)
        #self.frame_toolbar.grid_rowconfigure(1, weight=1)

        self.toolbar=NavigationToolbar2Tk(self.canvas,self.frame_toolbar)
        self.toolbar.update()


        self.cid1=self.f.canvas.mpl_connect('button_press_event',self.left_del)
        self.cid2=self.f.canvas.mpl_connect('button_press_event',self.right_del)
        self.cid3=self.f.canvas.mpl_connect('button_press_event',self.section)

        self.reset_button=Button(self.window,text="Reset Values",command=self.reset_line)
        self.reset_button.grid(row=2,column=1,sticky='nsew')
        #self.reset_button.grid_columnconfigure(1, weight=1)
        #self.reset_button.grid_rowconfigure(2, weight=1)

        self.section_var=IntVar()

        self.checkbutton_section=Checkbutton(self.window,text='Section',onvalue=1,offvalue=0,var=self.section_var)
        self.checkbutton_section.grid(row=2, column=0,sticky='nsew')
        #self.checkbutton_section.grid_columnconfigure(0, weight=1)
        #self.checkbutton_section.grid_rowconfigure(2, weight=1)


        self.send_button=Button(self.window,text='Send',command=self.send_data)
        self.send_button.grid(row=2,column=2,sticky='nsew')

        #self.send_button.grid_columnconfigure(2, weight=1)
        #self.send_button.grid_rowconfigure(2, weight=1)

        self.window.grid_columnconfigure(0, weight=1)
        self.window.grid_rowconfigure(0, weight=1)

        self.window.grid_columnconfigure(0, weight=1)
        #self.window.grid_rowconfigure(1, weight=1)

        self.window.grid_columnconfigure(2, weight=1)
        #self.window.grid_rowconfigure(2, weight=1)

        self.window.mainloop()

    def send_data(self):

        if self.left_index!=-1 and self.right_index!=-1:
            if self.right_index<=self.left_index:
                messagebox.showwarning("Warning", "Right delimiter can't be equal or lower than left delimiter")
            elif self.section_index!=-1:
                if self.right_index<self.section_index:
                    messagebox.showwarning("Warning", "Right delimiter can't be lower than section delimiter")
                elif self.left_index>=self.section_index:
                    messagebox.showwarning("Warning", "Left delimiter can't be equal or greater than section delimiter")
                else:
                    self.f.canvas.mpl_disconnect(self.cid1)
                    self.f.canvas.mpl_disconnect(self.cid2)
                    self.f.canvas.mpl_disconnect(self.cid3)
                    self.toolbar.destroy()
                    self.frame_toolbar.destroy
                    self.window.quit()
                    self.window.destroy() 
            else:
                self.f.canvas.mpl_disconnect(self.cid1)
                self.f.canvas.mpl_disconnect(self.cid2)
                self.f.canvas.mpl_disconnect(self.cid3)
                self.frame_toolbar.destroy
                self.toolbar.destroy()
                self.window.quit()
                self.window.destroy() 

        else:
            self.f.canvas.mpl_disconnect(self.cid1)
            self.f.canvas.mpl_disconnect(self.cid2)
            self.f.canvas.mpl_disconnect(self.cid3)
            self.frame_toolbar.destroy
            self.toolbar.destroy()
            self.window.quit()
            self.window.destroy()  

    def close_window(self):
        self.f.canvas.mpl_disconnect(self.cid1)
        self.f.canvas.mpl_disconnect(self.cid2)
        self.f.canvas.mpl_disconnect(self.cid3)
        self.frame_toolbar.destroy
        self.toolbar.destroy()
        self.window.quit()
        self.window.destroy()
        self.section_closed=True  


    def ret_value_left_delimiter(self):
        return self.left_index

    def ret_value_right_delimiter(self):
        return self.right_index

    def ret_value_section(self):
        return self.section_index

    def closed(self):
        return self.section_closed

    