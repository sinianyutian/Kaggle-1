# -*- coding: utf-8 -*-
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from sklearn.preprocessing import StandardScaler
from sklearn.cross_validation import train_test_split
from sklearn import cross_validation
from sklearn import linear_model
from sklearn import svm
from sklearn.ensemble import RandomForestClassifier
import time
from matplotlib.font_manager import FontProperties
font = FontProperties(fname=r"c:\windows\fonts\simsun.ttc", size=14)    # 解决windows环境下画图汉字乱码问题

# baseline：逻辑回归模型——0.75598
def baseline_logisticRegression():
    train_data = pd.read_csv(r"data/train.csv")
    #print u"数据信息：\n",train_data.info()
    #print u'数据描述：\n',train_data.describe()  
    #display_data(train_data)  # 简单显示数据信息
    #display_with_process(train_data) # 根据数据的理解，简单处理一下数据显示,验证猜想
    process_data = pre_processData(train_data,'process_train_data')  # 数据预处理，要训练的数据
    train_data = process_data.filter(regex='Survived|Age|SibSp|Parch|Fare|Cabin_.*|Embarked_.*|Sex_.*|Pclass_.*')  # 使用正则抽取想要的数据
    train_np = train_data.as_matrix()  # 转为矩阵
    '''训练model'''
    X = train_np[:,1:]
    y = train_np[:,0]
    #=X_train,X_test,y_train,y_test = train_test_split(X,y,test_size=0.2)
    #=model = linear_model.LogisticRegression(C=1.0,tol=1e-6).fit(X_train,y_train)
    model = linear_model.LogisticRegression(C=1.0,tol=1e-6).fit(X,y)
    print pd.DataFrame({"columns":list(train_data.columns)[1:],"coef_":list(model.coef_.T)})
    #=prediction = model.predict(X_test)
    #=cv_error = pd.DataFrame(data=list(X_test[np.where(prediction!=y_test)]),columns=list(train_data.columns)[1:])
    #=cv_error.to_csv(r'error.csv',index=True)
    #=print np.float32(np.sum(prediction == y_test))/np.float32(prediction.shape[0])
    
    '''测试集上预测'''
    test_data = pd.read_csv(r"data/test.csv")
    process_test_data = pre_processData(test_data,'process_test_data')  # 预处理数据
    test_data = process_test_data.filter(regex='Age|SibSp|Parch|Fare|Cabin_.*|Embarked_.*|Sex_.*|Pclass_.*')
    test_np = test_data.as_matrix()
    predict = model.predict(test_np)
    result = pd.DataFrame(data={'PassengerId':process_test_data['PassengerId'].as_matrix(),'Survived':predict.astype(np.int32)})
    result.to_csv(r'baseline_logisticRegression_result/prediction.csv',index=False)
    #clf = linear_model.LogisticRegression(C=1.0,tol=1e-6)
    #print cross_validation.cross_val_score(clf, X,y,cv=5)


# baseline：SVM模型——0.78947 
def baseline_svm():
    train_data = pd.read_csv(r"data/train.csv")
    print u"数据信息：\n",train_data.info()
    print u'数据描述：\n',train_data.describe()  
    #display_data(train_data)  # 简单显示数据信息
    #display_with_process(train_data) # 根据数据的理解，简单处理一下数据显示,验证猜想
    process_data = pre_processData(train_data,'process_train_data')  # 数据预处理，要训练的数据
    train_data = process_data.filter(regex='Survived|Age|SibSp|Parch|Fare|Cabin_.*|Embarked_.*|Sex_.*|Pclass_.*')  # 使用正则抽取想要的数据
    train_np = train_data.as_matrix()  # 转为矩阵
    '''训练model'''
    X = train_np[:,1:]
    y = train_np[:,0]
    model = svm.SVC(C=1.0,tol=1e-6).fit(X,y)
    # print pd.DataFrame({"columns":list(train_data.columns)[1:],"coef_":list(model.coef_.T)})
   
    '''测试集上预测'''
    test_data = pd.read_csv(r"data/test.csv")
    process_test_data = pre_processData(test_data,'process_test_data')  # 预处理数据
    test_data = process_test_data.filter(regex='Age|SibSp|Parch|Fare|Cabin_.*|Embarked_.*|Sex_.*|Pclass_.*')
    test_np = test_data.as_matrix()
    predict = model.predict(test_np)
    result = pd.DataFrame(data={'PassengerId':process_test_data['PassengerId'].as_matrix(),'Survived':predict.astype(np.int32)})
    result.to_csv(r'baseline_svm_result/prediction.csv',index=False)    
    
    

# baseline：随机森林模型——0.76077
def baseline_randomForest():
    train_data = pd.read_csv(r"data/train.csv")
    print u"数据信息：\n",train_data.info()
    print u'数据描述：\n',train_data.describe()  
    #display_data(train_data)  # 简单显示数据信息
    #display_with_process(train_data) # 根据数据的理解，简单处理一下数据显示,验证猜想
    process_data = pre_processData(train_data,'process_train_data',optimize=False)  # 数据预处理，要训练的数据
    train_data = process_data.filter(regex='Survived|Age|SibSp|Parch|Fare|Cabin_.*|Embarked_.*|Sex_.*|Pclass_.*')  # 使用正则抽取想要的数据
    train_np = train_data.as_matrix()  # 转为矩阵
    
    '''训练model'''
    X = train_np[:,1:]
    y = train_np[:,0] 
    X_train,X_test,y_train,y_test = train_test_split(X,y,test_size=0.2)
    
    model = RandomForestClassifier(n_estimators=100).fit(X,y)
    #predictions = model.predict(X_test)
    #print np.float32(np.sum(predictions == y_test))/np.float32(predictions.shape[0])
    '''预测'''
    test_data = pd.read_csv(r"data/test.csv")
    process_test_data = pre_processData(test_data,'process_test_data',optimize=False)  # 预处理数据
    test_data = process_test_data.filter(regex='Age|SibSp|Parch|Fare|Cabin_.*|Embarked_.*|Sex_.*|Pclass_.*')
    test_np = test_data.as_matrix()
    predict = model.predict(test_np)
    result = pd.DataFrame(data={'PassengerId':process_test_data['PassengerId'].as_matrix(),'Survived':predict.astype(np.int32)})
    result.to_csv(r'baseline_randomForest_result/prediction.csv',index=False)   
# baseline crossValidate：SVM模型———进行交叉验证：
def baseline_svm_crossValidate():
    origin_train_data = pd.read_csv(r"data/train.csv")
    process_data = pre_processData(origin_train_data,'process_train_data')  # 数据预处理，要训练的数据
    process_data_train,process_data_cv = train_test_split(process_data,test_size=0.2)   
    train_data = process_data_train.filter(regex='Survived|Age|SibSp|Parch|Fare|Cabin_.*|Embarked_.*|Sex_.*|Pclass_.*')  # 使用正则抽取想要的数据
    train_np = train_data.as_matrix()  # 转为矩阵
    '''训练model'''
    X_train = train_np[:,1:]
    y_train = train_np[:,0]
    model = svm.SVC(kernel='rbf',tol=1e-6).fit(X_train,y_train)
    #print pd.DataFrame({"columns":list(train_data.columns)[1:],"coef_":list(model.coef_.T)})
    cv_data = process_data_cv.filter(regex='Survived|Age|SibSp|Parch|Fare|Cabin_.*|Embarked_.*|Sex_.*|Pclass_.*')
    cv_np = cv_data.as_matrix()
    X_cv = cv_np[:,1:]
    y_cv = cv_np[:,0]
    predictions = model.predict(X_cv)
    print np.float32(np.sum(predictions == y_cv))/np.float32(predictions.shape[0])

    error_items = origin_train_data.loc[origin_train_data['PassengerId'].isin(process_data_cv[predictions != y_cv]['PassengerId'].values)]
    predictions_item = pd.DataFrame(data=process_data_cv[predictions != y_cv]['PassengerId'])
    predictions_item.columns=['error_PassengerId']
    # error_items = error_items.reset_index(drop=True)
    error_result = pd.concat([error_items,predictions_item],axis=1)
    error_result.to_csv(r'error.csv',index=False)
    
    
    '''测试集上预测'''
    '''test_data = pd.read_csv(r"data/test.csv")
    process_test_data = pre_processData(test_data,'process_test_data',optimize=False)  # 预处理数据
    test_data = process_test_data.filter(regex='Age|SibSp|Parch|Fare|Cabin_.*|Embarked_.*|Sex_.*|Pclass_.*')
    test_np = test_data.as_matrix()
    predict = model.predict(test_np)
    result = pd.DataFrame(data={'PassengerId':process_test_data['PassengerId'].as_matrix(),'Survived':predict.astype(np.int32)})
    result.to_csv(r'svm_result/prediction.csv',index=False)'''
    
    
    
# baseline crossValidate：逻辑回归模型——进行交叉验证
def baseline_logisticRegression_crossValidate():
    origin_train_data = pd.read_csv(r"data/train.csv")
    process_data = fe_preprocessData(origin_train_data,'process_train_data')  # 数据预处理，要训练的数据
    process_data_train,process_data_cv = train_test_split(process_data,test_size=0.2)
    train_data = process_data_train.filter(regex='Survived|Age|SibSp|Parch|Fare|Cabin_.*|Embarked_.*|Sex_.*|Pclass_.*')  # 使用正则抽取想要的数据
    train_np = train_data.as_matrix()  # 转为矩阵
    '''训练model'''
    X_train = train_np[:,1:]
    y_train = train_np[:,0]
    model = linear_model.LogisticRegression(C=1.0,tol=1e-6).fit(X_train,y_train)
    print pd.DataFrame({'columns':list(train_data.columns[1:]),'coef_':list(model.coef_.T)})
    
    cv_data = process_data_cv.filter(regex='Survived|Age|SibSp|Parch|Fare|Cabin_.*|Embarked_.*|Sex_.*|Pclass_.*')
    cv_np = cv_data.as_matrix()
    X_cv = cv_np[:,1:]
    y_cv = cv_np[:,0]
    predictions = model.predict(X_cv)
    print np.float32(np.sum(predictions == y_cv))/np.float32(predictions.shape[0])
    
    '''找到预测错的原始数据，并保存到文件'''
    error_items = origin_train_data.loc[origin_train_data['PassengerId'].isin(process_data_cv[predictions != y_cv]['PassengerId'].values)]
    predictions_item = pd.DataFrame(data=process_data_cv[predictions != y_cv]['PassengerId'])
    predictions_item.columns=['error_PassengerId']
    error_result = pd.concat([error_items,predictions_item],axis=1)
    error_result.to_csv(r'error.csv',index=False)
    
    #=print pd.DataFrame({"columns":list(train_data.columns)[1:],"coef_":list(model.coef_.T)})
    #=prediction = model.predict(X_test)
    #=print np.float32(np.sum(prediction == y_test))/np.float32(prediction.shape[0])    
    
    '''测试集上预测'''
    '''test_data = pd.read_csv(r"data/test.csv")
    process_test_data = fe_preprocessData(test_data,'process_test_data',optimize=True)  # 预处理数据
    test_data = process_test_data.filter(regex='Age|SibSp|Parch|Fare|Cabin_.*|Embarked_.*|Sex_.*|Pclass_.*')
    test_np = test_data.as_matrix()
    predict = model.predict(test_np)
    result = pd.DataFrame(data={'PassengerId':process_test_data['PassengerId'].as_matrix(),'Survived':predict.astype(np.int32)})
    result.to_csv(r'logisticRegression_result/prediction.csv',index=False)'''
    #clf = linear_model.LogisticRegression(C=1.0,tol=1e-6)
    #print cross_validation.cross_val_score(clf, X,y,cv=5)    
    
    

'''optimize: 逻辑回归模型——0.77033'''
def optimize_logisticRegression():
    train_data = pd.read_csv(r"data/train.csv")
    print u"数据信息：\n",train_data.info()
    print u'数据描述：\n',train_data.describe()  
    #display_data(train_data)  # 简单显示数据信息
    #display_with_process(train_data) # 根据数据的理解，简单处理一下数据显示,验证猜想
    process_data = fe_preprocessData(train_data,'process_train_data')  # 数据预处理，要训练的数据
    train_data = process_data.filter(regex='Survived|Age|SibSp|Parch|Fare|Cabin_.*|Embarked_.*|Sex_.*|Pclass_.*')  # 使用正则抽取想要的数据
    train_np = train_data.as_matrix()  # 转为矩阵
    '''训练model'''
    X = train_np[:,1:]
    y = train_np[:,0]
    #=X_train,X_test,y_train,y_test = train_test_split(X,y,test_size=0.2)
    #=model = linear_model.LogisticRegression(C=1.0,tol=1e-6).fit(X_train,y_train)
    model = linear_model.LogisticRegression(C=1.0,tol=1e-6).fit(X,y)
    print pd.DataFrame({"columns":list(train_data.columns)[1:],"coef_":list(model.coef_.T)})

    '''测试集上预测'''
    test_data = pd.read_csv(r"data/test.csv")
    process_test_data = fe_preprocessData(test_data,'process_test_data')  # 预处理数据
    test_data = process_test_data.filter(regex='Age|SibSp|Parch|Fare|Cabin_.*|Embarked_.*|Sex_.*|Pclass_.*')
    test_np = test_data.as_matrix()
    predict = model.predict(test_np)
    result = pd.DataFrame(data={'PassengerId':process_test_data['PassengerId'].as_matrix(),'Survived':predict.astype(np.int32)})
    result.to_csv(r'optimize_logisticRegression_result/prediction.csv',index=False)
    #clf = linear_model.LogisticRegression(C=1.0,tol=1e-6)
    #print cross_validation.cross_val_score(clf, X,y,cv=5)    
## 两项映射为多项式 
def mapFeature(X1,X2):
    degree = 2;                     # 映射的最高次方
    out = np.ones((X1.shape[0],1))  # 映射后的结果数组（取代X）
    '''
    这里以degree=2为例，映射为1,x1,x2,x1^2,x1*x2,x2^2
    '''
    for i in np.arange(1,degree+1): 
        for j in range(i+1):
            temp = X1**(i-j)*(X2**j)    #矩阵直接乘相当于matlab中的点乘.*
            out = np.hstack((out, temp.reshape(-1,1)))
    return out
  

## baseline：数据预处理  
def pre_processData(train_data,file_path):
    train_data.loc[(train_data.Age.isnull()), 'Age' ] = np.mean(train_data.Age)  # 为空的年龄补为平均年龄
    train_data.loc[(train_data.Cabin.notnull(),'Cabin')] = 'yes' # Cabin不为空的设为yes
    train_data.loc[(train_data.Cabin.isnull(),'Cabin')] = 'no'    
    '''0/1对应处理'''
    dummies_cabin = pd.get_dummies(train_data['Cabin'],prefix='Cabin')  # get_dummies返回对应的0/1格式的数据，有几类返回几列，prefix指定为Cabin
    dummies_Embarked = pd.get_dummies(train_data['Embarked'], prefix='Embarked')
    dummies_Sex = pd.get_dummies(train_data['Sex'], prefix='Sex')
    dummies_Pclass = pd.get_dummies(train_data['Pclass'],prefix='Pclass')
    train_data = pd.concat([train_data,dummies_cabin,dummies_Embarked,dummies_Pclass,dummies_Sex], axis=1)  # 拼接dataframe,axis=1为列
    train_data.drop(['Pclass','Name','Sex','Embarked','Cabin','Ticket'],axis=1,inplace=True)   # 删除之前没有处理的数据列            
    header_string = ','.join(train_data.columns.tolist())  # 将列名转为string，并用逗号隔开
    np.savetxt(file_path+r'/pre_processData1.csv', train_data, delimiter=',',header=header_string)  # 预处理数据保存到指定目录下    
    '''均值归一化处理(Age和Fare)'''
    scaler = StandardScaler()
    age_scaler = scaler.fit(train_data['Age'])
    train_data['Age'] = age_scaler.fit_transform(train_data['Age'])
    if np.sum(train_data.Fare.isnull()):  # 如果Fare中有为空的，就设为均值
        train_data.loc[(train_data.Fare.isnull(),'Fare')]=np.mean(train_data.Fare)
    fare_scaler = scaler.fit(train_data['Fare'])
    train_data['Fare'] = fare_scaler.transform(train_data['Fare'])
    header_string = ','.join(train_data.columns.tolist())  # 将列名转为string，并用逗号隔开
    np.savetxt(file_path+r'/pre_processData_scaled.csv', train_data, delimiter=',',header=header_string)  # 预处理数据保存到指定目录下    
    return train_data
    
    




## feature engineering：特征工程-预处理数据
def fe_preprocessData(train_data,file_path):
    if np.sum(train_data.Fare.isnull()):  # 如果Fare中有为空的，就设为均值
        train_data.loc[(train_data.Fare.isnull(),'Fare')]=np.mean(train_data.Fare)    
    '''年龄数据处理'''    
    age_train = train_data[['Age','SibSp','Parch','Fare','Pclass']]
    scaler_fare = StandardScaler()
    scaler_fare.fit(age_train.Fare)
    age_train['Fare'] = scaler_fare.transform(age_train.Fare)
    
    known_age = age_train[age_train.Age.notnull()].as_matrix()
    unknown_age = age_train[age_train.Age.isnull()].as_matrix()
    X_train_age = known_age[:,1:]
    y_train_age = known_age[:,0]
    X_test_age = unknown_age[:,1:]
    model = svm.SVR(C=1.0,kernel='rbf').fit(X_train_age,y_train_age)   # svm模型训练年龄
    y_test_predict = model.predict(X_test_age)
    train_data.loc[train_data.Age.isnull(),'Age'] = y_test_predict
    
    
    #train_data.loc[(train_data.Age.isnull()), 'Age' ] = np.mean(train_data.Age)  # 为空的年龄补为平均年龄
    train_data.loc[(train_data.Cabin.notnull(),'Cabin')] = 'yes' # Cabin不为空的设为yes
    train_data.loc[(train_data.Cabin.isnull(),'Cabin')] = 'no'    
    '''0/1对应处理'''
    dummies_cabin = pd.get_dummies(train_data['Cabin'],prefix='Cabin')  # get_dummies返回对应的0/1格式的数据，有几类返回几列，prefix指定为Cabin
    dummies_Embarked = pd.get_dummies(train_data['Embarked'], prefix='Embarked')
    dummies_Sex = pd.get_dummies(train_data['Sex'], prefix='Sex')
    dummies_Pclass = pd.get_dummies(train_data['Pclass'],prefix='Pclass')
    '''映射Sex_female和Pclass_1'''
    map_female_pclass = mapFeature(dummies_Sex['Sex_female'], dummies_Pclass['Pclass_1'])
    map_Sex_female_data = pd.DataFrame(data=map_female_pclass, columns=['Sex_female_1','Sex_female_2','Sex_female_3','Sex_female_4','Sex_female_5','Sex_female_6'])      
    '''映射Sex_male和Pclass_1'''
    map_male_pclass = mapFeature(dummies_Sex['Sex_male'], dummies_Pclass['Pclass_1'])
    map_Sex_male_data = pd.DataFrame(data=map_male_pclass, columns=['Sex_male_1','Sex_male_2','Sex_male_3','Sex_male_4','Sex_male_5','Sex_male_6'])      
    '''映射pclass3和cabin'''
    map_pclass3_cabin = mapFeature(dummies_Pclass['Pclass_3'], dummies_cabin['Cabin_no'])
    map_pclass3_cabin_data = pd.DataFrame(data=map_pclass3_cabin, columns=['Pclass_Cabin_1','Pclass_Cabin_2','Pclass_Cabin_3','Pclass_Cabin_4','Pclass_Cabin_5','Pclass_Cabin_6'])      

    train_data = pd.concat([train_data,dummies_cabin,dummies_Embarked,dummies_Pclass,dummies_Sex,map_Sex_female_data,map_Sex_male_data,map_pclass3_cabin_data], axis=1)  # 拼接dataframe,axis=1为列
    train_data.drop(['Pclass','Name','Sex','Embarked','Cabin','Ticket','Pclass_3','Cabin_no','Pclass_1','Sex_female','Sex_male'],axis=1,inplace=True)   # 删除之前没有处理的数据列        
    header_string = ','.join(train_data.columns.tolist())  # 将列名转为string，并用逗号隔开
    np.savetxt(file_path+r'/pre_processData1.csv', train_data, delimiter=',',header=header_string)  # 预处理数据保存到指定目录下    
    '''均值归一化处理(Age和Fare)'''
    scaler = StandardScaler()
    age_scaler = scaler.fit(train_data['Age'])
    train_data['Age'] = age_scaler.fit_transform(train_data['Age'])

    fare_scaler = scaler.fit(train_data['Fare'])
    train_data['Fare'] = fare_scaler.transform(train_data['Fare'])
    header_string = ','.join(train_data.columns.tolist())  # 将列名转为string，并用逗号隔开
    np.savetxt(file_path+r'/pre_processData_scaled.csv', train_data, delimiter=',',header=header_string)  # 预处理数据保存到指定目录下    
    return train_data    

## 简单显示数据
def display_data(train_data):
    plt.subplot(231)
    # plt.bar([train_data.Survived.value_counts().index],train_data.Survived.value_counts())
    train_data.Survived.value_counts().plot(kind='bar')  # 存活情况条形图，Survived里包含索引0/1
    '''kind : str
             ‘line’ : line plot (default)
             ‘bar’ : vertical bar plot
             ‘barh’ : horizontal bar plot
             ‘hist’ : histogram
             ‘box’ : boxplot
             ‘kde’ : Kernel Density Estimation plot
             ‘density’ : same as ‘kde’
             ‘area’ : area plot
             ‘pie’ : pie plot
             ‘scatter’ : scatter plot
             ‘hexbin’ : hexbin plot'''
    plt.title(u'存活情况(1为存活)',fontproperties=font)
    plt.grid()

    plt.subplot(232)
    train_data.Pclass.value_counts().plot(kind='bar')  # Pclass中包含索引1/2/3
    plt.grid()
    plt.title(u'3个等级存活情况',fontproperties=font)   

    plt.subplot(233)
    plt.scatter(train_data.Age,train_data.Survived)     # 年龄，是否存活，y坐标只有0/1
    plt.grid()
    plt.title(u'存活年龄分布',fontproperties=font)

    plt.subplot(234)
    plt.scatter(train_data.PassengerId,train_data.Age)  # 年龄的分布
    plt.grid()
    plt.title(u'年龄情况',fontproperties=font)

    plt.subplot(224)
    train_data.Age[train_data.Pclass == 1].plot(kind='kde',label=u'level 1')  # Pclass=1的年龄的密度图
    train_data.Age[train_data.Pclass == 2].plot(kind='kde',label=u'level 2')
    train_data.Age[train_data.Pclass == 3].plot(kind='kde',label=u'level 3')
    plt.grid()
    plt.xlabel(u'年龄',fontproperties=font)
    plt.ylabel(u'密度',fontproperties=font)
    plt.title(u'3个等级的年龄分布',fontproperties=font)
    plt.legend()
    plt.show()    
    
## 根据自己的理解简单处理显示一下数据
def display_with_process(train_data):
    '''显示（1）3个等级的死亡和存活的柱状对比图
           （2）死亡和存活的男女柱状对比图'''
    plt.subplot(1,2,1)
    survived_0 = train_data.Pclass[train_data.Survived == 0].value_counts().reindex([1,2,3]) # Pclass包含索引1/2/3，找到死亡的，注意重新索引一下，因为他会自动排序
    survived_1 = train_data.Pclass[train_data.Survived == 1].value_counts().reindex([1,2,3])

    index = np.array([1,2,3])
    bar_width=0.4
    plt.bar(index, survived_0,width=0.4,color='r',label=u'dead') # label对应查询的条件
    plt.bar(index+bar_width, survived_1,width=0.4,color='b',label=u'live')
    plt.xticks(index+bar_width,('Level 1','Level 2','Level 3'))
    plt.grid()
    plt.title(u'3个等级各自存活对比图',fontproperties=font)
    plt.legend(loc='best')
    
    plt.subplot(1,2,2)
    survived_male = train_data.Survived[train_data.Sex == 'male'].value_counts().reindex([0,1])  # Survived包含0/1,找到性别为male的
    survived_female = train_data.Survived[train_data.Sex == 'female'].value_counts().reindex([0,1])
    index = np.array([0,1])
    plt.bar(index, survived_male,width=0.4,color='r',label=u'male') # label对应查询的条件
    plt.bar(index+bar_width, survived_female,width=0.4,color='b',label=u'female')
    plt.grid()
    plt.xticks(index+bar_width,('dead','live'))
    plt.legend(loc='best')
    plt.show()
    '''显示（1）各个登录港口的死亡、存活柱状对比图'''
    plt.subplot(1,2,1)
    survived_0 = train_data.Embarked[train_data.Survived == 0].value_counts().reindex(['C','Q','S'])  #Embarked包含C/Q/S，
    survived_1 = train_data.Embarked[train_data.Survived == 1].value_counts().reindex(['C','Q','S'])
    index = np.array([1,2,3])
    plt.bar(index, survived_0, width=0.4,color='r',label='dead') # label对应查询的条件
    plt.bar(index+bar_width, survived_1, width=0.4,color='g',label='live')
    plt.grid()
    plt.xticks(index+bar_width,('C','Q','S'))
    plt.legend(loc='best')
    plt.title(u'登录港口存活情况',fontproperties=font)
    
    plt.subplot(1,2,2)
    survived_cabin = train_data.Survived[pd.notnull(train_data.Cabin)].value_counts().reindex([0,1])  # Survived包含所以0/1
    survived_nocabin = train_data.Survived[pd.isnull(train_data.Cabin)].value_counts().reindex([0,1])
    index = np.array([0,1])
    plt.bar(index, survived_cabin,width=0.4,color='g',label='cabin')  # label对应查询的条件
    plt.bar(index+bar_width, survived_nocabin, width=0.4,color='r',label='nocabin')
    plt.xticks(index+bar_width,('dead','live'))
    plt.grid()
    plt.title(u'有无cabin项的存活情况',fontproperties=font)
    plt.legend(loc='best')
    
    plt.show()
 
 


 
    
'''测试——异常检测，但实际不好'''    
def anomalyDetection():
    train_data = pd.read_csv(r"data/train.csv")
    process_data = pre_processData(train_data,'process_train_data')  # 数据预处理，要训练的数据
    train_data_filter = process_data.filter(regex='Survived|Age|SibSp|Parch|Fare|Cabin_.*|Embarked_.*|Sex_.*|Pclass_.*')  # 使用正则抽取想要的数据
    #train_data_filter.Pclass_3.plot(kind='kde')
    #plt.show()
    data = train_data_filter.as_matrix()
    anomaly_test_data = process_data.filter(regex='Survived|Age|SibSp|Parch|Fare')  
    other_attribute = pre_processData(train_data,'process_train_data').filter(regex='Survived|Cabin_.*|Embarked_.*|Sex_.*|Pclass_.*')  
    other_attribute_data = other_attribute.as_matrix()
    X_other = other_attribute_data[:,1:]
    y_other = other_attribute_data[:,0]
    other_model = linear_model.LogisticRegression(tol=1e-6).fit(X_other,y_other)    
    X_train = data[:,1:]
    y_train = data[:,0]
    anomaly_test = anomaly_test_data.as_matrix()
    X = anomaly_test[:,1:]
    y = anomaly_test[:,0]
    mu,Sigma2 = estimateGaussian(X)
    p = multivariateGaussian(X, mu, Sigma2)
    model = linear_model.LogisticRegression(C=1.0,tol=1e-6).fit(X_train,y_train)
    predictions = model.predict(X_train)
    print np.where(predictions!=y_train)
    print np.float32(np.sum(predictions == y_train))/np.float32(predictions.shape[0])
    train_data['yval'] = 0
    train_data.yval[train_data.ix[predictions != train_data.Survived.values,['Survived']].index]=1
    yval = train_data.yval.values
    Xval = X
    pval = multivariateGaussian(Xval, mu, Sigma2)
    epsilon,F1 = selectThreshold(yval, pval)
    print epsilon,F1
    train_data.to_csv(r'test.csv',index=False)
    '''测试集上预测'''
    test_data = pd.read_csv(r"data/test.csv")
    process_test_data = pre_processData(test_data,'process_test_data')  # 预处理数据
    test_data = process_test_data.filter(regex='Age|SibSp|Parch|Fare|Cabin_.*|Embarked_.*|Sex_.*|Pclass_.*')
    test_np = test_data.as_matrix()
    predict = model.predict(test_np)
    anomaly_data = process_test_data.filter(regex='Age|SibSp|Parch|Fare')    
    anomaly_data_np = anomaly_data.as_matrix()
    mu,Sigma2 = estimateGaussian(anomaly_data_np)
    p = multivariateGaussian(anomaly_data_np, mu, Sigma2)
    anomaly_prediction = np.ravel(np.array(np.where(p<epsilon)))
    
    for i in range(len(anomaly_prediction)):
        predict[i] = other_model.predict(test_np[anomaly_prediction[i],5:])
    #for i in range(len(anomaly_prediction)):
        #if predict[anomaly_prediction[i]] == 0 and test_np[i,0]<0 and test_np[i,-2]==1:
            #predict[anomaly_prediction[i]] = 1
        #elif predict[anomaly_prediction[i]] == 1 and test_np[i,0]>0 and test_np[i,-2]==0:
            #predict[anomaly_prediction[i]] = 0
        #else:
            #pass
    
    result = pd.DataFrame(data={'PassengerId':process_test_data['PassengerId'].as_matrix(),'Survived':predict.astype(np.int32)})
    result.to_csv(r'optimize_logisticRegression_result/prediction.csv',index=False)
# 参数估计函数（就是求均值和方差）
def estimateGaussian(X):
    m,n = X.shape
    mu = np.zeros((n,1))
    sigma2 = np.zeros((n,1))
    
    mu = np.mean(X, axis=0) # axis=0表示列，每列的均值
    sigma2 = np.var(X,axis=0) # 求每列的方差
    return mu,sigma2
   
# 多元高斯分布函数    
def multivariateGaussian(X,mu,Sigma2):
    k = len(mu)
    if (Sigma2.shape[0]>1):
        Sigma2 = np.diag(Sigma2)
    '''多元高斯分布函数'''    
    X = X-mu
    argu = (2*np.pi)**(-k/2)*np.linalg.det(Sigma2)**(-0.5)
    p = argu*np.exp(-0.5*np.sum(np.dot(X,np.linalg.inv(Sigma2))*X,axis=1))  # axis表示每行
    return p


# 选择最优的epsilon，即：使F1Score最大    
def selectThreshold(yval,pval):
    '''初始化所需变量'''
    bestEpsilon = 0.
    bestF1 = 0.
    F1 = 0.
    step = (np.max(pval)-np.min(pval))/1000
    '''计算'''
    for epsilon in np.arange(np.min(pval),np.max(pval),step):
        cvPrecision = pval<epsilon
        tp = np.sum((cvPrecision == 1) & (yval == 1)).astype(float)  # sum求和是int型的，需要转为float
        fp = np.sum((cvPrecision == 1) & (yval == 0)).astype(float)
        fn = np.sum((cvPrecision == 1) & (yval == 0)).astype(float)
        precision = tp/(tp+fp)  # 精准度
        recision = tp/(tp+fn)   # 召回率
        F1 = (2*precision*recision)/(precision+recision)  # F1Score计算公式
        if F1 > bestF1:  # 修改最优的F1 Score
            bestF1 = F1
            bestEpsilon = epsilon
    return bestEpsilon,bestF1



# 主函数
if __name__ == '__main__':
    '''baseline model'''
    #baseline_logisticRegression()
    baseline_svm()
    #baseline_randomForest()
    '''优化model'''
    #optimize_logisticRegression()
    '''调优测试'''
    #anomalyDetection()

