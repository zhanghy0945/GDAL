#!/usr/bin/env python
# coding: utf-8

# In[7]:


import os
from osgeo import gdal

def resample_tiff(pathin, pathout):
    path = os.chdir(pathin)
    fn_names = os.listdir(pathin)
    for fn_name in fn_names:
        if fn_name[-4:] == ".tif":
            print (fn_name)
    in_ds = gdal.Open(fn_name)
    print (in_ds)
    in_band = in_ds.GetRasterBand(1)
    out_rows = in_band.YSize
    out_cols = in_band.XSize
    
    gtiff_driver = gdal.GetDriverByName('Gtiff')
    out_ds = gtiff_driver.Create('band1_resample1.tif', out_cols, out_rows)
    out_ds.SetProjection(in_ds.GetProjection())
    geotransform = list(in_ds.GetGeoTransform())
    geotransform[1] /= 2           #相当于：x /=2,即：x = x/2
    geotransform[5] /= 2
    out_ds.SetGeoTransform(geotransform)
    
    data = in_band.ReadAsArray(buf_xsize = out_cols, buf_ysize = out_rows)
    out_band = out_ds.GetRasterBand(1)
    out_band.WriteArray(data)
    
    out_band.FlushCache()
    out_band.ComputeStatistics(False)
    out_ds.BuildOverviews('average', [2, 4, 8, 16, 32, 64, 128, 256])
    
    del out_ds
    
if __name__ == "__main__":
    pathin = r"F:\Python_jupyter\GDAL_practice_Data\result"
    pathout = r"F:\Python_jupyter\GDAL_practice_Data\9.4"
    resample_tiff(pathin, pathout)


# In[ ]:




