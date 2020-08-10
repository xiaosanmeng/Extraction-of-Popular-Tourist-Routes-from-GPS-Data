"""板块三：进行轨迹相似度衡量"""
"""1.DTW距离计算"""
"""2.EMD计算，采用相关的集成的函数scipy.stats中的EMD计算函数"""
"""详情请查阅网站：https://blog.csdn.net/yeziand01/article/details/84404383"""
'''
'''


def img_to_sig(arr):
    """Convert a 2D array to a signature for cv2.EMD"""

    # cv2.EMD requires single-precision, floating-point input
    sig = np.empty((arr.size, 3), dtype=np.float32)
    count = 0
    for i in range(arr.shape[0]):
        for j in range(arr.shape[1]):
            sig[count] = np.array([arr[i, j], i, j])
            count += 1
    return sig


dtw_Matrix = np.zeros([len(group_key), len(group_key)])
EMD_Matrix = np.zeros([len(group_key), len(group_key)])
for i in tqdm(range(len(group_key))):
    traj1 = sparseRoute_info[(sparseRoute_info['userID'] == group_key[i][0]) & (
            sparseRoute_info['date'] == group_key[i][1])]
    signature1 = img_to_sig(np.array(traj1[['Stime', 'x', 'y']].values.tolist()))
    for j in tqdm(range(len(group_key))):
        if i > j:
            traj2 = sparseRoute_info[(sparseRoute_info['userID'] == group_key[j][0]) & (
                    sparseRoute_info['date'] == group_key[j][1])]
            signature2 = img_to_sig(np.array(traj2[['Stime', 'x', 'y']].values.tolist()))
            EMD_Matrix[i][j] = cv2.EMD(signature1, signature2, cv2.DIST_L2, cost=None, lowerBound=0)[0]
            EMD_Matrix[j][i] = EMD_Matrix[i][j]
            dtw_Matrix[i][j] = dtw_distance(traj1[['x', 'y']].values.tolist(),
                                            traj2[['x', 'y']].values.tolist())
            dtw_Matrix[j][i] = dtw_Matrix[i][j]

"""板块三：将EMD距离与DTW距离归一化"""
"""EMD的归一化：1-x/xmax"""
# EMD_Matrix = np.where(EMD_Matrix >= 0, EMD_Matrix, 1)
EMD_Matrix = 1 - abs(EMD_Matrix)
dtw_Matrix = 1 - dtw_Matrix / dtw_Matrix.max()
trajsim = EMD_Matrix * dtw_Matrix
