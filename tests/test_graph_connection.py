import json

from scaflow.model import Connection, Input, Output
from scaflow.model.dispatcher import dispatcher

EXAMPLE_JSON = """{
    "id": 1,
    "input_socket_key": "test",
    "output_socket_key": "test",
    "input_node": 0,
    "output_node": 1,
    "__class__": "Connection"
}"""


class TestGraphConnection:
    def test_serialization(self):
        o = Output("test", "Output")
        i = Input("test", "Input")
        c = Connection(
            output_socket_key=o.key, input_socket_key=i.key, input_node=0, output_node=1
        )

        json_data = json.dumps(c, default=dispatcher.encoder_default, indent=4)
        print(json_data)
        assert json_data == EXAMPLE_JSON

    def test_deserialization(self):
        n = json.loads(EXAMPLE_JSON, object_hook=dispatcher.decoder_hook)
        assert isinstance(n, Connection)
        assert n.id == 1
        assert n.input_socket_key == "test"
        assert n.output_socket_key == "test"
        assert n.input_node == 0
        assert n.output_node == 1

    def test_repr(self):
        o = Output("test", "Output")
        i = Input("test", "Input")
        c = Connection(
            output_socket_key=o.key, input_socket_key=i.key, input_node=0, output_node=1
        )
        assert repr(c) == "<Connection between 0:test and 1:test>"
