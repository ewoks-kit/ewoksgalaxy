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
