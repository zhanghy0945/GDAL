import os, glob
from osgeo import gdal
import numpy as np 
import pandas as pd

bands = {
    "B8" : None,
    "B3" : None,
    "B2" : None
}
pathin = r"E:\Python\data\001_compositeAndNDVI\JiaYuGuan"
pathout = r"E:\Python\data\001_compositeAndNDVI\NDVI"
data_list = os.listdir(pathin)
for in_file in data_list:
    if in_file.endswith('tif') is True:
        if "B8" in in_file:
            bands['B8'] = os.path.join(pathin, in_file)
            print (in_file)
        if "B4" in in_file:
            bands['B4'] = os.path.join(pathin, in_file)
            print (in_file)
        if "B3" in in_file:
            bands['B3'] = os.path.join(pathin, in_file)
            print (in_file)
        if "B2" in in_file:
            bands['B2'] = os.path.join(pathin, in_file)

b8_data = gdal.Open(bands["B8"], gdal.GA_ReadOnly)
b4_data = gdal.Open(bands["B4"], gdal.GA_ReadOnly)
b3_data = gdal.Open(bands["B3"], gdal.GA_ReadOnly)
b2_data = gdal.Open(bands["B2"], gdal.GA_ReadOnly)


geotransform = b8_data.GetGeoTransform()
geoprojection = b8_data.GetProjection()
print (geotransform)
print (geoprojection)
xsize = b4_data.RasterXSize
ysize = b4_data.RasterYSize
print (xsize, ysize)

b8_band = b8_data.GetRasterBand(1).ReadAsArray()
b4_band = b4_data.GetRasterBand(1).ReadAsArray()
b3_band = b3_data.GetRasterBand(1).ReadAsArray()
b2_band = b2_data.GetRasterBand(1).ReadAsArray()
nodata = b8_data.GetRasterBand(1).GetNoDataValue()
print (nodata)

b4_band = b4_band.astype(np.float32)
b3_band = b3_band.astype(np.float32)
b2_band = b2_band.astype(np.float32)

# 检查波段数据的最大值和最小值
print("B8 min/max:", np.min(b8_band), np.max(b8_band))
print("B4 min/max:", np.min(b4_band), np.max(b4_band))


out_name = os.path.join(pathout, 'Sentinel2_2021NDVI_JiaYuGuan.tif')
out_driver = gdal.GetDriverByName('Gtiff')
out_data = out_driver.Create(out_name, xsize, ysize, 1, gdal.GDT_Float32)
out_data.SetGeoTransform(geotransform)
out_data.SetProjection(geoprojection)


add_band = np.add(b8_band, b4_band)
sub_band = np.subtract(b8_band, b4_band)

ndvi = np.divide(sub_band, add_band)

out_band = out_data.GetRasterBand(1)
out_band.WriteArray(ndvi)
out_band.SetNoDataValue(np.nan)

del out_data










        
        



