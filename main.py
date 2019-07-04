import json
import sys

from PySide2 import QtWidgets, QtGui
from PySide2.QtCore import Slot, QUrl, Qt
from PySide2.QtWebEngineWidgets import QWebEngineView
from keylogger import KeyloggerRunner
from PySide2.QtCore import Signal, QPoint, QCoreApplication
from api import MockedApi as StackOverflowApi
from background import BackgroundRunner


class AssistantWidget(QtWidgets.QWidget):

    msg_signal = Signal(str)
    hidden = False
    last_position = QPoint(0, 0)
    current_answer = 0
    answers = []

    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent, Qt.FramelessWindowHint | Qt.WindowSystemMenuHint | Qt.WindowStaysOnTopHint)
        self.runner = KeyloggerRunner()
        self.runner.start_running(self.msg_signal)
        self.msg_signal.connect(self.get_events)
        self.webview = QWebEngineView()
        self.text_input = QtWidgets.QLineEdit()
        self.search_button = QtWidgets.QPushButton("search")
        self.clear_button = QtWidgets.QPushButton("x")
        self.progress = QtWidgets.QLabel()
        movie = QtGui.QMovie("progress.gif")
        self.progress.setMovie(movie)
        movie.start()
        self.previous_button = QtWidgets.QPushButton()
        self.previous_button.setIcon(QtGui.QIcon('left.png'))
        self.next_button = QtWidgets.QPushButton()
        self.next_button.setIcon(QtGui.QIcon('right.png'))
        self.logo = QtGui.QPixmap('stacko.png')
        self.logo_label = QtWidgets.QLabel()
        self.logo_label.setPixmap(self.logo)
        self.build_layout()
        self.clear_button.clicked.connect(self.clear_search)
        self.search_button.clicked.connect(self.find_answers)
        self.previous_button.clicked.connect(self.show_previous_answer)
        self.next_button.clicked.connect(self.show_next_answer)
        self.api = StackOverflowApi()
        self.answers_runner = BackgroundRunner()
        self.answers_runner.msg_signal.connect(self.answers_loaded)

    def build_layout(self):
        self.parent_layout = QtWidgets.QHBoxLayout()
        self.parent_layout.addLayout(self.build_left_side())
        self.parent_layout.addLayout(self.build_right_side())
        self.setLayout(self.parent_layout)

    def build_left_side(self):
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.logo_label)
        return layout

    def build_right_side(self):
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.text_input)
        layout.addWidget(self.search_button)
        layout.addWidget(self.progress)
        self.progress.setVisible(False)
        buttons_layout = QtWidgets.QHBoxLayout()
        layout.addLayout(buttons_layout)
        buttons_layout.addWidget(self.clear_button)
        self.clear_button.setVisible(False)
        buttons_layout.addWidget(self.previous_button)
        self.previous_button.setVisible(False)
        buttons_layout.addWidget(self.next_button)
        self.next_button.setVisible(False)
        self.webview.setVisible(False)
        layout.addWidget(self.webview)
        return layout

    @Slot(str)
    def get_events(self, event):
        callback = getattr(self, f'event_{event}_callback', self.unknown_event_callback)
        callback(event=event)

    @Slot(str)
    def answers_loaded(self, answers_json):
        answers = json.loads(answers_json)
        self.answers = answers
        print(self.answers)
        self.current_answer = 0
        self.previous_button.setVisible(True)
        self.previous_button.setEnabled(False)
        self.next_button.setVisible(True)
        if len(self.answers) > 1:
            self.next_button.setEnabled(True)
        self.clear_button.setVisible(True)
        self.search_button.setVisible(False)
        self.progress.setVisible(False)
        self.webview.setVisible(True)
        self.webview.setHtml(self.answers[self.current_answer]['content'])

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

    def clear_search(self):
        self.current_answer = 0
        self.answers = []
        self.previous_button.setVisible(False)
        self.next_button.setVisible(False)
        self.clear_button.setVisible(False)
        self.search_button.setVisible(True)
        self.text_input.setVisible(True)
        self.webview.setVisible(False)

    def find_answers(self):
        self.progress.setVisible(True)
        self.answers_runner.stop_jobs()
        self.answers_runner.start_jobs(self.api.get_answers, args=(self.text_input.text(),))

    def mousePressEvent(self, event):
        self.last_position = event.pos()
        super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if event.buttons() & Qt.LeftButton:
            diff = event.pos() - self.last_position
            newpos = self.pos() + diff
            self.move(newpos)

    def show_previous_answer(self):
        if len(self.answers) > 0 and 0 <= self.current_answer - 1 < len(self.answers):
            self.current_answer = self.current_answer - 1
            self.webview.setHtml(self.answers[self.current_answer]['content'])
            if self.current_answer == 0:
                self.previous_button.setEnabled(False)
            if not self.next_button.isEnabled():
                self.next_button.setEnabled(True)

    def show_next_answer(self):
        if len(self.answers) > 0 and 0 <= self.current_answer + 1 < len(self.answers):
            self.current_answer = self.current_answer + 1
            self.webview.setHtml(self.answers[self.current_answer]['content'])
            if self.current_answer == len(self.answers) - 1:
                self.next_button.setEnabled(False)
            if not self.previous_button.isEnabled():
                self.previous_button.setEnabled(True)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    widget = AssistantWidget()
    widget.show()
    sys.exit(app.exec_())
