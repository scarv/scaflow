import logging
from typing import Optional

from PySide6.QtCore import QRectF, Qt
from PySide6.QtGui import QBrush, QColor, QPainter, QPen
from PySide6.QtWidgets import (
    QGraphicsTextItem,
    QStyleOptionGraphicsItem,
    QWidget,
)

from scaflow import editor
from scaflow.editor.editor_widget import EditorWidget
from scaflow.model import Control

logger = logging.getLogger(__name__)


class NodeControl(EditorWidget):
    def __init__(
        self,
        parent: "editor.NodeWidget",
        width: int,
        height: int,
        control: "Control",
    ):
        super().__init__(parent=parent)

        self._node = parent.node
        self._debug = parent.debug_mode
        self._control = control

        self._total_width = width
        self._total_height = height

        # Minus the height because of rounded edges (diameter height)
        self._text_width = self._total_width - self._total_height

        self._placeholder_text = QGraphicsTextItem(self._control._display_name, self)
        self._placeholder_text.setPos(self._total_height / 2, 0)
        self._placeholder_text.setDefaultTextColor("#545454")

        self._value = ""
        self._value_text = QGraphicsTextItem("", self)
        self._value_text.setPos(self._total_height / 2, 0)
        self._value_text.setDefaultTextColor("#000000")
        self._value_text.hide()

        # self._placeholder_text.setFont(placeholder_font)

        # self._placeholder_text.se

    @property
    def debug_mode(self):
        return self._debug

    @debug_mode.setter
    def debug_mode(self, value):
        self._debug = value

    def boundingRect(self) -> QRectF:
        return QRectF(0, 0, self._total_width, self._total_height)

    def paint(
        self,
        painter: QPainter,
        option: QStyleOptionGraphicsItem,
        widget: Optional[QWidget] = ...,
    ) -> None:
        brush = QBrush(QColor("#ffffff"))
        painter.setBrush(brush)
        painter.setPen(Qt.NoPen)
        painter.drawRoundedRect(
            QRectF(
                0,
                0,
                self._total_width,
                self._total_height,
            ),
            self._total_height / 2,
            self._total_height / 2,
        )

        if self._value:
            self._placeholder_text.hide()
            self._value_text.show()
        else:
            self._value_text.hide()
            self._placeholder_text.show()

        if self._debug:
            debug_pen = QPen(QColor(255, 255, 0))
            debug_pen.setWidthF(0.5)
            debug_pen.setStyle(Qt.DashLine)
            painter.setPen(debug_pen)
            painter.setBrush(Qt.NoBrush)
            painter.drawPolygon(self.boundingRect())
