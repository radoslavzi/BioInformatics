from sklearn import svm
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
import numpy as np

X = [[0, 0], [2, 2]]
y = [0.5, 2.5]
clf = svm.SVR()
clf.fit(X, y)

clf.predict([[1, 1]])

from sklearn.datasets import load_boston
data = load_boston()
print(data.keys())
plt.hist(data.target)
plt.xlabel('price ($1000s)')
plt.ylabel('count')
plt.show()

X_train, X_test, y_train, y_test = train_test_split(data.data, data.target)
clf = LinearRegression()
clf.fit(X_train, y_train)
predicted = clf.predict(X_test)
expected = y_test
plt.scatter(expected, predicted)
plt.plot([0, 50], [0, 50], '--k')
plt.axis('tight')
plt.xlabel('True price ($1000s)')
plt.ylabel('Predicted price ($1000s)')
plt.show()
print("RMS:", np.sqrt(np.mean((predicted - expected) ** 2)))


print("IRIS dataset")
from sklearn import datasets

svc = svm.SVC(kernel='linear')
iris = datasets.load_iris()
X = iris.data[:, :2]
y = iris.target
svc.fit(X, y)

import plot_estimator as plt_est

plt_est.plot_estimator(svc, X, y, plt)
plt_est.plot_estimator(svm.LinearSVC(), X, y, plt)

X, y = X[np.in1d(y, [1, 2])], y[np.in1d(y, [1, 2])]
plt_est.plot_estimator(svc, X, y, plt)

svc = svm.SVC(kernel='linear', C=1e3)
plt_est.plot_estimator(svc, X, y, plt)

svc = svm.SVC(kernel='linear', C=1e-3)
plt_est.plot_estimator(svc, X, y, plt)

svc = svm.SVC(kernel='poly', degree=4)
plt_est.plot_estimator(svc, X, y, plt)
plt.scatter(svc.support_vectors_[:, 0], svc.support_vectors_[:, 1], s=80, facecolors='none', zorder=10)
plt.title('Polynomial kernel')

svc = svm.SVC(kernel='rbf', gamma=1e2)
plt_est.plot_estimator(svc, X, y, plt)
plt.scatter(svc.support_vectors_[:, 0], svc.support_vectors_[:, 1], s=80, facecolors='none', zorder=10)
plt.title('RBF kernel')

plt.show()