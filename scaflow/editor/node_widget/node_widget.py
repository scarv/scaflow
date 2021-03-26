import logging
from typing import Any, Dict, Optional, Type

from PySide6 import QtCore, QtGui, QtWidgets

from scaflow.editor.editor_widget import EditorWidget
from scaflow.model.base import ControlType, Node
from .controls.filename_control import FilenameControl
from .node_background import NodeBackground
from .node_control import NodeControl
from .node_text import NodeText
from .socket_widget import SocketWidget

control_widget_map: Dict[ControlType, Type[NodeControl]] = {
    ControlType.FilePath: FilenameControl
}

logger = logging.getLogger(__name__)


class NodeWidget(EditorWidget):
    """Generic widget for drawing a node of the graph"""

    nodeChanged = QtCore.Signal(object)

    def __init__(
        self,
        node: Node,
        debug_mode=False,
        parent=None,
    ):
        super().__init__(parent)

        self._node = node

        self._debug: bool = debug_mode
        self._hovering = False

        self.setHandlesChildEvents(False)
        self.setFlag(QtWidgets.QGraphicsItem.ItemIsMovable)
        self.setFlag(QtWidgets.QGraphicsItem.ItemIsSelectable)
        self.setFlag(QtWidgets.QGraphicsItem.ItemIsFocusable)
        self.setFlag(QtWidgets.QGraphicsObject.ItemSendsGeometryChanges)
        self.setFlag(
            QtWidgets.QGraphicsObject.ItemSendsScenePositionChanges,
        )
        self.setAcceptHoverEvents(True)

        self._background = NodeBackground(self)
        self._text = NodeText(self)
        self._text.setPos(self._node.padding.left, self._node.padding.top)
        self._sockets: Dict[str, SocketWidget] = {}
        self._controls: Dict[str, NodeControl] = {}

        self.setPos(QtCore.QPointF(node.position[0], node.position[1]))
        self.draw_sockets()

    @property
    def bg_color(self):
        """Background color of node

        Returns:
            A QColor of the current background color
        """
        if self._hovering:
            return self._node.color.lighter(114)
        return self._node.color

    @property
    def width(self):
        """The width of the node (excluding margin)"""
        return self._node.width

    @property
    def height(self):
        """The height of the node (excluding margin)"""
        return self._node.height

    @property
    def node(self):
        return self._node

    def itemChange(
        self,
        change: QtWidgets.QGraphicsItem.GraphicsItemChange,
        value: Any,
    ) -> Any:
        """Called when the widget is changed in any way.

        Args:
            change: Change that happened
            value:

        Returns:

        """
        if change == self.ItemPositionHasChanged:
            self.nodeChanged.emit(self)
        return super().itemChange(change, value)

    def boundingRect(self) -> QtCore.QRectF:
        """Bounding rectangle of widget.

        The top left of a node widget is at (0, 0). Padding extends into negatives
        """
        return QtCore.QRectF(
            -self._node.margin.left,
            -self._node.margin.top,
            self._node.width + self._node.margin.lr,
            self._node.height + self._node.margin.tb,
        )

    def draw_sockets(self):
        """Calculate positions and create socket widgets for node"""

        def draw_socket_pos(key, socket, pos_x: int, align_right):
            """Create a socket widget at a given position, specifying alignment.

            Args:
                key: Key to access socket information
                socket: Socket model
                pos_x: X position (in widget space) to render socket at
                align_right: Position text on the right of the node
            """
            socket_widget: Optional[SocketWidget] = None
            if key in self._sockets:
                socket_widget = self._sockets[key]

            if socket_widget is None:
                logger.debug("Adding socket <%s>", key)

                socket_widget = SocketWidget(self, socket, align_right)
                self._sockets[key] = socket_widget

            socket_widget.setPos(QtCore.QPointF(pos_x, self._current_height_offset))
            self._current_height_offset += socket.height

        # self._current_height_offset = (
        #     self._node.padding.top + self._text.height + Socket.height / 2
        # )
        # self._current_height_offset = next(self._node.iter_socket_heights())
        for socket_key, socket, x, y in self._node.iter_sockets():
            socket_widget: Optional[SocketWidget] = None
            if socket_key in self._sockets:
                socket_widget = self._sockets[socket_key]

            if socket_widget is None:
                logger.debug("Adding socket <%s>", socket_key)

                socket_widget = SocketWidget(self, socket, x == 0)
                self._sockets[socket_key] = socket_widget

            socket_widget.setPos(QtCore.QPointF(x, y))

    def draw_controls(self):
        for k, v, y in self._node.iter_controls():
            if k in self._controls:
                control_widget = self._controls[k]
            else:
                logger.debug("Adding control widget <%s>", k)

                control_widget = control_widget_map[v.type](
                    self, self._node.inner_width, 25, v
                )
                self._controls[k] = control_widget

            # TODO(fergus): Set height of control
            control_widget.setPos(QtCore.QPointF(self._node.padding.left, y))

    def paint(
        self,
        painter: QtGui.QPainter,
        option: QtWidgets.QStyleOptionGraphicsItem,
        widget: Optional[QtWidgets.QWidget] = None,
    ) -> None:
        """Called when a widget needs to be repainted.

        Args:
            painter:
            option:
            widget:
        """
        self._hovering = False
        if option.state & QtWidgets.QStyle.State_MouseOver:
            self._hovering = True

        self.draw_sockets()
        self.draw_controls()

        if self._debug:
            painter.setPen(QtGui.QColor(255, 255, 0))
            painter.setBrush(QtCore.Qt.NoBrush)
            h1 = QtCore.QPoint(0, self.height / 2)
            h2 = QtCore.QPoint(self.width, self.height / 2)
            painter.drawLine(h1, h2)

            v1 = QtCore.QPoint(self.width / 2, 0)
            v2 = QtCore.QPoint(self.width / 2, self.height)
            painter.drawLine(v1, v2)

            painter.drawRect(self.boundingRect())
