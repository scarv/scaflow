from typing import Dict

from .file_node import FileNode
from ...base import Output
from ...controls import FileControl
from ...dispatcher import dispatcher


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
        return self.controls["file_control"].data["filename"]
