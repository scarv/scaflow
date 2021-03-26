import logging
import os

from PySide6.QtCore import Qt
from PySide6.QtGui import QFontMetrics
from PySide6.QtWidgets import QFileDialog, QGraphicsItem, QGraphicsSceneMouseEvent

from scaflow import editor
from scaflow.model.base import Control
from ..node_control import NodeControl

logger = logging.getLogger(__name__)


class FilenameControl(NodeControl):
    def __init__(
        self,
        parent: "editor.NodeWidget",
        width: int,
        height: int,
        control: "Control",
    ):
        super(FilenameControl, self).__init__(parent, width, height, control)

        self.setFlag(
            QGraphicsItem.ItemIsSelectable
        )  # Needed in order to receive click events
        filename = self._control.data.get("filename", None)
        if filename:
            self._set_filename(filename)

    def _set_filename(self, filename):
        font_metrics = QFontMetrics(self._value_text.font())
        elided = font_metrics.elidedText(
            os.path.relpath(filename), Qt.TextElideMode.ElideLeft, self._text_width
        )
        self._value = filename
        self._value_text.setPlainText(elided)

    def mouseDoubleClickEvent(self, event: QGraphicsSceneMouseEvent) -> None:
        filename, _ = QFileDialog.getOpenFileName(
            self.parentWidget(),
            caption="Select trace file",
            dir=os.getcwd(),
            filter="Trace Files (*.ets *.npy)",
        )
        if not filename:
            return
        # TODO(fergus): Make relpath relative to saved graph file
        logger.info("Trace file selected: '%s'", os.path.relpath(filename))
        self._control.update_data("filename", filename)
        self._set_filename(filename)
        QGraphicsItem.mouseDoubleClickEvent(self, event)
