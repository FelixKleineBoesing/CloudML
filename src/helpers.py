from pathlib import Path
import os


def create_dir_if_not_exist(path: Path):
    for parent in reversed(path.parents):
        if not os.path.exists(parent):
            os.mkdir(parent)
