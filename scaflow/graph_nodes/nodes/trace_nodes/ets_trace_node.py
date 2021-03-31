import logging
from pathlib import Path
from typing import Dict, List, Type

from estraces import TraceHeaderSet
import scared

from scaflow.model.dispatcher import dispatcher
from scaflow.model.input_socket import Input
from scaflow.model.output_socket import Output
from scaflow.model.node import Node

logger = logging.getLogger(__name__)


@dispatcher
class ETSTraceNode(Node):

    display_name = "ETS Trace Input"

    def __init__(self, name="Trace Input"):
        super().__init__(name)

    @classmethod
    def create_node(cls):
        n = cls()
        n.add_input(Input("filename", "Trace File", accepted_types=["str"]))
        n.add_output(Output("traces", "Output", return_type="TraceHeaderSet"))
        return n

    def execute(self, kwargs):
        filename = kwargs.get("filename")
        logger.debug("Input to trace node: %s", filename)
        suffix = Path(filename).suffix
        if suffix == ".ets":
            traces = scared.traces.read_ths_from_ets_file(filename)
        else:
            raise TypeError("Invalid file type for trace node")
        return traces
