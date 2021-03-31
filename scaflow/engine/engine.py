import logging
from typing import Dict

from scaflow import model
from scaflow.model import Connection, Input, Node

logger = logging.getLogger(__name__)


class EngineNode:
    def __init__(self, node):
        self._node = node
        self.output_data = None

    @property
    def node(self) -> Node:
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
        i: Input
        for i in engine_node.node.inputs.values():
            conn: Connection
            for conn in i.connections:
                logger.debug("Connection: %s", conn)
                outputs = self._process_node(conn.output_node)

                input_data[conn.output_socket_key] = outputs
        return input_data

    def _process_node(self, node_id) -> Dict[str, any]:
        if node_id in self._engine_graph:
            engine_node = self._engine_graph[node_id]
        else:
            engine_node = EngineNode(self._graph[node_id])
            self._engine_graph[node_id] = engine_node
        if engine_node.output_data is None:
            logger.debug("Processing node: %s", engine_node.node)

            input_data = self._get_input_data(engine_node)
            logger.debug(
                "Executing node: %s, with input data: %s", engine_node.node, input_data
            )
            engine_node.output_data = engine_node.node.execute(input_data)
            logger.debug("Result: %s", engine_node.output_data)
            self._visited.append(node_id)
        return engine_node.output_data
