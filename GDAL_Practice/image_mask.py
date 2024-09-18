import os
from osgeo import gdal
import numpy as np

def geotransform(pathin ,pathout):
    fil_names = os.listdir(pathin)
    data_list = []
    for file_name in fil_names:
        if file_name[-4:] == ".tif":
            print (file_name)
            in_file = os.path.join(pathin, file_name)
            print (in_file)
            in_data = gdal.Open(in_file)
            out_geotransform = in_data.GetGeoTransform()
            out_projection = in_data.GetProjection()
            print (out_geotransform, "\n", out_projection)
            
            in_xsize = in_data.RasterXSize
            in_ysize = in_data.RasterYSize
            print ("原始图像的行列数：", in_xsize, in_ysize)
            print ("原始图像的仿射变换参数： ", out_geotransform)
            print ("\n")
            print ("原始图像的投影信息：", out_projection)
            #print (in_xsize, in_ysize)
            
if __name__ == "__main__":
    pathin = r"D:\MOD13Q1_origin"
    pathout = r"D:\MOD13Q1_origin"
    geotransform(pathin ,pathout)
    