import logging
from typing import Optional

from PySide6.QtCore import QObject

from scaflow import editor, model
from scaflow.editor.edge_widget import EdgeWidget

logger = logging.getLogger(__name__)


class EventHandler(QObject):
    def __init__(self, parent: editor.GraphicsScene = None):
        QObject.__init__(self, parent)
        logger.debug("Initialising {parent: %s}", parent)
        self.parent = parent
        self.graph: Optional[model.Graph] = None
        self.link_events()

    def link_events(self):
        if self.parent:
            self.graph = self.parent.graph
            self.graph.nodeAddedEvent.add(self._nodeAddedEvent)
            self.graph.edgeAddedEvent.add(self._edgeAddedEvent)
        else:
            logger.error("Cannot connect to graph")

    def _nodeAddedEvent(self, node_id):
        logger.debug("Node added event")
        self.parent.add_node(node_id)

    def _edgeAddedEvent(self, connection):
        logger.debug("Edge added event")
        self.parent.add_edge(connection)

    def removeItems(self, items):
        if not items:
            return
        for i in items:
            if self.parent.is_edge(i):
                i: EdgeWidget = i
                logger.debug("Removing edge: %s", i)
                self.graph.remove_edge(i.src.socket, i.dest.socket)
