from azureml.core import Workspace, Experiment, Environment, ScriptRunConfig


def run_script_in_cloud():
    ws = Workspace.from_config()
    experiment = Experiment(workspace=ws, name='day1-experiment-hello')

    config = ScriptRunConfig(source_directory='./', script='print_fibonacci.py',
                             compute_target='cpu-cluster')

    run = experiment.submit(config)
    aml_url = run.get_portal_url()
    print(aml_url)


if __name__ == "__main__":
    run_script_in_cloud()