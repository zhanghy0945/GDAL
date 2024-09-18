#字节序列重采样
import os
import numpy as np
from osgeo import gdal
print ("Check really!")

def byte_series(pathin, pathout): #定义一个函数，
    in_datas = os.listdir(pathin)
    for in_data in in_datas:
        if in_data[:] == "nat_color.tif":
            print (in_data)
            in_data1 = pathin + "/" + "nat_color.tif"
    in_ds = gdal.Open(in_data1)
    out_rows = int(in_ds.RasterYSize / 2)
    out_columns = int(in_ds.RasterXSize / 2)
    num_bands = in_ds.RasterCount
    
    out_name = pathout + "/" + "nat_color_resampled.tif"
    gtiff_driver = gdal.GetDriverByName("GTiff")
    out_ds = gtiff_driver.Create (out_name, out_columns, out_rows, num_bands)
    out_ds.SetProjection(in_ds.GetProjection())
    geotransform = list(in_ds.GetGeoTransform())
    geotransform[1] *= 2
    geotransform[5] *= 2
    out_ds.SetGeoTransform(geotransform)
    data = in_ds.ReadRaster(buf_xsize = out_columns, buf_ysize = out_rows)
    out_ds.WriteRaster(0, 0, out_columns, out_rows, data)
    out_ds.FlushCache()
    
    for i in range(num_bands):
        out_ds.GetRasterBand(i + 1).ComputeStatistics(False)
    out_ds.BuildOverviews("avarage", [2, 4, 8, 16])
    del out_ds
if __name__ == "__main__":
    pathin = r"E:\osgeopy-data\osgeopy-data-landsat-washington-nat-color\osgeopy-data\Landsat\Washington"
    pathout = r"E:\osgeopy-data\osgeopy-data-landsat-washington-nat-color\osgeopy-data\Landsat\Washington"
    byte_series(pathin, pathout)
    
            