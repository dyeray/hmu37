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
        key_presses = []
        def on_press(key):
            if key == keyboard.Key.ctrl:
                key_presses.clear()
                key_presses.append('command')
            elif hasattr(key, 'char') and key.char == 'ñ' and key_presses:
                key_presses.clear()
                msg_signal.emit('invoke')
            elif hasattr(key, 'char') and key.char == 'q' and key_presses:
                key_presses.clear()
                msg_signal.emit('quit')
            else:
                key_presses.clear()
        self.listener = keyboard.Listener(on_press=on_press)
        self.listener.start()
