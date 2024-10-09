from osgeo import gdal
import glob
import numpy as np
import os



def mosaic_images(input_folder, output_path):
    # 获取所有图像文件
    image_files = glob.glob(os.path.join(input_folder, '*.tif'))  # 修改扩展名根据需要
    print(f"找到 {len(image_files)} 张图像。")  # 调试信息

    if not image_files:
        print("未找到任何图像文件，请检查输入文件夹路径和文件扩展名。")
        return

    # 打开第一个图像以获取元数据
    first_image = gdal.Open(image_files[0])
    if first_image is None:
        print("无法打开第一张图像。")
        return

    # 获取数据类型和 NoData 值
    data_type = first_image.GetRasterBand(1).DataType
    nodata_value = first_image.GetRasterBand(1).GetNoDataValue()
    nodata_value = 0 if nodata_value is None else nodata_value  # 如果没有设置 NoData 值，则使用 0

    # 创建输出文件
    driver = gdal.GetDriverByName('GTiff')
    out_dataset = driver.Create(output_path, first_image.RasterXSize, first_image.RasterYSize, 1, data_type)
    out_dataset.SetGeoTransform(first_image.GetGeoTransform())
    out_dataset.SetProjection(first_image.GetProjection())
    out_dataset.GetRasterBand(1).SetNoDataValue(nodata_value)

    # 初始化镶嵌数组
    mosaic_array = np.full((first_image.RasterYSize, first_image.RasterXSize), nodata_value, dtype=np.float32 if data_type == gdal.GDT_Float32 else np.uint8)

    # 镶嵌图像
    for img_file in image_files:
        img_dataset = gdal.Open(img_file)
        if img_dataset is None:
            print(f"无法打开图像: {img_file}")
            continue

        # 读取数据
        band_data = img_dataset.GetRasterBand(1).ReadAsArray()
        
        # 计算图像的地理变换
        geo_transform = img_dataset.GetGeoTransform()
        y_offset = int((geo_transform[3] - first_image.GetGeoTransform()[3]) / geo_transform[5])
        x_offset = int((geo_transform[0] - first_image.GetGeoTransform()[0]) / geo_transform[1])

        # 替换 NoData 值为 nodata_value
        band_data = np.where(band_data == nodata_value, nodata_value, band_data)

        # 将 band_data 写入正确的位置
        mosaic_array[y_offset:y_offset + band_data.shape[0], x_offset:x_offset + band_data.shape[1]] = np.where(
            mosaic_array[y_offset:y_offset + band_data.shape[0], x_offset:x_offset + band_data.shape[1]] == nodata_value,
            band_data,
            np.maximum(mosaic_array[y_offset:y_offset + band_data.shape[0], x_offset:x_offset + band_data.shape[1]], band_data)
        )

        # 关闭图像数据集
        img_dataset = None

    # 写入输出文件
    out_dataset.GetRasterBand(1).WriteArray(mosaic_array.astype(data_type))

    # 关闭输出数据集
    out_dataset = None
    print(f"镶嵌完成，输出文件保存在 {output_path}")



if __name__ == '__main__':
    input_folder_path = r"F:\LULC_Article\2021\ESA_v200\GanSu"  # 替换为输入文件夹路径
    output_mosaic_path = r"F:\LULC_Article\2021\ESA_v200\GanSu\output_mosaic.tif" # 替换为输出文件路径
    mosaic_images(input_folder_path, output_mosaic_path)





#  r"F:\LULC_Article\2021\ESA_v200\GanSu"  # 替换为输入文件夹路径
#  r"F:\LULC_Article\2021\ESA_v200\GanSu\output_mosaic.tif" # 替换为输出文件路径












