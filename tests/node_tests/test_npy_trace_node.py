from estraces import TraceHeaderSet
import pytest

from scaflow.graph_nodes.nodes import NpyTraceNode
import numpy as np


class TestNpyTraceNode:
    def test_create_node(self):
        n = NpyTraceNode.create_node()
        assert len(n.inputs) == 3
        assert "filename" in n.inputs
        assert "plaintext" in n.inputs
        assert "ciphertext" in n.inputs
        assert len(n.outputs) == 1
        assert "traces" in n.outputs

    def test_execute_node(self, mocker):
        mocker.patch("numpy.load", return_value=np.ndarray(shape=(0, 0)))

        n = NpyTraceNode.create_node()
        r = n.execute({"filename": "test.npy"})
        assert isinstance(r, TraceHeaderSet)

    def test_invalid_execute_node(self, mocker):
        mocker.patch("numpy.load", return_value=np.ndarray(shape=(0, 0)))

        n = NpyTraceNode.create_node()
        with pytest.raises(TypeError):
            n.execute({"filename": "test"})
