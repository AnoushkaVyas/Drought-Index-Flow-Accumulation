from osgeo import ogr, gdal

shape_file = 'test.shp'
output_raster = 'test.tiff'

input_shp = ogr.Open(shape_file)
shp_layer = input_shp.GetLayer()

pixel_size = 0.01
xmin, xmax, ymin, ymax = shp_layer.GetExtent()

ds = gdal.Rasterize(output_raster, shape_file, xRes=pixel_size, yRes=pixel_size, 
                    burnValues=255, outputBounds=[xmin, ymin, xmax, ymax], 
                    outputType=gdal.GDT_Byte)
ds = None
