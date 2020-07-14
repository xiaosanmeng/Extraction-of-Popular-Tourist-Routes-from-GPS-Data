import numpy as np
import matplotlib.pyplot as plt
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
        print("Iteration is stopped.")

'''
dateNum = []
for i in range(len(chunks)):
    dates = chunks[i]['date'].value_counts()
    dict_date = {'date': dates.index, 'value' + str(i): dates.values}
    df_date = pd.DataFrame(dict_date)
    dateNum.append(df_date)

result = dateNum[0]
for i in [k for k in range(len(dateNum)) if k > 0]:
    result = pd.merge(result, dateNum[i], how='outer', on=['date'])


result = result.fillna(0)
result.loc[:, 'Num'] = result.apply(lambda r: (r['value0'] + r['value1'] + r['value2'] + r['value3']), axis=1)
result = result.sort_values(by=['Num'], ascending=False)
filePath = r'E:\交通科研数据集\Geolife Trajectories 1.3\未改变范围\dateNum.csv'
result.to_csv(filePath, index=True)
result1 = result.head(100)
result1 = result1.set_index('date')
plt.figure(figsize=(30, 10))
result1['Num'].plot(color='r', kind='bar')
plt.savefig('1.png')
'''
# 第二步依据时间范围将需要的数据进行筛选出来，目标一是 2008.9.27到10.4日
for i in range(len(chunks)):
    chunks[i].loc[:, 'date'] = chunks[i].apply(lambda r: (parse_ymd(r['date'])), axis=1)
    chunks[i] = chunks[i][(chunks[i]['date'] >= datetime(2008, 9, 27)) & (chunks[i]['date'] <= datetime(2008, 10, 7))]
timeLimit = pd.concat(chunks)

filePath = r'E:\交通科研数据集\Geolife Trajectories 1.3\未改变范围\国庆时间筛选.csv'
timeLimit.to_csv(filePath, index=False)
