import os 
import numpy as np
from osgeo import gdal

def make_raster (in_ds, fn, data, data_type, nodata = None):
    driver = gdal.GetDriverByName("GTiff") #确定栅格数据的格式
    out_ds = driver.Create(fn, in_ds.RasterXSize, in_ds.RasterYSize, 1, data_type)#创建栅格数据的基础信息
    out_ds.SetProjection(in_ds.GetProjection())#设置输出影像的投影信息，保持和输入图像的信息一致
    out_ds.GetGeoTransform(in_ds.GetGeoTransform())#设置输出影像的坐标信息，保持与输入图像的一致
    out_band = out_ds.GetRasterBand(1)
    
    if nodata is not None:
        out_band.SetNodataValue(nodata)
        out_band.FlushCache()
        out_band.ComputeStatistics(False)
        return out_ds