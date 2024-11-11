import os
from osgeo import gdal
import numpy as np

# 打开数据集
os.chdir(r"H:\颉老师专著\Hexi_dataGS(2024)0650")
dataset = gdal.Open('HeXi_RGB.tif', gdal.GA_ReadOnly)

# 创建输出数据集
driver = gdal.GetDriverByName('GTiff')
output_dataset = driver.Create('output_cleaned.tif', dataset.RasterXSize, dataset.RasterYSize, dataset.RasterCount, gdal.GDT_UInt16)

# 读取每个波段的数据
red_band = dataset.GetRasterBand(1).ReadAsArray()
green_band = dataset.GetRasterBand(2).ReadAsArray()
blue_band = dataset.GetRasterBand(3).ReadAsArray()

# 定义异常值的条件（你可以根据实际情况调整这些条件）
red_outliers = 15692
green_outliers = 13054
blue_outliers = 11537
# 综合出所有异常值的位置
combined_outliers = red_outliers | green_outliers | blue_outliers

# 将所有波段的异常值设置为NoData
red_band[combined_outliers] = 0.0
green_band[combined_outliers] = 0.0
blue_band[combined_outliers] = 0.0

# 写入输出数据集
output_dataset.GetRasterBand(1).WriteArray(red_band)
output_dataset.GetRasterBand(2).WriteArray(green_band)
output_dataset.GetRasterBand(3).WriteArray(blue_band)

# 设置NoData值
output_dataset.GetRasterBand(1).SetNoDataValue(np.nan)
output_dataset.GetRasterBand(2).SetNoDataValue(np.nan)
output_dataset.GetRasterBand(3).SetNoDataValue(np.nan)

# 清理
output_dataset.FlushCache()
del dataset
del output_dataset
