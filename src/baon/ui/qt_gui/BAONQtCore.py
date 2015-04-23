# baon/ui/qt_gui/BAONQtCore.py
#
# (C) Copyright 2012-present  Cristian Dinu <goc9000@gmail.com>
#
# This file is part of BAON.
#
# Licensed under the GPL-3


from enum import Enum

from PyQt4.QtCore import QObject, pyqtSlot, pyqtSignal, QThread

from baon.core.errors.BAONError import BAONError

from baon.core.utils.progress.ProgressInfo import ProgressInfo

from baon.core.files.scan_files import scan_files
from baon.core.parsing.parse_rules import parse_rules


class BAONQtCore(QObject):
    class State(Enum):
        NOT_STARTED = 'not_started'
        READY = 'ready'
        SCANNING_FILES = 'scanning_files'
        SHUTDOWN = 'shutdown'

    prologue_finished = pyqtSignal()

    base_path_required = pyqtSignal()

    started_scanning_files = pyqtSignal()
    scan_files_progress = pyqtSignal(ProgressInfo)
    scan_files_ok = pyqtSignal()
    scan_files_error = pyqtSignal(BAONError)
    scanned_files_updated = pyqtSignal(list)

    rules_ok = pyqtSignal()
    rules_error = pyqtSignal(BAONError)

    ready = pyqtSignal()

    has_shutdown = pyqtSignal()

    # Inputs
    _base_path = ''
    _scan_recursive = False
    _rules_text = ''
    _use_extension = False
    _use_path = False

    # Intermediary data
    _scanned_files = None
    _rules = None

    # State
    _state = None
    _worker_thread = None

    def __init__(self, args):
        super().__init__()

        self._init_inputs(args)
        self._state = self.State.NOT_STARTED

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

    def _switch_state(self, new_state):
        self._state = new_state

    @pyqtSlot()
    def start(self):
        assert self._state == self.State.NOT_STARTED

        self._switch_state(self.State.READY)
        self.prologue_finished.emit()
        self._rescan_files()

    @pyqtSlot(str)
    def update_base_path(self, base_path):
        assert self._state in [self.State.READY, self.State.SCANNING_FILES]

        self._base_path = base_path
        self._rescan_files()

    @pyqtSlot(bool)
    def update_scan_recursive(self, scan_recursive):
        assert self._state in [self.State.READY, self.State.SCANNING_FILES]

        self._scan_recursive = scan_recursive
        self._rescan_files()

    @pyqtSlot(str)
    def update_rules_text(self, rules_text):
        assert self._state in [self.State.READY, self.State.SCANNING_FILES]

        self._rules_text = rules_text
        self._recompile_rules()

    @pyqtSlot()
    def shutdown(self):
        assert self._state in [self.State.NOT_STARTED, self.State.READY, self.State.SCANNING_FILES]

        self._stop_worker()
        self._switch_state(self.State.SHUTDOWN)
        self.has_shutdown.emit()

    def _rescan_files(self):
        self._stop_worker()
        self._switch_state(self.State.READY)

        self._scanned_files = None

        if self._base_path == '':
            self.scanned_files_updated.emit([])
            self.base_path_required.emit()
            self._recompile_rules()
        else:
            self._switch_state(self.State.SCANNING_FILES)
            self.started_scanning_files.emit()

            self._start_worker(
                work=lambda: scan_files(
                    self._base_path,
                    self._scan_recursive,
                    on_progress=lambda progress: self.scan_files_progress.emit(progress),
                    check_abort=lambda: self._should_worker_abort(),
                ),
                on_finished=self._on_scan_files_finished,
            )

    def _on_scan_files_finished(self, result):
        self._switch_state(self.State.READY)

        if isinstance(result, BAONError):
            self.scanned_files_updated.emit([])
            self.scan_files_error.emit(result)
        else:
            self._scanned_files = result
            self.scanned_files_updated.emit(result)
            self.scan_files_ok.emit()

        self._recompile_rules()

    def _recompile_rules(self):
        try:
            self._rules = parse_rules(self._rules_text)
            self.rules_ok.emit()
        except BAONError as error:
            self.rules_error.emit(error)

        self._ready()

    def _ready(self):
        if self._state == self.State.READY:
            self.ready.emit()

    def _start_worker(self, work, on_finished):
        self._stop_worker()

        class WorkerThread(QThread):
            should_abort = False
            result = None
            on_finished = None

            def run(self):
                try:
                    self.result = work()
                except BAONError as error:
                    self.result = error

        self._worker_thread = WorkerThread(self)
        self._worker_thread.on_finished = on_finished
        self._worker_thread.finished.connect(self._on_worker_finished)
        self._worker_thread.start()

    def _should_worker_abort(self):
        return self._worker_thread.should_abort

    @pyqtSlot()
    def _on_worker_finished(self):
        worker = self.sender()
        if worker.should_abort or worker is not self._worker_thread:
            return

        self._worker_thread = None
        worker.on_finished(worker.result)

    def _stop_worker(self):
        if self._worker_thread is None:
            return

        self._worker_thread.should_abort = True
        self._worker_thread.wait()
        self._worker_thread = None
