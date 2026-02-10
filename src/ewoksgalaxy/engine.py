from ewokscore.engine_interface import WorkflowEngine
from ewokscore.graph import TaskGraph


class GalaxyEngine(WorkflowEngine):
    def execute_graph(self, graph: TaskGraph, *args, **kwargs) -> dict | None:
        pass
