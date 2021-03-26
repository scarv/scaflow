import abc
from typing import Dict
import enum

from scaflow.model.dispatcher import JsonSerializable, dispatcher


class ControlType(str, enum.Enum):
    FilePath = "file_path"


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
        self.key: str = key  #: Unique key
        self.type: ControlType = control_type
        self.display_name: str = name  #: Control name
        self.data = {}

    def as_dict(self) -> Dict:
        return {
            "key": self.key,
            "name": self.display_name,
            "type": self.type,
            "data": self.data,
        }

    @classmethod
    def from_dict(cls, data):
        socket = cls(key=data["key"], control_type=data["type"], name=data["name"])
        socket.data = data["data"]
        return socket

    def update_data(self, key, value):
        self.data[key] = value
