import matplotlib.pyplot as plt

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

# 创建图例
fig, ax = plt.subplots(figsize=(5, 3))

# 添加图例
for land_type, color in zip(land_cover_types.keys(), colors):
    ax.scatter(0, 0, color=color, label=f'{land_cover_types[land_type]} ({land_type})', s=100)  # 使用圆点

# 设置图例
ax.legend(loc='center', fontsize=11, frameon=False, title='Land Cover Types', title_fontsize=12, ncol=2)

# 去除坐标轴
ax.axis('off')

# 设置字体
plt.rc('font', family='Times New Roman')  # 设置全局字体为 Times New Roman

# 设置图例标题字体
ax.legend(title_fontsize=12, title='Land Cover Types', loc='upper left', fontsize=11)

# 保存图例
plt.savefig(r"F:\LULC_Article\2021\Sentinel-2_2021_dataset\legend.png", dpi=1000, bbox_inches='tight')
plt.show()
