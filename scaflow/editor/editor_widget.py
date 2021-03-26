from PySide6 import QtWidgets


class EditorWidget(QtWidgets.QGraphicsObject):
    """Superclass for widgets within editor with debug modes"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self._debug = False

    @property
    def debug_mode(self) -> bool:
        """Controls if widget is drawn with debug lines

        Changes propagate down through child items

        Returns:
            Widget debug mode
        """
        return self._debug

    @debug_mode.setter
    def debug_mode(self, value):
        if value != self.debug_mode:
            self._debug = value
            for item in self.childItems():
                item.debug_mode = value
