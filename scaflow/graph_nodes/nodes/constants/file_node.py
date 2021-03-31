from typing import Dict, List, Type

from scaflow.model.node import Node
from scaflow.model.output_socket import Output
from scaflow.graph_nodes.controls import FileControl
from scaflow.model.dispatcher import dispatcher


@dispatcher
class FileNode(Node):
    display_name = "File"
    output_type = "file"

    def __init__(self, name=None):
        super().__init__(name if name else self.display_name)

    @classmethod
    def create_node(cls):
        c = cls()
        output = Output("filename", "File", return_type="str")
        c.add_output(output)
        c.add_control(FileControl("file_control", "File Path"))
        return c

    def execute(self, kwargs) -> Dict[str, any]:
        return self.controls["file_control"]._data["filename"]
