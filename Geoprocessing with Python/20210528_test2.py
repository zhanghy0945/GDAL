import os 
import gdal
from osgeo import gdal
import numpy as np

os.chdir(r'E:\test\2014')
in_ds = gdal.Open('201401_mean_LAI.tif')
in_band = in_ds.GetRasterBand(1)
out_rows = in_band.YSize * 2
out_columns = in_band.XSize * 2

gtiff_driver = gdal.GetDriverByName('Gtiff')
out_ds = gtiff_driver.Create('band1_resampled.tif', out_columns,out_rows)

out_ds.SetProjection(in_ds.GetProjection())
geotransform = list(in_ds.GetGeoTransform())
geotransform [1] /= 2
geotransform [5] /= 2
out_ds.SetGeoTransform(geotransform)

data = in_band.ReadAsArray(buf_xsize = out_columns, buf_ysize = out_rows)
out_band = out_ds.GetRasterBand(1)
out_band.WriteArray(data)

out_band.FlushCache()
out_band.ComputeStatistics(False)

del out_ds

# python3 20210528_test2.py
