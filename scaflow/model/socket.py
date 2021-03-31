from __future__ import annotations

import logging
from typing import List, TYPE_CHECKING

from scaflow.model import JsonSerializable, dispatcher

if TYPE_CHECKING:
    from .connection import Connection
    from .type_hints import SocketDict

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

    def has_connection(self):
        return len(self.connections) > 0

    def remove_connection(self, connection: Connection):
        self.connections.remove(connection)

    def remove_connections(self):
        for conn in self.connections:
            self.remove_connection(conn)

    def add_compatible(self, compatible: str):
        if compatible not in self._compatible:
            self._compatible.append(compatible)
