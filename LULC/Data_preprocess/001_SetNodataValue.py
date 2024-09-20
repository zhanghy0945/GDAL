import os, glob
from osgeo import gdal
from osgeo import osr
import numpy as np
import pandas as pd 
from numpy import nan as NA

pathin =  r"F:\LULC_Article\2019\Sentinel-2_2019_origin\LanZhou"
pathout = r"F:\LULC_Article\2019\Sentinel-2_2019_process\LanZhou"
filelist = os.listdir(pathin)
print (filelist)
for filename in filelist:
    if filename[-4:] == '.tif':
        print (filename)
        indatapath= pathin + "/" + filename
        outdatapath = pathout + "/" + filename
        #outdatapath = pathout + '/' + filename.split('.')[0] + "1" + ".tif"
        indataset = gdal.Open(indatapath)
        print (indataset, type(indataset))
#-------------------------------------- in dataset setting-----------------------------
        metadata = indataset.GetMetadata()
        print (metadata)
        geotransform = indataset.GetGeoTransform()
        projection = indataset.GetProjection()
        print ("projection is: ", projection)
        print (geotransform)
        originX = geotransform[0]
        originY = geotransform[3]
        pixelWidth = geotransform[1]
        pixelHeight = geotransform[5]
        cols = indataset.RasterXSize
        rows = indataset.RasterYSize
        print (cols, rows)

        in_band = indataset.GetRasterBand(1)
        in_nodatavalue = in_band.GetNoDataValue()
        print ("nodata value == ", in_nodatavalue, "\n nodata value's type is: ", type(in_nodatavalue))
        inBand_Array = in_band.ReadAsArray()
        inBand_Array[inBand_Array == 0] = np.nan


       # data_setnull = np.where(inBand_Array == 0, np.nan, inBand_Array) #把nodata赋值为-999
        print (inBand_Array [2356, 1526])

#--------------------------------------out dataset setting------------------------------
        outband_driver = gdal.GetDriverByName('GTiff')
        outdataset = outband_driver.Create(outdatapath, cols, rows, 1, gdal.GDT_Float32)

        outdataset.SetGeoTransform(geotransform)
        outdataset.SetProjection(projection)

        out_band = outdataset.GetRasterBand(1)
        out_band.SetNoDataValue(np.nan)
        out_band.WriteArray(inBand_Array)
        out_band.FlushCache()

        in_band1 = out_band.ReadAsArray()
        print (in_band1)

        print ("--------------------------------------all is ready!------------------------------")
        
        del in_band
        del out_band
        del indataset
        del outdataset



        
        






        




    

