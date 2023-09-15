from os import getcwd
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import seaborn as sn
from imblearn.under_sampling import RandomUnderSampler
from matplotlib import rcParams
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_selection import SelectFromModel
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (accuracy_score, classification_report,
                             confusion_matrix, f1_score)
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score

class CustomerChurn:
    def __init__(self):
        self.seed = 145

        self.x_train = None
        self.x_test = None

        self.y_train = None
        self.y_test = None

        # self.model = LogisticRegression(random_state=self.seed, n_jobs=-1, max_iter=1000)
        self.model = LogisticRegression(C=1, penalty='l2', solver="newton-cg", class_weight={1: 0.4, 0:0.6})
        self.train()
        

    @staticmethod
    def encode_data(dataset):
        encoded_data = dataset.copy()
        encoded_data['TotalCharges'] = encoded_data['TotalCharges'].replace(to_replace=' ', value='0')
        encoded_data['TotalCharges'] = pd.to_numeric(dataset['TotalCharges'], errors='ignore')
        for i in dataset.columns:
            if encoded_data[i].dtype.name == 'object':
                encoder = LabelEncoder()
                encoded_data[i] = encoder.fit_transform(encoded_data[i])
        return encoded_data

    def random_undersample(self, x, y):
        rus = RandomUnderSampler(random_state=self.seed)
        x_resampled, y_resampled = rus.fit_resample(x,y)
        self.x_train, self.x_test, self.y_train, self.y_test = train_test_split(x_resampled,y_resampled, test_size=.25)

    def train(self, dataset=None):
        if dataset is None:
            dataset = pd.read_csv(f'{getcwd()}\\custonova_app\\scripts\\data\\logistic_data\\train.csv')
        # encode the data
        self.encoded_data = self.encode_data(dataset)
        # split the data into x and y
        x = self.encoded_data.drop(['Churn'], axis=1)
        y = self.encoded_data['Churn']
        # random under sample the data
        self.random_undersample(x, y)
        # train the model
        self.model.fit(self.x_train, self.y_train)
        y_true = self.y_test
        y_pred = self.model.predict(self.x_test)
        return {
            'accuracy_score': accuracy_score(y_true, y_pred),
            'f1_score': f1_score(y_true, y_pred),
            'precision_score': precision_score(y_true, y_pred),
            'recall_score': recall_score(y_true, y_pred),
        }

    def predict(self, dataset = None):
        
        if dataset is None:
            return

        encoded_data = self.encode_data(dataset)
        # results = dataset.copy()
        prob = self.model.predict_proba(encoded_data)[:, 1]
        pred = self.model.predict(encoded_data)

        # probabs = pd.DataFrame(prob)
        # preds = pd.DataFrame(pred)

        # prob_data = [
        #     len(probabs[(probabs >= 0) & (probabs <= 49)]),
        #     len(probabs[(probabs >= 50) & (probabs <= 69)]),
        #     len(probabs[(probabs >= 70) & (probabs <= 100)])
        # ]

        # preds_data = [
        #     len(preds[preds == 1]),
        #     len(preds[preds == 1]),
        # ]
        
        # pred_labels = ['1', '0']
        # probs_labels = ['0% - 49%', '50% - 69%', '70% - 100%']
        # print(preds_data)
        # print(preds_data)
        return {
            'probability': list(prob),
            'predictions': list(pred),
            
        }
        
        # return results

    def performance(self, data):
        y_true = LabelEncoder().fit_transform(data['Churn'])
        x = data.drop(['Churn'], axis=1)
        y_pred = self.model.predict(self.encode_data(x))
        return {
            'accuracy_score': accuracy_score(y_true, y_pred),
            'f1_score': f1_score(y_true, y_pred),
            'precision_score': precision_score(y_true, y_pred),
            'recall_score': recall_score(y_true, y_pred),
        }
        
    def evaluate(self):
        pass
