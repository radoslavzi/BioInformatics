from sklearn import datasets
from sklearn import svm
import matplotlib.pyplot as plt

iris = datasets.load_iris()
#print(iris.data)

svc = svm.SVC()
#print(svc.fit(iris.data[:-3], iris.target[:-3]))

#print(svc.predict(iris.data[-3:]))

#data1 = datasets.load_digits()

#plt.figure(1, figsize=(3,3))
#plt.imshow(data1.images[-2], cmap=plt.cm.gray_r, interpolation='nearest')
#plt.show()


from sklearn import preprocessing
#import numpy as np

#scaler = preprocessing.StandardScaler().fit(iris.data[:10])
#print(scaler.transform(iris.data[:10]))


min_max = preprocessing.MinMaxScaler().fit(iris.data[:-1])
res = min_max.transform(iris.data[:-1])

print(svc.fit(res, iris.target[:-1]))

print(svc.predict(X=res[-1]))


#transformer = preprocessing.FunctionTransformer