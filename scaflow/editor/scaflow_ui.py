import functools
import json
import logging
import os
from pathlib import Path
from typing import Dict, List, Optional, Type

from PySide6.QtCore import QFile, QIODevice
from PySide6.QtUiTools import QUiLoader
from PySide6.QtWidgets import QFileDialog, QMainWindow, QMenu

from scaflow import editor, engine, model

# noinspection PyUnresolvedReferences
from .ui_models import icons_rc
from ..graph_nodes import nodes
from ..model import Node
from ..model.dispatcher import dispatcher

logger = logging.getLogger(__name__)


class ScaflowUI(
    QMainWindow,
):
    def __init__(self):
        super().__init__()

        ui_path = Path(__file__).parent / "ui_models/main_editor.ui"
        ui_file = QFile(str(ui_path))
        ui_file.open(QIODevice.ReadOnly)
        loader = QUiLoader()
        self.ui_model = loader.load(ui_file)
        ui_file.close()

        self.setCentralWidget(self.ui_model)

        self.graph = model.Graph()
        self.view: Optional[editor.GraphicsView] = None

        self._engine = engine.Engine(self.graph)

        self.debug_mode = False

        self._init_graphics_view()
        self._init_node_tree()
        self.setWindowTitle("scaflow")

        self.ui_model.actionDraw_debug_lines.triggered.connect(self.toggle_draw_debug)
        self.ui_model.actionSave_Graph.triggered.connect(self.save_graph)
        self.ui_model.actionOpen_Graph.triggered.connect(self.read_graph)
        self.ui_model.actionExecute_Graph.triggered.connect(self._engine)

        self.ui_model.actionAbout.triggered.connect(self._show_about)

        # TODO(fergus): Implement zoom sliders
        # self.ui_model.statusbar.addWidget(ZoomSlider())

    def _init_graphics_view(self):
        self.view = editor.GraphicsView(ui=self, parent=self.ui_model.gview)
        self.ui_model.gviewLayout.addWidget(self.view)

    def _init_node_tree(self):
        self.nodeTree = editor.NodeTreeWidget(ui=self, parent=self.ui_model.nodesTree)
        self.ui_model.nodesTreeLayout.addWidget(self.nodeTree)

    @staticmethod
    def _show_about():
        dlg = editor.AboutUI()
        dlg.exec_()

    @property
    def node_types(
        self,
    ) -> Dict[str, List[Type[Node]]]:
        """All supported node types, used in creation of context menus.

        Returns:
            A nested list of strings identifying types of nodes allowed within the editor
        """
        return {
            "Constants": [
                nodes.TraceFileNode,
                nodes.PlaintextFileNode,
                nodes.CiphertextFileNode,
            ],
            "Input": [nodes.ETSTraceNode, nodes.NpyTraceNode],
            "Output": [],
            "Selection": [nodes.FirstSubBytesNode],
            "Model": [nodes.HammingWeightNode],
            "Discriminants": [nodes.MaxAbsNode],
            "Attack": [nodes.CPAAttackNode],
            "Preprocessing": [nodes.FindPeaksNode]
            # "Processing": [nodes.SplitNode, nodes.ConcatNode],
        }

    def add_node_option(self, node_type: "Type[model.Node]", pos):
        logger.info("Adding node to graph: %s", node_type)
        node = node_type.create_node()
        node.position = (pos[0], pos[1])

        self.graph.add_node(node)

    def toggle_draw_debug(self):
        logger.info("Toggle draw debug lines: %s", self.ui_model.actionDraw_debug_lines)
        self.debug_mode = self.ui_model.actionDraw_debug_lines.isChecked()
        for node in self.view.scene().get_nodes():
            node.debug_mode = self.debug_mode

        self.view.scene().update()

    def save_graph(self):
        filename, _ = QFileDialog.getSaveFileName(
            self,
            caption="Save scaflow graph",
            dir=os.getcwd(),
            filter="JSON (*.json)",
        )
        if not filename:
            return
        logger.info("Saving graph to file '%s'", filename)

        logger.debug(json.dumps(self.graph, default=dispatcher.encoder_default))
        with open(filename, "w") as file:
            file.write(json.dumps(self.graph, default=dispatcher.encoder_default))

    def read_graph(self):
        filename, _ = QFileDialog.getOpenFileName(
            self,
            caption="Open graph from file",
            dir=os.getcwd(),
            filter="JSON (*.json)",
        )
        if not filename:
            return
        with open(filename, "r") as file:
            self.graph.from_graph(
                json.loads(file.read(), object_hook=dispatcher.decoder_hook)
            )

        # self.graph.from_JSON(json_data)

    def create_context_menu(self, parent, pos, node_menu=False):
        parent.clear()

        menu_add_node = QMenu("Add node:", parent)
        menu_node_color = QMenu("Node color:", parent)
        menu_node_attributes = QMenu("Attributes:", parent)

        # If not over a node, create context menus for adding nodes
        if not node_menu:
            for submenu in self.graph.node_types:
                submenu_widget = QMenu(submenu)
                for node in self.graph.node_types[submenu]:
                    # logger.debug("Node added %s", node)
                    node_action = submenu_widget.addAction(node.display_name)
                    node_action.triggered.connect(
                        functools.partial(
                            self.add_node_option, node_type=node, pos=[pos.x(), pos.y()]
                        )
                    )
                menu_add_node.addMenu(submenu_widget)
            parent.addMenu(menu_add_node)

        if node_menu:
            parent.addMenu(menu_node_color)
            parent.addMenu(menu_node_attributes)
