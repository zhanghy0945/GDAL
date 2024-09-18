#!/usr/bin/env python
# coding: utf-8

# In[9]:


#数据位置 Vashon Island

import os 
from osgeo import gdal

def transform_cov(pathin,pathout):
    vashon_ulx, vashon_uly = 532000, 5262600
    vashon_lrx, vashon_lry = 548500, 5241500
    
    work_path = os.chdir(pathin)
    fn_names = os.listdir(pathin)
    for fn_name in fn_names:
        print ('File name is: ',fn_name)
    print ('---------------------------------')
    in_ds = gdal.Open(fn_name)
    print (in_ds)
    in_gt = in_ds.GetGeoTransform()
    
    inv_gt = gdal.InvGeoTransform(in_gt)
    ''''if gdal.VersionInfo()[0] =="1":
        if unv_gt[0] == 1:
            inv_gt = inv_gt[1]
        else:
            raise RuntimeError('Inverse geotramsform failed')
    elif inv_gt is None:
        raise RuntimeError('Inverse geotramsform failed')'''
        
    offsets_ul = gdal.ApplyGeoTransform(inv_gt, vashon_ulx, vashon_uly)
    offsets_lr = gdal.ApplyGeoTransform(inv_gt, vashon_lrx, vashon_lry)
    
    off_ulx, off_uly = map(int,offsets_ul)
    off_lrx, off_lry = map(int,offsets_lr)
    
    rows = off_lry - off_uly
    columns = off_lrx - off_ulx
    
    gtiff_driver = gdal.GetDriverByName('GTiff')
    out_name = os.path.join(pathout, 'vashon4.tif')
    out_ds = gtiff_driver.Create(out_name, columns, rows, 3)
    out_ds.SetProjection(in_ds.GetProjection())
    subset_ulx, subset_uly = gdal.ApplyGeoTransform(in_gt, off_ulx, off_lry)
    out_gt = list(in_gt)
    out_gt[0] = subset_ulx
    out_gt[3] = subset_uly
    out_ds.SetGeoTransform(out_gt)
    
    for i in range(1,4):
        in_band = in_ds.GetRasterBand(i)
        out_band = out_ds.GetRasterBand(i)
        data = in_band.ReadAsArray(off_ulx, off_uly, columns, rows)
        out_band.WriteArray(data)
        
    del out_ds

if __name__ == "__main__":
    pathin = r"F:\Python_jupyter\GDAL_practice_Data\9.3_2"
    pathout = r"F:\Python_jupyter\GDAL_practice_Data\9.3_2"
    transform_cov(pathin,pathout)
    
    
    


# In[ ]:


for i in range(1,4):
    print (i)


# In[ ]:





# In[ ]:




