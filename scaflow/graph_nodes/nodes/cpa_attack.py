import logging
from typing import Any, Callable, Dict, Type

from estraces import TraceHeaderSet
import numpy as np
import scared
from scared import Model
from scared.selection_functions import SelectionFunction

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
        n.add_input(Input("traces", "Traces", accepted_types=["TraceHeaderSet"]))
        n.add_input(
            Input(
                "selection",
                "Selection function",
                accepted_types=["selection"],
            )
        )
        n.add_input(Input("model", "Model", accepted_types=["model"]))
        n.add_input(
            Input("discriminant", "Discriminant", accepted_types=["discriminant"])
        )
        n.add_output(Output("output", "Data", return_type="bool"))
        return n

    def execute(self, kwargs) -> Dict[str, any]:
        traces: TraceHeaderSet = kwargs.get("traces")
        selection = kwargs.get("selection")
        model: Type[Model] = kwargs.get("model")
        discriminant = kwargs.get("discriminant")
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
