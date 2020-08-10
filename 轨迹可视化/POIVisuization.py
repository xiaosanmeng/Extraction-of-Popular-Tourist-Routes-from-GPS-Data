import numpy as np
import pandas as pd
import folium
from folium import DivIcon
from folium.plugins import MarkerCluster


POIPath = r'E:\交通科研数据集\Geolife Trajectories 1.3\未改变范围\POIDataProject6.csv'
POI = pd.read_csv(POIPath)
POI_Map = folium.Map(location=[POI['lat'].mean(), POI['lng'].mean()],
                     zoom_start=10,
                     tiles=r'http://{s}.tiles.wmflabs.org/bw-mapnik/{z}/{x}/{y}.png',
                     attr='© <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>')
marker_cluster = MarkerCluster().add_to(POI_Map)
POILocation = POI[['lat', 'lng']].values.tolist()
for i in range(len(POILocation)):
    kw = {'prefix': 'fa', 'color': 'darkpurple', 'icon': 'arrow-up'}
    angle = 180
    icon = folium.Icon(angle=angle, **kw)
    folium.Marker(location=POILocation[i], icon=icon, tooltip=str(angle)).add_to(marker_cluster)
    """为每一个点添加文本标注"""
    '''
    textID = POI['name'].iloc[i]
    iframe = folium.IFrame(textID, width=50, height=50)
    popup = folium.Popup(iframe, max_width=100)
    Text = folium.Marker(location=POILocation[i], popup=popup)
    marker_cluster.add_child(Text)
    '''
    '''
    """上面为添加图标，下面为添加文本"""
    folium.map.Marker(location=POILocation[i], icon=DivIcon(icon_size=(500, 100), icon_anchor=(250, 0),
                      html='<div style="font-family:STKaiti;font-weight: bold;text-align:center; '
                      'font-size: 13pt; color:SLATEBLUE;">' + textID + '</div>', )).add_to(POI_Map)
    '''
POI_Map.save(r'D:\Program\轨迹数据挖掘\POI_Map1.html')
