import os
from osgeo import gdal
from tqdm import tqdm
import numpy as np

# 输入输出路径
pathin = r"F:\LULC_Article\Sentinel-2_2020_process\JiuQuan"
pathout = r"F:\LULC_Article\Sentinel-2_dataset\JiuQuan"

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

# 创建输出图像 (真彩色, 3个波段, float32)
out_name = os.path.join(pathout, "Sentinel-2_True2021_JiuQuan.tif")
driver = gdal.GetDriverByName('GTiff')
out_data = driver.Create(out_name, xsize, ysize, 3, gdal.GDT_Float32)

# 设置投影和地理信息
out_data.SetGeoTransform(geotransform)
out_data.SetProjection(projection)

# 每次处理一行，减少内存占用
print("正在分块写入波段数据...")
for y in tqdm(range(ysize), desc="Processing rows"):
    b4_band = b4_data.GetRasterBand(1).ReadAsArray(0, y, xsize, 1).astype(np.float32)
    b3_band = b3_data.GetRasterBand(1).ReadAsArray(0, y, xsize, 1).astype(np.float32)
    b2_band = b2_data.GetRasterBand(1).ReadAsArray(0, y, xsize, 1).astype(np.float32)
    
    out_data.GetRasterBand(1).WriteArray(b4_band, 0, y)  # 红色
    out_data.GetRasterBand(2).WriteArray(b3_band, 0, y)  # 绿色
    out_data.GetRasterBand(3).WriteArray(b2_band, 0, y)  # 蓝色

# 刷新缓存并关闭文件
out_data.FlushCache()
out_data = None
b4_data = None
b3_data = None
b2_data = None

print(f"真彩色合成完成，输出文件保存在: {out_name}")
