import logging
from pathlib import Path

import estraces
import scared
import numpy as np

from scaflow.model.dispatcher import dispatcher
from scaflow.model.base.input_socket import Input
from scaflow.model.base.output_socket import Output
from scaflow.model.base.node import Node

logger = logging.getLogger(__name__)


@dispatcher
class ETSTraceNode(Node):

    display_name = "ETS Trace Input"

    def __init__(self, name="Trace Input"):
        super().__init__(name)

    @classmethod
    def create_node(cls):
        n = cls()
        n.add_input(Input("filename", "Trace File"))
        n.add_output(Output("traces", "Output"))
        return n

    def execute(self, kwargs):
        filename = kwargs.get("filename")
        logger.debug("Input to trace node: %s", filename)
        suffix = Path(filename).suffix
        if suffix == ".ets":
            traces = scared.traces.read_ths_from_ets_file(filename)
        elif suffix == ".npy":
            traces = np.load(filename)
            traces = estraces.read_ths_from_ram(samples=np.copy(traces))
            logger.debug(traces)
        else:
            raise TypeError("Invalid file type for trace node")
        return traces
