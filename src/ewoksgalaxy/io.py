from typing import Any

from ewokscore.engine_interface import TaskGraph

_DEFAULT_LICENSE = "MIT"
_DEFAULT_CREATOR = [{"class": "Organization", "name": "ESRF"}]


def _node_doc(node: dict) -> str:
    return node.get("doc") or node.get("annotation") or f"Ewoks task {node['id']}"


def _graph_doc(graph_metadata: dict[str, Any]) -> str:
    return (
        graph_metadata.get("doc")
        or graph_metadata.get("annotation")
        or graph_metadata.get("label")
        or f"Ewoks workflow {graph_metadata['id']}"
    )


def _ewoks_node_to_galaxy_step(node: dict) -> dict[str, Any]:
    step: dict[str, Any] = {
        "doc": _node_doc(node),
        "label": node.get("label") or node["id"],
        "tool_id": node["task_identifier"],
        "type": "tool",
        "out": [],  # required according to specs but unused in real Galaxy workflows?
    }

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

    graph_metadata: dict[str, Any] = graph_dict["graph"]
    galaxy_graph: dict[str, Any] = {
        "class": "GalaxyWorkflow",
        "creator": graph_metadata.get("creator") or _DEFAULT_CREATOR,
        "doc": _graph_doc(graph_metadata),
        "inputs": [],  # TODO
        "license": graph_metadata.get("license") or _DEFAULT_LICENSE,
        "outputs": [],  # TODO
        "tags": graph_metadata.get("tags", []),
    }

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
