import logging
from typing import Dict, List

from scaflow import model

logger = logging.getLogger(__name__)


class EngineNode:
    def __init__(self, node):
        self._node = node
        self.output_data = None

    @property
    def node(self):
        return self._node


class Engine:
    def __init__(self, graph: model.Graph):
        self._graph = graph
        self._engine_graph = {}
        self._visited = []

    def __call__(self, *args, **kwargs):
        self._visited = []
        for node_id in self._graph:
            if node_id not in self._visited:
                self._process_node(node_id)

    def _get_input_data(self, engine_node: EngineNode) -> Dict[str, any]:
        logger.debug("Getting inputs for node: %s", engine_node.node)
        input_data: Dict[str, any] = {}
        logger.debug("Inputs: %s", engine_node.node.inputs)
        for i in engine_node.node.inputs.values():
            # logger.debug(i.connections)
            for conn in i.connections:
                if conn.output_node_id:
                    outputs = self._process_node(conn.output_node_id)

                    input_data[conn.input_socket_key] = outputs
        # logger.debug(input_data)
        return input_data

    def _process_node(self, node_id) -> Dict[str, any]:
        engine_node = EngineNode(self._graph[node_id])
        self._engine_graph[node_id] = engine_node
        logger.debug("Processing node: %s", engine_node.node)
        if not engine_node.output_data:
            input_data = self._get_input_data(engine_node)
            engine_node.output_data = engine_node.node.execute(input_data)
            self._visited.append(node_id)
        return engine_node.output_data
