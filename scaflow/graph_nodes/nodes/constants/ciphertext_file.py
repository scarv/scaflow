from typing import Dict

from scaflow.graph_nodes.controls import FileControl
from scaflow.model import Output, dispatcher
from .file_node import FileNode


@dispatcher
class CiphertextFileNode(FileNode):
    display_name = "Ciphertext File"
    output_type = "file"

    @classmethod
    def create_node(cls):
        c = cls()
        output = Output("ciphertext", "File")
        c.add_output(output)
        c.add_control(FileControl("file_control", "File Path"))
        return c

    def execute(self, kwargs) -> Dict[str, any]:
        return self.controls["file_control"]._data["filename"]
