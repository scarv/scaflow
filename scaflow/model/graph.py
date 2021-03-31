"""Internal graph data structure for use by editor"""
from __future__ import annotations

import logging
from typing import Dict, TYPE_CHECKING

from scaflow.model import GraphEvent, JsonSerializable, dispatcher
from .node import Node

if TYPE_CHECKING:
    from .connection import Connection
    from .input_socket import Input
    from .output_socket import Output
    from .type_hints import GraphDict

logger = logging.getLogger(__name__)


@dispatcher
class Graph(JsonSerializable):
    """Internal representation of the graph of nodes in the editor"""

    def __init__(self):
        self._nodes: Dict[int, Node] = {}
        self._connections: Dict[int, Connection] = {}

        self.nodeAddedEvent = GraphEvent(self)
        self.nodeRemovedEvent = GraphEvent(self)
        self.edgeAddedEvent = GraphEvent(self)
        self.edgeRemovedEvent = GraphEvent(self)

    def __len__(self):
        return len(self._nodes)

    def __contains__(self, item):
        if isinstance(item, Node):
            return item.id in self._nodes
        return item in self._nodes

    def __iter__(self):
        return iter(self._nodes)

    def __getitem__(self, n):
        return self._nodes[n]

    @property
    def edges(self):
        return self._connections

    def iter_edges(self):
        for conn in self._connections.values():
            yield conn

    def add_node(self, node: "Node"):
        """Add a node to the graph.

        Args:
            node: Node to be added to the graph
        """
        self._nodes[node.id] = node
        self.nodeAddedEvent(node.id)

    def remove_node(self, node: "Node"):
        for c in node.connections:
            node.removeConnection(c)
        self._nodes.pop(node.id)
        self.nodeRemovedEvent(node)

    def add_edge(self, output_socket: "Output", input_socket: "Input"):
        """Add edge between two sockets on the graph.

        Args:
            output_socket: Output socket of a node
            input_socket: Input socket of a node
        """
        logger.info(
            "Adding edge to graph: %s: %s -> %s: %s",
            output_socket.node.id,
            output_socket.key,
            input_socket.node.id,
            input_socket.key,
        )
        connection = output_socket.add_connection(input_socket)
        self._connections[connection.id] = connection

        self.edgeAddedEvent(connection)

    def remove_edge(self, connection: "Connection"):
        connection.remove()
        self.edgeRemovedEvent(connection)

    def as_dict(self) -> "GraphDict":
        return {
            "nodes": list(self._nodes.values()),
            "edges": list(self._connections.values()),
        }

    @classmethod
    def from_dict(cls, data: "GraphDict"):
        g = cls()
        # TODO(fergus): Need to update UI when clearing current nodes and edges
        logger.info("Loading object: %s", data)
        n: Node
        for n in data["nodes"]:
            g.add_node(n)

        # logger.debug([(n.id, n.inputs, n.outputs) for n in g._nodes.values()])
        e: "Connection"
        for e in data["edges"]:
            g._connections[e.id] = e
            g._nodes[e.output_node].outputs[e.output_socket_key].connections.append(e)
            g._nodes[e.input_node].inputs[e.input_socket_key].connections.append(e)
        return g

    def from_graph(self, graph: "Graph"):
        for n in graph:
            self.add_node(graph[n])
        for e in graph.iter_edges():
            out_socket = self._nodes[e.output_node].outputs[e.output_socket_key]
            in_socket = self._nodes[e.input_node].inputs[e.input_socket_key]
            out_socket.connections.append(e)
            in_socket.connections.append(e)
            self._connections[e.id] = e

            self.edgeAddedEvent(e)
