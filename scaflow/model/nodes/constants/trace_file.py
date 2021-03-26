from .file_node import FileNode
from ...dispatcher import dispatcher


@dispatcher
class TraceFileNode(FileNode):
    display_name = "Trace File"
    output_type = "file"
