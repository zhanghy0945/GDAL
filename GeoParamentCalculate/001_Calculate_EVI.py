# EVI = 2.5*(NIR - Red) / (NIR + 6*Red - 7.5*Blue + 1)
# 一是练习逐渐使用Pandas处理数据
#二是写EVI的算法

import os, glob
from osgeo import gdal
import numpy as np
import pandas as pd

def evi_calcul (pathin, pathout):

    fname_list = os.listdir(pathin)
    bands = {
        'B8' : None,
        'B4' : None,
        'B3' : None,
        'B2' : None
        }
    
    for fname in fname_list:
        if fname[-4:] == ".tif" and "B8" in fname:
            bands['B8'] = os.path.join(pathin, fname)
        if fname[-4:] == ".tif" and "B4" in fname:
            bands['B4']= os.path.join(pathin, fname)
        if fname[-4:] == ".tif" and "B3" in fname:
            bands['B3'] = os.path.join(pathin, fname)
        if fname[-4:] == ".tif" and "B2" in fname:
            bands['B2'] = os.path.join(pathin, fname)


    b8_data = gdal.Open(bands['B8'], gdal.GA_ReadOnly)
    b4_data = gdal.Open(bands['B4'], gdal.GA_ReadOnly)
    b3_data = gdal.Open(bands['B3'], gdal.GA_ReadOnly)
    b2_data = gdal.Open(bands['B2'], gdal.GA_ReadOnly)

    b8_band = b8_data.GetRasterBand(1)
    b4_band = b4_data.GetRasterBand(1)
    b3_band = b3_data.GetRasterBand(1)
    b2_band = b2_data.GetRasterBand(1)

    transform = b8_data.GetGeoTransform()
    projection = b8_data.GetProjection()
    data_xsize = b8_band.XSize
    data_ysize = b8_band.YSize

    print (data_xsize, data_ysize)

    b8_array = b8_band.ReadAsArray()
    b4_array = b4_band.ReadAsArray()
    b3_array = b3_band.ReadAsArray()
    b2_array = b2_band.ReadAsArray()
    print (b8_array)

    b8_band = b8_array.astype(np.float32)
    b4_band = b4_array.astype(np.float32)
    b3_band = b3_array.astype(np.float32)
    b2_band = b2_array.astype(np.float32)

    
    evi_name = os.path.join(pathout, "EVI.tif")
    driver_type = gdal.GetDriverByName('Gtiff')
    evi_driver = driver_type.Create(evi_name, data_xsize, data_ysize, 1, gdal.GDT_Float32)
    evi_driver.SetGeoTransform(transform)
    evi_driver.SetProjection(projection)


    # EVI = 2.5*(NIR - Red) / (NIR + 6*Red - 7.5*Blue + 1)

    #one_matrix = np.ones(data_xsize, data_ysize).reshape()
    #print (one_matrix)
    L = 2.5,
    c1 = 6,
    c2 = 7.5
    G = 2.5
    # first_cal = 2.5 * ( b8_array - b4_array )
    # second_cal =  6 * b4_array  - 7.5 * b2_array 
    # third_cal = b8_array + second_cal + 1
    # evi_cal = first_cal / third_cal
    evi1 = b8_array + (c1 * b4_array) - (c2 * b2_array) + L
    evi = np.where(evi1 != 0, G * ((b8_array - b4_array)/ evi1), np.nan)


    evi_band = evi_driver.GetRasterBand(1)
    evi_band.WriteArray(evi)
    evi_band.SetNoDataValue(np.nan)
    evi_driver.FlushCache()

    del evi_driver
    del b8_data
    del b4_data
    del b3_data
    del b2_data
    print(f"EVI 计算完成，输出文件保存在: {evi_name}")

if __name__ == "__main__":
    pathin = r"E:\data\001_compositeAndVI\JiaYuGuan"
    pathout = r"E:\data\001_compositeAndVI\EVI"
    evi_calcul (pathin, pathout)







    
                          




 
    


        


