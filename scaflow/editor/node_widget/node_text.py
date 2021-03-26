from typing import Optional

from PySide6 import QtCore, QtGui, QtWidgets
from PySide6.QtCore import QRectF, Qt
from PySide6.QtGui import QFontMetrics

from scaflow import editor
from scaflow.editor.editor_widget import EditorWidget
from scaflow.model.base import Node


class NodeText(EditorWidget):
    def __init__(self, parent: "editor.NodeWidget"):
        super().__init__(parent=parent)

        self._node: Node = parent.node
        self._debug = parent.debug_mode

        title_font = QtGui.QFont()
        title_font.setPointSize(18)
        font_metrics = QFontMetrics(title_font)
        elided = font_metrics.elidedText(
            self._node.display_name, Qt.TextElideMode.ElideRight, self._node.inner_width
        )
        self._text = QtWidgets.QGraphicsTextItem(elided, self)
        self._text.setFont(title_font)

    @property
    def debug_mode(self):
        return self._debug

    @debug_mode.setter
    def debug_mode(self, value):
        self._debug = value

    @property
    def height(self):
        return self.boundingRect().height()

    def boundingRect(self) -> QtCore.QRectF:
        return QRectF(0, 0, self._node.inner_width, self._node.title_height)

    def paint(
        self,
        painter: QtGui.QPainter,
        option: QtWidgets.QStyleOptionGraphicsItem,
        widget: Optional[QtWidgets.QWidget] = ...,
    ) -> None:

        if self._debug:
            debug_pen = QtGui.QPen(QtGui.QColor(255, 255, 0))
            debug_pen.setWidthF(0.5)
            debug_pen.setStyle(QtCore.Qt.DashLine)
            painter.setPen(debug_pen)
            painter.drawPolygon(self.boundingRect())
