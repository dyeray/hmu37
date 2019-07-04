import json
import sys

from PySide2 import QtWidgets
from PySide2.QtCore import Slot, QUrl, Qt
from PySide2.QtWebEngineWidgets import QWebEngineView
from keylogger import KeyloggerRunner
from PySide2.QtCore import Signal, QPoint, QCoreApplication
from api import MockedApi
from background import BackgroundRunner


class AssistantWidget(QtWidgets.QWidget):

    msg_signal = Signal(str)
    hidden = False
    last_position = QPoint(0, 0)

    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent, Qt.FramelessWindowHint | Qt.WindowSystemMenuHint | Qt.WindowStaysOnTopHint)
        self.runner = KeyloggerRunner()
        self.runner.start_running(self.msg_signal)
        self.msg_signal.connect(self.get_events)
        self.webview = QWebEngineView()
        self.button = QtWidgets.QPushButton("Click me!")
        self.prueba = QtWidgets.QPushButton("prueba")
        self.text = QtWidgets.QLabel("Hello World")
        self.build_layout()
        self.button.clicked.connect(self.magic)
        self.prueba.clicked.connect(self.find_answers)
        self.api = MockedApi()
        self.answers_runner = BackgroundRunner()
        self.answers_runner.msg_signal.connect(self.answers_loaded)

    def build_layout(self):
        self.layout = QtWidgets.QVBoxLayout()
        self.layout.addWidget(self.text)
        self.layout.addWidget(self.button)
        self.layout.addWidget(self.prueba)
        self.layout.addWidget(self.webview)
        self.setLayout(self.layout)

    @Slot(str)
    def get_events(self, event):
        callback = getattr(self, f'event_{event}_callback', self.unknown_event_callback)
        callback(event=event)

    @Slot(str)
    def answers_loaded(self, answers_json):
        answers = json.loads(answers_json)
        print(answers)
        self.webview.setHtml(answers[0]['content'])

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

    def find_answers(self):
        self.answers_runner.stop_jobs()
        self.answers_runner.start_jobs(self.api.get_answers)

    def mousePressEvent(self, event):
        self.last_position = event.pos()
        super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if event.buttons() & Qt.LeftButton:
            diff = event.pos() - self.last_position
            newpos = self.pos() + diff
            self.move(newpos)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    widget = AssistantWidget()
    widget.show()
    sys.exit(app.exec_())
