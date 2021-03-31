from __future__ import annotations

from typing import TYPE_CHECKING

from scaflow.model.dispatcher import JsonSerializable, dispatcher

if TYPE_CHECKING:
    from .type_hints import ConnectionDict


@dispatcher
class Connection(JsonSerializable):
    _last_conn_id = 0  #: Static variable for creating unique connection IDs

    @staticmethod
    def _get_id() -> int:
        Connection._last_conn_id += 1
        return Connection._last_conn_id

    # TODO: Does this need to know its input and output or is it managed by graph.py?
    # def __init__(self, output_socket: Output, input_socket: Input) -> None:
    def __init__(
        self,
        output_socket_key: str,
        output_node: int,
        input_socket_key: str,
        input_node: int,
    ) -> None:
        self._id: int = Connection._get_id()  #: Unique ID of node

        self.output_socket_key = output_socket_key
        self.input_socket_key = input_socket_key
        self.output_node = output_node
        self.input_node = input_node

        # TODO(fergus): Move into graph logic
        # self.input_socket.add_connection(self)

    def __repr__(self):
        return f"<Connection between {self.input_node}:{self.input_socket_key} and {self.output_node}:{self.output_socket_key}>"

    @property
    def id(self):
        return self._id

    def as_dict(self) -> ConnectionDict:
        return {
            "id": self._id,
            "input_socket_key": self.input_socket_key,
            "output_socket_key": self.output_socket_key,
            "input_node": self.input_node,
            "output_node": self.output_node,
        }

    @classmethod
    def from_dict(cls, data: ConnectionDict):
        c = cls(
            input_node=data["input_node"],
            output_node=data["output_node"],
            input_socket_key=data["input_socket_key"],
            output_socket_key=data["output_socket_key"],
        )
        c._id = data["id"]
        Connection._last_conn_id = max(Connection._last_conn_id, data["id"])
        return c
