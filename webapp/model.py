# -*- coding: utf-8 -*-
"""model.py
"""

import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
from sklearn.preprocessing import StandardScaler
from sklearn import svm


class FakeAccClassifier():
    X_train = None
    y_train = None
    scaler = StandardScaler()
    clf = svm.NuSVC(max_iter=1500)

    def __init__(self):
        # Preprocess training data
        data_train = pd.read_csv('../datasets/train.csv', header=None)
        ini_train = np.array(data_train.iloc[1:, :11])
        self.X_train = self.preprocess(ini_train, True)
        self.y_train = np.array(data_train.iloc[1:, 11])

        # Fit model to data
        self.clf.fit(self.X_train, self.y_train)

        # data_test = pd.read_csv('../datasets/test.csv', header=None)
        # ini_test = np.array(data_test.iloc[1:,:11])
        # X_test = self.preprocess(ini_test, True)
        # y_test = np.array(data_test.iloc[1:,11])
        # print(self.clf.score(X_test, y_test))

    def predict(self, ar):
        data = np.reshape(ar, (1, -1))
        data = self.scaler.transform(data)
        print("Data: ", ar)

        # Get prediction from model
        tmp = self.clf.predict(data)
        tmp = tmp.astype(float)
        pred = tmp[0]
        print("Predictions: ", pred)
        if pred == 1:
            print("Fake account")
            return "This seems like a spam account..."
        else:
            print("Real account")
            return "This account looks real!"

    def preprocess(self, ar, stand):
        new_data = np.zeros(11)
        new_data = np.reshape(new_data, (1, 11))

        for line in ar:
            new_line = line[0:11]
            new_line = np.reshape(new_line, (1, 11))
            new_data = np.append(new_data, new_line, axis=0)

        new_data = new_data[1:]

        if stand:
            new_data = self.scaler.fit_transform(new_data)

        return new_data