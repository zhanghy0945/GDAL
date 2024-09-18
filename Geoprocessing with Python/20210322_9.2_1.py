import os 
import numpy as np
from osgeo import gdal

a = []
def read_tiff( pathin):
    path = os.chdir(pathin) #改变工作目录到当前路径，这是初次编写时必须的步骤
    fn_names = os.listdir(pathin)
    for fn_name in fn_names:
        if fn_name[:] == "gt30w140n90.tif":
            #print (fn_name)
            in_ras = gdal.Open(fn_name)
            a.append(in_ras)
    for a_a in a:        
        print (a_a)
    in_ds = a[0]
    print ('First band is: ',a[0])
    in_band = in_ds.GetRasterBand(1)
    xsize = in_band.XSize
    ysize = in_band.YSize
    print (xsize,ysize)
    block_xsize,block_ysize = in_band.GetBlockSize()
    nodata = in_band.GetNoDataValue()
    print (block_xsize,block_ysize,nodata)
    
    out_ds = in_ds.GetDriver().Create('DEM_feet1.tif',xsize,ysize,1,in_band.DataType)
    out_ds.SetProjection(in_ds.GetProjection())
    out_ds.SetGeoTransform(in_ds.GetGeoTransform())
    out_band = out_ds.GetRasterBand(1)
    
    for x in range(0, xsize, block_xsize):
        if x + block_xsize < xsize:
            cols = block_xsize
        else:
            cols = xsize - x
        for y in range(0, xsize, block_ysize):
            if y + block_ysize < ysize:
                rows = block_ysize
            else:
                rows = ysize - y
            data = in_band.ReadAsArray(x, y, cols, rows)
            data = np.where(data == nodata, nodata, data * 3.28084)
            out_band.WriteArray(data, x, y)
            
    out_band.FlushCache()
    #out_band.SetNoDataValue(nodata)
    out_band.ComputeStatistics(False)
    #out_ds.BuildOverViews('average', [2, 4, 6, 8, 16, 32])
    del out_ds
if __name__ == "__main__":
    pathin = r"E:\osgeopy-data\osgeopy-data-washington\Washington\dem"
    read_tiff (pathin)