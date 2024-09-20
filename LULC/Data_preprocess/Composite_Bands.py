import os
from osgeo import gdal
from tqdm import tqdm
import numpy as np

# 输入输出路径
pathin = r"F:\LULC_Article\2019\Sentinel-2_2019_process\LanZhou"
pathout = r"F:\LULC_Article\2019\Sentinel-2_2019_dataset\LanZhou"

# Sentinel-2 真彩色波段 (B4, B3, B2)
bands = {
    'B4': None,  # 红色
    'B3': None,  # 绿色
    'B2': None   # 蓝色
}

# 查找文件
namelist = os.listdir(pathin)
for fname in namelist:
    if fname.endswith('.tif'):
        if 'B4' in fname:
            bands['B4'] = os.path.join(pathin, fname)
        elif 'B3' in fname:
            bands['B3'] = os.path.join(pathin, fname)
        elif 'B2' in fname:
            bands['B2'] = os.path.join(pathin, fname)

# 检查波段是否找到
if None in bands.values():
    raise ValueError("缺少必要的波段 (B4, B3, B2) 进行真彩色合成！")

# 打开波段文件
b4_data = gdal.Open(bands['B4'], gdal.GA_ReadOnly)
b3_data = gdal.Open(bands['B3'], gdal.GA_ReadOnly)
b2_data = gdal.Open(bands['B2'], gdal.GA_ReadOnly)

# 获取地理信息和投影
geotransform = b4_data.GetGeoTransform()
projection = b4_data.GetProjection()

# 获取图像大小
xsize = b4_data.RasterXSize
ysize = b4_data.RasterYSize

# 读取波段数据并显示进度条
print("正在读取波段数据...")
b4_band = b4_data.GetRasterBand(1).ReadAsArray()
b3_band = b3_data.GetRasterBand(1).ReadAsArray()
b2_band = b2_data.GetRasterBand(1).ReadAsArray()

# 检查每个波段的最小值和最大值
print(f"B4 (红色波段) 最小值: {np.min(b4_band)}, 最大值: {np.max(b4_band)}")
print(f"B3 (绿色波段) 最小值: {np.min(b3_band)}, 最大值: {np.max(b3_band)}")
print(f"B2 (蓝色波段) 最小值: {np.min(b2_band)}, 最大值: {np.max(b2_band)}")

# 确保波段的数据类型为 float32
b4_band = b4_band.astype(np.float32)
b3_band = b3_band.astype(np.float32)
b2_band = b2_band.astype(np.float32)

# 创建输出图像 (真彩色, 3个波段, float32)
out_name = os.path.join(pathout, os.path.basename(fname).split(".")[0] + "_True.tif")
driver = gdal.GetDriverByName('GTiff')
out_data = driver.Create(out_name, xsize, ysize, 3, gdal.GDT_Float32)

# 设置投影和地理信息
out_data.SetGeoTransform(geotransform)
out_data.SetProjection(projection)


# 写入红色、绿色、蓝色波段并添加进度条
print("正在写入波段数据...")
with tqdm(total=3, desc="写入波段", unit="band") as pbar:
    out_data.GetRasterBand(1).WriteArray(b4_band)  # 红色
    pbar.update(1)
    
    out_data.GetRasterBand(2).WriteArray(b3_band)  # 绿色
    pbar.update(1)
    
    out_data.GetRasterBand(3).WriteArray(b2_band)  # 蓝色
    pbar.update(1)

# 刷新缓存并关闭文件
out_data.FlushCache()
out_data = None
b4_data = None
b3_data = None
b2_data = None

print(f"真彩色合成完成，输出文件保存在: {out_name}")
