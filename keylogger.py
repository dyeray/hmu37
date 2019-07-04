from pynput import keyboard
from multiprocessing import Queue


def start_keylogger(queue: Queue):

    def on_press(key):
        queue.put(key)

    with keyboard.Listener(on_press=on_press) as listener:
        listener.join()


class KeyloggerRunner:

    def __init__(self):
        super().__init__()

    def start_running(self, msg_signal):
        def on_press(key):
            msg_signal.emit(str(key))

        self.listener = keyboard.Listener(on_press=on_press)
        self.listener.start()
