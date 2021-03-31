from __future__ import annotations

from enum import Enum
from typing import Dict, List, Optional, TYPE_CHECKING, Tuple, Type, TypedDict

if TYPE_CHECKING:
    from scaflow.model import Connection, Control, Input, Node, Output

Position = Tuple[float, float]


class ControlType(str, Enum):
    FilePath = "file_path"


class ControlDict(TypedDict):
    key: str
    name: str
    type: ControlType
    data: Dict


class SocketDict(TypedDict):
    key: str
    name: str
    compatible: List[str]
    multi_conns: bool


class InputDict(SocketDict):
    control: Optional["Control"]
    accepted_types: List[str]


class OutputDict(SocketDict):
    return_type: str


class NodeDict(TypedDict):
    id: int
    name: str
    inputs: List[Input]
    outputs: List[Output]
    controls: List[Control]
    position: Position


class ConnectionDict(TypedDict):
    id: int
    input_socket_key: str
    output_socket_key: str
    input_node: int
    output_node: int


class GraphDict(TypedDict):
    nodes: List["Node"]
    edges: List["Connection"]
