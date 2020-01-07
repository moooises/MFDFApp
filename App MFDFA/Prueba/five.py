from tkinter import *
master = Tk()

w = Canvas(master, width=250, height=200)
w.create_rectangle(0, 0, 10, 10, fill="blue", outline = 'blue')
w.pack()
master.mainloop()
