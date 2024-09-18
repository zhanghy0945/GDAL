import os 
import numpy as np
from osgeo import gdal

vashon_ulx, vashon_uly = 532000, 5262600
vashon_lrx, vashon_lry = 548000, 5241500

os.chdir(r'E:\test\2014')
in_ds = gdal.Open('201401_mean_LAI.tif')
in_gt = in_ds.GetGeoTransform()
inv_gt = gdal.InvGeoTransform(in_gt)

offsets_ul = gdal.ApplyGeoTransform(inv_gt, vashon_ulx, vashon_uly)
offsets_lr = gdal.ApplyGeoTransform(inv_gt, vashon_lrx, vashon_lry)

off_ulx, off_uly = map(int, offsets_ul)
off_lrx, off_lry = map(int, offsets_lr)

rows = off_lry - off_uly
columns = off_lrx - off_ulx

gtiff_driver = gdal.GetDriverByName('GTiff')
out_ds = gtiff_driver.Create('vashon2.tif', columns, rows,3)
subset_ulx, subset_uly = gdal.ApplyGeoTransform(in_gt, off_ulx, off_uly)
out_gt = list(in_gt)
out_gt[0] = subset_uly
out_gt[3] = subset_uly
out_ds.SetGeoTransform(out_gt)

for i in range(1,4):
    in_band = in_ds.GetRasterBand(i)
    out_band = out_ds.GetRasterBand(i)
    data = in_band.ReadAsArray(off_ulx, off_uly, columns,rows)
    out_band.WriteArray(data)

del out_ds

#python3 20210527_9.5.py
    
