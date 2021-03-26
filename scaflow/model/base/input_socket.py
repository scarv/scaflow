from scaflow.model.base.connection import Connection
from scaflow.model.dispatcher import dispatcher
from scaflow.model.base.socket import Socket


@dispatcher
class Input(Socket):
    def __init__(self, key: str, name: str, multi_conns: bool = False) -> None:
        super().__init__(key, name, multi_conns)

    def __repr__(self):
        return f'<Input "{self.key}">'

    def add_connection(self, conn: "Connection"):
        if not self.multi_conns and self.has_connection():
            pass
            # raise Exception("Multiple connections not allowed")
        self.connections.append(conn)
