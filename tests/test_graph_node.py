import json
from typing import Dict

import pytest

from scaflow import model
from scaflow.model import Input
from scaflow.model.node import Spacing
from scaflow.graph_nodes.controls import FileControl
from scaflow.model.dispatcher import dispatcher


@dispatcher
class ExampleNode(model.Node):
    @classmethod
    def create_node(cls):
        pass

    def execute(self, kwargs) -> Dict[str, any]:
        pass


EXAMPLE_JSON = """{
    "id": 1,
    "name": "Test",
    "inputs": [
        {
            "key": "input",
            "name": "",
            "compatible": [],
            "multi_conns": false,
            "control": null,
            "accepted_types": [
                "str"
            ],
            "__class__": "Input"
        }
    ],
    "outputs": [
        {
            "key": "output",
            "name": "",
            "compatible": [],
            "multi_conns": true,
            "return_type": "str",
            "__class__": "Output"
        }
    ],
    "controls": [
        {
            "key": "file",
            "name": "File",
            "type": "file_path",
            "data": {},
            "__class__": "FileControl"
        }
    ],
    "position": [
        100,
        100
    ],
    "__class__": "ExampleNode"
}"""


class TestGraphNode:
    def test_no_abstract_node(self):
        with pytest.raises(TypeError):
            model.Node()

    def test_spacing_all(self):
        s = Spacing(111)
        assert s.top == 111 and s.right == 111 and s.bottom == 111 and s.left == 111
        assert s.lr == 222
        assert s.tb == 222

    def test_spacing_tb_lr(self):
        s = Spacing(111, 222)
        assert s.top == 111 and s.right == 222 and s.bottom == 111 and s.left == 222
        assert s.lr == 444
        assert s.tb == 222

    def test_spacing_t_lr_b(self):
        s = Spacing(111, 222, 333)
        assert s.top == 111 and s.right == 222 and s.bottom == 333 and s.left == 222
        assert s.lr == 444
        assert s.tb == 444

    def test_spacing_t_r_b_l(self):
        s = Spacing(111, 222, 333, 444)
        assert s.top == 111 and s.right == 222 and s.bottom == 333 and s.left == 444
        assert s.lr == 666
        assert s.tb == 444

    def test_inputs(self):
        n = ExampleNode("Test")
        i = model.Input("input", "", accepted_types=["str"])
        n.add_input(i)
        assert len(n.inputs) == 1
        assert i.key in n.inputs
        n.remove_input(i)
        assert len(n.inputs) == 0

    def test_outputs(self):
        n = ExampleNode("Test")
        o = model.Output("output", "", return_type="str")
        n.add_output(o)
        assert len(n.outputs) == 1
        assert o.key in n.outputs
        n.remove_output(o)
        assert len(n.outputs) == 0

    def test_duplicate_key_raises_exception(self):
        n = ExampleNode("Test")
        n.add_input(model.Input("input", "", accepted_types=["str"]))
        with pytest.raises(Exception):
            n.add_input(model.Input("input", "", accepted_types=["str"]))

    def test_already_assigned_node_raises_error(self):
        n = ExampleNode("Test")
        i = model.Input("input", "", accepted_types=["str"])
        n.add_input(i)
        n2 = ExampleNode("Test2")
        with pytest.raises(Exception):
            n2.add_input(i)

    def test_control_duplicate_key_raises_exception(self):
        n = ExampleNode("Test")
        n.add_control(FileControl("file", "File"))
        with pytest.raises(Exception):
            n.add_control(FileControl("file", "File"))

    def test_controls(self):
        n = ExampleNode("Test")
        ctrl = FileControl("file", "File")
        n.add_control(ctrl)
        assert ctrl.key in n.controls
        assert len(n.controls) == 1
        n.remove_control(ctrl)
        assert len(n.controls) == 0

    def test_serialization(self):
        model.Node._last_node_id = 0
        n = ExampleNode("Test")
        n.add_input(Input("input", "", accepted_types=["str"]))
        n.add_control(FileControl("file", "File"))
        n.add_output(model.Output("output", "", return_type="str"))
        n.position = (100, 100)

        json_data = json.dumps(n, default=dispatcher.encoder_default, indent=4)
        assert json_data == EXAMPLE_JSON

    def test_deserialization(self):
        n = json.loads(EXAMPLE_JSON, object_hook=dispatcher.decoder_hook)
        assert isinstance(n, ExampleNode)
        assert n.id == 1
        assert n.display_name == "Test"
        assert len(n.inputs) == 1
        assert len(n.outputs) == 1
        assert len(n.controls) == 1
        assert n.position == (100, 100)
