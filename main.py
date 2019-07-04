import sys

from PySide2 import QtWidgets
from PySide2.QtCore import Slot
from keylogger import KeyloggerRunner


class MyWidget(QtWidgets.QWidget):

    def __init__(self):
        QtWidgets.QWidget.__init__(self)
        self.runner = KeyloggerRunner()
        self.runner.start_running()
        self.runner.msg_signal.connect(self.get_events)
        self.button = QtWidgets.QPushButton("Click me!")
        self.text = QtWidgets.QLabel("Hello World")
        self.layout = QtWidgets.QVBoxLayout()
        self.layout.addWidget(self.text)
        self.layout.addWidget(self.button)
        self.setLayout(self.layout)
        self.button.clicked.connect(self.magic)

    @Slot(str)
    def get_events(self, event):
        self.text.setText(event)

    def magic(self):
        print("hehe")


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    widget = MyWidget()
    widget.show()
    sys.exit(app.exec_())
