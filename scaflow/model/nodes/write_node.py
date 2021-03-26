from scaflow.model.base.input_socket import Input
from scaflow.model.base.node import Node


class WriteNode(Node):
    display_name = "Write to file"

    def __init__(self, name=None):
        super().__init__(name if name else self.name)

    @classmethod
    def create_node(cls):
        n = cls()
        n.add_input(Input("input", "Input data"))
        return n
