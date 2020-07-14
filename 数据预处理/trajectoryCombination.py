import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import os
import gmplot

df_final = pd.DataFrame(columns=('lat', 'lng', 'date', 'time', 'userID'))
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
        df_i.drop(['zero', 'days', 'alt'], axis=1, inplace=True)
        df_i['userID'] = userID
        frames = [df_final, df_i]
        df_final = pd.concat(frames)
    df_final.to_csv(r'E:\交通科研数据集\Geolife Trajectories 1.3' + '\\' + 'Result' + str(j)
                    + '.csv', header=False, index=False)
    df_final = pd.DataFrame(columns=('lat', 'lng', 'date', 'time', 'userID'))


for i in [k for k in range(8) if k > 0]:
    with open(r'E:\交通科研数据集\Geolife Trajectories 1.3' + '\\' + 'trajectoryCombination.csv', 'ab') as f:
        f.write(open(r'E:\交通科研数据集\Geolife Trajectories 1.3' + '\\' + 'Result' + str(i) + '.csv', 'rb').read())
