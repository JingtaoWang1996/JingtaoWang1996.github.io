"""
@Date: 2023/5/10 11:22
@Author: Jingtao Wang
@Version:1.0
"""
import folium


class mapSettings:
    def __init__(self):
        # 添加地点及对应经纬度坐标,负号表示西经和南纬
        self.map2loc_city = {"Xichang": [27.899, 102.2626], "Chengdu": [30.65984, 104.063365],
                             "Beijing": [39.906, 116.391], "Xiongan": [39.048, 115.907], "Nanning": [22.82, 108.363],
                             "Leshan": [29.585, 103.748], "zhengzhou": [34.748, 113.62],
                             "Chongqing": [29.565, 106.5466], "Toronto": [43.653, -79.385], "Buffalo": [42.886, -78.88]
                             }
        self.map2loc_pos = {"UB": [43.002, -78.785], "NiagaraFall": [43.256, -79.072], "CQPUT": [29.533532, 106.6042]}
        self.map_center = self.map2loc_city["zhengzhou"]  # 控制地图中心点的坐标为成都
        self.map = folium.Map(location=self.map_center, zoom_start=13)

    def add_loc_maker(self):
        # 添加标注
        for key in self.map2loc_city:
            folium.Marker(self.map2loc_city[key], popup=key).add_to(self.map)
        for key in self.map2loc_pos:
            folium.Marker(self.map2loc_pos[key], popup=key).add_to(self.map)


if __name__ == "__main__":
    m = mapSettings()
    m.add_loc_maker()
    # 保存地图
    m.map.save("map.html")
