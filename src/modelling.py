from typing import Tuple
import pandas as pd
import tensorflow as tf
import numpy as np
from tensorflow.keras.layers import Dense, Input
from tensorflow.keras.models import Model
from tensorflow.keras.activations import relu, linear, sigmoid
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.losses import binary_crossentropy
from sklearn.model_selection import KFold


def get_model(input_shape: Tuple):
    inputs = Input(shape=input_shape)
    x = Dense(128, activation=relu)(inputs)
    x = Dense(64, activation=relu)(x)
    x = Dense(1, activation=sigmoid)(x)

    model = Model(inputs, x, name="TravelInsuranceModel")

    return model


def compile_model(model, optimizer=None, loss=None, metrics=None):
    if loss is None:
        loss = binary_crossentropy
    if metrics is None:
        metrics = ["accuracy"]
    if optimizer is None:
        optimizer = get_adam_optimizer()
    model.compile(loss=loss, optimizer=optimizer, metrics=metrics)
    return model


def get_adam_optimizer(learning_rate: float = 0.001):
    optimizer = Adam(learning_rate=learning_rate)
    return optimizer


def cross_validate(train_model_func, data, label, folds: int = 5, data_processing_func=None):
    kfold = KFold(folds, shuffle=True)
    metrics_per_fold = []
    for train, test in kfold.split(data, label):
        train_data, train_label = data.iloc[train, :], label.iloc[train]
        test_data, test_label = data.iloc[test, :], label.iloc[test]
        if data_processing_func is not None:
            train_data, train_label, test_data, test_label = \
                data_processing_func(train_data, train_label, test_data, test_label)
        model = train_model_func(train_data, train_label)
        scores = model.evaluate(test_data, test_label, verbose=0)

        metrics_per_fold.append(scores)
    return pd.DataFrame(metrics_per_fold)


def get_trained_model(input_shape, learning_rate, callback=None):
    def wrapper(data, label):
        model = get_model(input_shape)
        optimizer = get_adam_optimizer(learning_rate=learning_rate)
        model = compile_model(model=model, optimizer=optimizer, metrics=["accuracy", tf.metrics.Recall()])
        if callback is not None:
            model.fit(data, label, batch_size=128, epochs=50, verbose=True, callbacks=[callback])
        else:
            model.fit(data, label, batch_size=128, epochs=50, verbose=True)
        return model
    return wrapper