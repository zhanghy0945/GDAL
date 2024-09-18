import os
import numpy as np 
from osgeo import gdal


os.chdir(r"E:\osgeopy-data\osgeopy-data-switzerland")
original_ds = gdal.Open("dem_class.tif")
print (original_ds)
driver = gdal.GetDriverByName("gtiff")
ds = driver.CreateCopy("dem_class2.tif", original_ds)
print ("---------------------------------------")
band = ds.GetRasterBand(1)
colors = gdal.ColorTable()
colors.SetColorEntry(1, (112, 153, 89))
colors.SetColorEntry(2, (242, 238, 162))    
colors.SetColorEntry(3, (242, 206, 133)) 
colors.SetColorEntry(4, (194, 140, 124))     
colors.SetColorEntry(5, (214, 193, 156))      
print ("-----------------------------------------")
    
band.SetRasterColorTable(colors)
band.SetRasterColorInterpretation(gdal.GCI_PaletteIndex)  
    
del band, ds

