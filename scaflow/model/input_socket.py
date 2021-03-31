from typing import Optional, TYPE_CHECKING

from scaflow.model import dispatcher
from .socket import Socket

if TYPE_CHECKING:
    from .type_hints import InputDict
    from .control import Control
    from .connection import Connection


@dispatcher
class Input(Socket):
    def __init__(self, key: str, name: str, multi_conns: bool = False) -> None:
        super().__init__(key, name, multi_conns)
        self._control: Optional["Control"] = None

    def __repr__(self):
        return f'<Input "{self.key}">'

    def add_connection(self, conn: "Connection"):
        if not self.multi_conns and self.has_connection():
            raise Exception("Multiple connections not allowed")
        self.connections.append(conn)

    def as_dict(self) -> "InputDict":
        return {
            "key": self.key,
            "name": self.display_name,
            "compatible": self._compatible,
            "multi_conns": self.multi_conns,
            "control": self._control,
        }

    @classmethod
    def from_dict(cls, data: "InputDict"):
        c = cls(data["key"], data["name"], data["multi_conns"])
        c._control = data["control"]
        c._compatible = data["compatible"]
        return c
