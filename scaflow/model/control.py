from __future__ import annotations

from typing import TYPE_CHECKING

from scaflow.model import JsonSerializable, dispatcher

if TYPE_CHECKING:
    from .type_hints import ControlDict, ControlType


@dispatcher
class Control(JsonSerializable):
    size = 24
    height = size

    def __init__(
        self,
        key: str,
        control_type: ControlType,
        name: str,
    ) -> None:
        self._key: str = key  #: Unique key
        self._type: ControlType = control_type
        self._display_name: str = name  #: Control name
        self._data = {}
        self._parent = None

    def set_parent(self, parent):
        self._parent = parent

    def as_dict(self) -> ControlDict:
        return {
            "key": self._key,
            "name": self._display_name,
            "type": self._type,
            "data": self._data,
        }

    @classmethod
    def from_dict(cls, data: ControlDict):
        socket = cls(key=data["key"], control_type=data["type"], name=data["name"])
        socket._data = data["data"]
        return socket

    def update_data(self, key, value):
        self._data[key] = value

    @property
    def key(self):
        return self._key
