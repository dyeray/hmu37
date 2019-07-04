from multiprocessing import Process, Queue
from PySide2 import QtCore
from PySide2.QtCore import QObject, Signal


class Runner(QtCore.QObject):
    """
    Runs a job in a separate process and forwards messages from the job to the
    main thread through a signal.
    """

    def __init__(self, start_signal, msg_signal):
        super(Runner, self).__init__()
        self.job_input = None
        self.msg_signal = msg_signal
        start_signal.connect(self._run)

    def _run(self):
        queue = Queue()
        for func in self.job_functions:
            p = Process(target=func, args=(queue,))
            p.start()
        while True:
            msg = queue.get()
            self.msg_signal.emit(str(msg))


class BackgroundRunner(QtCore.QObject):

    msg_signal = Signal(str)

    def __init__(self):
        super().__init__()
        self.runner_thread = QtCore.QThread()
        self.runner = Runner(
            start_signal=self.runner_thread.started,
            msg_signal=self.msg_signal
        )
        self.runner.moveToThread(self.runner_thread)

    def start_jobs(self, funcs, input=None):
        self.runner.job_input = input
        self.runner.job_functions = funcs
        self.runner_thread.start()
