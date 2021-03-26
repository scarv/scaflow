import logging
from typing import Dict, List

from scaflow.model.base.connection import Connection
from scaflow.model.dispatcher import JsonSerializable, dispatcher

logger = logging.getLogger(__name__)


@dispatcher
class Socket(JsonSerializable):
    size = 24
    height = size

    def __init__(self, key: str, name: str, multi_conns: bool) -> None:
        self.key: str = key  #: Unique key
        self.display_name: str = name  #: IO name
        self.multi_conns: bool = (
            multi_conns  #: Whether multiple connections are allowed
        )
        self.connections: List[Connection] = []  #: List of connections
        self._compatible: List[str] = []
        self.node = None

        self._radius = self.size / 2

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Socket):
            return (
                self.key == other.key
                and self.display_name == other.display_name
                and self.multi_conns == other.multi_conns
            )
        return NotImplemented

    def compatibleWith(self, socket: "Socket"):
        # logger.debug("%s, %s", self.key, socket.key)
        return self.key == socket.key or socket.key in self._compatible

    def has_connection(self):
        return len(self.connections) > 0

    def remove_connection(self, connection: Connection):
        self.connections.remove(connection)

    def remove_connections(self):
        self.connections = []

    def add_compatible(self, compatible: str):
        if compatible not in self._compatible:
            self._compatible.append(compatible)

    def as_dict(self) -> Dict:
        return {
            "key": self.key,
            "name": self.display_name,
            "compatible": self._compatible,
            "multi_conns": self.multi_conns,
        }

    @classmethod
    def from_dict(cls, data):
        socket = cls(
            key=data["key"], name=data["name"], multi_conns=data["multi_conns"]
        )
        socket._compatible = data.get("compatible", [])
        return socket
