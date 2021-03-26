from scaflow.model.base import Control, ControlType
from scaflow.model.dispatcher import dispatcher


@dispatcher
class FileControl(Control):
    def __init__(self, key: str, name: str, control_type=ControlType.FilePath):
        super().__init__(key=key, name=name, control_type=control_type)
