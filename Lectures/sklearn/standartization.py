from sklearn import preprocessing
import numpy as np

X_train = np.array([[ 1., -1.,  2.],[ 2.,  0.,  0.],[ 0.,  1., -1.]])
X_scaled = preprocessing.scale(X_train)
print(X_scaled.mean(axis=0))
print(X_scaled.std(axis=0))
print(X_scaled)


#StandartScaler
scaler = preprocessing.StandardScaler().fit(X_train)
print("scaler mean = " + str(scaler.mean_))
print("scaler scale = " + str(scaler.scale_))
print(scaler.transform(X_train))

X_test = [[-1., 1., 0.]]
print(scaler.transform(X_test))

#Min Max scaler
min_max_scaler = preprocessing.MinMaxScaler()
X_train_minmax = min_max_scaler.fit_transform(X_train)
print(X_train_minmax)

#Max Abs Scaler
max_abs_scaler = preprocessing.MaxAbsScaler()
X_train_maxabs = max_abs_scaler.fit_transform(X_train)
print(X_train_maxabs)