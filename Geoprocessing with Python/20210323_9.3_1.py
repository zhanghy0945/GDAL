#!/usr/bin/env python
# coding: utf-8

# In[17]:


import os
from osgeo import gdal

def read_srs(pathin):
    path = os.chdir(pathin)
    fn_names = os.listdir(pathin)
    for fn_name in fn_names:
        print (fn_name)
    in_ds = gdal.Open(fn_name)
    cols = in_ds.RasterXSize
    rows = in_ds.RasterYSize
    print ('cols = ', cols, 'rows = ', rows)
    in_band = in_ds.GetRasterBand(1)
    xsize = in_band.XSize
    ysize = in_band.YSize
    proj = in_ds.GetProjection()
    transf = in_ds.GetGeoTransform()#[1]
    
    data = in_band.ReadAsArray(0, 0, cols, rows)
    print (xsize, '\n',  ysize)
    print ('--------------------------------')
    print (proj)
    print ('--------------------------------')
    print (transf)
    print ('--------------------------------')
    print (data)
    
if __name__ == "__main__":
    pathin = r"F:\Python_jupyter\GDAL_practice_Data\9.3_2"
    read_srs(pathin)


# In[2]:


s = [0.1, 1.2, 2.6, 3.9, 4.1, 5.2, 6.5, 7.8, 8.4, 9.6]
for i in s:
    x = map(int, i)
    print (x)


# In[ ]:




