import os
from osgeo import gdal
import numpy as np
from numpy import nan as NA

# 输入和输出路径
pathin = r"F:\LULC_Article\Sentinel-2_2020_process\LongNan"
pathout = r"F:\LULC_Article\Sentinel-2_dataset\LongNan"
datalist = os.listdir(pathin)

print(datalist)

b2 = []
b2_rows = [] 
b2_cols = [] 
transform_list = []
projection_b2 = None

# 遍历文件并读取图像数据
for data in datalist:
    if data.endswith('.tif') and 'B4' in data:
        print(f"处理文件: {data}")
        datapath = os.path.join(pathin, data)
        
        # 打开影像并获取波段数据
        dataori = gdal.Open(datapath, gdal.GA_ReadOnly)
        if dataori is None:
            raise RuntimeError(f"无法打开影像文件: {datapath}")

        inBand_b2 = dataori.GetRasterBand(1)

        # 获取图像的基本信息
        transform = dataori.GetGeoTransform()
        if projection_b2 is None:
            projection_b2 = dataori.GetProjection()
        
        rows = inBand_b2.YSize  # 行数
        cols = inBand_b2.XSize  # 列数
        b2_rows.append(rows)
        b2_cols.append(cols)
        b2.append(inBand_b2.ReadAsArray())
        transform_list.append(transform)
        
        print(f"行数: {rows}, 列数: {cols}")
        print("<<<-------------------------------------->>>")

# 确保有两张影像进行拼接
if len(b2) != 2:
    raise ValueError("必须有两张图像进行镶嵌！")

# 确认图像行数是否一致
if b2_rows[0] != b2_rows[1]:
    raise ValueError("两张图像的行数不同，无法直接拼接！")

# 输出图像的行列数（拼接后列数为两张图像列数相加）
out_rows = b2_rows[0]
out_cols = b2_cols[0] + b2_cols[1]

# 计算地理变换参数，用第一张图像的变换为基础
transform_b2 = transform_list[0]

# 创建输出影像
out_driver = gdal.GetDriverByName('GTiff')
out_name = pathout + "/" + 'Sentinel2_2021B4_LongNan.tif'
out_dataset = out_driver.Create(out_name, out_cols, out_rows, 1, gdal.GDT_Float32)
if out_dataset is None:
    raise RuntimeError(f"无法创建输出影像文件: {pathout}")

# 设置输出图像的投影和地理变换
out_dataset.SetGeoTransform(transform_b2)
out_dataset.SetProjection(projection_b2)

# 获取输出波段
out_band = out_dataset.GetRasterBand(1)

# 将第一张图像写入输出影像的左半部分
out_band.WriteArray(b2[0], 0, 0)

# 计算第二张图像在输出影像中的起始位置
# 计算第二张图像的左上角的实际地理坐标，然后将其转换为像素坐标
offset_x = int((transform_list[1][0] - transform_b2[0]) / transform_b2[1])
out_band.WriteArray(b2[1], offset_x, 0)
out_band.SetNoDataValue(-999)

# 刷新缓存并关闭文件
out_band.FlushCache()
out_dataset = None

print(f"镶嵌完成，输出文件保存在: {pathout}")
