import scared

from scaflow.model.dispatcher import dispatcher
from scaflow.model.node import Node
from scaflow.model.output_socket import Output


@dispatcher
class HammingWeightNode(Node):
    display_name = "Hamming Weight"

    def __init__(self, name=None):
        super().__init__(name if name else self.display_name)

    @classmethod
    def create_node(cls):
        n = cls()
        n.add_output(Output("model", "Hamming Weights"))
        return n

    def execute(self, kwargs):
        return scared.HammingWeight
