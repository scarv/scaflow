from typing import Type

import scared
from scared.selection_functions import SelectionFunction

from scaflow.model.dispatcher import dispatcher
from scaflow.model.node import Node
from scaflow.model.output_socket import Output


@dispatcher
class FirstSubBytesNode(Node):
    display_name = "First Sub Bytes"

    def __init__(self, name=None):
        super().__init__(name if name else self.display_name)

    @classmethod
    def create_node(cls):
        n = cls()
        n.add_output(Output("selection", "Data", return_type="selection"))
        return n

    def execute(self, kwargs) -> Type[SelectionFunction]:
        # Disable inspection as the type checker cannot determine that the class is wrapped with SelectionFunction
        # noinspection PyTypeChecker
        return scared.aes.selection_functions.encrypt.FirstSubBytes
