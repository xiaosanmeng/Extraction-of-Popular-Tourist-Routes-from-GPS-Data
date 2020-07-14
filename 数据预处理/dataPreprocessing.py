import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from math import radians, cos, sin, asin, sqrt
from datetime import datetime


def Haversine(lon1, lat1, lon2, lat2):
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a))
    r = 6371
    d = c * r
    return float('{0:0.3f}'.format(d))


def time2second(t):
    h, m, s = t.strip().split(":")
    return int(h) * 3600 + int(m) * 60 + int(s)


names = ['lat', 'lng', 'date', 'time', 'userID']
path = r'E:\交通科研数据集\Geolife Trajectories 1.3\未改变范围\国庆时间筛选.csv'
data = pd.read_csv(path, engine='c', header=6, names=names)
print('the original size of the data: {}'.format(len(data)))
# 进行数据处理：步骤一 将不在经纬度范围的数据筛选掉
data = data[((data['lat'] < 41.05) & (data['lat'] > 39.4) & (data['lng'] < 117.5) & (data['lng'] > 115.4))]
print('the data size filtered out by the boundary: {}'.format(len(data)))
# 接下来将一个数据的经纬度复制给上一个数据，并创造新的字段lat_1, lng_1
data.loc[:, 'lat_1'] = data['lat'].shift(-1)
data.loc[:, 'lng_1'] = data['lng'].shift(-1)
data.loc[:, 'time_1'] = data['time'].shift(-1)
data = data.drop(data.index[len(data)-1])
# 计算上下两点之间的距离
data.loc[:, 'distance'] = data.apply(lambda r: (Haversine(r['lng'], r['lat'], r['lng_1'], r['lat_1'])), axis=1)
data.loc[:, 'Stime'] = data.apply(lambda r: (time2second(r['time_1']) - time2second(r['time'])), axis=1)
data = data[((data['Stime'] != 0) & (data['distance'] != 0))]
print('the data size after distance and time filtered: {}'.format(len(data)))
# 将速度的阈值设置为最低2km/h，最高设置为70km/h
data.loc[:, 'Speed'] = data.apply(lambda r: (3600 * r['distance']/r['Stime']), axis=1)
data = data[((data['Speed'] >= 2) & (data['Speed'] <= 70))]
print('the data size beyond the speed range: {}'.format(len(data)))


