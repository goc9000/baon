# baon/ui/qt5_gui/mixins/CancellableWorkerMixin.py
#
# (C) Copyright 2012-present  Cristian Dinu <goc9000@gmail.com>
#
# This file is part of BAON.
#
# Licensed under the GPL-3


from PyQt5.QtCore import QObject, QThread, pyqtSlot


class CancellableWorkerMixin(QObject):
    """
    Mixin that provides a method for a QObject to perform work in a separate thread and remain responsive to signals.
    The main use case is executing work that may be cancelled in response to a signal - were we to perform it in the
    QObject's own thread, we would be unable to respond to the signal until the work was finished and we exited the
    slot it was executed in.
    """

    _worker_thread = None

    """
    Schedules a new item of work to be executed by the worker thread.

    Parameters:
    - work: a single-parameter callable that performs work and returns a result. It will receive a function that it
            should periodically call to check whether it should abort. Once that function returns True, the work
            function should try to exit as soon as possible.
    - on_finished: a single-parameter callable that will be invoked in the original thread of the QObject when the
                   worker completes. If the worker completes successfully, the result will be passed as the parameter.
                   If an exception was thrown, the exception will be passed instead. Note that on_finished will NOT be
                   called if the worker is cancelled.

    Note that only one item of work may be executing at any given time. If this is called while the worker is already
    busy, its current work will be cancelled and replaced by the new one.
    """
    def _start_worker(self, work, on_finished):
        self._stop_worker()

        class WorkerThread(QThread):
            should_abort = False
            result = None
            on_finished = None

            def run(self):
                try:
                    self.result = work(lambda: self.should_abort)
                except Exception as error:
                    self.result = error

        self._worker_thread = WorkerThread(self)
        self._worker_thread.on_finished = on_finished
        self._worker_thread.finished.connect(self._on_worker_finished)
        self._worker_thread.start()

    """
    Cancels the work currently being executed in the worker thread and waits until the thread has actually stopped
    executing.

    It is guaranteed that the on_finished() function will not be called for the current work once the worker has been
    cancelled.

    Note that this mechanism relies on the work function periodically calling the abort check function it received as
    its only parameter. If the work function is not compliant, it will not be forcefully terminated.

    Nothing happens if the worker is already finished.
    """
    def _stop_worker(self):
        if self._worker_thread is None:
            return

        self._worker_thread.should_abort = True
        self._worker_thread.wait()
        self._worker_thread = None

    @pyqtSlot()
    def _on_worker_finished(self):
        worker = self.sender()
        if worker.should_abort or worker is not self._worker_thread:
            return

        self._worker_thread = None
        worker.on_finished(worker.result)
