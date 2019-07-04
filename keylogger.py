from pynput import keyboard
from multiprocessing import Queue

from PySide2 import QtCore
from PySide2.QtCore import Signal


def start_keylogger(queue: Queue):

    def on_press(key):
        queue.put(key)

    with keyboard.Listener(on_press=on_press) as listener:
        listener.join()


class KeyloggerRunner(QtCore.QObject):
    msg_signal = Signal(str)

    def __init__(self):
        super().__init__()

    def start_running(self):
        signal = self.msg_signal

        def on_press(key):
            signal.emit(str(key))

        self.listener = keyboard.Listener(on_press=on_press)
        self.listener.start()
