import geopandas as gpd
import os

# 读取500km缓冲区的面状数据
os.chdir(r"F:\India\buffer")
buffer_zone = gpd.read_file("india_pakistan_200kmPolygon.shp")

# 读取墨西哥县的面状数据
mexico_counties_IND = gpd.read_file("gadm41_IND_3.shp")
mexico_counties_PAK = gpd.read_file("gadm41_PAK_3.shp")
# mexico_counties_AFG = gpd.read_file("gadm41_AFG_2.shp")
# 确保坐标参考系一致
mexico_counties_IND = mexico_counties_IND.to_crs(buffer_zone.crs)
mexico_counties_PAK = mexico_counties_PAK.to_crs(buffer_zone.crs)
# mexico_counties_AFG = mexico_counties_AFG.to_crs(buffer_zone.crs)
# 提取与缓冲区相交的墨西哥县
intersecting_counties_IND = mexico_counties_IND[mexico_counties_IND.intersects(buffer_zone.unary_union)]
intersecting_counties_PAK = mexico_counties_PAK[mexico_counties_PAK.intersects(buffer_zone.unary_union)]
# intersecting_counties_AFG = mexico_counties_AFG[mexico_counties_AFG.intersects(buffer_zone.unary_union)]
# 保存提取出来的完整县数据
intersecting_counties_IND.to_file("India_Level3_200kmbuffer.shp")
intersecting_counties_PAK.to_file("Pakistan_Level3_200kmbuffer.shp")
# intersecting_counties_AFG.to_file("Afghanistan_Level2_200kmbuffer.shp")