from tkinter import *
from tkinter import ttk
from tkinter.filedialog import askopenfile
from tkinter.filedialog import askopenfilename

#raiz=Tk()

#raiz.geometry('300x200')

#raiz.configure(bg='beige')

#raiz.title('Aplicacion')

#ttk.Button(raiz, text='Salir', command=quit).pack(side=BOTTOM)

#raiz.mainloop()


class Application():

    #def reload_q_max(self):
     #   global update_in_progress
      #  if update_in_progress: return
       # try:
        #    temp=self.q_entry.get()
        #except ValueError:
        #    return
        #new=self.q_entry.get()
        #update_in_progress=True
        #print(str(new))
        #self.q_max_entry.set(str(new))
        #update_in_progress=False

    #def reload_q_min(self):
     #   global update_in_progress
     #   if update_in_progress: return
      #  try:
       #     temp=self.q_entry.get()
        #except ValueError:
         #   return         
        #new=q.get()
        ##update_in_progress=True
        #print(str(new))
        #q_min.set('-'+str(new))
        #update_in_progress=False

    def reload_q_min_max(self):
        aux=str(self.q_entry.get())
        #self.q_max_entry.configure(state='normal')
        self.q_max_entry.delete(0,END)
        self.q_max_entry.insert(0,aux)
        #self.q_max_entry.configure(state='readonly')
        #self.q_min_entry.configure(state='normal')
        self.q_min_entry.delete(0,END)
        self.q_min_entry.insert(0,'-'+aux)
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
            self.info_text.insert(END,'\n\nThe application is prepared to only read .csv files, you can indicate the       separtor of the .csv in its field, by default is | . ')
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

    def open_file(self):
        global path
        file=askopenfilename()
        if file is not None and file.endswith('.csv'):            
            path=file
            print(path)
        else:
            print("Bad file")#write on text widget


    def __init__(self):

        self.raiz=Tk()
        self.info_active=False
        self.about_active=False


        self.raiz.grab_set()
        #self.raiz.geometry('300x200')
        self.raiz.resizable(width=False,height=False)
        self.raiz.configure(bg='white')
        self.raiz.title('MFDFA')

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
        self.m_spinbox=Spinbox(self.raiz,bg='white',from_=1, to=10, width=4)
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
        self.separator_label=Label(text='        CSV Separator',bg='white')
        self.separator_label.grid(row=15,column=1,sticky=W)
        self.separator_entry=Entry(self.raiz,bg='white',width=1)
        self.separator_entry.grid(row=15,column=1)

        #Noise like
     
        self.noise_checkbutton=Checkbutton(self.raiz,text='Noise structure',onvalue=1,offvalue=0)
        self.noise_checkbutton.grid(row=15,column=1, sticky=E)

        #Procesar
        self.start_button=Button(self.raiz, text='Start')
        self.start_button.grid(row=15, column=2)

        #ttk.Button(self.raiz, text='Salir', command=self.raiz.destroy).grid(row=15,column=0)
        #self.tinfo=Text(self.raiz)
        #self.tinfo.grid(row=3,column=0,padx=5, pady=5)

        self.raiz.grid_rowconfigure(4, minsize=50)
        self.raiz.grid_rowconfigure(6, minsize=30)
        self.raiz.grid_rowconfigure(8, minsize=20)
        self.raiz.grid_rowconfigure(12, minsize=50)
        self.raiz.grid_rowconfigure(15, minsize=50)

        self.raiz.mainloop()



if __name__=='__main__':
    mi_app=Application()
    