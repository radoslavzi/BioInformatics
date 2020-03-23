from sklearn import datasets
from sklearn import svm

iris = datasets.load_iris()
digits = datasets.load_digits()

print(digits.data)
print(digits.target)

clf = svm.SVC(gamma=0.001, C=100.)
print(clf.fit(digits.data[:-1], digits.target[:-1]))
print(clf.predict(digits.data[-1:]))



import matplotlib.pyplot as plt

#Load the digits dataset
digits = datasets.load_digits()

#Display the first digit
plt.figure(1, figsize=(3, 3))
plt.imshow(digits.images[-1], cmap=plt.cm.gray_r, interpolation='nearest')
plt.show()
