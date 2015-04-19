# baon/ui/qt_gui/BAONQtCore.py
#
# (C) Copyright 2012-present  Cristian Dinu <goc9000@gmail.com>
# 
# This file is part of BAON.
#
# Licensed under the GPL-3


from PyQt4.QtCore import QObject, pyqtSlot, pyqtSignal, QThread

from baon.core.errors.BAONError import BAONError


class BAONQtCore(QObject):
    prologue_finished = pyqtSignal()
    has_shutdown = pyqtSignal()

    # Inputs
    _base_path = ''
    _scan_recursive = False
    _rules_text = ''
    _use_extension = False
    _use_path = False

    # State
    _worker_thread = None

    def __init__(self, args):
        super().__init__()

        self._init_inputs(args)

    def _init_inputs(self, args):
        if args.base_path is not None:
            self._base_path = args.base_path
        if args.scan_recursive is not None:
            self._scan_recursive = args.scan_recursive
        if args.rules_text is not None:
            self._rules_text = args.rules_text
        if args.use_extension is not None:
            self._use_extension = args.use_extension
        if args.use_path is not None:
            self._use_path = args.use_path

    @pyqtSlot()
    def start(self):
        self.prologue_finished.emit()

    @pyqtSlot()
    def shutdown(self):
        self._stop_worker()
        self.has_shutdown.emit()

    def _start_worker(self, work, on_finished, on_error):
        self._stop_worker()

        class WorkerThread(QThread):
            should_abort = False

            completed = pyqtSignal(object)
            error = pyqtSignal(BAONError)

            def run(self):
                try:
                    self.completed.emit(work())
                except BAONError as error:
                    self.error.emit(error)

        self._worker_thread = WorkerThread(self)
        self._worker_thread.completed.connect(on_finished)
        self._worker_thread.error.connect(on_error)
        self._worker_thread.start()

    def _should_worker_abort(self):
        return self._worker_thread.should_abort

    def _stop_worker(self):
        if self._worker_thread is None:
            return

        self._worker_thread.should_abort = True
        self._worker_thread.wait()
        self._worker_thread = None
