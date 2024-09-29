import os, glob
import numpy 
import pandas
from osgeo import gdal
import matplotlib as mpt

def cellstatiseic (pathin):
    fnamelist = os.listdir(pathin)
    for fname in fnamelist:
        print (fname)
        if fname[-4:] == '.tif':
            datapath = os.path.join(pathin, fname)
            in_data = gdal.Open(datapath)
            print (in_data)
            
if __name__ =="__main__":
    pathin = r"F:\LULC_Article\Sentinel-2_2021_dataset\BaiYin"
    