from ewokscore.engine_interface import TaskGraph

from ewoksgalaxy.io import ewoks_to_galaxy
from ewoksgalaxy.io import galaxy_to_ewoks


def test_ewoks_to_galaxy(ewoks_workflow):
    assert ewoks_to_galaxy(TaskGraph(ewoks_workflow)) == {
        "class": "GalaxyWorkflow",
        "inputs": [],
        "outputs": [],
        "id": "galaxy_test",
        "label": "An Ewoks workflow to test Galaxy",
        "steps": [
            {
                "state": {"a": 1},
                "tool_id": "ewokscore.tests.examples.tasks.sumtask.SumTask",
                "type": "tool",
                "out": [],
            },
            {
                "state": {"b": 2},
                "tool_id": "ewokscore.tests.examples.tasks.sumtask.SumTask",
                "type": "tool",
                "out": [],
            },
            {
                "state": {"b": 1},
                "tool_id": "ewokscore.tests.examples.tasks.sumtask.SumTask",
                "type": "tool",
                "in": {
                    "a": {"source": "0/result"},
                    "b": {"source": "1/result"},
                    "delay": {"source": "1/result"},
                },
                "out": [],
            },
        ],
    }


def test_galaxy_to_ewoks(iris_workflow_path):
    assert galaxy_to_ewoks(iris_workflow_path) == {
        "graph": {
            "label": "Workflow constructed from history 'Iris'",
        },
        "nodes": [
            {
                "id": 0,
                "default_inputs": [
                    {
                        "name": "description",
                        "value": "",
                    },
                    {
                        "name": "name",
                        "value": "iris.csv",
                    },
                ],
                "label": "Input dataset",
                "task_type": "class",
                "task_identifier": "ewoksgalaxy.tasks.LoadDataInput",
            },
            {
                "id": 1,
                "label": "Convert",
                "task_type": "script",
                "task_identifier": "Convert characters1",
            },
            {
                "id": 2,
                "label": "Remove beginning",
                "task_type": "script",
                "task_identifier": "Remove beginning1",
            },
        ],
        "links": [
            {
                "data_mapping": [
                    {
                        "source_output": "output",
                        "target_input": "input",
                    },
                ],
                "source": 0,
                "target": 1,
            },
            {
                "source": 1,
                "target": 2,
                "data_mapping": [
                    {"source_output": "out_file1", "target_input": "input"}
                ],
            },
        ],
    }
