import numpy as np

from sklearn.preprocessing import LabelEncoder


class TumorLabelEncoder:

    def __init__(self):

        self.encoder = LabelEncoder()

    def fit(self, labels):

        self.encoder.fit(labels)

    def transform(self, labels):

        return self.encoder.transform(labels)

    def fit_transform(self, labels):

        return self.encoder.fit_transform(labels)

    def inverse_transform(self, labels):

        return self.encoder.inverse_transform(labels)

    def classes(self):

        return self.encoder.classes_
