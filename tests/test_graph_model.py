from typing import Dict
from unittest import mock

import pytest

from scaflow import model


class ExampleNode(model.base.Node):
    @classmethod
    def create_node(cls):
        pass

    def execute(self, kwargs) -> Dict[str, any]:
        pass


class TestGraphModel:
    def test_create_graph(self):
        g = model.Graph()
        assert isinstance(g, model.Graph)
        assert len(g) == 0

    def test_node_types_is_list(self):
        g = model.Graph()
        assert type(g.node_types) is dict

    def test_add_node(self):
        g = model.Graph()
        n = ExampleNode("Test")
        g.add_node(n)
        assert len(g) == 1
        assert n in g

    def test_add_input(self):
        n = ExampleNode("Test")
        n.add_input(model.base.Input("input", ""))
        assert len(n.inputs) == 1

    def test_add_output(self):
        n = ExampleNode("Test")
        n.add_output(model.base.Output("output", ""))
        assert len(n.outputs) == 1

    def test_add_edge(self):
        g = model.Graph()
        n = ExampleNode("Test")
        n.add_input(model.base.Input("input", "Input", multi_conns=True))
        n2 = ExampleNode("Test2")
        n2.add_output(model.base.Output("output", "Output"))
        g.add_edge(output_socket=n2.outputs["output"], input_socket=n.inputs["input"])
        assert len(g) == 2

        n2.add_output(model.base.Output("output2", "Output"))
        g.add_edge(output_socket=n2.outputs["output2"], input_socket=n.inputs["input"])

    def test_graph_callback(self):
        g = model.Graph()
        cb = mock.Mock()
        g.nodeAddedEvent.add(cb)
        n = ExampleNode("Test")
        g.add_node(n)
        cb.assert_called()

    def test_adding_invalid_callback(self):
        g = model.Graph()
        with pytest.raises(TypeError):
            g.nodeAddedEvent.add("aaaa")
