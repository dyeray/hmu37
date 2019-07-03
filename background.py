from multiprocessing import Process, Queue
from PySide2 import QtCore


class Runner(QtCore.QObject):
    """
    Runs a job in a separate process and forwards messages from the job to the
    main thread through a signal.
    """

    def __init__(self, start_signal):
        """
        :param start_signal: the pyqtSignal that starts the job

        """
        super(Runner, self).__init__()
        self.job_input = None
        start_signal.connect(self._run)

    def _run(self):
        queue = Queue()
        for func in self.job_functions:
            p = Process(target=func, args=(queue,))
            p.start()
        while True:
            msg = queue.get()
            print(msg)


class BackgroundRunner:
    def __init__(self):
        self.runner_thread = QtCore.QThread()
        self.runner = Runner(start_signal=self.runner_thread.started)
        # runner.msg_from_job.connect(handle_msg)
        self.runner.moveToThread(self.runner_thread)

    def start_jobs(self, funcs, input=None):
        self.runner.job_input = input
        self.runner.job_functions = funcs
        self.runner_thread.start()
