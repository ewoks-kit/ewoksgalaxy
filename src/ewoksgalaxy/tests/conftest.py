import pytest


@pytest.fixture
def ewoks_workflow():
    graph = {
        "id": "galaxy_test",
        "label": "An Ewoks workflow to test Galaxy",
        "schema_version": "1.1",
    }

    task = "ewokscore.tests.examples.tasks.sumtask.SumTask"
    nodes = [
        {
            "id": "task1",
            "default_inputs": [{"name": "a", "value": 1}],
            "task_type": "class",
            "task_identifier": task,
        },
        {
            "id": "task2",
            "default_inputs": [{"name": "b", "value": 2}],
            "task_type": "class",
            "task_identifier": task,
        },
        {
            "id": "task3",
            "default_inputs": [{"name": "b", "value": 1}],
            "task_type": "class",
            "task_identifier": task,
        },
    ]
    links = [
        {
            "source": "task1",
            "target": "task3",
            "data_mapping": [{"source_output": "result", "target_input": "a"}],
        },
        {
            "source": "task2",
            "target": "task3",
            "data_mapping": [
                {"source_output": "result", "target_input": "b"},
                {"source_output": "result", "target_input": "delay"},
            ],
        },
    ]

    return {"graph": graph, "links": links, "nodes": nodes}
