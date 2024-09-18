# -*- coding : utf-8 -*-
# C:/python3.6
import os
os.environ   # 输出environ字典对象
os.environ['PATH']   # 查看环境变量的PATH变量信息，其他变量可用同样方式查看


#from osgeo import gdal, ogr, osr
#import warnings
#warnings.simplefilter ("ignore")
#from osgeo import gdal
#from pyhdf.SD import SD, SDC, SDim


'''File path'''
#filepath = r'F:\test\NIEER_CGF-MODIS_SCE_20010101_DAILY_500m_V02.hdf'
'''Data'''
#filename = filepath.split('\\')[-1].split('.')[0]
#hdf = SD(filepath)
#snow = hdf.select('Day_Snow_Cover_Area').get()

'''Spatial Reference'''
#sr = osr.SpatialReference()
#sr.ImportFromEPSG(4326)
#s=sr.ExportToWkt()
#driver=gdal.GetDriverByName("GTiff")
#dataset=driver.Create(filename+'.tif',14000,8000,1,gdal.GDT_Int16, ["TILED=YES", "COMPRESS=LZW"])
#im_geotrans=(72,0.005,0.0,56,0.0,-0.005)
#dataset.SetGeoTransform(im_geotrans)
#dataset.SetProjection(s)
#dataset.GetRasterBand(1).WriteArray(snow)








