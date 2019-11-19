# -*- coding: utf-8 -*-
"""model.py
Support Vector Classifier: NuSVC (Supervised learning)
nu-parameter: upper bound on fraction of margin errors & lower bound on #(support vectors)/#(training samples)
    nu = 0.5 (default) (at most 50% misclassified, at least 50% of training samples are support vectors)
"""

import pandas as pd
import numpy as np
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
        self.X_train = self.preprocess(ini_train)
        self.y_train = np.array(data_train.iloc[1:, 11])

        # Fit model to data
        self.clf.fit(self.X_train, self.y_train)

    def predict(self, ar):
        # Reshape & scale input data
        data = np.reshape(ar, (1, -1))
        data = self.scaler.transform(data)

        # Get prediction from classifier
        tmp = self.clf.predict(data)
        tmp = tmp.astype(float)
        pred = tmp[0]
        if pred == 1:
            return "This seems like a fake account..."
        else:
            return "This account looks real!"

    def preprocess(self, ar):
        new_data = np.zeros(11)
        new_data = np.reshape(new_data, (1, 11))

        for line in ar:
            new_line = line[0:11]
            new_line = np.reshape(new_line, (1, 11))
            new_data = np.append(new_data, new_line, axis=0)

        new_data = new_data[1:]

        # Standardize data
        new_data = self.scaler.fit_transform(new_data)
        return new_data