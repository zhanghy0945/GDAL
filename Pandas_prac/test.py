import pandas as pd
print ("1OK!")
import numpy as np
print ("2OK!")

import scipy
print ("5OK!")
import statsmodels
print ("6OK!")

from osgeo import gdal 

import torch
# Summary: 检测当前Pytorch和设备是否支持CUDA和cudnn

if __name__ == '__main__':
	print("Support CUDA ?: ", torch.cuda.is_available())
	x = torch.Tensor([1.0])
	xx = x.cuda()
	print(xx)
 
	y = torch.randn(2, 3)
	yy = y.cuda()
	print(yy)
 
	zz = xx + yy
	print(zz)
 
	# CUDNN TEST
	from torch.backends import cudnn
	print("Support cudnn ?: ",cudnn.is_acceptable(xx))

import matplotlib as pt
print ("8OK!")
import geemap
print ("9OK!")
import sklearn
print ("10OK!")








