from typing import Dict

from scaflow.model.base.output_socket import Output
from scaflow.model.controls import FileControl
from scaflow.model.dispatcher import dispatcher
from .file_node import FileNode


@dispatcher
class PlaintextFileNode(FileNode):
    display_name = "Plaintext File"
    output_type = "file"

    @classmethod
    def create_node(cls):
        c = cls()
        output = Output("plaintext", "File")
        c.add_output(output)
        c.add_control(FileControl("file_control", "File Path"))
        return c

    def execute(self, kwargs) -> Dict[str, any]:
        return self.controls["file_control"].data["filename"]
