from typing import Dict

import scared

from ...dispatcher import dispatcher
from scaflow.model.base.node import Node
from scaflow.model.base.output_socket import Output


@dispatcher
class MaxAbsNode(Node):
    display_name = "Maximum absolute discriminant"

    def __init__(self, name=None):
        super().__init__(name if name else self.display_name)

    @classmethod
    def create_node(cls):
        n = cls()
        n.add_output(Output("discriminant", "Data"))
        return n

    def execute(self, kwargs) -> Dict[str, any]:
        return scared.maxabs
