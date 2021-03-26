import pytest

from scaflow import model
from scaflow.model.dispatcher import dispatcher
import json


class TestGraphSerialisation:
    def test_socket_json(self):
        output = model.base.Output("key", "name")
        json_data = json.dumps(output, default=dispatcher.encoder_default)

        output2: model.base.Output = json.loads(
            json_data, object_hook=dispatcher.decoder_hook
        )

        assert type(output2) == type(output)
        assert output.key == output2.key
        assert output.display_name == output2.display_name
        assert output.multi_conns == output2.multi_conns

        assert output == output2

    def test_invalid_serialise_class(self):
        with pytest.raises(TypeError):

            @dispatcher
            class Invalid:
                pass
