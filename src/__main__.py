from pathlib import Path
import tensorflow as tf
import os

from src.data_processing import clean_data, write_data_to_directory, target_encode
from src.helpers import create_dir_if_not_exist, sampling
from src.modelling import get_model, compile_model, get_adam_optimizer, cross_validate

DATA_PATH = Path("..", "data", "travel insurance.csv")
CLEANED_DATA_PATH = Path("..", "data", "cleaned_data", "cleaned_data.feather")


def get_trained_model(input_shape, learning_rate):
    def wrapper(data, label):
        model = get_model(input_shape)
        optimizer = get_adam_optimizer(learning_rate=learning_rate)
        model = compile_model(model=model, optimizer=optimizer, metrics=["accuracy", tf.metrics.Recall()])
        model.fit(data, label, batch_size=128, epochs=50, verbose=True)
        return model
    return wrapper


def process_data(train_data, train_label, test_data, test_label):
    encoder, train_data = target_encode(train_data, train_label)
    _, test_data = target_encode(test_data, test_label, encoder)
    train_data, train_label = sampling(train_data, train_label, "up")
    return train_data, train_label, test_data, test_label


def main():
    create_dir_if_not_exist(CLEANED_DATA_PATH)
    data = clean_data(DATA_PATH)
    write_data_to_directory(data, CLEANED_DATA_PATH)
    label = data["label"]
    data.drop(["label"], axis=1, inplace=True)

    train_model_func = get_trained_model((data.shape[1], ), learning_rate=0.001)
    metrics = cross_validate(train_model_func=train_model_func,
                             data=data, label=label,
                             data_processing_func=process_data)
    print(metrics)


if __name__ == "__main__":
    physical_devices = tf.config.list_physical_devices('GPU')
    if len(physical_devices) > 0:
        tf.config.experimental.set_memory_growth(physical_devices[0], enable=True)

    my_devices = tf.config.experimental.list_physical_devices(device_type='CPU')
    tf.config.experimental.set_visible_devices(devices=my_devices[0], device_type='CPU')
    os.environ['CUDA_VISIBLE_DEVICES'] = '-1'
    main()



