import pandas as pd
from sklearn import preprocessing
from sklearn.ensemble import GradientBoostingClassifier
import tqdm
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import accuracy_score
import time


dt=pd.read_csv(r'E:\2019bigData\2019bigdata\train_visit_set.csv')
#print(dt['0'].value_counts())
dt=dt.ix[:,1:]
train_y=dt.ix[:,:1]

x=dt.ix[:,1:]
std_scale=preprocessing.StandardScaler().fit(x)
train_x=std_scale.transform(x)

start_time=time.time()

# gbm0=GradientBoostingClassifier(random_state=10)
# gbm0.fit(train_x,train_y.values.ravel())
# y_pred=gbm0.predict(train_x)
# print('gbm0:',accuracy_score(train_y,y_pred))


param_test1={'n_estimators':range(20,201,10)}
gsearch1 = GridSearchCV(estimator = GradientBoostingClassifier(learning_rate=0.1, min_samples_split=300,
                                  min_samples_leaf=20,max_depth=8,max_features='sqrt', subsample=0.8,random_state=10),
                       param_grid = param_test1, scoring='accuracy',iid=False,cv=5)
# gsearch1.fit(train_x,train_y.values.ravel())
# print(gsearch1.best_params_,gsearch1.best_score_,sep='\n')

param_test2 = {'max_depth':range(3,14,2), 'min_samples_split':range(100,801,200)}
gsearch2 = GridSearchCV(estimator = GradientBoostingClassifier(learning_rate=0.1, n_estimators=200, min_samples_leaf=20,
      max_features='sqrt', subsample=0.8, random_state=10),
   param_grid = param_test2, scoring='accuracy',iid=False, cv=5)
gsearch2.fit(train_x,train_y.values.ravel())
print(gsearch2.best_params_,gsearch2.best_score_,sep='\n')




# dt_test=pd.read_csv(r'E:\2019bigData\2019bigdata\test_visit_set.csv')
# test_x=std_scale.transform(dt_test.ix[:,1:])
# test_y=rf0.predict(test_x)
#
# f = open("RF_result_m0.txt", "w+")
# for index in range(10000):
#     result = test_y[index]
#     f.write("%s \t %03d\n"%(str(index).zfill(6), result))
# f.close()

end_time=time.time()
print(end_time-start_time)