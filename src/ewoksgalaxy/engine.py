from pathlib import Path
from typing import Any
from typing import List
from typing import Optional
from typing import Union

from ewokscore.engine_interface import RawExecInfoType
from ewokscore.engine_interface import TaskGraph
from ewokscore.engine_interface import WorkflowEngineWithSerialization
from ruamel.yaml import YAML

from . import io


class GalaxyWorkflowEngine(WorkflowEngineWithSerialization):
    _GALAXY_REPR = "gxwf"

    def execute_graph(
        self,
        graph: Any,
        *,
        inputs: Optional[List[dict]] = None,
        load_options: Optional[dict] = None,
        varinfo: Optional[dict] = None,
        execinfo: RawExecInfoType = None,
        task_options: Optional[dict] = None,
        outputs: Optional[List[dict]] = None,
        merge_outputs: Optional[bool] = True,
        **execute_options,
    ) -> None:
        raise NotImplementedError("TODO")

    def deserialize_graph(
        self,
        graph: Any,
        *,
        inputs: Optional[List[dict]] = None,
        representation: Optional[str] = None,
        root_dir: Optional[Union[str, Path]] = None,
        root_module: Optional[str] = None,
        **deserialize_options,
    ) -> TaskGraph:
        raise NotImplementedError("TODO")

    def serialize_graph(
        self,
        graph: TaskGraph,
        destination: str | Path,
        *,
        representation: Optional[str] = None,
        **serialize_options,
    ) -> Union[str, Path, dict]:
        if representation is None:
            representation = self.get_graph_representation(destination)

        if representation == self._GALAXY_REPR:
            galaxy_graph = io.ewoks_to_galaxy(graph)
            yaml = YAML(typ="safe")
            with open(destination, "w") as dest_file:
                return yaml.dump(galaxy_graph, dest_file)
            return destination

        return graph.dump(
            destination, representation=representation, **serialize_options
        )

    def get_graph_representation(self, graph: Any) -> Optional[str]:
        if not isinstance(graph, (Path, str)):
            return None

        graph_path = str(graph)
        if graph_path.endswith(".ga"):
            return self._GALAXY_REPR

        if graph_path.endswith(".yml") or graph_path.endswith(".yaml"):
            yaml = YAML(typ="safe")
            graph_dict = yaml.load(graph_path)
            if graph_dict.get("class") == "GalaxyWorkflow":
                return self._GALAXY_REPR
        return None
