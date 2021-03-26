from typing import Dict

from scaflow.model.base.node import Node
from scaflow.model.base.output_socket import Output
from scaflow.model.controls import FileControl
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
        output = Output("filename", "File")
        c.add_output(output)
        c.add_control(FileControl("file_control", "File Path"))
        return c

    def execute(self, kwargs) -> Dict[str, any]:
        return self.controls["file_control"].data["filename"]
