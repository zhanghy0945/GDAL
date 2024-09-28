
import os
import numpy as np
import rasterio
from rasterio.windows import Window

# 设置输入和输出目录
output_dir = './train/img'
output_label_dir = './train/label'
os.makedirs(output_dir, exist_ok=True)
os.makedirs(output_label_dir, exist_ok=True)
city_names = ['LanZhou', 'XX', 'XX']
for city_name in city_names:
    input_image_path = os.path.join('./dataset',city_name,f"Sentinel-2_True2021_{city_name}.tif")
    input_label_path = os.path.join('./dataset',city_name,f"ESAv200_2021_{city_name}.tif")
# 创建输出目录
# 定义裁剪大小
tile_size = 512
# 读取标签
with rasterio.open(input_label_path) as src_label:
    img_width = src_label.width
    img_height = src_label.height

    # 遍历裁剪窗口
    for i in range(0, img_width, tile_size):
        for j in range(0, img_height, tile_size):
            # 确保不超出边界
            window = Window(i, j, min(tile_size, img_width - i), min(tile_size, img_height - j))

            # 裁剪标签
            label_data = src_label.read(window=window)

            if label_data.ndim == 2:  # 如果是二维数组
                label_data = label_data[np.newaxis, ...]  # 添加通道维度
            elif label_data.ndim == 3 and label_data.shape[0] == 1:
                label_data = label_data[0, :, :]  # 将单通道数据展平

            # 检查是否为全黑标签图像
            if np.all(label_data == 0):
                continue  # 跳过全黑标签图像

            # 裁剪影像
            with rasterio.open(input_image_path) as src:
                img_data = src.read(window=window)

            # 保存裁剪后的影像为 TIFF，不保存地理信息
            output_image_path = os.path.join(output_dir, f"{city_name}_tile_{j//tile_size}_{i//tile_size}.tif")
            with rasterio.open(
                output_image_path,
                'w',
                driver='GTiff',
                height=img_data.shape[1],
                width=img_data.shape[2],
                count=src.count,
                dtype=img_data.dtype
            ) as dst:
                dst.write(img_data)

            # 保存裁剪后的标签为 TIFF，不保存地理信息
            output_label_path = os.path.join(output_label_dir, f"{city_name}_tile_{j//tile_size}_{i//tile_size}.tif")
            with rasterio.open(
                output_label_path,
                'w',
                driver='GTiff',
                height=label_data.shape[0],  # 高度
                width=label_data.shape[1],
                count=1,  # 标签只有一个通道
                dtype=label_data.dtype
            ) as dst_label:
                dst_label.write(label_data, 1)
