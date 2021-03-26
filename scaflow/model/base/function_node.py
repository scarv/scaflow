import abc

from scaflow.model.base import Node


class FunctionNode(Node, abc.ABC):
    @abc.abstractmethod
    def execute(self):
        pass
