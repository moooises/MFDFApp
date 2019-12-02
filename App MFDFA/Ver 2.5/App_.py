from tkinter import *
from tkinter import ttk
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
    i=0
    while round(q[i])!=0:
        i=i+1

    ind=i

    q_index=[]

    for j in range(1,5): ##Change this value(4) to get more q plots
        q_index.append(j*4)

    return q_index

def DFA(data,scale,m,noise,figure,scale_min,scale_max,scale_res):
    #plot the data
    #plt.figure(figsize=(6,3))

    #m=1
    segments=[]
    F=[]
    RMS=[]
    #print(data)


    if noise=="1":
        print("Tiene estructura ruido")
    else:
        print("NO")

    if figure=="1":
        print("Subplot")
    else:
        print("Muchas figuras")

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
        if noise=="1":
            plt.figure(1)
            plt.plot(data,label='time series')
            plt.xlabel('time')
            plt.ylabel('Amplitude')
            plt.rcParams["axes.titlesize"] = 8
            plt.title("Time serie")
            data=np.cumsum(data-np.mean(data))
            plt.plot(data,label='Random Walk')
            plt.legend()
        else:
            plt.figure(1)
            plt.plot(data,label='time series')
            plt.xlabel('time')
            plt.ylabel('Amplitude')
            plt.rcParams["axes.titlesize"] = 8
            plt.title("Time serie")
            plt.legend()


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
            #print(Index)
            #print(len(Index))
            #print(X_Idx)
            C=np.polyfit(Index,X_Idx,m)
            #print(C)
            #print()
            fit=np.polyval(C,Index)
            #0.036
            RMS[ns].append(math.sqrt(np.mean((X_Idx-fit)**2)))
            Idx_start=Idx_stop+1
            Idx_stop=Idx_stop+sum
        F.append(np.sqrt(np.mean([l**2 for l in RMS[ns]])))
        
        

    X=np.log2(scale)
    Ch=np.polyfit(X,np.log2(F),1)
    H=Ch[0]
    RegLine=np.polyval(Ch,X)

    if figure=="1":
        print("Subplot")
    else:
        print("Muchas figuras")

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

    print(scale)

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

    scale=np.delete(scale,0)
    scale=np.delete(scale,len(scale)-1)
    print(scale)    
    scale_selector=Aux_Window("Scale Selector",scale_min,scale_max,scale)
    s=scale_selector.ret_value_scale()
    return int(s)

def MFDFA(data,scale,q,m,qindex,Adjustment,noise,figure,scale_min,scale_max,scale_res,scale_limit):
    #probar con los arrays de numpy
    if noise=="1":
        data=np.cumsum(data-np.mean(data))



    segments=[]
    RMS=[]
    qRMS=[]
    Fq=[]
    Hq=[]
    qRegLine1=[]
    qRegLine2=[]



    print(scale)

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
    
    ###Prueba###
    ind_np=np.where(scale==scale_limit)

    ind=int(ind_np[0])

    print(np.linspace(scale_min,scale_max,scale_res))
    print(scale[ind])
    print(scale[0:ind+1])
    print(scale[ind:])

    
    for nq in range(0,len(q)):

        C=np.polyfit(np.log2(scale[0:ind+1]),np.log2(Fq[nq][0:ind+1]),1)
        Hq1=C[0]
        qRegLine1.append(np.polyval(C,np.log2(scale[0:ind+1])))

        C=np.polyfit(np.log2(scale[ind:]),np.log2(Fq[nq][ind:]),1)
        Hq2=C[0]
        qRegLine2.append(np.polyval(C,np.log2(scale[ind:])))

        Hq.append([])
        #qRegLine.append([])

        Hqaux=np.concatenate((Hq1,Hq2), axis=None)
        for y in Hqaux:
            Hq[nq].append(y)

        #qRegLineaux=np.concatenate((qRegLine1,qRegLine2), axis=None)
        #for x in qRegLi    neaux:
            #qRegLine[nq].append(x)

        #print(qRegLine[nq])
 


    X=np.log2(scale)

    
    i=0
    if figure=="1":
        plt.subplot(4,2,4)
        plt.xlabel('scale')
        plt.ylabel('Fq')
        for k in qindex:
            plt.plot(X,np.log2(Fq[k]),"o",color=colours[i],label="q="+str(int(q[k])))
            plt.plot(X[0:ind+1],qRegLine1[k],color=colours[i])
            plt.plot(X[ind:],qRegLine2[k],color=colours[i])
            i=i+1

        #plt.xticks(X,np.linspace(scale_min,scale_max,scale_res))
        plt.xticks(X,scale)
        #plt.yticks(,np.round(np.linspace(-1,32,20)))
        plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.30), shadow=True, ncol=4)   
    else:
        plt.figure(4)
        plt.xlabel('scale')
        plt.ylabel('Fq')
        for k in qindex:
            plt.plot(X,np.log2(Fq[k]),"o",color=colours[i],label="q="+str(int(q[k])))
            plt.plot(X[0:ind+1],qRegLine1[k],color=colours[i])
            plt.plot(X[ind:],qRegLine2[k],color=colours[i])
            i=i+1
        #plt.xticks(X,np.linspace(scale_min,scale_max,scale_res))####
        plt.xticks(X,scale)
        #plt.yticks(,np.round(np.linspace(-1,32,20)))
        plt.legend(loc='upper center', bbox_to_anchor=(0.5, 1.00), shadow=True, ncol=4)


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
        plt.plot(q[0:-1],hq,color="blue")

        plt.subplot(4,2,6)
        plt.xlabel('q-order')
        plt.ylabel('Dq')
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
    else:

        plt.figure(5)
        plt.xlabel('q-order')
        plt.ylabel('hq')
        plt.plot(q[0:-1],hq,color="blue")

        plt.figure(6)
        plt.xlabel('q-order')
        plt.ylabel('Dq')
        plt.plot(q[0:-1],Dq,color="blue")

        plt.figure(8)
        plt.rcParams["axes.titlesize"] = 8
        plt.title("Multifractal spectrum of Dq and hq")
        plt.xlabel('hq')
        plt.ylabel('Dq')
        plt.plot(hq,Dq,color="blue")

        plt.figure(3)
        plt.rcParams["axes.titlesize"] = 8
        plt.title("Hurst exponent in each q-order",)
        plt.xlabel('q-order')
        plt.ylabel('Hq')
        plt.plot(q,Hq,color="blue")


    return  Hq,tq,hq,Dq,Fq


def start_MFDFA(data,m,scale,q,q_index,noise,figure,scale_min,scale_max,scale_res):
    s=Select_Scale(data,scale,q,m,q_index,noise,figure,scale_min,scale_max,scale_res)

    #print(s)
    #print(r)
    H=DFA(data,scale,m,noise,figure,scale_min,scale_max,scale_res)

    Adjustment=0
    if H<0.2:
        Adjustment-=1
    else:
        if H>1.2 and H<1.8:
            Adjustment+=1
        else:
            if H>1.8:
                Adjustment+=2

    Hq,tq,hq,Dq,Fq=MFDFA(data,scale,q,m,q_index,Adjustment,noise,figure,scale_min,scale_max,scale_res,s)
    if figure:
        plt.subplots_adjust(wspace=0.3,hspace=0.7)
    plt.show(block=True)
    plt.show()
    return Hq,tq,hq,Dq,Fq


class Application():


    def reload_q_min_max(self):
        aux=str(self.q_entry.get())
        #self.q_max_entry.configure(state='normal')
        self.q_max_entry.delete(0,END)
        self.q_max_entry.insert(0,int(aux))
        #self.q_max_entry.configure(state='readonly')
        #self.q_min_entry.configure(state='normal')
        self.q_min_entry.delete(0,END)
        self.q_min_entry.insert(0,int('-'+aux))
        #self.q_min_entry.configure(state='readonly')
        return True

    def open_info(self):
        if not self.info_active:
            self.info_active=True
            self.raiz_info=Toplevel()
            self.raiz_info.title('Info')
            self.info_text=Text(self.raiz_info)
            self.info_text.insert('1.0','Information about input parameters\n\nScale:\n\nThese parameters indicate the size of each segment from each scalation in MFDFA.It is recommend to use values powers of 2 except for Res.\n') 
            self.info_text.insert(END,'In order to make it simple you need to insert the smallest segment size in Min, the largest segment size in Max and how many scales you want in Res.\n')
            self.info_text.insert(END,'Min needs to be bigger than 10, I recommend around 16.\nMax depends of the size  of your sample data and how many scales you want, 1/10 of the size of the sample data should provide at least 10 representative scales.\n')
            self.info_text.insert(END,'Res is up to you, but also depends of the Max value you chose.\nThese are just recomendations to generate representative data, you can try      whatever you decide.\n\n')
            self.info_text.insert(END,'m:\n\nThis is the order of the polinominal trend used to calculate the local          fluctuations RMS, the bigger it is the more complex will be its shape. An order of 2 or 3 is more than enough, but I allow up to 10 if you want to experiment.\n\n')
            self.info_text.insert(END,'q:\n\nDecide the q-order weighing of the local fluctuations RMS.\nIt should consist on both positive and negative q to weight the period of small and big fluctuations in the time series\n')
            self.info_text.insert(END,'It is recommended to avoid large number because they inflict more numerical     errors in the tails of the multifractal spectrum. For biomedical data -5 and 5  are recommended.')
            #self.info_text.insert(END,'\n\nThe application is prepared to only read .csv files, you can indicate the       separtor of the .csv in its field, by default is | . ')
            self.info_text.insert(END,'\n\nThe Noise Structure check button must be checked if your data has a noise like  structure, because in that case your data must be preprocesed to work with this algorithm.')
            self.info_text.configure(state=DISABLED)
            self.info_text.pack(side=TOP,fill=BOTH,expand=1)
            self.info_button=Button(self.raiz_info,text='Close',command=self.close_info)
            self.info_button.pack(side=BOTTOM)
            self.raiz_info.geometry('646x650')
            self.raiz_info.resizable(width=False,height=False)


            #self.raiz_info.update()
            #print(self.raiz_info.winfo_geometry())
            self.raiz_info.protocol('WM_DELETE_WINDOW', self.close_info)
            self.raiz_info.mainloop()


    def close_info(self):
        self.info_active=False
        self.raiz_info.destroy()

    def open_about(self):
        if not self.about_active:
            self.about_active=True
            self.raiz_about=Toplevel()
            self.raiz_about.title("About")
            var=StringVar()
            self.about_message=Message(self.raiz_about,textvariable=var)
            var.set("Coded by Moises Guerrero Lopez\n\nGithub: moooises\n\nInspired by the work of\nEspen A. F. Ihlen\n\nin his paper\nIntroduction to multifractal detrended fluctuations analysis in Matlab\n\npublished in\nFrontiers by Physiology")
            self.about_message.pack(side=TOP,fill=BOTH,expand=1)
            self.about_button=Button(self.raiz_about,text='Close',command=self.close_about)
            self.about_button.pack(side=BOTTOM)
            self.raiz_about.protocol('WM_DELETE_WINDOW', self.close_about)
            self.raiz_about.mainloop()


    def close_about(self):
        self.about_active=False
        self.raiz_about.destroy()

    def write_text(self,output):
        self.result_text.insert(END,output)

    def open_file(self):
        #file=askopenfilename()
        #if file is not None:            
        #    self.path_time=file
        #    print(self.path_time)
        #else:
        #    self.write_text("Time file not selected")

        file=askopenfilename()
        if file is not None:            
            self.path=file
            print(self.path)
        else:
            #self.path_time=""
            self.write_text("Data file not selected")




    def prepare_MFDFA(self,data,scale_min,scale_max,scale_res,q_min,q_max,m,noise,figure):
        aux=""

        m=int(m)
        exponents=np.linspace(math.log2(int(scale_min)),math.log2(int(scale_max)),int(scale_res))
        scale=np.around(2**exponents,0)

        ###Arregalr aqui q
        if q_min<0:
            cant=(int(q_min)*-1)*2
        else:
            cant=int(q_min)*2

        if q_max<0:
            cant=cant+(int(q_max)*-1)*2
        else:
            cant=cant+int(q_max)*2

        cant=cant+1

        q=np.linspace(float(q_min),float(q_max),cant)

        q_index=index(q)
        print(q)
        print(q_index)
        
        Hq,tq,hq,Dq,Fq=start_MFDFA(data,int(m),scale,q,q_index,noise,figure,int(scale_min),int(scale_max),int(scale_res))

        #self.write_text("Hq: "+str(Hq)+"\n")
        #self.write_text("tq: "+str(tq)+"\n")
        #self.write_text("hq: "+str(hq)+"\n")
        #self.write_text("Dq: "+str(Dq)+"\n")
        #self.write_text("Fq: "+str(Fq)+"\n")



    def start(self):
        plt.close('all')

        output=""

        path_file=self.path

        if path_file=="":
            output=output+"No data file selected\n"

        #path_file_time=self.path_time
        #if path_file_time=="":
            #output=output+"No data file selected\n"
            
        #csv.field_size_limit(sys.maxsize)
        #with open(path_file_time) as file:
            #reader_time=csv.reader(file,delimiter=separator)
            #time=list(reader_time)#arreglar esto
            #time_r=list(file.read().splitlines())


        if path_file!="":
            data=[]

            if path_file[-4:]==".mat":
                data_r= scipy.io.loadmat('fractaldata.mat')

                for e in data_r:
                    data.append(float(e[0]))

            else:    
                with open(path_file) as file:
                    #reader=csv.reader(file,delimiter=separator)
                    #data=list(reader)
                    data_r=list(file.read().splitlines())

                #time=[]
                #print(data_r[0])
                #print(time_r[0])
        
                data=list(map(float,data_r))
                #time=list(map(float,time_r))
                #print(data)
                #print(type(data))




        scale_min=self.scale_min_entry.get()
        if scale_min=="":
            output=output+"Min value in scale not given\n"

        scale_max=self.scale_max_entry.get()
        if scale_max=="":
            output=output+"Max value in scale not given\n"
        else:
            if int(scale_max)>len(data)/4:
                output=output+"Max in value in scale can't be bigger than a quarter of the size of the data\n"

        scale_res=self.scale_res_entry.get()
        if scale_res=="":
            output=output+"Res value in scale not given\n" 

        q_min=self.q_min_entry.get()
        if q_min=="":
            output=output+"q min value in q not given\n"   

        q_max=self.q_max_entry.get()
        if q_max=="":
            output=output+"q max value in q not given\n"

        q_min=int(q_min)
        q_max=int(q_max)

        if q_min>q_max:
            output=output+"q max must be bigger than q min\n"
        else:
            if q_max==q_min:
                output=output+"q max and q min can't be equal\n"

        #separator=self.separator_entry.get()
        m=self.m_spinbox.get()
        print(type(m))
        f=self.figure.get()
        if output!="":
            self.write_text(output)
        else:
            self.prepare_MFDFA(data,float(scale_min),float(scale_max),float(scale_res),q_min,q_max,m,self.noise.get(),self.figure.get())


    def close_window(self):
        self.raiz.quit()
        plt.close('all')
        self.raiz.destroy()

    def __init__(self):
        self.path=""
        #self.path_time=""

        self.raiz=Tk()
        self.info_active=False
        self.about_active=False
        self.noise=StringVar()
        self.noise.set("1")
        self.figure=StringVar()
        self.figure.set("1")

        self.raiz.grab_set()
        #self.raiz.geometry('300x200')
        self.raiz.resizable(width=False,height=False)
        self.raiz.configure(bg='white')
        self.raiz.title('MFDFA')
        self.raiz.protocol('WM_DELETE_WINDOW', self.close_window)


        #Menu
        self.menubar=Menu(self.raiz)
        self.menubar.add_command(label='Info',command=self.open_info)
        self.menubar.add_command(label='About',command=self.open_about)
        self.raiz.config(menu=self.menubar)



        #Escala
        self.scale_label=Label(text='Scale',bg='white')
        self.scale_label.grid(row=2,column=1)
        self.scale_min_label=Label(text='Min', bg='white',borderwidth=3,relief="sunken")
        self.scale_min_label.grid(row=3,column=0)
        self.scale_min_entry=Entry(self.raiz, bg='white')
        self.scale_min_entry.grid(row=4,column=0)
        self.scale_max_label=Label(text='Max', bg='white',borderwidth=3,relief="sunken")
        self.scale_max_label.grid(row=3,column=1,padx=10, pady=10)
        self.scale_max_entry=Entry(self.raiz, bg='white')
        self.scale_max_entry.grid(row=4,column=1,padx=50, pady=5)
        self.scale_res_label=Label(text='Res', bg='white',borderwidth=3,relief="sunken")
        self.scale_res_label.grid(row=3,column=2)
        self.scale_res_entry=Entry(self.raiz, bg='white')
        self.scale_res_entry.grid(row=4,column=2)

        # m
        self.m_label=Label(text='m',bg='white')
        self.m_label.grid(row=6,column=1)
        self.m_spinbox=Spinbox(self.raiz,bg='white',from_=1, to=5, width=4)
        self.m_spinbox.grid(row=7,column=1)

        # q
        self.raiz.register(self.reload_q_min_max)

        self.q_label=Label(text='q', bg='white')
        self.q_label.grid(row=9, column=1)
        #self.q,validate='focusout',validatecommand=self.reload_q_min_max())
        self.q_entry=Entry(self.raiz, bg='white', width=4,validate="focusout", validatecommand=self.reload_q_min_max)
        self.q_entry.grid(row=10,column=1)

        self.q_min_label=Label(text='q min',bg='white',borderwidth=3,relief="sunken")
        self.q_min_label.grid(row=11,column=0)
        self.q_min_entry=Entry(self.raiz,bg='white', width=4,state="normal")
        self.q_min_entry.grid(row=12, column=0)
        #self.q_min_text.config(state=DISABLED)
        self.q_max_label=Label(text='q max',bg='white',borderwidth=3,relief="sunken")
        self.q_max_label.grid(row=11,column=2)
        self.q_max_entry=Entry(self.raiz,bg='white', width=4,state="normal")
        self.q_max_entry.grid(row=12, column=2)
        

        #Cuadro de texto
        self.result_text=Text(self.raiz,padx=10,pady=10,bg='grey90')
        #self.result_text.insert(END,'Results\n--------------------------------------------------------------------------------')
        self.result_text.grid(row=13, column=0, columnspan=3)

        #Pedir archivo
        self.file_label=Label(text='        Select data file   ', bg='white')
        self.file_label.grid(row=15,column=0,sticky=W)
        self.file_button=Button(self.raiz,text='.....',command=self.open_file)
        self.file_button.grid(row=15, column=0,sticky=E)

        #Separtator
        #self.separator_label=Label(text='        CSV Separator',bg='white')
        #self.separator_label.grid(row=15,column=1,sticky=W)
        #self.separator_entry=Entry(self.raiz,bg='white',width=1)
        #self.separator_entry.grid(row=15,column=1)

        #One figure in all<
        self.figure_checkbutton=Checkbutton(self.raiz,text='One figure',onvalue=1,offvalue=0,variable=self.figure)
        self.figure_checkbutton.grid(row=15,column=2,sticky=W)

        #Noise like
     
        self.noise_checkbutton=Checkbutton(self.raiz,text='Noise structure',onvalue=1,offvalue=0,variable=self.noise)
        self.noise_checkbutton.grid(row=15,column=1)

        #Procesar
        self.start_button=Button(self.raiz, text='Start', command=self.start,height = 1, width = 5)
        self.start_button.grid(row=15, column=2,sticky=E)

        #ttk.Button(self.raiz, text='Salir', command=self.raiz.destroy).grid(row=15,column=0)
        #self.tinfo=Text(self.raiz)
        #self.tinfo.grid(row=3,column=0,padx=5, pady=5)

        self.raiz.grid_rowconfigure(4, minsize=50)
        self.raiz.grid_rowconfigure(6, minsize=30)
        self.raiz.grid_rowconfigure(8, minsize=20)
        self.raiz.grid_rowconfigure(12, minsize=50)
        self.raiz.grid_rowconfigure(15, minsize=50)

        #self.write_text("First select the time file and then select the data file")

        self.write_text("Hq: Slope of the overall RMS(Hurst exponent)\n")
        self.write_text("q: Order-q values\n")
        self.write_text("tq: q-order mass exponent\n")
        self.write_text("hq: q-order singularity exponent (Tangent slope of tq\n")
        self.write_text("Dq: q-order singularity dimension\n")
        self.write_text("Fq: q-order overall RMS\n")
        self.write_text("F: Overall RMS\n")
        self.write_text("--------------------------------------------------------------------------------\n")

        self.raiz.mainloop()


class Aux_Window():

    def valuecheck(self,value):
        newvalue=min(self.scale_window, key=lambda x:abs(x-float(value)))
        self.window_scale.set(newvalue)


    def __init__(self,title,scale_min,scale_max,scale):
        self.scale_window=scale

        self.window=Tk()
        self.window.title(title)
        self.window.protocol('WM_DELETE_WINDOW', self.close_window)
        self.var=DoubleVar()
        self.var.set((scale_max-scale_min)/2)
        #print(self.var.get())    
        self.window.resizable(width=False,height=False)

        self.window_label=Label(self.window,text="Select the value for the next regresion and the regresion value:")
        self.window_label.grid(row=0,column=0)
        self.window_scale=Scale(self.window,from_=scale_min,to=scale_max,variable=self.var,orient=HORIZONTAL,sliderlength=10,length=int(scale_max/2),tickinterval=int(scale_max/8),command=self.valuecheck)
        self.window_scale.set(int(scale_max/2))
        self.window_scale.grid(row=1,column=0)
        

        self.window_spinbox=Spinbox(self.window,bg='white',from_=1, to=5, width=4)
        self.window_spinbox.grid(row=2,column=0)

        self.window_button=Button(self.window,text="Send",command=self.close_window)
        self.window_button.grid(row=5,column=0)

        self.window.mainloop()

    def close_window(self):
        self.window.quit()
        #plt.close(20)# desactivada temporalmente
        self.scale_value=self.window_scale.get()
        self.regresion_value=self.window_spinbox.get()
        self.window.destroy()   

    def ret_value_scale(self):
        return self.scale_value

    def ret_value_regresion(self):
        return self.regresion_value


if __name__=='__main__':

    mi_app=Application()
    