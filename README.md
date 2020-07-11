# Tourism-Trip-Chain-Extraction-Based-on-Multi-Big-Data
从一般的交通大数据中识别游客，挖掘游客热点轨迹
### 数据预处理
1. 数据预处理：但由于文件太多，第一步将所有文件都合并为一个文件，方便后面读取
- 步骤一：文件读取，以下代码将所有文件合并为trajectoryCombination.cs
 **步骤二：**将所有文件读取到python中去，利用缓存机制分块读取。
1. **数据预处理：**但由于文件太多，第一步将所有文件都合并为一个文件，方便后面读取

- **步骤一：**文件读取，以下代码将所有文件合并为**trajectoryCombination.csv **

```python
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import os
import gmplot

df_final = pd.DataFrame(columns=('lat', 'lng', 'alt', 'date', 'time', 'userID'))
userID = ''
for j in [m for m in range(8) if m > 0]:
    for i in [k for k in range(30 * j) if k >= 30 * (j - 1)]:
        if i < 10:
            userID = '00' + str(i)
        elif 10 <= i <= 99:
            userID = str(0) + str(i)
        elif 100 <= i <= 181:
            userID = str(i)
        else:
            break
        fileName = r'E:\交通科研数据集\Geolife Trajectories 1.3\data' + '\\' + userID + '\\Trajectory'
        fileList = os.listdir(fileName)
        names = ['lat', 'lng', 'zero', 'alt', 'days', 'date', 'time']
        df_i_list = [pd.read_csv(fileName + '\\' + f, header=6, names=names, index_col=False) for f in fileList]
        df_i = pd.concat(df_i_list, ignore_index=True)
        df_i.drop(['zero', 'days'], axis=1, inplace=True)
        df_i['userID'] = userID
        frames = [df_final, df_i]
        df_final = pd.concat(frames)
    df_final.to_csv(r'E:\交通科研数据集\Geolife Trajectories 1.3' + '\\' + 'Result' + str(j)
                    + '.csv', header=False, index=False)
    df_final = pd.DataFrame(columns=('lat', 'lng', 'alt', 'date', 'time', 'userID'))


for i in [k for k in range(8) if k > 1]:
    with open(r'E:\交通科研数据集\Geolife Trajectories 1.3' + '\\' + 'Result1.csv', 'ab') as f:
        f.write(open(r'E:\交通科研数据集\Geolife Trajectories 1.3' + '\\' + 'Result' + str(i) + '.csv', 'rb').read())
```

- **步骤二：**将所有文件读取到python中去，利用缓存机制分块读取，代码如下：

  ```python
  import numpy as np
  import matplotlib.pyplot as plt
  import pandas as pd
  
  names = ['lat', 'lng', 'alt', 'date', 'time', 'userID']
  path = r'E:\交通科研数据集\Geolife Trajectories 1.3\trajectoryCombination.csv'
  chunks = []
  data = pd.read_csv(path, engine='c', iterator=True, header=6, names=names)
  loop = True
  chunkSize = 2500000
  index = 0
  while loop:
      try:
          print(index)
          chunk = data.get_chunk(chunkSize)
          chunks.append(chunk)
          index = index + 1
  
      except StopIteration:
          loop = False
          print("Iteration is stopped.")
  ```

- **步骤三：**进行数据预处理

- 1. 根据**时间范围**进行筛选

  - 将所有原始数据进行探索性数据分析，发现单周数据量最大的是[9.27-10.4]，双周数据量最大的是[11.3-11.16]，在这里将时间的范围扩大到了【9.27-10.7】
```python
import pandas as pd
from datetime import datetime


def parse_ymd(s):
    year_s, mon_s, day_s = s.split('-')
    return datetime(int(year_s), int(mon_s), int(day_s))


names = ['lat', 'lng', 'date', 'time', 'userID']
path = r'E:\交通科研数据集\Geolife Trajectories 1.3\未改变范围\trajectoryCombination.csv'
chunks = []
data = pd.read_csv(path, engine='c', iterator=True, header=6, names=names)
loop = True
chunkSize = 1000000
index = 0
while loop:
    try:
        print(index)
        chunk = data.get_chunk(chunkSize)
        chunks.append(chunk)
        index = index + 1

    except StopIteration:
        loop = False
        print("Iteration is stopped.")4
        
 for i in range(len(chunks)):
    chunks[i].loc[:, 'date'] = chunks[i].apply(lambda r: (parse_ymd(r['date'])), axis=1)
    chunks[i] = chunks[i][(chunks[i]['date'] >= datetime(2008, 9, 27)) & (chunks[i]['date'] <= datetime(2008, 10, 7))]
timeLimit = pd.concat(chunks)

filePath = r'E:\交通科研数据集\Geolife Trajectories 1.3\未改变范围\国庆时间筛选.csv'
timeLimit.to_csv(filePath, index=False)
```

- 2. 先将不合适的数据或者异常数据清除掉

  - **范围筛选：**经纬度不在北京范围内的晒出掉（经度范围：115.4°—117.5°）（纬度范围：39.4°—41.05°）24858301，剩余数据量20154986

```python
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from math import radians, cos, sin, asin, sqrt
from datetime import datetime

names = ['lat', 'lng', 'date', 'time', 'userID']
path = r'E:\交通科研数据集\Geolife Trajectories 1.3\未改变范围\国庆时间筛选.csv'
data = pd.read_csv(path, engine='c', header=6, names=names)
print('the original size of the data: {}'.format(len(data)))
# 进行数据处理：步骤一 将不在经纬度范围的数据筛选掉
data = data[((data['lat'] < 41.05) & (data['lat'] > 39.4) & (data['lng'] < 117.5) & (data['lng'] > 115.4))]
print('the data size filtered out by the boundary: {}'.format(len(data)))
```

- 计算相邻轨迹之间的距离**distance**与相邻点之间的时间差**Stime**

```python
data.loc[:, 'lat_1'] = data['lat'].shift(-1)
data.loc[:, 'lng_1'] = data['lng'].shift(-1)
data.loc[:, 'time_1'] = data['time'].shift(-1)
data = data.drop(data.index[len(data)-1])
# 计算上下两点之间的距离
data.loc[:, 'distance'] = data.apply(lambda r: (Haversine(r['lng'], r['lat'], r['lng_1'], r['lat_1'])), axis=1)
data.loc[:, 'Stime'] = data.apply(lambda r: (time2second(r['time_1']) - time2second(r['time'])), axis=1)
```
- 依据距离与时间差计算相邻点之间的速度**Speed**
```python
data.loc[:, 'Speed'] = data.apply(lambda r: (3600 * r['distance']/r['Stime']), axis=1)
```
- **时间与距离筛选：**将距离为0与时间为0的轨迹点筛出，表示静止不动的点

```python
data = data[((data['Stime'] != 0) & (data['distance'] != 0))]
```
- **速度筛选：**将速度在2km/h与70km/h的轨迹点筛出

```python
data = data[((data['Speed'] >= 2) & (data['Speed'] <= 70))]
```
- 
