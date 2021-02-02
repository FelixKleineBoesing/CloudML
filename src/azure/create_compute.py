from pathlib import Path

from azureml.core import Workspace
from azureml.core.compute import ComputeTarget, AmlCompute
from azureml.core.compute_target import ComputeTargetException


def create_compute_cluster(azureml_path: str = Path("..", "..", ".azureml")):
    ws = Workspace.from_config(azureml_path)

    # Choose a name for your CPU cluster
    cpu_cluster_name = "cpu-cluster"

    # Verify that the cluster does not exist already
    try:
        cpu_cluster = ComputeTarget(workspace=ws, name=cpu_cluster_name)
        print('Found existing cluster, use it.')
    except ComputeTargetException:
        compute_config = AmlCompute.provisioning_configuration(vm_size='STANDARD_D2_V2',
                                                               idle_seconds_before_scaledown=1200,
                                                               min_nodes=0,
                                                               max_nodes=1)
        cpu_cluster = ComputeTarget.create(ws, cpu_cluster_name, compute_config)

    cpu_cluster.wait_for_completion(show_output=True)


if __name__ == "__main__":
    create_compute_cluster()
