# baon/ui/qt_gui/BAONQtCore.py
#
# (C) Copyright 2012-present  Cristian Dinu <goc9000@gmail.com>
#
# This file is part of BAON.
#
# Licensed under the GPL-3


from enum import Enum

from PyQt4.QtCore import QObject, pyqtSlot, pyqtSignal

from baon.ui.qt_gui.mixins.CancellableWorkerMixin import CancellableWorkerMixin

from baon.core.errors.BAONError import BAONError

from baon.core.utils.progress.ProgressInfo import ProgressInfo

from baon.core.files.scan_files import scan_files
from baon.core.parsing.parse_rules import parse_rules


class BAONQtCore(CancellableWorkerMixin, QObject):
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

    def __init__(self, args):
        super().__init__()

        self._init_inputs(args)
        self._state = self.State.NOT_STARTED

    @pyqtSlot()
    def start(self):
        assert self._state == self.State.NOT_STARTED

        self._switch_state(self.State.READY)
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
        if new_state == self._state:
            return

        self._on_exit_state(new_state)
        old_state = self._state
        self._state = new_state
        self._on_enter_state(old_state)

    def _on_exit_state(self, new_state):
        prologue_states = {self.State.NOT_STARTED}

        if self._state in prologue_states and new_state not in prologue_states:
            self.prologue_finished.emit()

    def _on_enter_state(self, old_state):
        if self._state == self.State.SHUTDOWN:
            self.has_shutdown.emit()
        elif self._state == self.State.SCANNING_FILES:
            self.started_scanning_files.emit()
        elif self._state == self.State.READY:
            self.ready.emit()

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
            self._start_worker(
                work=lambda check_abort: scan_files(
                    self._base_path,
                    self._scan_recursive,
                    on_progress=lambda progress: self.scan_files_progress.emit(progress),
                    check_abort=check_abort,
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
