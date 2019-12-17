from sklearn import preprocessing
import numpy as np
import scipy.sparse as sp
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import PolynomialFeatures
from sklearn.preprocessing import FunctionTransformer

print("Normalizer")
X = [[ 1., -1.,  2.],[ 2.,  0.,  0.],[ 0.,  1., -1.]]
X_normalized = preprocessing.normalize(X, norm='l2')
print(X_normalized)

normalizer = preprocessing.Normalizer().fit(X)
print(normalizer.transform(X))

print("OrdinalEncoder")
enc = preprocessing.OrdinalEncoder()
X = [['male', 'from US', 'uses Safari'], ['female', 'from Europe', 'uses Firefox']]
enc.fit(X)
print(enc.transform([['female', 'from US', 'uses Safari']]))

print("KBinsDiscretizer")
X = np.array([[ -3., 5., 15 ],[  0., 6., 14 ],[  6., 3., 11 ]])
est = preprocessing.KBinsDiscretizer(n_bins=[3, 2, 2], encode='ordinal').fit(X)
print(est.transform(X))

print("Binarizer")
binarizer = preprocessing.Binarizer().fit(X)
print(binarizer.transform(X))

print("SimpleImputer")
import pandas as pd
df = pd.DataFrame([["a", "x"],[np.nan, "y"],["a", np.nan],["b", "y"]], dtype="category")
imp = SimpleImputer(strategy="most_frequent")
print(imp.fit_transform(df))

print("PolynomialFeatures")
poly = PolynomialFeatures(2)
print(poly.fit_transform(X))

print("FunctionTransformer")
transformer = FunctionTransformer(np.log1p, validate=True)
X = np.array([[0, 1], [2, 3]])
print(transformer.transform(X))