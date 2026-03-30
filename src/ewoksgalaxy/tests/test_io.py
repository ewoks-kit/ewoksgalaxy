from ewokscore.engine_interface import TaskGraph

from ewoksgalaxy.io import ewoks_to_galaxy


def test_ewoks_to_galaxy(ewoks_workflow):
    assert ewoks_to_galaxy(TaskGraph(ewoks_workflow)) == {
        "class": "GalaxyWorkflow",
        "creator": [{"class": "Organization", "name": "ESRF"}],
        "doc": "An Ewoks workflow to test Galaxy",
        "inputs": [],
        "id": "galaxy_test",
        "label": "An Ewoks workflow to test Galaxy",
        "license": "MIT",
        "outputs": [],
        "tags": [],
        "steps": [
            {
                "doc": "Ewoks task task1",
                "label": "task1",
                "state": {"a": 1},
                "tool_id": "ewokscore.tests.examples.tasks.sumtask.SumTask",
                "type": "tool",
                "out": [],
            },
            {
                "doc": "Ewoks task task2",
                "label": "task2",
                "state": {"b": 2},
                "tool_id": "ewokscore.tests.examples.tasks.sumtask.SumTask",
                "type": "tool",
                "out": [],
            },
            {
                "doc": "Ewoks task task3",
                "label": "task3",
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


def test_ewoks_to_galaxy_preserves_optional_metadata(ewoks_workflow):
    ewoks_workflow["graph"]["annotation"] = "Workflow annotation"
    ewoks_workflow["graph"]["creator"] = [{"class": "Organization", "name": "Ewoks"}]
    ewoks_workflow["graph"]["license"] = "Apache-2.0"
    ewoks_workflow["graph"]["tags"] = ["converted", "ewoks"]
    ewoks_workflow["nodes"][0]["label"] = "sum_a"
    ewoks_workflow["nodes"][0]["annotation"] = "First sum task"

    galaxy_workflow = ewoks_to_galaxy(TaskGraph(ewoks_workflow))

    assert galaxy_workflow["doc"] == "Workflow annotation"
    assert galaxy_workflow["creator"] == [{"class": "Organization", "name": "Ewoks"}]
    assert galaxy_workflow["license"] == "Apache-2.0"
    assert galaxy_workflow["tags"] == ["converted", "ewoks"]
    assert galaxy_workflow["steps"][0]["label"] == "sum_a"
    assert galaxy_workflow["steps"][0]["doc"] == "First sum task"
