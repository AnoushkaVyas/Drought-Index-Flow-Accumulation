import os
import numpy as np
import matplotlib 
import matplotlib.pyplot as plt

from osgeo import gdal
from shapely.geometry import shape

dem_path = 'test.tiff'
gdal_data = gdal.Open(dem_path)
gdal_band = gdal_data.GetRasterBand(1)
nodataval = gdal_band.GetNoDataValue()

data_array = gdal_data.ReadAsArray().astype(np.float)
if np.any(data_array == nodataval):
    data_array[data_array == nodataval] = np.nan

# Plot out data with Matplotlib's 'contour'
fig = plt.figure(figsize = (12, 8))
ax = fig.add_subplot(111)
plt.contour(data_array, cmap = "viridis", 
            levels = list(range(0, 500, 10)))
plt.title("")
cbar = plt.colorbar()
plt.gca().set_aspect('equal', adjustable='box')
plt.show()
