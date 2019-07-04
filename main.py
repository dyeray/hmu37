import sys

from PySide2 import QtWidgets
from PySide2.QtCore import Slot
from keylogger import KeyloggerRunner
from PySide2.QtCore import Signal, QPoint, QCoreApplication
from api import StackOverflowApi
from background import BackgroundRunner


class MyWidget(QtWidgets.QWidget):

    msg_signal = Signal(str)
    hidden = False
    last_position = QPoint(0, 0)

    def __init__(self):
        QtWidgets.QWidget.__init__(self)
        self.runner = KeyloggerRunner()
        self.runner.start_running(self.msg_signal)
        self.msg_signal.connect(self.get_events)
        self.button = QtWidgets.QPushButton("Click me!")
        self.prueba = QtWidgets.QPushButton("prueba")
        self.text = QtWidgets.QLabel("Hello World")
        self.layout = QtWidgets.QVBoxLayout()
        self.layout.addWidget(self.text)
        self.layout.addWidget(self.button)
        self.layout.addWidget(self.prueba)
        self.setLayout(self.layout)
        self.button.clicked.connect(self.magic)
        self.prueba.clicked.connect(self.foo)
        self.api = StackOverflowApi()
        self.background_runner = BackgroundRunner()
        self.background_runner.msg_signal.connect(self.answers_loaded)

    @Slot(str)
    def get_events(self, event):
        callback = getattr(self, f'event_{event}_callback', self.unknown_event_callback)
        callback(event=event)

    @Slot(str)
    def answers_loaded(self, answers):
        print(answers)

    def event_invoke_callback(self, **kwargs):
        if self.hidden:
            self.show()
            self.move(self.last_position.x(), self.last_position.y())
            self.hidden = False
        else:
            self.last_position = self.pos()
            self.hide()
            self.hidden = True

    def event_quit_callback(self, **kwargs):
        QCoreApplication.quit()

    def unknown_event_callback(self, event):
        print(f'Unknown event {event}')

    def magic(self):
        print("hehe")

    def foo(self):
        self.background_runner.start_jobs(self.api.get_answers, args=("java", ))


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    widget = MyWidget()
    widget.show()
    sys.exit(app.exec_())
