# 轨迹相似度聚类与地理可视化

**1.轨迹相似度聚类**

- 在上一个步骤利用轨迹相似度计算得到每两条轨迹之间的相似度，从而构成了轨迹相似度矩阵
- 这里提出轨迹相似度数量的差异系数，用于确定最佳的轨迹相似度阈值
- 利用轨迹相似度矩阵，结合最佳相似度阈值，从而得到每条轨迹的相似轨迹数量
- 将每条轨迹依据相似度轨迹的数量进行排序，确定热点轨迹

**2.轨迹可视化**

- 利用folium库对轨迹进行可视化，将排名前20的轨迹提取出来。
- 这里还利用folium加载了瓦片地图，调整地图样式；相关的请点击[瓦片地图样式选择](http://leaflet-extras.github.io/leaflet-providers/preview/index.html)
- 其中相关的瓦片地图在[使用教程](https://ithelp.ithome.com.tw/articles/10203732)
- 关于folium中绘制曲线，请参考[该教程](https://nbviewer.jupyter.org/github/python-visualization/folium/blob/master/examples/PolyLineTextPath_AntPath.ipynb)

**3.景点可视化**

- 利用folium的marker_cluster将相邻的景点聚类为一个然后展示出来
  






