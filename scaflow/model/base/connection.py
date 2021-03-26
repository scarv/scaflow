from scaflow.model.dispatcher import JsonSerializable, dispatcher


@dispatcher
class Connection(JsonSerializable):
    _last_conn_id = 0  #: Static variable for creating unique connection IDs

    @staticmethod
    def _get_id() -> int:
        Connection._last_conn_id += 1
        return Connection._last_conn_id

    # TODO: Does this need to know its input and output or is it managed by graph.py?
    def __init__(
        self,
        input_node_id: int,
        input_socket_key: str,
        output_node_id: int,
        output_socket_key: str,
    ) -> None:
        """Constructor method for a connection

        :param input_socket_key: Input node of connection
        :type input_socket_key: Input
        :param output_socket_key: Output node of connection
        :type output_socket_key: Output
        """
        self._id: int = Connection._get_id()  #: Unique ID of node

        self.input_node_id = input_node_id
        self.input_socket_key = input_socket_key
        self.output_node_id = output_node_id
        self.output_socket_key = output_socket_key

    def __repr__(self):
        return f"<Connection between {self.input_node_id}.{self.input_socket_key} and {self.output_node_id}.{self.output_socket_key}>"

    @property
    def id(self):
        return self._id

    def as_dict(self):
        return {
            "id": self._id,
            "input_socket_key": self.input_socket_key,
            "output_socket_key": self.output_socket_key,
            "input_node_id": self.input_node_id,
            "output_node_id": self.output_node_id,
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            input_node_id=data["input_node_id"],
            input_socket_key=data["input_socket_key"],
            output_node_id=data["output_node_id"],
            output_socket_key=data["output_socket_key"],
        )

    # def remove(self):
    #     self.input_node.remove_connection(self)
    #     self.output_node.remove_connection(self)

    # def __del__(self):
    #     self.remove()
