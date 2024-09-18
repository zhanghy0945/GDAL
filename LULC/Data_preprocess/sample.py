import rasterio
from rasterio.enums import Resampling

# 输入影像路径
input_image_path = r'F:\LULC_Article\ESA_v200\process\ESAv200_2021_JiuQuan.tif'  # 需要重新采样的影像
reference_image_path = r'F:\LULC_Article\Sentinel-2_dataset\JiuQuan\Sentinel-2_True2021_JiuQuan.tif'  # 尺寸参考影像
output_image_path = r'F:\LULC_Article\Sentinel-2_dataset\JiuQuan\ESAv200_2021_JiuQuan.tif'  # 重新采样后的输出影像

# 打开参考影像获取参考尺寸和变换参数
with rasterio.open(reference_image_path) as ref_src:
    ref_transform = ref_src.transform
    ref_width = ref_src.width
    ref_height = ref_src.height
    ref_crs = ref_src.crs

# 打开输入影像进行重新采样
with rasterio.open(input_image_path) as src:
    # 设置输出参数
    kwargs = src.meta.copy()
    kwargs.update({
        'crs': ref_crs,
        'transform': ref_transform,
        'width': ref_width,
        'height': ref_height
    })

    # 进行重采样并输出结果
    with rasterio.open(output_image_path, 'w', **kwargs) as dst:
        for i in range(1, src.count + 1):
            resampled_data = src.read(
                i,
                out_shape=(ref_height, ref_width),
                resampling=Resampling.nearest
            )
            dst.write(resampled_data, i)
