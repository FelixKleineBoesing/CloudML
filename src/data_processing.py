import pandas as pd
from src.helpers import create_dir_if_not_exist


def clean_data(file_path):
    data = pd.read_csv(file_path)
    pass


def write_data_to_directory(cleaned_data: pd.DataFrame, output_path):
    create_dir_if_not_exist(output_path)
    cleaned_data.to_csv(output_path)