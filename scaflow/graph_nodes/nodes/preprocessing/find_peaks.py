import logging
from typing import Dict

import estraces
import numpy as np
from scared.signal_processing import find_peaks

from scaflow.model import Input, Node, Output, dispatcher

logger = logging.getLogger(__name__)


@dispatcher
class FindPeaksNode(Node):
    display_name = "Synchronise Peaks"

    def __init__(self, name=None):
        super().__init__(name if name else self.display_name)

    @classmethod
    def create_node(cls):
        n = cls()
        n.add_input(Input("traces", "Traces"))
        n.add_output(Output("peaks", "Synced Peaks"))
        return n

    def execute(self, kwargs) -> Dict[str, any]:
        traces = kwargs.get("traces")
        # traces = input_data.get("traces")
        # logger.debug("Input to node: %s", traces)

        traces_resync = []

        traces_desync = traces.samples[:]

        for trace_desync in traces_desync:
            peaks = find_peaks(-trace_desync, min_peak_distance=5, min_peak_height=0.10)
            peak_index = peaks[0]

            trace_resync = trace_desync[peak_index - 500 : peak_index + 2000]
            trace_resync = np.reshape(trace_resync, (1, trace_resync.size))
            traces_resync.append(trace_resync)

        traces_resync = np.concatenate(traces_resync, axis=0)
        ths_resync = estraces.read_ths_from_ram(
            samples=traces_resync,
            **{"plaintext": traces.plaintext, "ciphertext": traces.ciphertext}
        )
        return ths_resync
