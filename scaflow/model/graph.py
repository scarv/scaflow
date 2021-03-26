"""Internal graph data structure for use by editor"""
import logging
from typing import Dict, List, TYPE_CHECKING, Type

from scaflow import model
from scaflow.model import nodes
from scaflow.model.dispatcher import JsonSerializable, dispatcher
from scaflow.model.base import Connection, Input, Node, Output

# if TYPE_CHECKING:
#     from scaflow.model import Connection, Node, Output, Input

logger = logging.getLogger(__name__)


@dispatcher
class Graph(JsonSerializable):
    """Internal representation of the graph of nodes in the editor"""

    def __init__(self):
        self._nodes: Dict[int, Node] = {}
        self._adj = {}

        self.nodeAddedEvent = model.GraphEvent(self)
        self.edgeAddedEvent = model.GraphEvent(self)
        self.edgeRemovedEvent = model.GraphEvent(self)

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

    def edges(self):
        for i in self._adj:
            for j in self._adj[i]:
                for conn in self._adj[i][j].values():
                    yield conn

    @property
    def node_types(
        self,
    ) -> "Dict[str, List[Type[Node]]]":
        """All supported node types, used in creation of context menus.

        Returns:
            A nested list of strings identifying types of nodes allowed within the editor
        """
        return {
            "Constants": [
                nodes.TraceFileNode,
                nodes.PlaintextFileNode,
                nodes.CiphertextFileNode,
            ],
            "Input": [nodes.ETSTraceNode, nodes.NpyTraceNode],
            "Output": [nodes.WriteNode],
            "Selection": [nodes.FirstSubBytesNode],
            "Model": [nodes.HammingWeightNode],
            "Discriminants": [nodes.MaxAbsNode],
            "Attack": [nodes.CPAAttackNode],
            "Preprocessing": [nodes.FindPeaksNode]
            # "Processing": [nodes.SplitNode, nodes.ConcatNode],
        }

    def add_node(self, node: "Node"):
        """Add a node to the graph.

        Args:
            node: Node to be added to the graph
        """
        if node.id not in self._adj:
            self._adj[node.id] = {}
            self._nodes[node.id] = node

            self.nodeAddedEvent(node.id)
        else:
            # TODO: Should update node information
            pass

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

        # Add nodes if they do not already exist
        if output_socket.node.id not in self._adj:
            self.add_node(output_socket.node)
        if input_socket.node.id not in self._adj:
            self.add_node(input_socket.node)

        edge = Connection(
            input_socket.node.id,
            input_socket.key,
            output_socket.node.id,
            output_socket.key,
        )

        if input_socket.node.id in self._adj[output_socket.node.id]:
            self._adj[output_socket.node.id][input_socket.node.id][edge.id] = edge
        else:
            self._adj[output_socket.node.id][input_socket.node.id] = {edge.id: edge}

        # output_socket.add_connection(edge)
        input_socket.add_connection(edge)

        self.edgeAddedEvent(edge)

    def remove_edge(self, output_socket: "Output", input_socket: "Input"):
        logger.info(
            "Removing edge from graph: %s: %s -> %s: %s",
            output_socket.node.id,
            output_socket.key,
            input_socket.node.id,
            input_socket.key,
        )

        edge = Connection(
            input_socket.node.id,
            input_socket.key,
            output_socket.node.id,
            output_socket.key,
        )

        # if input_socket.node.id in self._adj[output_socket.node.id]:
        #     self._adj[output_socket.node.id][input_socket.node.id][edge.id] = edge
        # else:
        #     self._adj[output_socket.node.id][input_socket.node.id] = {edge.id: edge}

        input_socket.remove_connection(edge)

        self.edgeRemovedEvent(edge)

    def as_dict(self):
        connections = []
        for i in self._adj:
            for j in self._adj[i]:
                for conn in self._adj[i][j].values():
                    connections.append(conn)
        return {
            "nodes": [node for node in self._nodes.values()],
            "edges": connections,
        }

    @classmethod
    def from_dict(cls, data):
        g = cls()
        g._nodes = {}
        g._adj = {}
        # TODO(fergus): Need to update UI when clearing current nodes and edges
        logger.info("Loading object: %s", data)
        for n in data["nodes"]:
            g.add_node(n)

        # logger.debug([(n.id, n.inputs, n.outputs) for n in g._nodes.values()])

        for e in data["edges"]:
            out_socket = g._nodes[e.output_node_id].outputs[e.output_socket_key]
            in_socket = g._nodes[e.input_node_id].inputs[e.input_socket_key]
            g.add_edge(out_socket, in_socket)
        return g

    def from_graph(self, graph: "Graph"):
        for n in graph:
            self.add_node(graph[n])
        for e in graph.edges():
            out_socket = self._nodes[e.output_node_id].outputs[e.output_socket_key]
            in_socket = self._nodes[e.input_node_id].inputs[e.input_socket_key]
            self.add_edge(out_socket, in_socket)
