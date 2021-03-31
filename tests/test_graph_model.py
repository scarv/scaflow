import json
from typing import Dict
from unittest import mock

import pytest

from scaflow.model import (
    Connection,
    Control,
    ControlType,
    Graph,
    Input,
    Node,
    Output,
    dispatcher,
)


@dispatcher
class ExampleNode(Node):
    @classmethod
    def create_node(cls):
        pass

    def execute(self, kwargs) -> Dict[str, any]:
        pass


EXAMPLE_JSON = """{
    "nodes": [
        {
            "id": 1,
            "name": "Test",
            "inputs": [],
            "outputs": [
                {
                    "key": "link",
                    "name": "Output",
                    "compatible": [],
                    "multi_conns": true,
                    "__class__": "Output"
                }
            ],
            "controls": [
                {
                    "key": "control",
                    "name": "File",
                    "type": "file_path",
                    "data": {},
                    "__class__": "Control"
                }
            ],
            "position": [
                0,
                0
            ],
            "__class__": "ExampleNode"
        },
        {
            "id": 2,
            "name": "Test",
            "inputs": [
                {
                    "key": "link",
                    "name": "Input",
                    "compatible": [],
                    "multi_conns": false,
                    "control": null,
                    "__class__": "Input"
                }
            ],
            "outputs": [],
            "controls": [],
            "position": [
                0,
                0
            ],
            "__class__": "ExampleNode"
        }
    ],
    "edges": [
        {
            "id": 1,
            "input_socket_key": "link",
            "output_socket_key": "link",
            "input_node": 2,
            "output_node": 1,
            "__class__": "Connection"
        }
    ],
    "__class__": "Graph"
}"""


class TestGraphModel:
    def test_create_graph(self):
        g = Graph()
        assert isinstance(g, Graph)
        assert len(g) == 0

    def test_add_node(self):
        g = Graph()
        n = ExampleNode("Test")
        g.add_node(n)
        assert len(g) == 1
        assert n in g
        assert n.id in g

    def test_add_edge(self):
        g = Graph()
        n = ExampleNode("Test")
        input_socket = Input("compatible", "Input", multi_conns=True)
        n.add_input(input_socket)
        g.add_node(n)
        n2 = ExampleNode("Test2")
        output = Output("compatible", "Output")
        n2.add_output(output)
        g.add_node(n2)
        g.add_edge(output_socket=output, input_socket=input_socket)
        assert len(g) == 2
        assert n2.outputs["compatible"].has_connection()
        assert n.inputs["compatible"].has_connection()

        with pytest.raises(Exception):
            n2.add_output(Output("compatible", "Output"))
            # g.add_edge(output_socket=n2.outputs["output2"], input_socket=n.inputs["input"])

    def test_graph_callback(self):
        g = Graph()
        cb = mock.Mock()
        g.nodeAddedEvent.add(cb)
        n = ExampleNode("Test")
        g.add_node(n)
        cb.assert_called()

    def test_adding_invalid_callback(self):
        g = Graph()
        with pytest.raises(TypeError):
            g.nodeAddedEvent.add("aaaa")

    def test_serialization(self):
        Node._last_node_id = 0
        Connection._last_conn_id = 0
        g = Graph()
        n = ExampleNode("Test")
        n.add_output(Output("link", "Output"))
        n.add_control(Control("control", ControlType.FilePath, "File"))
        n2 = ExampleNode("Test")
        n2.add_input(Input("link", "Input"))

        g.add_node(n)
        g.add_node(n2)
        g.add_edge(n.outputs["link"], n2.inputs["link"])

        json_data = json.dumps(g, default=dispatcher.encoder_default, indent=4)
        print(json_data)
        assert json_data == EXAMPLE_JSON

    def test_deserialization(self):
        g = json.loads(EXAMPLE_JSON, object_hook=dispatcher.decoder_hook)
        assert isinstance(g, Graph)
        assert len(g) == 2

        assert 1 in g
        n = g[1]
        assert len(n.outputs) == 1
        assert "link" in n.outputs
        assert n.outputs["link"].has_connection()
        assert len(n.controls) == 1
        assert "control" in n.controls

        assert 2 in g
        n2 = g[2]
        assert len(n2.inputs) == 1
        assert "link" in n2.inputs
        assert n2.inputs["link"].has_connection()

        assert len(g.edges) == 1
        e = next(g.iter_edges())
        assert e.id == 1
        assert e.input_socket_key == "link"
        assert e.output_socket_key == "link"


a = """{
    "edges": [
        {
            "id": 1,
            "input_socket": {
                "key": "link",
                "name": "Input",
                "compatible": [],
                "multi_conns": false,
                "control": null,
                "__class__": "Input"
            },
            "output_socket": {
                "key": "link",
                "name": "Output",
                "compatible": [],
                "multi_conns": true,
                "__class__": "Output"
            },
            "__class__": "Connection"
        }
    ],
    "__class__": "Graph"
}"""
