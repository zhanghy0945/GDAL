#!/usr/bin/env python
# coding: utf-8

# In[2]:


import os
from osgeo import gdal #导入GDAL模块

path = r"F:\Python_jupyter\GDAL_practice_Data\9.2"
os.chdir(path)
band1_fn = "LC08_L1TP_122044_20171023_20171107_01_T1_B3.TIF"
band2_fn = "LC08_L1TP_122044_20171023_20171107_01_T1_B4.TIF"
band3_fn = "LC08_L1TP_122044_20171023_20171107_01_T1_B5.TIF"

in_ds = gdal.Open(band1_fn) #打开Geotiff波段
in_band = in_ds.GetRasterBand(1) #获取数据集的第一波段
gtiff_driver = gdal.GetDriverByName('GTiff') #create tiff driver

# 创建栅格Gtiff的驱动对象或者说是创建输出对象的阐述
out_ds = gtiff_driver.Create('nat_color_543_3.tif',in_band.XSize, in_band.YSize, 3, in_band.DataType)
out_ds.SetProjection(in_ds.GetProjection()) #设置输出数据的投影
out_ds.SetGeoTransform(in_ds.GetGeoTransform()) #（仿射变换）读取输出数据的仿射变换参数，原点坐标等

in_data = in_band.ReadAsArray() #把栅格数据读进一个二维数组（Numpy数组）
out_band = out_ds.GetRasterBand(3)
out_band.WriteArray(in_data) 

in_ds = gdal.Open(band2_fn)
out_band = out_ds.GetRasterBand(2)
out_band.WriteArray(in_ds.ReadAsArray())

out_ds.GetRasterBand(1).WriteArray(gdal.Open(band3_fn).ReadAsArray())

out_ds.FlushCache()
for i in range(1,4):
    out_ds.GetRasterBand(i).ComputeStatistics(False)
    
    out_ds.BuildOverviews('Nearest', [2,4,8,16,24,32])
    
del out_ds


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:




