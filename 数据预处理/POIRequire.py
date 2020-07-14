import urllib
from urllib import parse
from urllib import request
import pandas as pd
import json
from coordTransform_utils import gcj02_to_wgs84

# 从高德爬取下来的坐标系属于火星坐标系，需要经过坐标转换。
mykey = 'bb7c055bad28f29a043a15187ff23cef'
url = r'https://restapi.amap.com/v3/place/text?'
result = []
url_i = []
for i in range(2):
    parameters = {
        'key': mykey,
        'keywords': '国家级景点',
        'types': '110202',
        'city': '110000',
        'citylimit': 'true',
        'output': 'JSON',
        'offset': '50',
        'page': str(i+1),
        }
    url_data = parse.urlencode(parameters)
    url_i.append(url + url_data)
# 创建一个服务器
    request = urllib.request.Request(url_i[i])
    # 访问网页
    response = urllib.request.urlopen(request)
    webpage = response.read()
    result.append(json.loads(webpage.decode('utf8', 'ignore'))['pois'])
# 将地名与经纬度数据获取出来

name = []
location = []
for i in range(len(result)):
    for k in range(len(result[i])):
        name.append(result[i][k]['name'])
        location.append(result[i][k]['location'])

# 提取出经纬度坐标
lng = []
lat = []
for i in range(len(location)):
    index_comma = location[i].index(',')
    lng.append(float(location[i][0:index_comma]))
    lat.append(float(location[i][index_comma+1:]))

POIDataGcj02 = {'name': name, 'lng': lng, 'lat': lat}
POIDataGcj02 = pd.DataFrame(POIDataGcj02)
# 还需要一步：将高德的火星坐标系转化未WGS84坐标系，为下一步做准备
Lon_list1 = POIDataGcj02.apply(lambda r: (gcj02_to_wgs84(r['lng'], r['lat']))[0], axis=1)
Lat_list1 = POIDataGcj02.apply(lambda r: (gcj02_to_wgs84(r['lng'], r['lat']))[1], axis=1)
POIDataWGS84 = {'name': name, 'lng': Lon_list1, 'lat': Lat_list1}
POIDataWGS84 = pd.DataFrame(POIDataWGS84)
FilePath = r'E:\交通科研数据集\Geolife Trajectories 1.3\POIDataWGS84.csv'
POIDataWGS84.to_csv(FilePath, header=False, index=False)
