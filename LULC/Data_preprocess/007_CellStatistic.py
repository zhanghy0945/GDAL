import os, glob
import numpy 
import pandas
from osgeo import gdal
import matplotlib as mpt

def cellstatiseic (pathin):
    files = {
        "ESAV200" : None,
        "Sentinel" : None
    }
    fnamelist = os.listdir(pathin)
    for fname in fnamelist:
        print (fname)
        if fname.endswith('.tif'):
            if "ESA" in fname:
                files['ESAV200'] = os.path.join(pathin, fname)
            if "Sentinel" in fname:
                files['Sentinel'] = os.path.join(pathin, fname)
                
    band_esa = gdal.Open(files["ESAV200"])
    band_sentinel = gdal.Open(files["Sentinel"])
             
if __name__ == "__main__":
    pathin = r"F:\LULC_Article\Sentinel-2_2021_dataset\BaiYin"
    cellstatiseic (pathin)
    