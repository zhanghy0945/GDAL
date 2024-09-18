import os
from osgeo import gdal
import numpy as np
from tqdm import tqdm

# 输入输出路径
pathin = r"F:\LULC_Article\ESA_v200\process"
pathout = r"F:\LULC_Article\ESA_v200\process"

# 读取数据列表
datalist = os.listdir(pathin)

b2 = []
b2_rows = [] 
b2_cols = [] 
transform_list = []
projection_b2 = None

# 设置进度条
for data in tqdm(datalist, desc="Processing files"):
    #if data[-4:] == '.tif' and 'B4' in data:
    if data[-4:] == '.tif' and "JiuQuan" in data:
        print(data)
        datapath = pathin + "/" + data
        print("datapath is:", datapath)
        print("<<<-------------------------------------->>>")
        print(f"处理文件: {data}")
        
        # 打开影像文件
        dataori = gdal.Open(datapath, gdal.GA_ReadOnly)
        if dataori is None:
            raise RuntimeError(f"无法打开影像文件: {datapath}")
        
        # 读取图像带
        inBand_b2 = dataori.GetRasterBand(1)
        gtiff_driver = gdal.GetDriverByName('Gtiff')

        # 获取图像的基本信息
        transform_b2 = dataori.GetGeoTransform()
        if projection_b2 is None:
            projection_b2 = dataori.GetProjection()
        
        nodata_value = inBand_b2.GetNoDataValue()
        print(nodata_value)
        
        rows = inBand_b2.YSize  # 获取图像的行数
        b2_rows.append(rows)
        
        cols = inBand_b2.XSize  # 获取图像的列数
        b2_cols.append(cols)
        
        b2.append(inBand_b2.ReadAsArray())
        
        transform_list.append(transform_b2)
        print(f"行数: {rows}, 列数: {cols}")

# 检验图像数量
if len(b2) != 2:
    raise ValueError("必须有两张图像进行镶嵌！")

# 设置输出图像的行列
rows1 = b2_rows[0]
rows2 = b2_rows[1]
out_rows = rows1 if rows1 == rows2 else rows1 + rows2

cols1 = b2_cols[0]
cols2 = b2_cols[1]
out_cols = cols1 if cols1 == cols2 else cols1 + cols2

transform_b2 = transform_list[0]

# 创建输出影像
out_driver = gdal.GetDriverByName('Gtiff')
out_name = os.path.join(pathout, "ESAv200_2021_JiuQuan.tif")
out_dataset = out_driver.Create(out_name, out_cols, out_rows, 1, gdal.GDT_Byte)
if out_dataset is None:
    raise RuntimeError(f"无法创建输出影像文件: {out_name}")
out_dataset.SetGeoTransform(transform_b2)
out_dataset.SetProjection(projection_b2)

# 写入图像数据并显示进度条
out_band = out_dataset.GetRasterBand(1)
out_band.WriteArray(b2[0], 0, 0)
offset_x = int((transform_list[1][0] - transform_b2[0]) / transform_b2[1])

# 使用进度条处理镶嵌
for i in tqdm(range(b2[1].shape[0]), desc="Mosaicking"):
    out_band.WriteArray(b2[1][i:i+1, :], offset_x, i)

#out_band.SetNoDataValue(np.nan)

# 刷新并保存
out_band.FlushCache()
out_dataset = None

print(f"镶嵌完成，输出文件保存在: {out_name}")
