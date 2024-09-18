import os, glob
from osgeo import gdal
import numpy as np
import pandas as pd


pathin = r"F:\LULC_Article\Sentinel-2_2020_origin\PingLiang"
datalist = os.listdir(pathin)
for data in datalist:
    print (data, type(data))
    dataori = pathin + '/' + data
    print (dataori)
    dataset = gdal.Open(dataori)
    print (dataset, type(dataset))

    # 获取图像的基本信息， 两种方法都可行
    #print("Driver: {}/{}".format(dataset.GetDriver().ShortName, dataset.GetDriver().LongName))
    

    data_exteninfo = dataset.GetDriver().ShortName, dataset.GetDriver().LongName
    print ("<<<------------------- data name is ------------------->>> ")
    print (data_exteninfo)
    data_sizeinfo = dataset.RasterXSize, dataset.RasterYSize, dataset.RasterCount
    print ("<<<------------------- data size is ------------------->>> ")
    print (data_sizeinfo)
    data_projection = dataset.GetProjection()
    print ("<<<------------------- data projection is ------------------->>> ")
    print (data_projection, type(data_projection))
    data_geotransform = dataset.GetGeoTransform()
    print ("<<<------------------- data geotransform is ------------------->>> ")
    print (data_geotransform, type(data_geotransform))

    '''#读取一个块
    dataset_band = dataset.GetRasterBand(1)
    read_block= dataset_band.ReadRaster(xoff = 0, yoff = 0,
                                        xsize = 1400, ysize = 1400,
                                        buf_xsize = 1400, buf_ysize = 1400,
                                        buf_type = gdal.GDT_Float64)
    print ("<<<------------------- read_block is ------------------->>> ")
    print (read_block)

    float_block = np.frombuffer(read_block, dtype = np.float64)
    float_block = float_block.reshape((1400, 1400))
    df_block = pd.DataFrame(float_block)
    print (df_block)'''
    #读取整个图像
    dataset_band = dataset.GetRasterBand(1)
    dataset_all = dataset_band.ReadRaster(xoff = 0, yoff = 0,
                                     xsize = dataset_band.XSize, ysize = dataset_band.YSize,
                                     buf_xsize = dataset_band.XSize, buf_ysize = dataset_band.YSize,
                                     buf_type = gdal.GDT_CFloat64)
    float_all = np.frombuffer(dataset_all, dtype = np.float64)  
    print (dataset_all) 
    print ("<<<------------------- dataset_all is ------------------->>> ")
    print (float_all)





    
    

