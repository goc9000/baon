# baon/ui/qt_gui/BAONQtCore.py
#
# (C) Copyright 2012-present  Cristian Dinu <goc9000@gmail.com>
# 
# This file is part of BAON.
#
# Licensed under the GPL-3


from PyQt4.QtCore import QObject, pyqtSlot, pyqtSignal, QThread

from baon.core.errors.BAONError import BAONError

from baon.core.utils.progress.ProgressInfo import ProgressInfo

from baon.core.files.scan_files import scan_files


class BAONQtCore(QObject):
    prologue_finished = pyqtSignal()

    base_path_required = pyqtSignal()

    scan_files_progress = pyqtSignal(ProgressInfo)
    scan_files_error = pyqtSignal(BAONError)

    scanned_files_updated = pyqtSignal(list)

    ready = pyqtSignal()

    has_shutdown = pyqtSignal()

    # Inputs
    _base_path = ''
    _scan_recursive = False
    _rules_text = ''
    _use_extension = False
    _use_path = False

    # Intermediary data
    _scanned_files = []

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
        self._rescan_files()

    @pyqtSlot(str)
    def update_base_path(self, base_path):
        self._base_path = base_path
        self._rescan_files()

    @pyqtSlot(bool)
    def update_scan_recursive(self, scan_recursive):
        self._scan_recursive = scan_recursive
        self._rescan_files()

    def _rescan_files(self):
        self._scanned_files = []
        self.scanned_files_updated.emit([])

        if self._base_path == '':
            self.base_path_required.emit()
            return

        self._start_worker(
            work=lambda: scan_files(
                self._base_path,
                self._scan_recursive,
                on_progress=lambda progress: self.scan_files_progress.emit(progress),
                check_abort=lambda: self._should_worker_abort(),
            ),
            on_finished=self._on_scan_files_finished,
        )

    @pyqtSlot(object)
    def _on_scan_files_finished(self, result):
        if isinstance(result, BAONError):
            self.scan_files_error.emit(result)
            return

        self._scanned_files = result
        self.scanned_files_updated.emit(result)
        self.ready.emit()

    @pyqtSlot()
    def shutdown(self):
        self._stop_worker()
        self.has_shutdown.emit()

    def _start_worker(self, work, on_finished):
        self._stop_worker()

        class WorkerThread(QThread):
            should_abort = False

            completed = pyqtSignal(object)

            def run(self):
                try:
                    result = work()
                except BAONError as error:
                    result = error

                if not self.should_abort:
                    self.completed.emit(result)

        self._worker_thread = WorkerThread(self)
        self._worker_thread.completed.connect(on_finished)
        self._worker_thread.start()

    def _should_worker_abort(self):
        return self._worker_thread.should_abort

    def _stop_worker(self):
        if self._worker_thread is None:
            return

        self._worker_thread.should_abort = True
        self._worker_thread.wait()
        self._worker_thread = None
