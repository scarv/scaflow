import logging
from typing import Dict

import numpy as np
import scared

from scaflow.model import Input, Node, Output, dispatcher

logger = logging.getLogger(__name__)


@dispatcher
class CPAAttackNode(Node):
    display_name = "CPA Attack"

    def __init__(self, name=None):
        super().__init__(name if name else self.display_name)

    @classmethod
    def create_node(cls):
        n = cls()
        traces_input = Input("traces", "Traces")
        traces_input.add_compatible("peaks")
        n.add_input(traces_input)
        n.add_input(Input("selection", "Selection function"))
        n.add_input(Input("model", "Model"))
        n.add_input(Input("discriminant", "Discriminant"))
        n.add_output(Output("output", "Data"))
        return n

    def execute(self, kwargs) -> Dict[str, any]:
        traces = kwargs.get("traces")
        selection = kwargs.get("selection")
        model = kwargs.get("model")
        discriminant = kwargs.get("discriminant")
        # logger.debug(kwargs)
        # logger.debug(traces, selection, model, discriminant)
        att = scared.CPAAttack(
            selection_function=selection(),
            model=model(),
            discriminant=discriminant,
        )
        container = scared.Container(traces)
        att.run(container)

        recovered_masterkey = np.argmax(att.scores, axis=0).astype("uint8")
        logger.info(
            "Recovered key: %s",
            "".join([format(key_byte, "02X") for key_byte in recovered_masterkey]),
        )

        recomputed_ciphertexts = scared.aes.encrypt(
            traces.plaintext, recovered_masterkey
        )
        logger.info(
            "Recomputed ciphertexts equal: %s",
            np.array_equal(recomputed_ciphertexts, traces.ciphertext),
        )
        return {}
