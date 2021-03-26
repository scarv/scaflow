import abc
import logging
from typing import Dict, TYPE_CHECKING, Tuple

from PySide6 import QtGui


from scaflow.model.dispatcher import JsonSerializable, dispatcher

if TYPE_CHECKING:
    from scaflow.model.base import Input, Output, Control

Position = Tuple[float, float]  #: A pair of coordinates between -1 and 1

logger = logging.getLogger(__name__)


class Spacing:
    def __init__(self, *args):
        if len(args) == 1:  #: All
            self.top = args[0]
            self.right = args[0]
            self.bottom = args[0]
            self.left = args[0]
        elif len(args) == 2:  #: Top/bottom, left/right
            self.top = args[0]
            self.right = args[1]
            self.bottom = args[0]
            self.left = args[1]
        elif len(args) == 3:  #: Top, left/right, bottom
            self.top = args[0]
            self.right = args[1]
            self.bottom = args[2]
            self.left = args[1]
        else:  #: Top, left, right, bottom
            self.top = args[0]
            self.right = args[1]
            self.bottom = args[2]
            self.left = args[3]

    @property
    def lr(self):
        return self.left + self.right

    @property
    def tb(self):
        return self.top + self.bottom


@dispatcher
class Node(JsonSerializable, abc.ABC):
    """A single node in a flow diagram

    :param name: The name of the node
    :type name: str
    """

    _last_node_id = 0  #: Static variable for creating unique node IDs
    display_name = ""

    def __init__(self, name: str = "") -> None:
        """Constructor method"""
        self.display_name: str = name  #: Name of node
        self._id: int = Node._get_id()  #: Unique ID of node
        self._position: Position = (0, 0)  #: Position of node
        self._inputs: Dict[str, Input] = {}
        self._outputs: Dict[str, Output] = {}
        self._controls: Dict[str, Control] = {}
        self._color: QtGui.QColor = QtGui.QColor(110, 136, 255, 204)

        self._width = 200
        self._margin: Spacing = Spacing(3)
        self._padding: Spacing = Spacing(10)
        self._item_margin = 5
        self._title_height = 25

        self._base_height = 90

    @staticmethod
    def _get_id() -> int:
        Node._last_node_id += 1
        return Node._last_node_id

    @property
    def title_height(self):
        return self._title_height

    @property
    def id(self):
        return self._id

    @property
    def position(self) -> Position:
        return self._position

    @position.setter
    def position(self, pos):
        self._position = pos

    @property
    def color(self):
        return self._color

    @property
    def width(self):
        return self._width

    @property
    def height(self):
        heights = (
            [self._title_height]
            + [i.height for i in self._inputs.values()]
            + [i.height for i in self._outputs.values()]
            + [i.height for i in self._controls.values()]
        )

        return (
            sum(heights)
            + self._item_margin * (len(heights) - 1)
            + self._padding.top
            + self._padding.bottom
        )

    def iter_sockets(self):
        height = self._padding.top + self._title_height + self._item_margin
        for k, v in self._inputs.items():
            # logger.debug("Input socket height: %s", height)
            yield k, v, 0, height
            height += v.height
            height += self._item_margin
        for k, v in self._outputs.items():
            # logger.debug("Output socket height: %s", height)
            yield k, v, self._width, height
            height += v.height
            height += self._item_margin

    def iter_controls(self):
        heights = (
            [self._title_height]
            + [i.height for i in self._inputs.values()]
            + [i.height for i in self._outputs.values()]
        )
        height = self._padding.top + sum(heights) + self._item_margin * len(heights)
        for k, v in self._controls.items():
            # logger.debug("Control height: %s", height)
            yield k, v, height
            height += v.height
            height += self._item_margin

    @property
    def inner_width(self):
        return self._width - self._padding.left - self._padding.right

    @property
    def margin(self):
        return self._margin

    @property
    def padding(self):
        return self._padding

    def as_dict(self):
        return {
            "id": self._id,
            "inputs": [v for _, v in self._inputs.items()],
            "outputs": [v for _, v in self._outputs.items()],
            "controls": [v for _, v in self._controls.items()],
            "position": self._position,
            "name": self.display_name,
        }

    @classmethod
    def from_dict(cls, data: Dict):
        node = cls(data["name"])
        node._id = data["id"]
        node._position = tuple(data["position"])
        for j in data["inputs"]:
            node.add_input(j)
        for j in data["outputs"]:
            node.add_output(j)
        for j in data["controls"]:
            node.add_control(j)
        Node._last_node_id = max(node._id, Node._last_node_id)

        return node

    def add_input(self, input_node: "Input"):
        if input_node.key in self._inputs or input_node.key in self._outputs:
            raise Exception("Item with key already in node")
        elif input_node.node is not None:
            raise Exception("Item already assigned to node")
        else:
            input_node.node = self
            self._inputs[input_node.key] = input_node

    def remove_input(self, input_node: "Input"):
        input_node.remove_connections()
        input_node.node_widget = None
        self._inputs.pop(input_node.key)

    def add_output(self, output_node: "Output"):
        if output_node.key in self._outputs or output_node.key in self._inputs:
            raise Exception("Item with key already in node")
        elif output_node.node is not None:
            raise Exception("Item already assigned to node")
        else:
            output_node.node = self
            self._outputs[output_node.key] = output_node

    def add_control(self, control: "Control"):
        if control.key in self._controls:
            raise Exception("Item with key already in node")
        self._controls[control.key] = control

    @property
    def inputs(self) -> "Dict[str, Input]":
        return self._inputs

    @property
    def outputs(self) -> "Dict[str, Output]":
        return self._outputs

    @property
    def controls(self):
        return self._controls

    @classmethod
    @abc.abstractmethod
    def create_node(cls):
        pass

    @abc.abstractmethod
    def execute(self, kwargs) -> Dict[str, any]:
        pass
