import os, glob
from osgeo import gdal
import numpy as np
import pandas as pd

def img_block (pathin, pathout):
    filelist = os.listdir(pathin, pathout)
    for file_name in filelist:
        if file_name[-4:] == ".tif":
            in_file = os.path.join(pathin, file_name)
            in_data = gdal.Open(in_file, gdal.GA_ReadOnly)
            geotransform = in_data.GetGeoTransform()
            projection = in_data.GeoProjection()
            in_band = in_data.GetRasterBand(1)

            
