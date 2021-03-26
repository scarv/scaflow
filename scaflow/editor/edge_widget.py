import logging
import typing
from typing import TYPE_CHECKING

from PySide6.QtCore import QLineF, QPointF, QRectF, QSizeF, Signal
from PySide6.QtGui import QColor, QPainter, QPainterPath, QPainterPathStroker
from PySide6.QtWidgets import QGraphicsItem, QStyle, QStyleOptionGraphicsItem, QWidget

if TYPE_CHECKING:
    from scaflow import editor

from .editor_widget import EditorWidget

logger = logging.getLogger(__name__)


class EdgeWidget(EditorWidget):
    deleted = Signal()

    def __init__(self, src, dest, parent=None):
        super().__init__(parent)

        self.src: editor.SocketWidget = src
        self.dest: editor.SocketWidget = dest

        self.bezier = QPainterPath()
        self._line_width = 5

        self._hovering = False
        self._selected = False

        self.setFlag(QGraphicsItem.ItemIsSelectable)
        self.setFlag(QGraphicsItem.ItemIsFocusable)
        self.setAcceptHoverEvents(True)
        self.setZValue(-1)

    def __del__(self):
        logger.debug("Deleted")

    def get_line(self):
        src_rect: QRectF = self.src.sceneBoundingRect()
        p1 = QPointF(src_rect.right(), src_rect.center().y())
        dest_rect: QRectF = self.dest.sceneBoundingRect()
        p2 = QPointF(dest_rect.left(), dest_rect.center().y())
        return QLineF(self.mapFromScene(p1), self.mapFromScene(p2))

    def update_bezier(self):
        line = self.get_line()
        path = QPainterPath()
        path.moveTo(line.p1().x() + self._line_width / 2, line.p1().y())

        delta_x = line.p2().x() - line.p1().x()
        delta_y = line.p2().y() - line.p1().y()
        tangent = min((delta_x * delta_x + delta_y * delta_y) ** 0.5, 200)
        # logger.debug("Tangent: %s", tangent)
        path.cubicTo(
            line.p1().x() + tangent,
            line.p1().y(),
            line.p2().x() - tangent,
            line.p2().y(),
            line.p2().x() - self._line_width / 2,
            line.p2().y(),
        )

        self.bezier = path

    def boundingRect(self) -> QRectF:
        line = self.get_line()
        p1 = line.p1()
        p2 = line.p2()
        return QRectF(p1, QSizeF(p2.x() - p1.x(), p2.y() - p1.y())).normalized()

    @property
    def line_color(self):
        if self._hovering or self._selected:
            return QColor("#ff0000")
        return QColor("#ffffff")

    def paint(
        self,
        painter: QPainter,
        option: QStyleOptionGraphicsItem,
        widget: typing.Optional[QWidget] = ...,
    ) -> None:
        self.update_bezier()
        self._hovering = False
        self._selected = False
        if option.state & QStyle.State_MouseOver:
            self._hovering = True
        if option.state & QStyle.State_Selected:
            self._selected = True

        stroker = QPainterPathStroker()
        stroker.setWidth(self._line_width)
        expanded_path = stroker.createStroke(self.bezier)
        # painter.drawPath(expanded_path)
        painter.fillPath(expanded_path, self.line_color)
