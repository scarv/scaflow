from typing import Optional

from PySide6 import QtCore, QtGui, QtWidgets

from scaflow import editor
from scaflow.editor.editor_widget import EditorWidget


class NodeBackground(EditorWidget):
    def __init__(self, parent=None, scene=None):
        super().__init__(parent)

        self.setFlag(QtWidgets.QGraphicsItem.ItemIsSelectable, False)
        self.setFlag(QtWidgets.QGraphicsItem.ItemIsSelectable, False)

        self.node_widget: editor.NodeWidget = self.parentItem()

    def boundingRect(self) -> QtCore.QRectF:
        return self.node_widget.boundingRect()

    def paint(
        self,
        painter: QtGui.QPainter,
        option: QtWidgets.QStyleOptionGraphicsItem,
        widget: Optional[QtWidgets.QWidget] = ...,
    ) -> None:
        brush = QtGui.QBrush(self.node_widget.bg_color)
        painter.setBrush(brush)
        painter.setPen(QtCore.Qt.NoPen)
        painter.drawRoundedRect(
            QtCore.QRectF(0, 0, self.node_widget.width, self.node_widget.height), 10, 10
        )

        # path = QtGui.QPainterPath()
        # path.addRoundedRect(
        #     QtCore.QRectF(self.border, self.border, self.width, self.height), 10, 10
        # )
        # painter.fillPath(path, self.node_color)
