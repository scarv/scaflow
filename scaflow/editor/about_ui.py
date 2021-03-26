from PySide6 import QtCore, QtUiTools, QtWidgets
from PySide6.QtCore import QIODevice


class AboutUI(QtWidgets.QDialog):
    def __init__(self):
        super().__init__()

        ui_file = QtCore.QFile("editor/ui_models/about.ui")
        ui_file.open(QIODevice.ReadOnly)
        loader = QtUiTools.QUiLoader()
        self.ui_model = loader.load(ui_file)
        ui_file.close()

        layout = QtWidgets.QBoxLayout(QtWidgets.QBoxLayout.Direction.Up)
        layout.addWidget(self.ui_model)
        self.setLayout(layout)
