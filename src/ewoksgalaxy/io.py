import json
from pathlib import Path
from typing import Any

from ewokscore.engine_interface import TaskGraph


def _ewoks_node_to_galaxy_step(node: dict) -> dict[str, Any]:
    step: dict[str, Any] = {
        "tool_id": node["task_identifier"],
        "type": "tool",
        "out": [],  # required according to specs but unused in real Galaxy workflows?
    }
    label = node.get("label")
    if label is not None:
        step["label"] = label

    default_inputs = node.get("default_inputs")
    if not default_inputs:
        return step

    state: dict[str, Any] = {}
    for default_input in default_inputs:
        name = default_input["name"]
        value = default_input["value"]
        state[name] = value

    return {"state": state, **step}


def _ewoks_link_to_galaxy_input(link: dict, galaxy_step_indices: dict[str, str]):
    galaxy_input: dict[str, dict] = {}

    for mapping in link["data_mapping"]:
        galaxy_index = galaxy_step_indices[link["source"]]
        galaxy_input[mapping["target_input"]] = {
            "source": f"{galaxy_index}/{mapping['source_output']}"
        }

    return galaxy_input


def ewoks_to_galaxy(raw_graph: TaskGraph) -> dict[str, Any]:
    graph_dict = raw_graph.dump()

    galaxy_graph: dict[str, Any] = {
        "class": "GalaxyWorkflow",
        "inputs": [],  # TODO
        "outputs": [],  # TODO
    }

    graph_metadata: dict[str, str] = graph_dict["graph"]
    graph_id = graph_metadata.get("id")
    if graph_id is not None:
        galaxy_graph["id"] = graph_id
    label = graph_metadata.get("label")
    if label is not None:
        galaxy_graph["label"] = label

    steps: list[dict] = []
    # Keep a mapping between Ewoks ids and Galaxy step indices for parsing the data mapping
    galaxy_step_indices: dict[str, int] = {}
    for i, node in enumerate(graph_dict["nodes"]):
        steps.append(_ewoks_node_to_galaxy_step(node))
        galaxy_step_indices[node["id"]] = i

    for link in graph_dict["links"]:
        target_id = galaxy_step_indices[link["target"]]
        if "in" not in steps[target_id]:
            steps[target_id]["in"] = {}
        steps[target_id]["in"].update(
            _ewoks_link_to_galaxy_input(link, galaxy_step_indices)
        )
    galaxy_graph["steps"] = steps

    return galaxy_graph


def _galaxy_data_input_to_ewoks_node(step: dict) -> dict:
    node: dict[str, Any] = {
        "task_type": "class",
        "task_identifier": "ewoksgalaxy.tasks.LoadDataInput",
    }

    step_id = step.get("id")
    if step_id is not None:
        node["id"] = step_id

    name = step.get("name")
    if name is not None:
        node["label"] = name

    inputs: list[dict[str, str]] = step.get("inputs", [])
    if inputs:
        default_inputs = []
        for input in inputs:
            for name, value in input.items():
                default_inputs.append({"name": name, "value": value})
        node["default_inputs"] = default_inputs

    return node


def _galaxy_tool_to_ewoks_node(step: dict) -> dict:
    node = {
        # All Galaxy tools are script-based
        "task_type": "script"
    }

    step_id = step.get("id")
    if step_id is not None:
        node["id"] = step_id

    tool_id = step.get("tool_id")
    if tool_id is not None:
        node["task_identifier"] = tool_id

    tool_name = step.get("name")
    if tool_name is not None:
        node["label"] = tool_name

    return node


def _galaxy_connections_to_ewoks_links(step: dict) -> list[dict]:
    links_per_source = {}

    target_id = step.get("id")

    for target_input, connection in step["input_connections"].items():
        source_id = connection["id"]

        if source_id not in links_per_source:
            links_per_source[source_id] = {
                "source": source_id,
                "target": target_id,
                "data_mapping": [],
            }

        links_per_source[source_id]["data_mapping"].append(
            {"source_output": connection["output_name"], "target_input": target_input}
        )

    return list(links_per_source.values())


def galaxy_to_ewoks(graph: Any) -> dict:
    if not isinstance(graph, (str, Path)):
        raise TypeError(f"{graph} should be a str or Path. Got {type(graph)}.")

    with open(graph, "r") as graph_file:
        galaxy_graph = json.load(graph_file)

    if not isinstance(galaxy_graph, dict):
        raise TypeError(f"{galaxy_graph} should be a dict. Got {type(galaxy_graph)}.")

    ewoks_graph = {"graph": {}, "nodes": [], "links": []}
    graph_name = galaxy_graph.get("name")
    if graph_name:
        ewoks_graph["graph"]["label"] = graph_name

    graph_id = galaxy_graph.get("id")
    if graph_id:
        ewoks_graph["graph"]["id"] = graph_id

    for step in galaxy_graph["steps"].values():
        if step["type"] == "tool":
            ewoks_graph["nodes"].append(_galaxy_tool_to_ewoks_node(step))
            if "input_connections" in step:
                ewoks_graph["links"].extend(_galaxy_connections_to_ewoks_links(step))

        if step["type"] == "data_input":
            ewoks_graph["nodes"].append(_galaxy_data_input_to_ewoks_node(step))

    return ewoks_graph
