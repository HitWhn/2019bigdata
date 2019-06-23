import pandas as pd
import datetime
import numpy as np
import os
import tqdm
import time
import dataprocessing


if __name__=='__main__':
    test_features=[]
    for filename in tqdm.tqdm(os.listdir(r'E:\2019bigData\2019bigdata\test_visit\test')):
        path = 'E:/2019bigData/2019bigdata/test_visit/test/' + filename
        feature_of_pertxt = []  # 每个文件提取的特征集合
        test_features.append(dataprocessing.getFeatures(path, feature_of_pertxt))
    dt = pd.DataFrame(test_features)
    #print(dt)
    dt.to_csv(r'E:\2019bigData\2019bigdata\test_visit_new_set.csv',index=False)
