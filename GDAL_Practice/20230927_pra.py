import os
from osgeo import gdal
import numpy as np

def read_file(pathin, pathout):
    in_files = []
    indata_list = os.listdir(pathin)
    for in_data in indata_list:
        if in_data[-4:] == ".tif":
            print (in_data)
            in_file1 = os.path.join(pathin, in_data)
            in_files.append(in_file1)
    for in_image in in_files:
        print (in_image)
        print (len(in_files))
        in_ds = gdal.Open(in_image)#这个是提取出文件夹里的影像文件
        #in_band = in_ds.GetRasterBand(1)#这个仅仅是读取了影像的波段信息
        #print ("in_band is: ", in_band, "-------")
        out_geotransform = in_ds.GetGeoTransform()
        print ("\n")
        out_projection = in_ds.GetProjection()
        print (out_geotransform, out_projection)
        
        in_number = in_ds.ReadAsArray()
        print (in_number)
if __name__ == "__main__":
    pathin = r"F:\test1"
    pathout = r"F:\test1"
    read_file(pathin, pathout)
    
            


