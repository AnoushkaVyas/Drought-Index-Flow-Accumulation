from func import *
import time
from osgeo import ogr, gdal
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.backend_bases import key_press_handler
from tkinter import messagebox
import matplotlib
matplotlib.use('TkAgg')
from tkinter import * 
from tkinter.ttk import *
from tkinter import filedialog
from matplotlib.figure import Figure
from tkinter.filedialog import askopenfile 

import sys
if sys.version_info[0] < 3:
    import Tkinter as Tk
else:
    import tkinter as Tk

root = Tk.Tk()
root.geometry('900x900')
root.wm_title("Flow Direction and Accumulation")
root.configure(background="light blue") 

equation = StringVar()

expression_field = Entry(root, textvariable=equation)

f = ""
canvas = ""
toolbar = ""

# Testing File
dempath = 'test.tiff'
ds = gdal.Open(dempath)
nodata = 0
demdata = ds.GetRasterBand(1).ReadAsArray()
fdir = flowDirectionTestInward(demdata, nodata)
flowto = flowsTo(fdir, nodata)
group1 = firstGroup(flowto, nodata)
fac, group = flowaccum(flowto, group1, nodata)

#Plots
def plotelevation():
    global canvas,toolbar,f

    if canvas != "":
        canvas.get_tk_widget().pack_forget()
    if toolbar != "":
        toolbar.pack_forget()
    if f != "":
        f.destroy()


    fig = Figure(figsize=(8, 6), dpi=100)
    a = fig.add_subplot(111)

    grid,grid.dem=getdem(inputfile_entry.get())

    im=a.imshow(grid.dem, extent=grid.extent, cmap='cubehelix', zorder=1)
    fig.colorbar(im,label='Elevation (m)')
    a.set_title('Digital Elevation Map')
    a.set_xlabel('Longitude')
    a.set_ylabel('Latitude')

    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas.draw()
    canvas.get_tk_widget().pack(side=Tk.TOP, fill=Tk.BOTH, expand=1)

    fig.savefig('result/elevationplot.png') 

    toolbar = NavigationToolbar2Tk(canvas, root)
    toolbar.update()
    canvas._tkcanvas.pack(side=Tk.TOP, fill=Tk.BOTH, expand=1)

def plotdirection():
    global canvas,toolbar,f

    if canvas != "":
        canvas.get_tk_widget().pack_forget()
    if toolbar != "":
        toolbar.pack_forget()
    if f != "":
        f.destroy()

    fig = Figure(figsize=(8, 6), dpi=100)
    a = fig.add_subplot(111)

    dirmap = (64,  128,  1,   2,    4,   8,    16,  32)
    grid,grid.dem=getdem(inputfile_entry.get())
    grid, fdir=flowdirection(dirfile_entry.get(),grid)

    im=a.imshow(fdir, extent=grid.extent, cmap='viridis', zorder=1)
    boundaries = ([0] + sorted(list(dirmap)))
    fig.colorbar(im,boundaries= boundaries, values=sorted(dirmap))
    a.set_title('Flow Direction Grid')
    a.set_xlabel('Longitude')
    a.set_ylabel('Latitude')

    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas.draw()
    canvas.get_tk_widget().pack(side=Tk.TOP, fill=Tk.BOTH, expand=1)
    fig.savefig('result/plotdirection.png')

    toolbar = NavigationToolbar2Tk(canvas, root)
    toolbar.update()
    canvas._tkcanvas.pack(side=Tk.TOP, fill=Tk.BOTH, expand=1)

def plotaccumulation():
    global canvas,toolbar,f

    if canvas != "":
        canvas.get_tk_widget().pack_forget()
    if toolbar != "":
        toolbar.pack_forget()
    if f != "":
        f.destroy()

    fig = Figure(figsize=(8, 6), dpi=100)
    a = fig.add_subplot(111)

    dirmap = (64,  128,  1,   2,    4,   8,    16,  32)
    x, y = -97.294167, 32.73750
    grid,grid.dem=getdem(inputfile_entry.get())
    grid, fdir=flowdirection(dirfile_entry.get(),grid)
    grid, catch=dilineatecatchmant(dirmap,x,y,grid)
    grid, facc=flowaccumulation(grid,dirmap)

    im=a.imshow(facc, extent=grid.extent, zorder=1,cmap='cubehelix', norm=colors.LogNorm(1, grid.acc.max()))
    boundaries = ([0] + sorted(list(dirmap)))
    fig.colorbar(im, label='Upstream Cells')
    a.set_title('Flow Accumulation')
    a.set_xlabel('Longitude')
    a.set_ylabel('Latitude')

    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas.draw()
    canvas.get_tk_widget().pack(side=Tk.TOP, fill=Tk.BOTH, expand=1)
    fig.savefig('result/plotaccumulation.png')

    toolbar = NavigationToolbar2Tk(canvas, root)
    toolbar.update()
    canvas._tkcanvas.pack(side=Tk.TOP, fill=Tk.BOTH, expand=1)

def _clear():
	global f,canvas,toolbar
	if canvas != "":
		canvas.get_tk_widget().pack_forget()
	if toolbar != "":
		toolbar.pack_forget()
	if f != "":
		f.destroy()

	f = ""
	canvas = ""
	toolbar = ""

def _quit():
    root.quit()     
    root.destroy()

inputfile_label = Tk.Label(root, text = 'Dem Data File/Folder',font=('calibre',10, 'bold')) 
inputfile_entry = Tk.Entry(root,font=('calibre',10,'normal'))

inputfile_label.pack(side = Tk.TOP, pady = 0)
inputfile_entry.pack(side = Tk.TOP, pady = 5)

dirfile_label = Tk.Label(root, text = 'Dir Data File/Folder',font=('calibre',10, 'bold')) 
dirfile_entry = Tk.Entry(root,font=('calibre',10,'normal'))

dirfile_label.pack(side = Tk.TOP, pady = 0)
dirfile_entry.pack(side = Tk.TOP, pady = 5)

btn = Button(root, text ='Plot Elevation Data', command = lambda:plotelevation()) 
btn.pack(side = Tk.TOP, pady = 10)

btn = Button(text='Plot Flow Direction', command= lambda: plotdirection())
btn.pack(side = Tk.TOP, pady = 10)  

btn = Button(text='Plot Flow Accumulation', command= lambda: plotaccumulation())
btn.pack(side = Tk.TOP, pady = 10) 

btn = Button(text='Clear', command=lambda:_clear())
btn.pack(side = Tk.BOTTOM)  

button = Tk.Button(master=root, text='Quit', command=_quit)
button.pack(side=Tk.BOTTOM)

Tk.mainloop()

