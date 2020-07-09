import pandas as pd
import numpy as np
from sklearn import preprocessing
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
from sklearn.svm import SVC, SVR
from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client.breast_cancer

class Model:
    def __init__(self):
        self.modelData1 = db["clinical"].find({"vital_status" : "dead"})
        self.dataFrame1 = pd.DataFrame(list(self.modelData1))
        self.modelData2 = db["clinical"].find({})
        self.dataFrame2 = pd.DataFrame(list(self.modelData2))
        self.rmse = 0
        self.accuracy = 0
        self.scaler = None

    def createModel1(self):
        labelencoder = preprocessing.LabelEncoder()
        self.dataFrame1['tumor_stage_cat'] = labelencoder.fit_transform(self.dataFrame1['tumor_stage'])
        features = np.array(self.dataFrame1[['age_at_diagnosis','tumor_stage_cat']]).astype(np.float)
        target = np.array(self.dataFrame1['days_to_death']).astype(np.float)

        train_features, test_features, train_target, test_target = train_test_split(features, target, random_state=50, test_size=0.1)

        self.set_scaler(train_features)
        train_features = self.scaler.transform(train_features)
        test_features = self.scaler.transform(test_features)

        svc = SVC(kernel="poly", C=0.2)
        svc.fit(train_features, train_target)
        predictions = svc.predict(test_features)

        self.set_mean_squared_error(self.calculate_mean_squared_error(predictions, test_target))
        self.set_accuracy_in_percents(self.calculate_accuracy_in_percents(predictions, test_target))
        
        return svc

    def createModel2(self):
        labelencoder = preprocessing.LabelEncoder()
        self.dataFrame2['tumor_stage_cat'] = labelencoder.fit_transform(self.dataFrame2['tumor_stage'])

        days_to_death_combined = []
        for i in range(0, len(self.dataFrame2['days_to_last_follow_up'])):
            if self.dataFrame2['vital_status'][i] == "dead":
                days_to_death_combined.append(self.dataFrame2['days_to_death'][i])
            else:
                days_to_death_combined.append(self.dataFrame2['days_to_last_follow_up'][i])
        self.dataFrame2['days_to_death_combined'] = days_to_death_combined

        features = np.array(self.dataFrame2[['age_at_diagnosis','tumor_stage_cat']]).astype(np.float)
        target = np.array(self.dataFrame2['days_to_death_combined']).astype(np.float)

        train_features, test_features, train_target, test_target = train_test_split(features, target, random_state=50, test_size=0.1)

        self.set_scaler(train_features)
        train_features = self.scaler.transform(train_features)
        test_features = self.scaler.transform(test_features)

        svr = SVR(kernel='rbf', C=1000, gamma=5, epsilon=10)
        svr.fit(train_features, train_target)
        predictions = svr.predict(test_features)

        self.set_mean_squared_error(self.calculate_mean_squared_error(predictions, test_target))
        
        return svr

    def set_scaler(self, train_features):
        scaler = preprocessing.StandardScaler()
        scaler.fit(train_features)
        self.scaler = scaler

    def normalize_data(self, data):
        return self.scaler.transform(data)

    def calculate_mean_squared_error(self, predictions, test_target):
        mse = mean_squared_error(test_target, predictions)
        rmse = np.sqrt(mse)

        return rmse

    def set_mean_squared_error(self, rmse):
        self.rmse = rmse

    def calculate_accuracy_in_percents(self, predictions, test_target):
        errors = abs(predictions - test_target)
        mape = 100 * (errors / test_target)
        accuracy = 100 - np.mean(mape)
    
        return round(accuracy, 2)

    def set_accuracy_in_percents(self, accuracy):
        self.accuracy = accuracy