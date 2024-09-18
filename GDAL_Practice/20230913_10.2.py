import  os 
import math
import numpy as np 
from osgeo import gdal
print ("----------Check bags success!----------")

def get_extent(fn):
    ds = gdal.Open(fn)
    gt = ds.GetGeoTransform()
    return (gt[0], gt[3], gt[0] + gt[1] * ds.RasterXSize, gt[3] + gt[5] * ds.RasterYSize)

def mosaic_image(pathin, pathout):
    in_files = []
    indata_list = os.listdir(pathin)
    str_1 = "O"
    for in_data in indata_list:
        if in_data[-4:] == ".tif" and  str_1 in in_data:
            print (in_data)
            in_file= pathin + "/" + in_data
            print (in_file)
            in_files.append(in_file)
    min_x, max_y, max_x, min_y = get_extent(in_files[0])
    print (in_files[0])
    for fn in in_files:
        minx, maxy, maxx, miny = get_extent(fn)
        min_x = min(min_x, minx)
        max_y = max(max_y, maxy)
        max_x = max(max_x, maxx)
        min_y = min(min_y, miny)
    
    in_ds = gdal.Open(in_files[0])
    gt = in_ds.GetGeoTransform()
    rows = math.ceil((max_y - min_y) / -gt[5])
    columns = math.ceil((max_x - min_x) / gt[1])
    
    driver = gdal.GetDriverByName("gtiff")
    out_path = os.path.join(pathout, "mosaic_2.tif")
    out_ds = driver.Create(out_path, columns, rows)
    out_ds.SetProjection(in_ds.GetProjection())
    out_band = out_ds.GetRasterBand(1)
    
    gt = list(in_ds.GetGeoTransform())
    gt[0], gt[3] = min_x, max_y
    out_ds.SetGeoTransform(gt)
    
    for fn in in_files:
        in_ds = gdal.Open(fn)
        trans = gdal.Transformer(in_ds, out_ds, [])
        success, xyz = trans.TransformPoint(False, 0, 0)
        x, y, z = map(int, xyz)
        data = in_ds.GetRasterBand(1).ReadAsArray()
        out_band.WriteArray(data, x, y)
    del in_ds, out_band, out_ds
    print ("success!")

if __name__ == "__main__":
    pathin = r"E:\osgeopy-data\Massachusetts"
    pathout = r"E:\osgeopy-data\Massachusetts_result"
    mosaic_image(pathin, pathout)
    0
    
#代码出错心得总结：