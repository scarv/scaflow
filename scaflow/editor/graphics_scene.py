import logging
from typing import Any, Dict, TYPE_CHECKING

from PySide6.QtCore import QLineF, Qt
from PySide6.QtGui import QBrush, QColor, QPen, QTransform
from PySide6.QtWidgets import (
    QApplication,
    QGraphicsLineItem,
    QGraphicsScene,
    QGraphicsSceneMouseEvent,
)

from scaflow import editor, model
from scaflow.editor.edge_widget import EdgeWidget
from scaflow.model import Connection, Input, Output

if TYPE_CHECKING:
    from scaflow.editor import NodeWidget

logger = logging.getLogger(__name__)


class GraphicsScene(QGraphicsScene):
    def __init__(
        self,
        ui: editor.ScaflowUI,
        graph: model.Graph,
        parent: editor.GraphicsView = None,
    ):
        QGraphicsScene.__init__(self, parent)

        self.ui = ui
        self.graph = graph

        self.line = None
        self.handler = editor.EventHandler(self)
        self.node_widgets: Dict[Any, NodeWidget] = {}

    def initialize(self):
        self.node_widgets = {}
        self.clear()

    def get_nodes(self):
        return [item for item in self.items() if self.is_node(item)]

    def is_node(self, item):
        return isinstance(item, editor.NodeWidget)

    def add_node(self, node_id):
        logger.debug("Adding node <%d>", node_id)

        if node_id in self.graph:
            node = self.graph[node_id]
            widget = editor.NodeWidget(node, debug_mode=self.ui.debug_mode)
            self.node_widgets[node_id] = widget
            self.addItem(widget)

            widget.nodeChanged.connect(self.node_changed_event)

    def add_edge(self, connection: Connection):
        logger.debug("Adding edge %s", connection)
        output_node_widget = self.node_widgets[connection.output_node]
        input_node_widget = self.node_widgets[connection.input_node]

        # logger.debug(output_node_widget._sockets)
        output_socket_widget = output_node_widget._sockets[connection.output_socket_key]
        input_socket_widget = input_node_widget._sockets[connection.input_socket_key]

        edge_widget = EdgeWidget(output_socket_widget, input_socket_widget)
        self.addItem(edge_widget)

    def mousePressEvent(self, event: QGraphicsSceneMouseEvent):

        item = self.itemAt(event.scenePos(), QTransform())
        # node = self.nodeAt(event.scenePos())

        # modifiers = QApplication.keyboardModifiers()

        if event.button() == Qt.LeftButton:
            if item:
                logger.debug("GraphicsScene: Clicked on item <%s>", item)
                if isinstance(item, editor.SocketWidget):
                    pen = QPen(
                        QBrush(QColor(251, 251, 251)),
                        1,
                        Qt.SolidLine,
                    )
                    self.line = QGraphicsLineItem(
                        QLineF(event.scenePos(), event.scenePos())
                    )
                    self.line.setPen(pen)
                    self.addItem(self.line)
                    self.update(self.itemsBoundingRect())

        self.update()
        QGraphicsScene.mousePressEvent(self, event)

    # def mouseDoubleClickEvent(self, event: QGraphicsSceneMouseEvent) -> None:
    #     QGraphicsScene.mouseDoubleClickEvent(self, event)

    def mouseMoveEvent(self, event):
        """Called when mouse moved in scene.

        Updates line, if a line is currently being drawn.

        Args:
            event:
        """
        if self.line:
            self.line.setLine(QLineF(self.line.line().p1(), event.scenePos()))

        QGraphicsScene.mouseMoveEvent(self, event)
        self.update()

    def mouseReleaseEvent(self, event: QGraphicsSceneMouseEvent):
        """Called when mouse is released over graphics scene.

        Creates an edge between sockets if valid

        Args:
            event:
        """
        if self.line:
            source_items = self.items(self.line.line().p1())

            # Remove line item from start and end points
            if source_items and source_items[0] == self.line:
                source_items.pop(0)

            dest_items = self.items(self.line.line().p2())

            if dest_items and dest_items[0] == self.line:
                dest_items.pop(0)

            if source_items and dest_items:
                source_conn = source_items[0]
                dest_conn = dest_items[0]

                logger.debug("Source: %s, Dest: %s", source_conn, dest_conn)

                if (
                    not isinstance(source_conn, editor.SocketWidget)
                    or not isinstance(dest_conn, editor.SocketWidget)
                    or source_conn == dest_conn
                ):
                    return

                src_dag = source_conn.socket
                dest_dag = dest_conn.socket

                if src_dag.compatible_with(dest_dag) or dest_dag.compatible_with(
                    src_dag
                ):
                    if isinstance(src_dag, Input) and isinstance(dest_dag, Output):
                        self.graph.add_edge(dest_dag, src_dag)
                    elif isinstance(src_dag, Output) and isinstance(dest_dag, Input):
                        self.graph.add_edge(src_dag, dest_dag)

        if self.line:
            self.line.scene().removeItem(self.line)
            self.line = None
        QGraphicsScene.mouseReleaseEvent(self, event)
        self.update()

    def node_changed_event(self, node: "NodeWidget"):
        pos = (node.pos().x(), node.pos().y())
        node.setToolTip("(%d, %d)" % (pos[0], pos[1]))
        node._node.position = pos

        # SIGNAL MANAGER (Scene -> Graph)
        # self.handler.sceneNodesUpdatedAction([node,])

    def node_deleted_event(self, node):
        if self.is_node(node):
            node.close()

        if self.is_edge(node):
            node.close()

    def color_changed_action(self, color):
        nodes = self.selectedNodes()
        for node in nodes:
            if self.is_node(node):
                node.dagnode.color = color
                node.from_graph()

    def is_edge(self, widget):
        return isinstance(widget, EdgeWidget)

    def validate_connection(self, src, dest, force=True):
        if self.line:
            if not self.is_connection(src) or not self.is_connection(dest):
                print(
                    "Error: source or destination objects are not Connection widgets."
                )
                return False

            if src.isInputConnection() or dest.isOutputConnection():
                print("Error: invalid connection order.")
                return False

            # don't let the user connect input/output on the same node!
            if str(src.dagnode._id) == str(dest.dagnode._id):
                print("Error: same node connection.")
                return False

            if not dest.is_connectable:
                if not force:
                    logger.warning(
                        'Error: "%s" is not connectable.', dest.connection_name
                    )
                    return False

                for edge in dest.connections.values():
                    logger.warning('forcing edge removal: "%s"', edge._display_name)
                    edge.close()
                return True

        return True
