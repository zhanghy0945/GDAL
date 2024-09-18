import os
from osgeo import gdal
from tqdm import tqdm

# 输入和输出路径
pathin = r"F:\LULC_Article\Sentinel-2_2020_origin\JiuQuan\Sentinel_B8"
pathout = r"F:\LULC_Article\Sentinel-2_2020_process\JiuQuan"

# 读取文件列表
datalist = [os.path.join(pathin, file) for file in os.listdir(pathin) if file.endswith('.tif')]

# 检查图像数量
if len(datalist) < 25:
    raise ValueError("至少需要25张图像进行拼接！")

# 创建虚拟栅格数据集 (VRT) 的进度条函数
def vrt_progress_callback(complete, message, cb_data):
    pbar.update(int(complete * 100) - pbar.n)  # 更新进度条
    return 1

# 创建进度条
with tqdm(total=100, desc="创建虚拟拼接文件") as pbar:
    vrt_options = gdal.BuildVRTOptions(resampleAlg='nearest', addAlpha=True)
    vrt_mosaic = gdal.BuildVRT(os.path.join(pathout, "mosaic.vrt"), datalist, options=vrt_options, callback=vrt_progress_callback)

if vrt_mosaic is None:
    raise RuntimeError("无法创建虚拟拼接文件！")

# 导出为GeoTIFF的进度条函数
def translate_progress_callback(complete, message, cb_data):
    pbar.update(int(complete * 100) - pbar.n)  # 更新进度条
    return 1

# 导出为GeoTIFF文件
out_name = os.path.join(pathout, "Sentinel2_2021B8_JiuQuan.tif")
with tqdm(total=100, desc="导出拼接文件为GeoTIFF") as pbar:
    gdal.Translate(out_name, vrt_mosaic, format='GTiff', outputType=gdal.GDT_Float32, callback=translate_progress_callback)

# 关闭数据集 
vrt_mosaic = None

print(f"拼接完成，输出文件保存在: {out_name}")
