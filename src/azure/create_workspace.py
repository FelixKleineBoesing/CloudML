from pathlib import Path

from azureml.core import Workspace
from dotenv.main import load_dotenv
import os

load_dotenv("../../.env")


def create_workspace(azureml_path: str = Path("..", "..", ".azureml")):
    ws = Workspace.create(name='TravelInsurance',
                          subscription_id=os.environ["SUBSCRIPTION_ID"],
                          resource_group=os.environ["RESOURCE_GROUP"],
                          create_resource_group=True,
                          location=os.environ["SERVER_LOCATION"])

    # write out the workspace details to a configuration file: .azureml/config.json
    ws.write_config(path=azureml_path)


if __name__ == "__main__":
    create_workspace()

