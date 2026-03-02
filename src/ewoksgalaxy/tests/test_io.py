from ewokscore.engine_interface import TaskGraph

from ewoksgalaxy.io import ewoks_to_galaxy


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
