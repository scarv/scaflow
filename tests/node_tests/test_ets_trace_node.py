import estraces
from estraces import TraceHeaderSet
import pytest

from scaflow.graph_nodes.nodes import ETSTraceNode
import numpy as np


class TestETSTraceNode:
    def test_create_node(self):
        n = ETSTraceNode.create_node()
        assert len(n.inputs) == 1
        assert "filename" in n.inputs
        assert len(n.outputs) == 1
        assert "traces" in n.outputs

    def test_execute_node(self, mocker):
        mocker.patch(
            "estraces.read_ths_from_ets_file",
            return_value=estraces.read_ths_from_ram(samples=np.ndarray(shape=(0, 0))),
        )

        n = ETSTraceNode.create_node()
        r = n.execute({"filename": "test.ets"})
        assert isinstance(r, TraceHeaderSet)

    def test_invalid_execute_node(self):
        n = ETSTraceNode.create_node()
        with pytest.raises(TypeError):
            n.execute({"filename": "test"})
