from tensorflow.keras.callbacks import Callback
from azureml.core import Run, Dataset, Workspace
import pandas as pd
import sys
import os
print(os.listdir("../../"))
print(os.listdir("../"))
print(os.listdir("./"))
print(os.listdir("/"))
os.environ["PYTHONPATH"] = "../../"
sys.path.append("../../")

from src.data_processing import process_data
from src.modelling import cross_validate, get_trained_model


class AzureLossCallback(Callback):

    def __init__(self, run=None):
        if run is None:
            run = Run.get_context()
        super().__init__()
        self.run = run

    def on_epoch_end(self, epoch, logs=None):
        if logs is not None:
            for key, val in logs.items():
                self.run.log(key, val)


def main():
    ws = Workspace.from_config()
    callback = AzureLossCallback(Run.get_context())
    dataset = Dataset.get_by_name(ws, name='TravelInsurance')
    data_path = dataset.download()
    data = pd.read_feather(data_path[0])
    label = data["label"]
    data.drop(["label"], axis=1, inplace=True)

    train_model_func = get_trained_model((data.shape[1],), learning_rate=0.001, callback=callback)
    metrics = cross_validate(train_model_func=train_model_func,
                             data=data, label=label,
                             data_processing_func=process_data)
    print(metrics)


if __name__ == "__main__":

    # physical_devices = tf.config.list_physical_devices('GPU')
    # if len(physical_devices) > 0:
    #     tf.config.experimental.set_memory_growth(physical_devices[0], enable=True)
    #
    # my_devices = tf.config.experimental.list_physical_devices(device_type='CPU')
    # tf.config.experimental.set_visible_devices(devices=my_devices[0], device_type='CPU')
    # os.environ['CUDA_VISIBLE_DEVICES'] = '-1'
    main()

