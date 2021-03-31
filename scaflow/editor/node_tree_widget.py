import logging

from PySide6 import QtCore, QtGui, QtWidgets

from scaflow import editor

logger = logging.getLogger(__name__)


class NodeTreeWidget(QtWidgets.QTreeWidget):
    """Tree of nodes that appears on the left side of editor.

    Allows the creation of nodes in the graph by double clicking an item, or dragging it to the editor
    """

    def __init__(self, ui: editor.ScaflowUI, parent=None):
        super().__init__(parent)

        self.logger = logging.getLogger(__name__)
        self._parent = ui

        for node_type in self._parent.node_types:
            type_header = QtWidgets.QTreeWidgetItem(self, [node_type])
            type_header.setExpanded(True)
            for node in self._parent.node_types[node_type]:
                item = QtWidgets.QTreeWidgetItem(type_header, [node.display_name])
                item.setData(1, 0, (node_type, node))

        self.itemDoubleClicked.connect(self._node_clicked)
        self.setDragEnabled(True)

    def startDrag(self, supported_actions: QtCore.Qt.DropActions) -> None:
        """Overrides default Qt operation for dragging tree widget items, adding the node data in the mime data

        Args:
            supported_actions: Supported drop actions
        """
        drag = QtGui.QDrag(self)
        mime = QtCore.QMimeData()
        selected_item: QtWidgets.QTreeWidgetItem = self.selectedItems()[0].data(1, 0)
        if selected_item:
            mime.setData(
                "node",
                QtCore.QByteArray(
                    bytes(
                        f"{selected_item[0]}/{selected_item[1].display_name}", "utf-8"
                    )
                ),
            )
            mime.setText(f"{selected_item[0]}/{selected_item[1].display_name}")
            # self.logger.debug(f"{selected_item[0]}/{selected_item[1].name}")
            drag.setMimeData(mime)
            drag.exec_(supported_actions)

    def _node_clicked(self, item: QtWidgets.QTreeWidgetItem):
        # self.logger.debug(item.data(1, 0))
        if item.data(1, 0):
            self._parent.add_node_option(node_type=item.data(1, 0)[1], pos=[0, 0])
