# TODO: experiment with different types of models

from keras.models import Sequential
from keras.layers import Dense  # standard multi-connexted layer
from sklearn import preprocessing
import pandas as pd
from keras.utils.np_utils import to_categorical


def train():
    model = Sequential()

    model.add(Dense(8, activation="relu", input_dim=50132))  # input layer
    # nodes normally increase than decrease
    model.add(Dense(16, activation="relu"))
    model.add(Dense(32, activation="relu"))  # more epochs for deeper model
    model.add(Dense(64, activation="relu"))
    model.add(Dense(32, activation="relu"))
    # another option is to make a shallow but wide network
    model.add(Dense(16, activation="relu"))
    model.add(Dense(8, activation="relu"))
    model.add(Dense(3, activation="softmax"))
    # output is [0, 0, 0]
    # where each col represents the probability of the user having said condition

    model.compile(
        optimizer='adam',
        loss='categorical_crossentropy',
        metrics=['accuracy']
    )

    data = pd.read_csv('./eye_dataset.csv')
    data = data.sample(frac=1)
    x_train = data.iloc[:, 1:]
    le = preprocessing.LabelEncoder()
    y_train = le.fit_transform(list(data["Type"]))
    y_train = to_categorical(y_train)

    model.fit(
        x_train,
        y_train,
        epochs=1000,
        validation_split=0.2
    )

    print("== summary ==")
    model.summary()
    model.save('trained_dataset.h5')


train()
