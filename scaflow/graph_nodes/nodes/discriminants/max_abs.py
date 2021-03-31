from typing import Any, Callable, Dict

import scared

from scaflow.model.dispatcher import dispatcher
from scaflow.model.node import Node
from scaflow.model.output_socket import Output


@dispatcher
class MaxAbsNode(Node):
    display_name = "Maximum absolute discriminant"

    def __init__(self, name=None):
        super().__init__(name if name else self.display_name)

    @classmethod
    def create_node(cls):
        n = cls()
        n.add_output(Output("discriminant", "Data", return_type="discriminant"))
        return n

    def execute(self, kwargs) -> Callable[[Any, Any], Any]:
        return scared.maxabs
