from tkinter import *
from tkinter import ttk
from tkinter.filedialog import askopenfile
from tkinter.filedialog import askopenfilename
from MFDFA_algorithm import start_MFDFA, Select_Scale, MFDFA, DFA

import matplotlib.pyplot as plt
import matplotlib.pyplot as plt_aux
import numpy as np
import scipy.io
import math
import csv
import sys
import random


random.seed(5)


class Application():


    def reload_q_min_max(self):
        aux=str(self.q_inc_entry.get())
        if aux!="":
            #self.q_max_entry.configure(state='normal')
            self.q_max_entry.delete(0,END)
            self.q_max_entry.insert(0,int(aux))
            #self.q_max_entry.configure(state='readonly')
            #self.q_min_entry.configure(state='normal')
            self.q_min_entry.delete(0,END)
            self.q_min_entry.insert(0,int('-'+aux))
            #self.q_min_entry.configure(state='readonly')
            return True
        else:
            self.q_max_entry.delete(0,END)
            self.q_min_entry.delete(0,END)
            return True




    def open_info(self):
        if not self.info_active:
            self.info_active=True
            self.raiz_info=Toplevel()
            self.raiz_info.title('Info')
            self.info_text=Text(self.raiz_info)
            self.info_text.insert('1.0','Information about input parameters\n\nScale:\n\nThese parameters indicate the size of each segment from each scalation in MFDFA.It is recommend to use values powers of 2 except for Res.\n') 
            self.info_text.insert(END,'In order to make it simple you need to insert the smallest segment size in Min, the largest segment size in Max and how many scales you want in Res.\n')
            self.info_text.insert(END,'Min needs to be bigger than 10, I recommend around 16.\nMax depends of the size  of your sample data and how many scales you want, 1/10 of the size of the sample data should provide at least 10 representative scales.It cannot be bigger than a quarter of sample data size.\n')
            self.info_text.insert(END,'Res is up to you, but also depends of the Max value you chose.\nThese are just recomendations to generate representative data, you can try      whatever you decide.\n\n')
            self.info_text.insert(END,'m:\n\nThis is the order of the polinominal trend used to calculate the local          fluctuations RMS, the bigger it is the more complex will be its shape. An order of 2 or 3 is more than enough, but I allow up to 10 if you want to experiment.\n\n')
            self.info_text.insert(END,'q:\n\nDecide the q-order weighing of the local fluctuations RMS.\nIt should consist on both positive and negative q to weight the period of small and big fluctuations in the time series\n')
            self.info_text.insert(END,'It is recommended to avoid large number because they inflict more numerical     errors in the tails of the multifractal spectrum. For biomedical data -5 and 5  are recommended.')
            #self.info_text.insert(END,'\n\nThe application is prepared to only read .csv files, you can indicate the       separtor of the .csv in its field, by default is | . ')
            self.info_text.insert(END,'\n\nThe Noise Structure check button must be checked if your data has a noise like  structure, because in that case your data must be preprocesed to work with this algorithm.')
            self.info_text.insert(END,'\n\nAll in organize all the graphics in one figure or two depending of the  section selected. If it is not checked will give each graphic in one figure, if you     select more than one section the graphics of every section will be shown in one figure each.')
            self.info_text.configure(state=DISABLED)
            self.info_text.pack(side=TOP,fill=BOTH,expand=1)
            self.info_button=Button(self.raiz_info,text='Close',command=self.close_info)
            self.info_button.pack(side=BOTTOM)
            self.raiz_info.geometry('646x700')
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




    def prepare_MFDFA(self,data,scale_min,scale_max,scale_res,q_inc,q_min,q_max,m,noise,figure):
        aux=""

        m=int(m)
        exponents=np.linspace(math.log2(int(scale_min)),math.log2(int(scale_max)),int(scale_res))
        scale=np.around(2**exponents,0)
        print(scale)
        ###Arregalr aqui q
       
        q=np.arange(q_min,q_max+q_inc,q_inc)
        q=np.round(q,2)
        aux_=np.linspace(q_min,q_max,len(q)*2)
        aux_=np.round(aux_,2)
        print(aux_)
        q=list(q)
        print("Los q")
        print(q)
     

        #print(q)
        #print(q_index)
        data=np.array(data)
        if len(q)<=8: #de esta forma evitamos que se repitan lineas cuando hay menos de 8 q-values
            lines=list(range(0,len(q)))
        else:
            lines=random.sample(range(len(q)),8)
            lines.sort()
        print("lines")
        print(lines)

        
        l,r,s=Select_Scale(data,scale,q,m,noise,figure,int(scale_min),int(scale_max),int(scale_res),lines)

        
        Hq,tq,hq,Dq,Fq=start_MFDFA(data,int(m),scale,q,noise,figure,int(scale_min),int(scale_max),int(scale_res),l,r,s,lines)

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

                data=list(map(float,data_r))

        scale_min=self.scale_min_entry.get()
        if scale_min=="":
            output=output+"Min value in scale not given\n"

        scale_max=self.scale_max_entry.get()
        if scale_max=="":
            output=output+"Max value in scale not given\n"
        else:
            print(scale_max)
            print(len(data))
            print(len(data)/4)
            if int(scale_max)>len(data)/4:
                output=output+"Max in value in scale can't be bigger than a quarter of the size of the data\n"

        scale_res=self.scale_res_entry.get()
        if scale_res=="":
            output=output+"Res value in scale not given\n" 

        q_inc=self.q_inc_entry.get()
        if q_inc=="":
            output=output+"q inc value not give\n"

        q_min=self.q_min_entry.get()
        if q_min=="":
            output=output+"q min value not given\n"   

        q_max=self.q_max_entry.get()
        if q_max=="":
            output=output+"q max value  not given\n"

        q_min=float(q_min)
        q_max=float(q_max)
        q_inc=float(q_inc)

        if q_min>q_max:
            output=output+"q max must be bigger than q min\n"
        else:
            if q_max==q_min:
                output=output+"q max and q min can't be equal\n"

        #separator=self.separator_entry.get()
        m=self.m_spinbox.get()
        #print(type(m))
        f=self.figure.get()
        if output!="":
            self.write_text(output)
        else:
            self.prepare_MFDFA(data,float(scale_min),float(scale_max),float(scale_res),q_inc,q_min,q_max,m,self.noise.get(),self.figure.get())


    def close_window(self):
        self.raiz.quit()
        plt.close('all')
        self.raiz.destroy()
        sys.exit()

    def __init__(self):
        self.path="/home/mo_oises/Schreibtisch/TFG/MFDFA/App MFDFA/Ver 2.5/multifractal_paper.dat"
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
        self.scale_min_entry=Entry(self.raiz, bg='white',justify='center')
        self.scale_min_entry.grid(row=4,column=0)
        self.scale_min_entry.insert(0,int(16))
        self.scale_max_label=Label(text='Max', bg='white',borderwidth=3,relief="sunken")
        self.scale_max_label.grid(row=3,column=1,padx=10, pady=10)
        self.scale_max_entry=Entry(self.raiz, bg='white',justify='center')
        self.scale_max_entry.grid(row=4,column=1,padx=50, pady=5)
        self.scale_max_entry.insert(0,int(1024))
        self.scale_res_label=Label(text='Res', bg='white',borderwidth=3,relief="sunken")
        self.scale_res_label.grid(row=3,column=2)
        self.scale_res_entry=Entry(self.raiz, bg='white',justify='center')
        self.scale_res_entry.grid(row=4,column=2)
        self.scale_res_entry.insert(0,int(19))


        # m
        self.m_label=Label(text='m',bg='white')
        self.m_label.grid(row=6,column=1)
        self.m_spinbox=Spinbox(self.raiz,bg='white',from_=1, to=3, width=4)
        self.m_spinbox.grid(row=7,column=1)

        # q
        #self.raiz.register(self.reload_q_min_max)

        self.q_inc_label=Label(text='\u0394q', bg='white',borderwidth=3,relief="sunken")
        self.q_inc_label.grid(row=9, column=1)
        #self.q,validate='focusout',validatecommand=self.reload_q_min_max())
        self.q_inc_entry=Entry(self.raiz, bg='white',width=4,justify='center')#,validate="focusout",validatecommand=self.reload_q_min_max)
        self.q_inc_entry.insert(0,int(1))
        self.q_inc_entry.grid(row=10,column=1)

        self.q_min_label=Label(text='q min',bg='white',borderwidth=3,relief="sunken")
        self.q_min_label.grid(row=9,column=0)
        self.q_min_entry=Entry(self.raiz,bg='white', width=4,state="normal",justify='center')
        self.q_min_entry.grid(row=10, column=0)
        self.q_min_entry.insert(0,int(-5))
        #self.q_min_text.config(state=DISABLED)
        self.q_max_label=Label(text='q max',bg='white',borderwidth=3,relief="sunken")
        self.q_max_label.grid(row=9,column=2)
        self.q_max_entry=Entry(self.raiz,bg='white', width=4,state="normal",justify='center')
        self.q_max_entry.grid(row=10, column=2)
        self.q_max_entry.insert(0,int(5))
        

        #Cuadro de texto
        self.result_text=Text(self.raiz,padx=10,pady=10,bg='grey90')
        #self.result_text.insert(END,'Results\n--------------------------------------------------------------------------------')
        self.result_text.grid(row=11, column=0, columnspan=3)

        #Pedir archivo
        self.file_label=Label(text='        Select data file   ', bg='white')
        self.file_label.grid(row=12,column=0,sticky=W)
        self.file_button=Button(self.raiz,text='.....',command=self.open_file)
        self.file_button.grid(row=12, column=0,sticky=E)

        #Separtator
        #self.separator_label=Label(text='        CSV Separator',bg='white')
        #self.separator_label.grid(row=15,column=1,sticky=W)
        #self.separator_entry=Entry(self.raiz,bg='white',width=1)
        #self.separator_entry.grid(row=15,column=1)

        #One figure in all<
        self.figure_checkbutton=Checkbutton(self.raiz,text='All in',onvalue=1,offvalue=0,variable=self.figure)
        self.figure_checkbutton.grid(row=12,column=2,sticky=W)

        #Noise like
     
        self.noise_checkbutton=Checkbutton(self.raiz,text='Noise structure',onvalue=1,offvalue=0,variable=self.noise)
        self.noise_checkbutton.grid(row=12,column=1)

        #Procesar
        self.start_button=Button(self.raiz, text='Start', command=self.start,height = 1, width = 5)
        self.start_button.grid(row=12, column=2,sticky=E)

        #ttk.Button(self.raiz, text='Salir', command=self.raiz.destroy).grid(row=15,column=0)
        #self.tinfo=Text(self.raiz)
        #self.tinfo.grid(row=3,column=0,padx=5, pady=5)

        self.raiz.grid_rowconfigure(4, minsize=50)
        self.raiz.grid_rowconfigure(6, minsize=30)
        self.raiz.grid_rowconfigure(8, minsize=20)
        self.raiz.grid_rowconfigure(10, minsize=50)
        self.raiz.grid_rowconfigure(12, minsize=50)

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

if __name__=='__main__':

    mi_app=Application()