from tkinter import *
from tkinter import ttk
from tkinter.filedialog import askopenfile
from tkinter.filedialog import askopenfilename

class Aux_Window():
    def __init__(self,title):
        self.window=Tk()
        self.window.title(title)
        self.window.protocol('WM_DELETE_WINDOW', self.close_window)
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
        self.window_button=Button(self.window,text="Send")
        self.window_button.grid(row=self.r+1,column=self.c)
        self.window.mainloop()

    def close_window(self):
        self.window.destroy()

if __name__=='__main__':
    w=Aux_Window("Prueba")
    w.add_scale("Introduce     :",0,1024)
    w.start_window()