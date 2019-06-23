import datetime
import string
import numpy as np
import os
for filename in os.listdir(r'E:\2019bigData\2019bigdata\train_visit\new'):
    print(filename)

# print( (datetime.datetime(2008,3,1) - datetime.datetime(2008,2,28)).days)

#a=1 if 3>4 else a=2
#print(a)
# score=80
# a=1 if score < 60 else 2
# print(a)

# def cal_interval(time1,time2):
#     y1,y2=int(time1[:4]),int(time2[:4])
#     m1=int(time1[4:6]) if time1[4]!='0' else int(time1[5])
#     m2=int(time2[4:6]) if time2[4]!='0' else int(time2[5])
#     d1=int(time1[6:]) if time1[6]!='0' else int(time1[7])
#     d2=int(time2[6:]) if time2[6]!='0' else int(time2[7])
#     return (datetime.datetime(y2,m2,d2) - datetime.datetime(y1,m1,d1)).days
#
# #print(cal_interval('20080101','20080101'))
# array=[1,0,2]
# print(min(array))
# print(1/3)
#
#
# a=np.array(([50,40,60,70,30]))
# print(round(np.median(a),4))#中位数
# aa=np.percentile(a,(25,50,75))#95%分位数
# for i in range(len(aa)):
#     print(aa[i])
# l1=[13.43, 23.33, 2.64, 64.0, 3.89]
# l2=[3.14, 3.89, 13.43, 23.33, 47.73]
# for i,j in zip(l1,l2):
#     print(i,j)
# l3=[0]*5
# l3[0]=1
# print(l3)
# print(type(datetime.datetime(2018,1,13).strftime("%w")))
# print(datetime.datetime(2018,1,14).strftime("%m"))
# print(np.array(l1).sum())
# l4=[2,4,6]
# print(np.array(l4)/2)
l=[1,2,3,4]
print(np.array(l)/4)
