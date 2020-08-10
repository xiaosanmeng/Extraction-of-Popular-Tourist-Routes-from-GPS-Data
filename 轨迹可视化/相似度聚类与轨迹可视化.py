
"""在folium上进行轨迹的可视化"""
trajectory = folium.Map(location=[sparseRoute_info['lat'].mean(), sparseRoute_info['lng'].mean()],
                        zoom_start=12,
                        tiles=r'http://{s}.tiles.wmflabs.org/bw-mapnik/{z}/{x}/{y}.png',
                        attr='© <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>')
threNum = []
for i in range(len(group_key)):
    threNum.append(sum(i > 0.933 for i in trajsim[i, :].tolist())-1)
"""得到前0.4的聚类中心的索引"""
maxNumIndex = np.argsort(-np.array(threNum)).tolist()[0:int(len(threNum)*0.3)]
# maxNumIndex = np.argsort(-np.array(threNum)).tolist()[0:10]
# marker_cluster = MarkerCluster().add_to(trajectory)
for j in maxNumIndex:
    opacityGrade = list(trajsim[j][:])
    opacityGrade1 = sorted(opacityGrade, reverse=True)
    for i in range(len(group_key)):
        try1 = sparseRoute_info[(sparseRoute_info['userID'] == group_key[i][0]) & (
                sparseRoute_info['date'] == group_key[i][1])]
        route = try1[['lat', 'lng']].values.tolist()
        """在这里将透明度与轨迹粗细分档进行计算"""
        Grade = opacityGrade1.index(trajsim[j][i]) + 1
        folium.PolyLine(route, weight=5-Grade*0.3, opacity=1/Grade, color='purple').add_to(trajectory)
        """目的地旅游景点的位置可以由tourist_info的经纬度得到，其名称可以由改数据的index得到"""
        POI_data = tourist_info[(tourist_info['userID'] == group_key[i][0]
                                 ) & (tourist_info['date'] == group_key[i][1])]
        lat = POI_data['lat'].mean()
        lng = POI_data['lng'].mean()
        kw = {'prefix': 'fa', 'color': 'green', 'icon': 'arrow-up'}
        angle = 180
        icon = folium.Icon(angle=angle, **kw)
        folium.Marker(location=[lat, lng], icon=icon, tooltip=str(angle)).add_to(trajectory)
        """为标志添加文本,将文本直接添加到地图上（这里存在的弊端是如果一人一天旅游多个地方，只能显示出一个来）"""
        textID = relationTable[(relationTable['tourist_id'] == POI_data.index.values.tolist()[0]
                                )]['sights_id'].values.tolist()[0]
        iframe = folium.IFrame(textID, width=50, height=50)
        popup = folium.Popup(iframe, max_width=100)
        Text = folium.Marker(location=[lat, lng], popup=popup)
        trajectory.add_child(Text)
        """上面为添加图标，下面为添加文本"""
        folium.map.Marker(location=[lat, lng], icon=DivIcon(icon_size=(500, 100), icon_anchor=(250, 0),
                          html='<div style="font-family:STKaiti;font-weight: bold;text-align:center; '
                          'font-size: 13pt; color:SLATEBLUE;">' + textID + '</div>', )).add_to(trajectory)

trajectory.save(r'D:\Program\轨迹数据挖掘\Result6_0.934.html')
