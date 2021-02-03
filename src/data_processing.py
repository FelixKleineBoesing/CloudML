import pandas as pd
from category_encoders.target_encoder import TargetEncoder

from src.helpers import create_dir_if_not_exist, sampling


def clean_data(file_path):
    data = pd.read_csv(file_path)
    data["label"] = 0
    data.loc[data["Claim"] == "Yes", "label"] = 1
    data.drop(["Claim"], axis=1, inplace=True)
    column_names = data.columns.values
    column_names = [clean_col(col) for col in column_names]
    data.columns = column_names
    return data


def write_data_to_directory(cleaned_data: pd.DataFrame, output_path):
    create_dir_if_not_exist(output_path)
    cleaned_data.to_feather(output_path)


def clean_col(col_name: str):
    col_name = col_name.lower().replace(" ", "_")
    return col_name


def target_encode(data, label, encoder=None):
    """

    :param data:
    :param label:
    :param encoder: if supplied the encoder will be used to predict onto data
    :return:
    """
    if encoder is None:
        encoder = TargetEncoder()
        data = encoder.fit_transform(data, label)
        return encoder, data
    else:
        return encoder, encoder.transform(data, label)


def process_data(train_data, train_label, test_data, test_label):
    encoder, train_data = target_encode(train_data, train_label)
    _, test_data = target_encode(test_data, test_label, encoder)
    train_data, train_label = sampling(train_data, train_label, "up")
    return train_data, train_label, test_data, test_label