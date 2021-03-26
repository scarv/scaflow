from scaflow.model.dispatcher import dispatcher
from scaflow.model.base.socket import Socket


@dispatcher
class Output(Socket):
    def __init__(self, key: str, name: str, multi_conns: bool = True) -> None:
        super().__init__(key, name, multi_conns)

    def __repr__(self):
        return f'<Output "{self.key}">'
