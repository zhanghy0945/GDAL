#!/usr/bin/env python
# coding: utf-8

import os 
import numpy as np
from osgeo import gdal


def read_tiff( pathin):
    path = os.chdir(pathin) #改变工作目录到当前路径，这是初次编写时必须的步骤
    fn_name = "ASTGTM2_N34E103_dem.tif"
    in_ds = gdal.Open(fn_name)
    print ('First band is: ',in_ds)
    in_band = in_ds.GetRasterBand(1)
    xsize = in_band.XSize
    ysize = in_band.YSize
    print (xsize,ysize)
    block_xsize,block_ysize = in_band.GetBlockSize()
    nodata = in_band.GetNoDataValue()
    print ('block_xsize,block_ysize,nodata', '\n', block_xsize,block_ysize,nodata)
    
    out_ds = in_ds.GetDriver().Create('DEM_feet1.tif',xsize,ysize,1,in_band.DataType)
    out_ds.SetProjection(in_ds.GetProjection())
    out_ds.SetGeoTransform(in_ds.GetGeoTransform())
    out_band = out_ds.GetRasterBand(1)
    
    for x in range(0, xsize, block_xsize): #列
        if x + block_xsize < xsize:
            cols = block_xsize
            print (cols)
        else:
            cols = xsize - x
            print ("else: ",cols)
        for y in range(0, ysize, block_ysize): #行
            if y + block_ysize < ysize:
                rows = block_ysize
                print (rows)
            else:
                rows = ysize - y
                print ("else: ",rows)
            data = in_band.ReadAsArray(x, y, cols, rows)
            data = np.where(data == nodata, nodata, data * 3.28084) #米转化为英尺，用Numpy的where函数处理
            out_band.WriteArray(data, x, y)
            
    out_band.FlushCache()
    #out_band.SetNoDataValue(nodata)
    out_band.ComputeStatistics(False)
    #out_ds.BuildOverViews('average', [2, 4, 6, 8, 16, 32])
    del out_ds
if __name__ == "__main__":
    pathin = r"F:\Python_jupyter\GDAL_practice_Data\9.3"
    read_tiff (pathin)





