from tkinter import *
from tkinter import ttk

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
        self.q_max_entry.configure(state='normal')
        self.q_max_entry.delete(0,END)
        self.q_max_entry.insert(0,aux)
        self.q_max_entry.configure(state='readonly')
        self.q_min_entry.configure(state='normal')
        self.q_min_entry.delete(0,END)
        self.q_min_entry.insert(0,'-'+aux)
        self.q_min_entry.configure(state='readonly')
        return True


    def __init__(self):
        global q,q_min,q_max
        global update_in_progress

        update_in_progress=False

        self.raiz=Tk()

        self.raiz.grid_columnconfigure(4, minsize=200)
        #self.raiz.geometry('300x200')
        self.raiz.resizable(width=True,height=True)
        self.raiz.configure(bg='white')
        self.raiz.title('Aplication')

        #Escala
        self.scale_label=Label(text='Scale',bg='white')
        self.scale_label.grid(row=2,column=1)
        self.scale_min_label=Label(text='min', bg='white',borderwidth=3,relief="sunken")
        self.scale_min_label.grid(row=3,column=0)
        self.scale_min_entry=Entry(self.raiz, bg='white')
        self.scale_min_entry.grid(row=4,column=0)
        self.scale_max_label=Label(text='max', bg='white',borderwidth=3,relief="sunken")
        self.scale_max_label.grid(row=3,column=1,padx=10, pady=10)
        self.scale_max_entry=Entry(self.raiz, bg='white')
        self.scale_max_entry.grid(row=4,column=1,padx=50, pady=5)
        self.scale_res_label=Label(text='Res', bg='white',borderwidth=3,relief="sunken")
        self.scale_res_label.grid(row=3,column=2)
        self.scale_res_entry=Entry(self.raiz, bg='white')
        self.scale_res_entry.grid(row=4,column=2)

        # m
        self.m_label=Label(text='m',bg='white')
        self.m_label.grid(row=1,column=4)
        self.m_spinbox=Spinbox(self.raiz,bg='white',from_=1, to=10, width=4)
        self.m_spinbox.grid(row=2,column=4)

        # q
        #q=StringVar()
        #q.set('5')
        #q_min=StringVar()
        #q_max=StringVar()

        #self.raiz.register(self.reload_q_min)
        self.raiz.register(self.reload_q_min_max)

        self.q_label=Label(text='q', bg='white')
        self.q_label.grid(row=1, column=7)
        #self.q,validate='focusout',validatecommand=self.reload_q_min_max())
        self.q_entry=Entry(self.raiz, bg='white', width=4,validate="focusout", validatecommand=self.reload_q_min_max)
        self.q_entry.grid(row=2,column=7)

        self.q_min_label=Label(text='q min',bg='white',borderwidth=3,relief="sunken")
        self.q_min_label.grid(row=3,column=6)
        self.q_min_entry=Entry(self.raiz,bg='white', width=4,state="readonly")
        self.q_min_entry.grid(row=4, column=6)
        #self.q_min_text.config(state=DISABLED)
        self.q_max_label=Label(text='q max',bg='white',borderwidth=3,relief="sunken")
        self.q_max_label.grid(row=3,column=8)
        self.q_max_entry=Entry(self.raiz,bg='white', width=4,state="readonly")
        self.q_max_entry.grid(row=4, column=8)
        #self.q_max_text.config(state=DISABLED)



        #self.reload_q_min_max(self.q_entry.get())
        #q_min.trace("w", reload_q_min)
        #q_max.trace("w", reload_q_max)

        #ttk.Button(self.raiz, text='Salir', command=self.raiz.destroy).grid(row=2,column=0)
        #self.tinfo=Text(self.raiz)
        #self.tinfo.grid(row=3,column=0,padx=5, pady=5)
        self.raiz.mainloop()



if __name__=='__main__':
    mi_app=Application()
    