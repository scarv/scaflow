import logging
import rich.logging

logging.basicConfig(
    level="INFO",
    format="%(module)s.%(funcName)s: %(message)s",
    datefmt="[%X]",
    handlers=[rich.logging.RichHandler(rich_tracebacks=True)],
)
logging.getLogger("numba").setLevel(logging.WARNING)
logging.getLogger("scared").setLevel(logging.WARNING)
logging.getLogger("h5py").setLevel(logging.WARNING)


if __name__ == "__main__":
    import sys

    from PySide6 import QtWidgets

    from scaflow import editor

    app = QtWidgets.QApplication()
    app.setApplicationName("scaflow")
    win = editor.ScaflowUI()
    win.show()
    sys.exit(app.exec_())
