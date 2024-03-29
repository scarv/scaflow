import logging
from pathlib import Path

import estraces
from estraces import TraceHeaderSet
import numpy as np

from scaflow.model.dispatcher import dispatcher
from scaflow.model.input_socket import Input
from scaflow.model.output_socket import Output
from scaflow.model.node import Node

logger = logging.getLogger(__name__)


@dispatcher
class NpyTraceNode(Node):

    display_name = "Numpy Trace Input"

    def __init__(self, name="Trace Input"):
        super().__init__(name)

    @classmethod
    def create_node(cls):
        n = cls()
        n.add_input(Input("filename", "Trace File", accepted_types=["str"]))
        n.add_input(Input("plaintext", "Plaintext File", accepted_types=["str"]))
        n.add_input(Input("ciphertext", "Ciphertext File", accepted_types=["str"]))
        n.add_output(Output("traces", "Output", return_type="TraceHeaderSet"))
        return n

    def execute(self, kwargs):
        filename = kwargs.get("filename")
        plaintext = kwargs.get("plaintext")
        ciphertext = kwargs.get("ciphertext")
        logger.debug("Input to trace node: %s, %s, %s", filename, plaintext, ciphertext)
        suffix = Path(filename).suffix
        if suffix != ".npy":
            raise TypeError("Invalid file type for trace node")
        traces = np.load(filename)
        plains = np.load(plaintext)
        ciphers = np.load(ciphertext)
        traces = estraces.read_ths_from_ram(
            samples=np.copy(traces), **{"plaintext": plains, "ciphertext": ciphers}
        )
        # out = {"traces": traces, "plaintext": plains, "ciphertext": ciphers}
        # logger.debug("Outputs: %s", out)

        return traces
