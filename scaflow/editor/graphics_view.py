import logging

import PySide6
from PySide6.QtCore import QPointF, Qt, Signal
from PySide6.QtGui import (
    QBrush,
    QColor,
    QDragEnterEvent,
    QDragMoveEvent,
    QDropEvent,
    QMouseEvent,
    QPainter,
    QWheelEvent,
)
from PySide6.QtWidgets import QGraphicsView, QMenu, QTreeWidget

from scaflow import editor, model

logger = logging.getLogger(__name__)


class GraphicsView(QGraphicsView):
    statusEvent = Signal(dict)
    selectionChanged = Signal()
    nodesChanged = Signal(list)

    def __init__(self, ui: editor.ScaflowUI, parent=None):
        QGraphicsView.__init__(self, parent)

        self._parent: editor.ScaflowUI = ui

        self._scale = 1
        self.current_cursor_pos: QPointF = QPointF(0, 0)

        self._init_graphics_scene(ui.graph, ui)

        self.setCacheMode(QGraphicsView.CacheBackground)
        self.setRenderHint(QPainter.Antialiasing)
        self.setTransformationAnchor(QGraphicsView.AnchorUnderMouse)
        self.setResizeAnchor(QGraphicsView.AnchorUnderMouse)
        self.setInteractive(True)
        self.setDragMode(QGraphicsView.RubberBandDrag)
        self.setBackgroundBrush(QBrush(QColor(34, 34, 34)))
        self.setMouseTracking(True)
        self.setAcceptDrops(True)
        self.setContextMenuPolicy(Qt.CustomContextMenu)

        self.scale(1.0, 1.0)

    def _init_graphics_scene(self, graph: model.Graph, ui: editor.ScaflowUI):
        scene = editor.GraphicsScene(ui=ui, graph=graph, parent=self)
        # TODO(fergus): Make scene size scale to be only as big as it needs to be
        scene.setSceneRect(-5000, -5000, 10000, 10000)
        self.setScene(scene)

    def wheelEvent(self, event: QWheelEvent):
        factor = 1.41 ** (event.angleDelta().y() / 480)

        logger.debug(
            f"WheelEvent {{angleDelta: {event.angleDelta().x()}, {event.angleDelta().y()}}}. Scaled to factor: {factor}"
        )

        if event.modifiers() & Qt.ControlModifier:
            self.scale(factor, factor)
            logger.debug(
                f"WheelEvent {{angleDelta: {event.angleDelta().y()}}}. Scaled to factor: {factor}"
            )
            self._scale = factor
        else:
            self.horizontalScrollBar().setValue(
                self.horizontalScrollBar().value() - event.angleDelta().x()
            )
            self.verticalScrollBar().setValue(
                self.verticalScrollBar().value() - event.angleDelta().y()
            )

    def mousePressEvent(self, event: QMouseEvent):
        self.current_cursor_pos = event.pos()
        if event.button() == Qt.LeftButton:
            if event.modifiers() & Qt.ControlModifier:
                self.setDragMode(QGraphicsView.ScrollHandDrag)
            else:
                self.setDragMode(QGraphicsView.RubberBandDrag)
        if event.button() == Qt.RightButton:
            item = self.itemAt(event.pos())
            self.showContextMenu(event.pos(), node_menu=item is not None)
        if event.button() == Qt.MiddleButton:
            self.setDragMode(QGraphicsView.ScrollHandDrag)

        QGraphicsView.mousePressEvent(self, event)

    def mouseReleaseEvent(self, event: QMouseEvent) -> None:
        if event.button() == Qt.MiddleButton:
            self.setDragMode(QGraphicsView.RubberBandDrag)
        QGraphicsView.mouseReleaseEvent(self, event)

    def mouseMoveEvent(self, event: QMouseEvent) -> None:
        if event.buttons() == Qt.MiddleButton:
            offset = self.current_cursor_pos - event.pos()
            self.current_cursor_pos = event.pos()
            self.verticalScrollBar().setValue(
                self.verticalScrollBar().value() + offset.y()
            )
            self.horizontalScrollBar().setValue(
                self.horizontalScrollBar().value() + offset.x()
            )
            self.update()
        QGraphicsView.mouseMoveEvent(self, event)

    # def mouseDoubleClickEvent(self, event: QMouseEvent) -> None:
    #     QGraphicsView.mouseDoubleClickEvent(self, event)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_A:
            bounds_rect = self.scene().itemsBoundingRect()
            self.fitInView(bounds_rect, Qt.KeepAspectRatio)

        if event.key() == Qt.Key_Delete or Qt.Key_Backspace:
            self.scene().handler.removeItems(self.scene().selectedItems())

        self.scene().update()
        return QGraphicsView.keyPressEvent(self, event)

    def showContextMenu(self, pos, node_menu=False):
        """Creates the context menu when right clicking the graphics view.

        Args:
            pos: Position of click
            node_menu: Whether over a node or not (changes contents of menu)
        """
        menu = QMenu()
        self._parent.create_context_menu(menu, self.mapToScene(pos), node_menu)
        menu.exec_(self.mapToGlobal(pos))

    def dragEnterEvent(self, event: QDragEnterEvent) -> None:
        """Called when a dragged object enters the graphics view.
        Used to accept incoming nodes from the node tree

        Args:
            event:
        """
        if isinstance(event.source(), QTreeWidget):
            event.accept()
        else:
            QGraphicsView.dragEnterEvent(self, event)

    def dragMoveEvent(self, event: QDragMoveEvent) -> None:
        """Called when a dragged object is moved over the graphics view.
        Used to accept incoming nodes from the node tree

        Args:
            event:
        """
        # logger.debug("Drag move event: %s", event.source())
        if isinstance(event.source(), QTreeWidget):
            event.accept()
        else:
            QGraphicsView.dragMoveEvent(self, event)

    def dropEvent(self, event: QDropEvent) -> None:
        """Called when an accepted drag object is released over the graphics view.
        Creates a node on the canvas.

        Args:
            event:

        """
        node = event.mimeData().data("node")
        pos = self.mapToScene(event.pos())
        if node:
            node_type, node = [str(s, "utf-8") for s in node.split("/")]
            # logger.debug("%s, %s", node_type, node)
            for n in self._parent.node_types[node_type]:
                if n.display_name == node:
                    event.acceptProposedAction()
                    self._parent.add_node_option(n, [pos.x(), pos.y()])
                    return
        QGraphicsView.dropEvent(self, event)
