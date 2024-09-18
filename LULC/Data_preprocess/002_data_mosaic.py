import os, glob
from osgeo import gdal
import numpy as np
from numpy import nan as NA


pathin = r"F:\LULC_Article\ESA_v200\process"
pathout = r"F:\LULC_Article\ESA_v200\process"
datalist = os.listdir(pathin)

print (datalist)

b2 = []
b2_rows = [] 
b2_cols = [] 
transform_list = []
projection_b2 = None

for data in datalist:
    #if data[-4:]=='.tif' and 'B4' in data:
    if data[-4:]=='.tif' and "JiuQuan" in data:
        print (data)
        datapath = pathin +  "/" + data
        print ("datapath is: ", datapath)
        print ("<<<-------------------------------------->>>")
        print(f"处理文件: {data}")
        dataori = gdal.Open(datapath, gdal.GA_ReadOnly)
        if dataori is None:
            raise RuntimeError(f"无法打开影像文件: {datapath}")
        inBand_b2 = dataori.GetRasterBand(1)
        gtiff_driver = gdal.GetDriverByName('Gtiff')

#-------------------------------------- 获取图像的基本信息 -----------------------------

        transform_b2 = dataori.GetGeoTransform()
        if projection_b2 is None:
            projection_b2 = dataori.GetProjection()
        print (transform_b2)
        projection_b2 = dataori.GetProjection()
        nodata_value = inBand_b2.GetNoDataValue()
        print (nodata_value)
        rows = inBand_b2.YSize #获取图像的行数
        b2_rows.append(rows) 
        cols = inBand_b2.XSize #获取图像的列数
        b2_cols.append(cols)
        print (rows, cols)
        b2.append(inBand_b2.ReadAsArray())
        print(f"行数: {rows}, 列数: {cols}")
        print("<<<-------------------------------------->>>")
        print (b2)
        print (b2_rows, b2_cols)
        print(f"行数: {rows}, 列数: {cols}")
        transform_list.append(transform_b2)

#-------------------------------------- 检验图像列表的长度 ----------------------------- 
#        
if len(b2) != 2 :
    raise ValueError("必须有两张图像进行镶嵌！")
if len(b2) ==2 :
    print ("OK!")

#-------------------------------------- 01.设置输出图像的信息 -----------------------------
#-------------------------------------- 01.01设置输出图像的行列 -----------------------------
rows1 = b2_rows[0] # 获取输出的列
rows2 = b2_rows[1]
if  rows1 == rows2:
    out_rows = rows1
elif rows1 != rows2:
    out_rows = rows1 + rows2   
cols1 = b2_cols[0] # 获取输出的行
cols2 = b2_cols[1] 
if  cols1 == cols2:
    out_cols = cols1
elif cols1 != cols2:
    out_cols = cols1 + cols2 
print (out_rows, out_cols)

transform_b2 = transform_list[0]

#-------------------------------------- 02.设置输出图像的基本信息 -----------------------------

out_driver = gdal.GetDriverByName('Gtiff')
out_name = pathout + "/" + "ESAv200_2021_JiuQuan.tif"
out_dataset = out_driver.Create(out_name, out_cols, out_rows, 1, gdal.GDT_Float32)
if out_dataset is None:
    raise RuntimeError(f"无法创建输出影像文件: {pathout}")
out_dataset.SetGeoTransform(transform_b2)
out_dataset.SetProjection(projection_b2)

#-------------------------------------- 02.01设置输出图像的详细信息 -----------------------------

out_band = out_dataset.GetRasterBand(1)
out_band.WriteArray(b2[0], 0, 0)
offset_x = int((transform_list[1][0] - transform_b2[0]) / transform_b2[1])
out_band.WriteArray(b2[1], offset_x, 0)
#out_band.SetNoDataValue(np.nan)


#-------------------------------------- 03.检验并输出 -----------------------------
out_band.FlushCache()
out_dataset = None

print(f"镶嵌完成，输出文件保存在: {pathout}")