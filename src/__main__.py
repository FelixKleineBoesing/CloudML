from pathlib import Path

from src.data_processing import clean_data, write_data_to_directory
from src.helpers import create_dir_if_not_exist

DATA_PATH = Path("..", "data", "travel insurance.csv")
CLEANED_DATA_PATH = Path("..", "data", "cleaned_data", "cleaned_data.csv")


def main():
    create_dir_if_not_exist(CLEANED_DATA_PATH)
    data = clean_data(DATA_PATH)
    write_data_to_directory(data, CLEANED_DATA_PATH)
    pass


if __name__ == "__main__":
    main()



