from .dispatcher import dispatcher
from .socket import Socket
from .connection import Connection

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .input_socket import Input


@dispatcher
class Output(Socket):
    def __init__(self, key: str, name: str, multi_conns: bool = True) -> None:
        super().__init__(key, name, multi_conns)

    def __repr__(self):
        return f'<Output "{self.key}">'

    def add_connection(self, input_socket: "Input"):
        if not self.compatible_with(input_socket):
            raise TypeError("Not compatible with socket")
        if not input_socket.multi_conns and input_socket.has_connection():
            raise Exception("Input already has a connection")
        if not self.multi_conns and self.has_connection():
            raise Exception("Output already has a connection")

        connection = Connection(
            output_socket_key=self.key,
            output_node=self.node.id,
            input_socket_key=input_socket.key,
            input_node=input_socket.node.id,
        )
        self.connections.append(connection)
        input_socket.add_connection(connection)
        return connection
