# read date each block
# 20230913
import os
import numpy as np
from osgeo import gdal
#print ("OK!")

os.chdir(r"E:\osgeopy-data\osgeopy-data-washington\Washington\dem")
in_ds = gdal.Open("gt30w140n90.tif")
in_band = in_ds.GetRasterBand(1)

xsize = in_band.XSize
ysize = in_band.YSize
block_xsize, block_ysize = in_band.GetBlockSize() #获取初始的块
nodata = in_band.GetNoDataValue()

out_ds = in_ds.GetDriver().Create("dem_feet_2.tif", xsize, ysize, 1, in_band.DataType)
#这一句是创建一个按块读取后的栅格的格式：数据名，列长度，行长度，内涵波段数，数据类型
out_ds.SetProjection(in_ds.GetProjection())
out_ds.SetGeoTransform(in_ds.GetGeoTransform())
out_band = out_ds.GetRsterBand(1) #获取out_ds的第一波段，进行下一步的处理

for x in range(0, xsize, block_xsize):  # block_xsize为增量，每次遍历多少行
    if x + block_xsize < xsize:
        cols = block_xsize
    else:
        cols = xsize - x
    for y in range(0, ysize, block_ysize):
        if y + block_ysize < ysize:
            rows = block_ysize
        else:
            rows = ysize - y
        data  = in_band.ReadAsArray(x, y, cols, rows) #从x列开始读取，从y行开始读取吗，读从cols列，rows列。
        data = np.where(data == nodata, nodata, data * 3.28084)
        out_band.WriteArray(data, x, y)

out_band.FlushCache()
out_band.SetNodataValue(nodata)
out_band.ComputeStatistics(False)
out_ds.BuildOverviews("avarage", [2, 4, 8, 16, 32])
del out_ds
    


    
