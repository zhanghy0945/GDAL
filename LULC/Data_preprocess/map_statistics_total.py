import os
import numpy as np
from osgeo import gdal
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter

# 输入路径列表
input_paths = [
    r'F:\LULC_Article\2021\Sentinel-2_2021_dataset\WuWei\ESAv200_2021_WuWei.tif',
    r'F:\LULC_Article\2021\Sentinel-2_2021_dataset\LanZhou\ESAv200_2021_LanZhou.tif',
    r'F:\LULC_Article\2021\Sentinel-2_2021_dataset\LinXia\ESAv200_2021_LinXia.tif',
    r'F:\LULC_Article\2021\Sentinel-2_2021_dataset\PingLiang\ESAv200_2021_PingLiang.tif',
    r'F:\LULC_Article\2021\Sentinel-2_2021_dataset\GanNan\ESAv200_2021_GanNan.tif',
    r'F:\LULC_Article\2021\Sentinel-2_2021_dataset\LongNan\ESAv200_2021_LongNan.tif',
]

# 与GEE一致的土地覆盖类型映射
land_cover_types = {
    10: "Tree cover",
    20: "Shrubland",
    30: "Grassland",
    40: "Cropland",
    50: "Built-up",
    60: "Bare / sparse vegetation",
    70: "Snow and ice",
    80: "Permanent water bodies",
    90: "Herbaceous wetland",
    100: "Moss and lichen"
}

# 与GEE一致的配色
colors = [
    '#006400',  # 树冠覆盖
    '#ffbb22',  # 灌木丛
    '#ffff4c',  # 草地
    '#f096ff',  # 农田
    '#fa0000',  # 城市
    '#b4b4b4',  # 裸土 / 稀疏植被
    '#f0f0f0',  # 雪和冰
    '#0064c8',  # 永久水体
    '#0096a0',  # 草本湿地
    '#fae6a0'   # 苔藓和地衣
]

# 创建子图
fig, axs = plt.subplots(2, 3, figsize=(19.3 / 2.54, 12.5 / 2.54))  # 设置整体图幅宽度和高度

# 设置子图间距
plt.subplots_adjust(hspace=0.3, wspace=0.3, left=0.1, right=0.9, top=0.9, bottom=0.2)

for i, input_path in enumerate(input_paths):
    # 打开数据集
    dataset = gdal.Open(input_path)
    if dataset is None:
        raise RuntimeError(f"无法打开数据集：{input_path}")

    # 读取波段数据
    band = dataset.GetRasterBand(1)
    data = band.ReadAsArray().astype(np.uint8)

    # 替换空值（假设空值用0表示）
    data[data == 0] = 255  # 或者选择其他合适的替代值

    # 获取唯一的土地覆盖类型及其对应的像元数
    unique_types, pixel_counts = np.unique(data, return_counts=True)

    # 创建像元数的列表和标签
    counts = [0] * len(land_cover_types)
    labels = list(land_cover_types.keys())  # 使用数字作为标签
    total_pixels = data.size  # 计算总像元数

    # 填充像元数
    for land_type, count in zip(unique_types, pixel_counts):
        if land_type in land_cover_types:
            counts[land_type // 10 - 1] = count  # 处理映射以适应索引

    # 将计数转换为比例
    proportions = [count / total_pixels for count in counts]

    # 绘制直方图
    bar_positions = np.arange(len(labels))  # 条形的x轴位置
    axs[i // 3, i % 3].bar(bar_positions, proportions, color=colors[:len(counts)], width=0.618, align='center')

    # 设置横轴标签
    axs[i // 3, i % 3].set_xticks(bar_positions)
    axs[i // 3, i % 3].set_xticklabels(labels, fontname='Times New Roman', fontsize=9)

    # 设置标题，去掉.tif
    title = os.path.basename(input_path).split("_")[2].replace('.tif', '')
    axs[i // 3, i % 3].set_title(f'ESA WorldCover 10m V200 - {title}', 
                                  fontname='Times New Roman', loc='left', pad=-0.1, fontsize=9)

    # 设置纵轴为十进制格式
    axs[i // 3, i % 3].yaxis.set_major_formatter(FuncFormatter(lambda x, _: f'{x:.0%}'))  # 格式化为百分比

    # 设置纵轴字体
    axs[i // 3, i % 3].tick_params(axis='y', labelsize=9)
    for label in axs[i // 3, i % 3].get_yticklabels():
        label.set_fontname('Times New Roman')

    # 在每一行第一列添加纵轴标签
    if i % 3 == 0:
        axs[i // 3, i % 3].set_ylabel('Proportion', fontname='Times New Roman', fontsize=9)

    # 显示纵轴
    if i % 3 == 0 or (i // 3 == 1 and i % 3 == 1):  # 第一行第一个和第二行第二个显示
        axs[i // 3, i % 3].get_yaxis().set_visible(True)
    else:  # 其他不显示
        axs[i // 3, i % 3].get_yaxis().set_visible(True)

    # 设置边框
    for spine in axs[i // 3, i % 3].spines.values():
        spine.set_visible(True)
        spine.set_linewidth(0.5)  # 设置边框宽度
        spine.set_color('black')  # 设置边框颜色

# 调整图形布局
plt.tight_layout()

# 保存图形，设置dpi为600，输出为JPG格式
output_file = r"F:\LULC_Article\2021\Sentinel-2_2021_dataset\output_histograms.jpg"  # 修改为你的输出文件名
plt.savefig(output_file, dpi=2000, bbox_inches='tight', format='jpg')

# 显示图形
plt.show()