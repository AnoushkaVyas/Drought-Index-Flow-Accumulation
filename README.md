# Flow Accumulation Project and Drought Identification Tool

## Team 10 Members
- Gaurav Batra 20171114
- Vani Sancheti 20171179
- Mudit Agarwal 20171090
- Dhruv Chauhan 20161123
- Anoushka Vyas 20171057

## How To Run
```
- python3 combined_tool.py
- Click on any one tool
```

## Calculation of Flow Accumulation and Direction

### Algorithm:
Flow directions are computed from a source DEM. The flow direction grid captures the topology of the drainage network. Flow directions are calculated using the D8 routing scheme. In this routing mode, each cell is routed to one of eight neighboring cells based on the direction of steepest descent.

DEMs should be conditioned before computing flow directions. In other words, depressions should be filled and flats should be resolved. We did this using inbuilt pysheds library.

Cardinal and intercardinal directions are represented by numeric values in the output grid. By default, the ESRI scheme is used. 

The Flow Accumulation tool calculates accumulated flow as the accumulated weight of all cells flowing into each downslope cell in the output raster. If no weight raster is provided, a weight of 1 is applied to each cell, and the value of cells in the output raster is the number of cells that flow into each cell.

The results of Flow Accumulation can be used to create a stream network by applying a threshold value to select cells with a high accumulated flow.

### Libraries used:

- pysheds (pip install pysheds)
- gdal (pip install GDAL)
- osgeo (pip install GDAL)

### Input:
- The program uses digital elevation data in the form of dem file.
- The dem data for the country of USA.
- Select the input folder using by typing `dem_data` in the `Dem Data File/Folder`.
- Select the input direction folder using by typing `dir_data` in the `Dir Data File/Folder`.

### Plot:
- Plot the Elevation Data by clicking on `Plot Elevation Data`.
- Plot the Flow Direction by clicking on `Plot Flow Direction`.
- Plot the Flow Accumulation by clicking on `Plot Flow Accumulation`.

### Miscellaneous Buttons:
#### Clear
- It is used to clear the screen.

#### Quit
- It is used to quit the program.

### Dataset
- Link: https://drive.google.com/drive/folders/1PtW9Vr1f4et6cXLQ5XaXb3gUBZrjnijt?usp=sharing
- Download `dem_data` and `dir_data` folders in the `Project` directory.

## Calculation of SPI

### Libraries used:

- climate-indices (pip install climate-indices)
- basemap (conda install basemap)

### Input:
- The program uses precipitation data in .nc file format.
- It is present in the data folder. 
- The data is precipitation data for the country of USA.
- Select the input file using `Open Input file` button.

### Output:
- We can get daily/monthly spi calculation spanning over days as specified.
- Just click on `Generate SPI` after selecting the input file.
- It will dump the output files in the output folder. (It might take some time).

### Plot:
- Click on Show SPI plot button to plot the SPI output generated in the `output` folder.

### Miscellaneous Buttons:
#### Clear
- It is used to clear the screen.

#### Quit
- It is used to quit the program.
