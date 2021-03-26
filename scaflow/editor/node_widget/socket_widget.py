from typing import Optional, TYPE_CHECKING

from PySide6 import QtCore, QtGui, QtWidgets
from PySide6.QtGui import QColor, QPen

from scaflow.editor.editor_widget import EditorWidget
from scaflow.model.base import Socket

if TYPE_CHECKING:
    from scaflow.editor import NodeWidget


class SocketWidget(EditorWidget):
    def __init__(self, parent: "NodeWidget", socket: "Socket", align_right: bool):
        super().__init__(parent)

        self._socket = socket
        self._align_right = align_right

        self._color: QtGui.QColor = QtGui.QColor("#96b38a")

        self._text = QtWidgets.QGraphicsTextItem(self._socket.display_name, self)

        self._hover_pen = QPen(QColor("#ffffff"))
        self._hover_pen.setWidth(4)

        label_font = QtGui.QFont()
        label_font.setPointSize(14)
        self._text.setFont(label_font)
        if self._align_right:
            self._text.setPos(self.size / 2, 0)
        else:
            self._text.setPos(-self.size / 2 - self.text_width, 0)

        self._debug = parent.debug_mode
        self._hovering = False

        self.setAcceptHoverEvents(True)
        self.setFlag(QtWidgets.QGraphicsObject.ItemIsSelectable)
        self.setFlag(QtWidgets.QGraphicsItem.ItemIsFocusable)

    def __repr__(self) -> str:
        return f"<SocketWidget: {self._socket.key}>"

    @property
    def size(self):
        return self._socket.size

    @property
    def text_width(self):
        return self._text.boundingRect().width()

    @property
    def text_height(self):
        return self._text.boundingRect().height()

    # def boundingRect(self) -> QtCore.QRectF:
    #     left = -self.size / 2 if self._align_right else -self.size / 2 - self.text_width
    #     return QtCore.QRectF(
    #         left,
    #         -self.size / 2,
    #         self.size + self.text_width,
    #         self.size,
    #     )

    def boundingRect(self) -> QtCore.QRectF:
        left = -self.size / 2 if self._align_right else -self.size / 2 - self.text_width
        return QtCore.QRectF(
            left,
            0,
            self.size + self.text_width,
            self.size,
        )

    @property
    def height(self):
        return self._socket.height

    @property
    def bg_color(self):
        return self._color

    def paint(
        self,
        painter: QtGui.QPainter,
        option: QtWidgets.QStyleOptionGraphicsItem,
        widget: Optional[QtWidgets.QWidget] = ...,
    ) -> None:
        self._hovering = False
        if option.state & QtWidgets.QStyle.State_MouseOver:
            self._hovering = True

        self.setToolTip(self._socket.display_name)

        painter.setBrush(QtGui.QBrush(self.bg_color))
        if self._hovering:
            painter.setPen(self._hover_pen)
        else:
            painter.setPen(QtCore.Qt.NoPen)
        ellipse_size = (self.size - 4) / 2 if self._hovering else self.size / 2
        painter.drawEllipse(
            QtCore.QPointF(0, self.size / 2), ellipse_size, ellipse_size
        )

        if self._debug:
            painter.setPen(QtGui.QColor(255, 255, 0))
            painter.setBrush(QtCore.Qt.NoBrush)

            painter.drawRect(self.boundingRect())

    @property
    def socket(self):
        return self._socket
