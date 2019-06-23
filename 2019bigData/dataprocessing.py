import pandas as pd
import datetime
import numpy as np
import os
import tqdm

def cal_user_count(user_behavior):
    return len(user_behavior)

def collect_all_records(user_behavior):
    records=[]
    date=[]
    time=[]
    for r in user_behavior:
        records.append(r.split(','))
        tmp_date=[]
        tmp_time=[]
        for each_r in r.split(','):
            tmp=each_r.split('&')
            tmp_date.append(tmp[0])
            tmp_time.append(tmp[1])
        date.append(tmp_date)
        time.append(tmp_time)
    return records,date,time

def cal_interval(time1,time2):
    y1,y2=int(time1[:4]),int(time2[:4])
    m1=int(time1[4:6]) if time1[4]!='0' else int(time1[5])
    m2=int(time2[4:6]) if time2[4]!='0' else int(time2[5])
    d1=int(time1[6:]) if time1[6]!='0' else int(time1[7])
    d2=int(time2[6:]) if time2[6]!='0' else int(time2[7])
    return (datetime.datetime(y2,m2,d2) - datetime.datetime(y1,m1,d1)).days

def cal_visit_interval(date_of_perrecord):
    result=[]
    for date in date_of_perrecord:
        tmp=[]
        if len(date)==1:
            tmp.append(180)
            result.append(tmp)
        for i in range(len(date)-1):
            st=date[i]
            nd=date[i+1]
            interval=cal_interval(st,nd)
            tmp.append(interval)
        result.append(tmp)
    return result

def cal_visit_time(time_of_perrecord):
    visit_time_of_perrecord=[]
    for time in time_of_perrecord:
        tmp=[]
        for i in time:
            tmp.append(len(i.split('|')))
        visit_time_of_perrecord.append(tmp)
    return visit_time_of_perrecord

def cal_closest_interval(visit_interval_of_perrecord):
    result=min(visit_interval_of_perrecord[0])
    count=0
    #mean_result=[]
    for record in visit_interval_of_perrecord:
        #mean_result.append(round(np.mean(record),2))
        if min(record)==result:
            count+=1
        if min(record)<result:
            result=min(record)
            count=1
    #print(result,count,len(visit_interval_of_perrecord),sep='\n')
    return result,round(count/len(visit_interval_of_perrecord),2)

def cal_MeanAndVar_of_interval(visit_interval_of_perrecord):
    mean_result=[]
    var_result=[]
    for record in visit_interval_of_perrecord:
        narray=np.array(record)
        mean_result.append(round(narray.mean(),2))
        var_result.append(round(narray.var(),2))
    return mean_result,var_result

def cal_MeanQuantile_of_interval(mean_interval_of_perrecord):
    mean=round(np.mean(mean_interval_of_perrecord),2)
    feature_array=[]
    quantile_array=[10,25,50,75,90]
    for i in quantile_array:
        feature_array.append(round(np.percentile(mean_interval_of_perrecord,i),2))
    return mean,feature_array

def cal_VarQuantile_of_interval(var_interval_of_perrecord):
    mean = round(np.mean(var_interval_of_perrecord), 2)
    feature_array = []
    quantile_array = [10, 25, 50, 75, 90]
    for i in quantile_array:
        feature_array.append(round(np.percentile(var_interval_of_perrecord, i), 2))
    return mean, feature_array

def cal_MeanAndVar_of_visitTime(visit_time_of_perrecord):
    mean_result = []
    var_result = []
    for record in visit_time_of_perrecord:
        narray = np.array(record)
        mean_result.append(round(narray.mean(), 2))
        var_result.append(round(narray.var(), 2))
    return mean_result, var_result
    return

def cal_MeanQuantile_of_time(mean_visitTime_of_perrecord):
    mean = round(np.mean(mean_visitTime_of_perrecord), 2)
    feature_array = []
    quantile_array = [10, 25, 50, 75, 90]
    for i in quantile_array:
        feature_array.append(round(np.percentile(mean_visitTime_of_perrecord, i), 2))
    return mean, feature_array

def cal_VarQuantile_of_time(var_visitTime_of_perrecord):
    mean = round(np.mean(var_visitTime_of_perrecord), 2)
    feature_array = []
    quantile_array = [10, 25, 50, 75, 90]
    for i in quantile_array:
        feature_array.append(round(np.percentile(var_visitTime_of_perrecord, i), 2))
    return mean, feature_array

def change_date(date):
    y = int(date[:4])
    m = int(date[4:6]) if date[4] != '0' else int(date[5])
    d = int(date[6:]) if date[6] != '0' else int(date[7])
    #return datetime.datetime(y,m,d).strftime("%w")
    return y,m,d

def check_dorn(hour):
    dic={'00':0,'01':0,'02':0,'03':1,'04':1,'05':1,'06':1,'07':2,'08':2,'09':2,'10':2,'11':3
    ,'12':3,'13':3,'14':3,'15':4,'16':4,'17':4,'18':4,'19':5,'20':5,'21':5,'22':5,'23':0}
    result=[]
    for time in hour:
        if dic[time] not in result:
            result.append(dic[time])
    return result

def cal_total_hours(hour):
    total=len(hour)
    if total<=1:
        return 0
    elif total<=3:
        return 1
    elif total<=8:
        return 2
    elif total<=12:
        return 3
    elif total<=24:
        return 4

def check_special_day(day):
    #【十月一号、十月七号、十月1-7号、平安夜、圣诞节、元旦第一天、第二天、第三天、
    # 小年、28、29、除夕、初一到初七、初七、情人节、正月十五、妇女节】
    dic = {'20181001':[0,2],'20181002':[2],'20181003':[2],'20181004':[2],'20181005':[2],'20181006':[2],'20181007':[1,2],
           '20181224':[3],'20181225':[4],'20181230':[5],'20181231':[6],'20190101':[7],'20190128':[8],'20190202':[9],
           '20190203':[10],'20190204':[11],'20190205':[12],'20190206':[12],'20190207':[12],'20190208':[12],
           '20190209':[12],'20190210':[12],'20190211':[12,13],'20190214':[14],'20190219':[15],'20190308':[16]}
    if day in dic:
        return dic[day]
    else:
        return []

def count_MonthDayHours(date_of_perrecord,time_of_perrecord):
    weak=[0]*7
    month=[0]*12
    day_or_night=[0]*6
    total_hours=[0]*5
    special_day=[0]*17
    count_visit=0
    # for date,time in zip(date_of_perrecord,time_of_perrecord):
    #     count_visit.append(len(date))
    #     for day,hours in zip(date,time):
    #         y,m,d=change_date(day)
    #         weak[int(datetime.datetime(y,m,d).strftime("%w"))]+=1
    #         month[m-1]+=1
    #         hour=hours.split('|')
    #         dorn=check_dorn(hour)
    #         for rs in dorn:
    #             day_or_night[rs]+=1
    #         th=cal_total_hours(hour)
    #         total_hours[th]+=1
    # mean=np.mean(count_visit)
    # quantile_array = []
    # for i in [10, 25, 50, 75, 90]:
    #     quantile_array.append(round(np.percentile(count_visit, i), 2))
    # return weak,month,day_or_night,total_hours,mean,quantile_array
    for date in date_of_perrecord:
        count_visit+=len(date)
        for day in date:
            sp_day=check_special_day(day)
            if len(sp_day)!=0:
                for rs in sp_day:
                    special_day[rs]+=1
    return list(np.around(np.array(special_day)/count_visit,decimals=4))


def ToRatio(feature):
    return list(np.around((np.array(feature)/np.array(feature).sum()),decimals=2))

def getFeatures(path,features):
    user_behavior = pd.read_csv(path, sep='\t', header=None)
    user_behavior.rename(columns={0: 'userID', 1: 'behavior'}, inplace=True)
    user_behavior = user_behavior['behavior']
    #user_behavior = user_behavior['behavior'].head()

    user_count = cal_user_count(user_behavior)  # 到访总人数
    # print(user_count)

    all_records, date_of_perrecord, time_of_perrecord = collect_all_records(user_behavior)
    #print(all_records,date_of_perrecord,time_of_perrecord,sep='\n')

    # visit_interval_of_perrecord = cal_visit_interval(date_of_perrecord)  # 每人每对相邻到访记录的时间间隔
    # #print(visit_interval_of_perrecord)
    #
    # feature1, feature2 = cal_closest_interval(visit_interval_of_perrecord)
    # # 这两个分别是最短间隔，及其所占所有记录的比例
    # # print(feature1,feature2)
    # features.append(feature1)
    # features.append(feature2)
    #
    # mean_interval_of_perrecord, var_interval_of_perrecord = cal_MeanAndVar_of_interval(visit_interval_of_perrecord)
    # # 计算每人每对相邻访客记录的时间间隔的均值和方差
    # # print(mean_interval_of_perrecord,var_interval_of_perrecord,sep='\n')
    #
    # feature3, feature4_8 = cal_MeanQuantile_of_interval(mean_interval_of_perrecord)  # （每人每对相邻到访记录的时间间隔的均值）的均值，以及分位数
    # # print(feature3,feature4_8)
    # features.append(feature3)
    # features.extend(feature4_8)
    #
    # feature9, feature10_14 = cal_VarQuantile_of_interval(var_interval_of_perrecord)  # （每人每对相邻到访记录的时间间隔的方差）的均值，以及分位数
    # # print(feature9,feature10_14)
    # features.append(feature9)
    # features.extend(feature10_14)
    #
    # visit_time_of_perrecord = cal_visit_time(time_of_perrecord)  # 每人每次的到访时间时长
    # # print(visit_time_of_perrecord)
    #
    # mean_visitTime_of_perrecord, var_visitTime_of_perrecord = cal_MeanAndVar_of_visitTime(
    #     visit_time_of_perrecord)  # 每人每次到访时间的均值和方差
    # # print(mean_visitTime_of_perrecord,var_visitTime_of_perrecord,sep='\n')
    #
    # feature15, feature16_20 = cal_MeanQuantile_of_time(mean_visitTime_of_perrecord)  # （每人每次到访时间的均值）的均值和分位数
    # # print(feature15,feature16_20)
    # features.append(feature15)
    # features.extend(feature16_20)
    #
    # feature21, feature22_26 = cal_VarQuantile_of_time(var_visitTime_of_perrecord)  # （每人每次到访时间的方差）的均值和分位数
    # # print(feature21,feature22_26)
    # features.append(feature21)
    # features.extend(feature22_26)

    # feature27_33, feature34_45, feature46_51, feature52_56, feature57, feature58_62 = count_MonthDayHours(
    #     date_of_perrecord, time_of_perrecord)
    #
    # feature27_33 = ToRatio(feature27_33)
    # feature34_45 = ToRatio(feature34_45)
    # feature46_51 = ToRatio(feature46_51)
    # feature52_56 = ToRatio(feature52_56)
    # # print(feature27_33,feature34_45,feature46_51,feature52_56,feature57,feature58_62,sep='\n')
    # features.extend(feature27_33)
    # features.extend(feature34_45)
    # features.extend(feature46_51)
    # features.extend(feature52_56)
    # features.append(feature57)
    # features.extend(feature58_62)
    feature63_79=count_MonthDayHours(date_of_perrecord,time_of_perrecord)
    features.extend(feature63_79)
    #print(features)
    #print(len(features))
    #print('--------------------------------------------------')
    return features

# if __name__=='__main__':
#     train_features=[]
#     for filename in tqdm.tqdm(os.listdir(r'E:\2019bigData\2019bigdata\train_visit\train')):
#         path = 'E:/2019bigData/2019bigdata/train_visit/train/' + filename
#         feature_of_pertxt = []  # 每个文件提取的特征集合
#         category = int(filename[9])  # target目标特征
#         feature_of_pertxt.append(category)
#         train_features.append(getFeatures(path,feature_of_pertxt))
#     dt=pd.DataFrame(train_features)
#     #print(dt)
#     dt.to_csv(r'E:\2019bigData\2019bigdata\train_visit_set.csv',index=False)
if __name__=='__main__':
    train_features=[]
    for filename in tqdm.tqdm(os.listdir(r'E:\2019bigData\2019bigdata\train_visit\train')):
        path = 'E:/2019bigData/2019bigdata/train_visit/train/' + filename
        feature_of_pertxt = []  # 每个文件提取的特征集合
        train_features.append(getFeatures(path,feature_of_pertxt))
    dt=pd.DataFrame(train_features)
    #print(dt)
    dt.to_csv(r'E:\2019bigData\2019bigdata\train_visit_new_set.csv',index=False)



