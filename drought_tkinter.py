import matplotlib 
matplotlib.use('TkAgg')
from tkinter import * 
from tkinter.ttk import *
from tkinter import filedialog
from tkinter.filedialog import askopenfile 
from numpy import arange, sin, pi
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.backend_bases import key_press_handler
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
import pandas as pd
import numpy as np
import pickle
from tkinter import messagebox
import os
from netCDF4 import Dataset as NetCDFFile 
from mpl_toolkits.basemap import Basemap
from tkinter import simpledialog,messagebox



import sys
if sys.version_info[0] < 3:
    import Tkinter as Tk
else:
    import tkinter as Tk

root = Tk.Tk()
root.geometry('900x900')
root.wm_title("Standardized Precipitation Index Calculation")
root.configure(background="light green") 

equation = StringVar()

expression_field = Entry(root, textvariable=equation) 

input_file_name = ""
output_file_name = ""
canvas = ""
toolbar = ""
scale = ""

def open_file():
    global input_file_name

    file = askopenfile(mode ='r', filetypes =[('Nc Files', '*.nc')])

    if file is not None:
        input_file_name = file.name


def Generate():
    global input_file_name,output_file_name,scale

    if input_file_name == "":
        messagebox.showinfo("Error", "First Select an Input File")
        return


    scale = simpledialog.askstring("Scale", "Number of Days", parent = root)
    timeline = simpledialog.askstring("Daily/Monthly", "Enter D/M",parent = root)

    if timeline == "D":
        times = "daily"
    elif timeline == "M":
        times = "monthly"
    else:
    	messagebox.showinfo("Error", "Invalid Input")

    os.system('process_climate_indices --index spi  --periodicity '+str(times)+' --netcdf_precip '+str(input_file_name)+' --var_name_precip prcp --output_file_base ./output/ --scales '+str(scale)+' --calibration_start_year 1998 --calibration_end_year 2016 --multiprocessing all')

    
def showPlot():
    global canvas,toolbar,output_file_name,scale



    if canvas != "":
        canvas.get_tk_widget().pack_forget()
    if toolbar != "":
        toolbar.pack_forget()

    output_file_name = askopenfile(mode ='r', filetypes =[('Nc Files', '*.nc')]).name
    nc = NetCDFFile(output_file_name)

    lat = nc.variables['lat'][:]
    lon = nc.variables['lon'][:]
    time = nc.variables['time'][:]
    print(str(output_file_name[output_file_name.find("spi"):-3]))
    t2 = nc.variables[str(output_file_name[output_file_name.find("spi"):-3])][:]

    lon_0 = lon.mean()
    lat_0 = lat.mean()

    fig,a = plt.subplots(1,1)


    m = Basemap(ax=a,projection='mill',lat_ts=10,llcrnrlon=lon.min(), \
      urcrnrlon=lon.max(),llcrnrlat=lat.min(),urcrnrlat=lat.max(), \
      resolution='c')

    lon, lat = np.meshgrid(lon, lat)
    xi, yi = m(lon, lat)

    # Plot Data
    cs = m.pcolor(xi,yi,t2.mean(axis = 2))

    # Add Grid Lines
    m.drawparallels(np.arange(-80., 81., 10.), labels=[1,0,0,0], fontsize=10)
    m.drawmeridians(np.arange(-180., 181., 10.), labels=[0,0,0,1], fontsize=10)

    # Add Coastlines, States, and Country Boundaries
    m.drawcoastlines()
    m.drawstates()
    m.drawcountries()

    # Add Colorbar
    cbar = m.colorbar(cs, location='bottom', pad="10%")
    # cbar.set_label(tmax_units)

    # Add Title
    

    # plt.show()

    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas.draw()
    canvas.get_tk_widget().pack(side=Tk.TOP, fill=Tk.BOTH, expand=1)

    toolbar = NavigationToolbar2Tk(canvas, root)
    toolbar.update()
    canvas._tkcanvas.pack(side=Tk.TOP, fill=Tk.BOTH, expand=1)





def _clear():
    global f,canvas,toolbar

    if canvas != "":
        canvas.get_tk_widget().pack_forget()
    canvas = ""

    if toolbar != "":
        toolbar.pack_forget()

    canvas = ""
    toolbar = ""

btn = Button(root, text ='Open Input File', command = lambda:open_file()) 
btn.pack(side = Tk.TOP, pady = 8)

btn = Button(root, text ='Generate SPI Output File', command = lambda:Generate()) 
btn.pack(side = Tk.TOP, pady = 8)


btn = Button(root, text ='Show SPI Plot', command = lambda:showPlot()) 
btn.pack(side = Tk.TOP, pady = 8)


btn = Button(text='Clear', command=lambda:_clear())
btn.pack(side = Tk.TOP, pady = 8)  



def _quit():
    root.quit()     
    root.destroy()

button = Tk.Button(master=root, text='Quit', command=_quit)
button.pack(side=Tk.BOTTOM)

Tk.mainloop()


