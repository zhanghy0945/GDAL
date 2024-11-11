import rasterio
import numpy as np
import os


pathin = os.chdir(r"F:\LULC_Article\trash")
in_file = "Sentinel-2_True2021_JiaYuGuan.tif"
# with open (in_file) as dataset:
#     print (dataset.name)
#     print (dataset.mode)
#     print (dataset.)

dataset = rasterio.open(in_file)
print (dataset.name)
print (dataset.mode)
print (dataset.bounds)
print (dataset.width)
print (dataset.height)
print (dataset.transform)
print (dataset.crs)

