"""
Created on July 12, 2020
@ author: Zhoujian Yao
Function: to identify the tourist using the grid method
"""
import pandas as pd
import numpy as np
from tqdm import tqdm


POIPath = r'E:\交通科研数据集\Geolife Trajectories 1.3\未改变范围\POIDataProject.csv'
POI = pd.read_csv(POIPath)
FinalDataPath = r'E:\交通科研数据集\Geolife Trajectories 1.3\未改变范围\FinalData.csv'
Point = pd.read_csv(FinalDataPath)
# step1: 设定网格的大小，设定一个网格编号计算的整数
bsz = 200
amp = 10000000
threshold = 200
# 计算POI点网格编号
POI['bid'] = POI['x'].apply(int)//bsz*amp + POI['y'].apply(int)//bsz
POI['index'] = POI.index
block_set = set(POI['bid'])
# 对每天的轨迹点进行POI匹配
# 计算轨迹点网格编号
Point.loc[:, 'bid'] = Point['x'].apply(int)//bsz*amp + Point['y'].apply(int)//bsz
Point['index'] = Point.index
match = np.full([len(Point), len(POI)], np.str)

for key, group in tqdm(Point.groupby('bid')):
    # 这里-1是表示自动计算，1表示一行或者1列的个数，这里表示重组为1列
    trail = group.drop_duplicates(['bid', 'x', 'y'])
    """将所有的展开为1列"""
    Point_x = np.array(trail['x']).reshape([-1, 1])
    Point_y = np.array(trail['y']).reshape([-1, 1])
    for dx in range(-1, 2):
        for dy in range(-1, 2):
            nkey = key + dx*amp + dy              
            if nkey in block_set:
                """提取出轨迹网格旁边网格的POI点"""
                POIs = POI[POI['bid'] == nkey]
                """提取出POI点的x与y的值，重组形状为1行"""
                POI_x = np.array(POIs['x']).reshape([1, -1])
                POI_y = np.array(POIs['y']).reshape([1, -1])
                """这里表示距离计算"""
                dis = np.sqrt((Point_x-POI_x)**2 + (Point_y-POI_y)**2)
                ID = np.where(dis <= threshold)
                """其中ID[0]表示在trail中的索引, ID[1]表示在站点之间的索引"""
                """ID[0]需要将trail中的索引转化到轨迹的索引,因此需要在轨迹点的后面添加索引列"""
                Point_index = trail.iloc[ID[0]]['index'].tolist()
                POI_index = POIs.iloc[ID[1]]['index'].tolist()
                """将符合条件的项目设置为该POI的名称"""
                val = POIs.iloc[ID[1]]['name'].tolist()
                match[Point_index, POI_index] = val
"""现在需要将符合条件的旅行相关的数据再次筛选出来，将非空数据的行与列提取出来"""
position = np.where(match != np.str)
tourist_id = position[0]
sights_id = position[1]
"""构建关于轨迹点与旅游景点的对照表"""
tourist_info = Point.iloc[tourist_id, :]
sights_info = POI.iloc[sights_id, :]
relationTable = {'tourist_id': tourist_id, 'sights_id': sights_info['name']}
relationTable = pd.DataFrame(relationTable)
"""这里可以将tourist_info依据date与userID进行相关的统计"""
"""然后依据统计的信息将原来的数据集合依据userID与date进行筛选，得到后面需要用的信息"""
tourist_classify = tourist_info.groupby(['userID', 'date']).count()
group_key = np.array(tourist_classify.index)
Result = []
"""直接依据该数组进行筛选"""
for i in range(len(group_key)):
    Result.append(Point[(Point['userID'] == group_key[i][0]) & (Point['date'] == group_key[i][1])])
Result = pd.concat(Result)
"""创建新的一列用于存储旅游景点信息"""
Result.loc[:, 'place'] = np.str
Result.loc[tourist_id, 'place'] = sights_info['name'].to_list()
