'''
python3 combined_tool.py
'''

from tkinter import * 
from tkinter.ttk import *
from tkinter.filedialog import askopenfile, askopenfilename 
import os

import sys
if sys.version_info[0] < 3:
    import Tkinter as Tk
else:
    import tkinter as Tk

root = Tk.Tk()
root.geometry('900x900')
root.wm_title("Flow and Drought Tool")
root.configure(background="light blue") 
equation = StringVar()

expression_field = Entry(root, textvariable=equation) 

def call_method1():
    os.system('python3  ./test.py')

def call_method2():
    os.system('python3  ./drought_tkinter.py')


label = Tk.Label(root, text = 'Tool Types',font=('calibre',10, 'bold')) 
label.pack(side = Tk.TOP, pady = 10)

method1 = Button(root, text ='Flow Accumulation & Direction', command = lambda:call_method1()) 
method1.pack(side = Tk.TOP, pady = 10)

method2 = Button(root, text ='Drought Identification', command = lambda:call_method2()) 
method2.pack(side = Tk.TOP, pady = 10)

def _quit():
    root.quit()     
    root.destroy()

button = Tk.Button(master=root, text='Quit', command=_quit)
button.pack(side=Tk.BOTTOM)

Tk.mainloop()


