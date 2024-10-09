import os
import numpy as np
from osgeo import gdal
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter

# 输入路径
input_path = r"F:\LULC_Article\2021\Sentinel-2_2021_dataset\GanNan\ESAv200_2021_GanNan.tif"  # 修改为你的输入路径

# 打开数据集
dataset = gdal.Open(input_path)
if dataset is None:
    raise RuntimeError("无法打开数据集！")

# 读取波段数据
band = dataset.GetRasterBand(1)
data = band.ReadAsArray()

# 获取唯一的土地覆盖类型及其对应的像元数
unique_types, pixel_counts = np.unique(data, return_counts=True)

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
    95: "Mangroves",
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
    '#00cf75',  # 红树林
    '#fae6a0'   # 苔藓和地衣
]

# 创建像元数的列表和标签
counts = [0] * len(land_cover_types)
labels = list(land_cover_types.keys())  # 使用数字作为标签

# 填充像元数
for land_type, count in zip(unique_types, pixel_counts):
    if land_type in land_cover_types:
        counts[land_type // 10 - 1] = count  # 处理映射以适应索引

# 创建绘图
fig, ax = plt.subplots(figsize=(2.56, 2.56))  # 设置图形大小为6.5cm*6.5cm

# 绘制直方图，条形宽度调整为更宽的值，间隙为0

bar_positions = np.arange(len(labels))  # 条形的x轴位置
bars = ax.bar(bar_positions, counts, color=colors[:len(counts)], width=0.618, align='center')  # align='edge'使条形紧密排列

# 设置横轴标签为10, 20, 30, ...
ax.set_xticks(bar_positions)  # 调整横轴标注位置
ax.set_xticklabels(labels, fontname='Times New Roman', fontsize=13)  # 设置为数字

ax.set_xlabel('Land Type', fontname='Times New Roman', fontsize=13)
ax.set_ylabel('Count', fontname='Times New Roman', fontsize=13)

# 设置标题，放在框内
ax.set_title('ESA WorldCover 10m V200 -GanNan', fontname='Times New Roman', loc='left', pad=-0.1, fontsize=13)

# 纵轴取值为十进制
def to_decimal(x, pos):
    return f'{int(x):,}'

ax.yaxis.set_major_formatter(FuncFormatter(to_decimal))

# 设置纵轴字体
ax.tick_params(axis='y', labelsize=13)  # 纵轴刻度标签大小
for label in ax.get_yticklabels():
    label.set_fontname('Times New Roman')

# 设置边框
for spine in ax.spines.values():
    spine.set_visible(True)
    spine.set_linewidth(0.5)  # 设置边框宽度
    spine.set_color('black')  # 设置边框颜色

# 调整图形布局
plt.tight_layout()

# 保存图形，设置dpi为600
output_file = r"output_histogram.png"  # 修改为你的输出文件名
plt.savefig(output_file, dpi=600)

# 显示图形
plt.show()
