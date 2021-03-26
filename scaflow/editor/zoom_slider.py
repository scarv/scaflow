import logging

import PySide6
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QSlider

logger = logging.getLogger(__name__)


class ZoomSlider(QSlider):
    def __init__(self, parent=None):
        QSlider.__init__(self, Qt.Orientation.Horizontal, parent)

        self.setMinimum(10)
        self.setMaximum(500)
        self.setValue(100)
        self.setTickPosition(QSlider.TickPosition.TicksBelow)

    def sliderChange(
        self, change: PySide6.QtWidgets.QAbstractSlider.SliderChange
    ) -> None:

        logger.debug(change)
        super().sliderChange(change)
