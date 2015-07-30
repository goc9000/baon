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

from baon.core.utils.progress.ProgressInfo import ProgressInfo

from baon.core.files.scan_files import scan_files
from baon.core.parsing.parse_rules import parse_rules
from baon.core.renaming.rename_files import rename_files, apply_rename_overrides


class BAONQtCore(CancellableWorkerMixin, QObject):
    class State(Enum):
        NOT_STARTED = 'not_started'
        READY = 'ready'
        SCANNING_FILES = 'scanning_files'
        RENAMING_FILES = 'renaming_files'
        SHUTDOWN = 'shutdown'

    prologue_finished = pyqtSignal()

    base_path_required = pyqtSignal()

    started_scanning_files = pyqtSignal()
    scan_files_progress = pyqtSignal(ProgressInfo)
    scan_files_ok = pyqtSignal()
    scan_files_error = pyqtSignal(Exception)
    scanned_files_updated = pyqtSignal(list)

    rules_ok = pyqtSignal()
    rules_error = pyqtSignal(Exception)

    not_ready_to_rename = pyqtSignal()
    no_files_to_rename = pyqtSignal()

    started_renaming_files = pyqtSignal()
    rename_files_progress = pyqtSignal(ProgressInfo)
    rename_files_ok = pyqtSignal()
    rename_files_error = pyqtSignal(Exception)
    renamed_files_updated = pyqtSignal(list)

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
    _renamed_files_before_overrides = None
    _overrides = None
    _renamed_files = None

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

        self._recompile_rules(isolated=True)
        self._rescan_files()

    @pyqtSlot(str)
    def update_base_path(self, base_path):
        assert self._state in [self.State.READY, self.State.SCANNING_FILES, self.State.RENAMING_FILES]

        self._base_path = base_path
        self._on_scan_files_inputs_changed()

    @pyqtSlot(bool)
    def update_scan_recursive(self, scan_recursive):
        assert self._state in [self.State.READY, self.State.SCANNING_FILES, self.State.RENAMING_FILES]

        self._scan_recursive = scan_recursive
        self._on_scan_files_inputs_changed()

    @pyqtSlot(str)
    def update_rules_text(self, rules_text):
        assert self._state in [self.State.READY, self.State.SCANNING_FILES, self.State.RENAMING_FILES]

        self._rules_text = rules_text
        self._recompile_rules()

    @pyqtSlot(bool)
    def update_use_path(self, use_path):
        assert self._state in [self.State.READY, self.State.SCANNING_FILES, self.State.RENAMING_FILES]

        self._use_path = use_path
        self._on_rename_files_inputs_changed()

    @pyqtSlot(bool)
    def update_use_extension(self, use_extension):
        assert self._state in [self.State.READY, self.State.SCANNING_FILES, self.State.RENAMING_FILES]

        self._use_extension = use_extension
        self._on_rename_files_inputs_changed()

    @pyqtSlot(str, str)
    def add_override(self, original_path, explicit_name):
        self._overrides[original_path] = explicit_name
        self._on_apply_overrides_inputs_changed()

    @pyqtSlot(str)
    def remove_override(self, original_path):
        self._overrides.pop(original_path, None)
        self._on_apply_overrides_inputs_changed()

    @pyqtSlot()
    def shutdown(self):
        assert self._state != self.State.SHUTDOWN

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

        self._overrides = args.overrides if args.overrides is not None else {}

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
        elif self._state == self.State.RENAMING_FILES:
            self.started_renaming_files.emit()
        elif self._state == self.State.READY:
            self.ready.emit()

    def _on_scan_files_inputs_changed(self):
        self._overrides = {}
        self._rescan_files()

    def _rescan_files(self):
        self._stop_worker()

        if self._base_path == '':
            self._on_scan_files_finished(None)
            return

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
        self._update_scanned_files(result)

    def _update_scanned_files(self, result):
        if result is not None and not isinstance(result, Exception):
            self._scanned_files = result
        else:
            self._scanned_files = None

        self.scanned_files_updated.emit(self._scanned_files if self._scanned_files is not None else [])

        if result is None:
            self.base_path_required.emit()
        elif isinstance(result, Exception):
            self.scan_files_error.emit(result)
        else:
            self.scan_files_ok.emit()

        self._on_rename_files_inputs_changed()

    def _recompile_rules(self, isolated=False):
        try:
            self._rules = parse_rules(self._rules_text)
            self.rules_ok.emit()
        except Exception as error:
            self._rules = None
            self.rules_error.emit(error)

        if not isolated:
            self._on_rename_files_inputs_changed()

    def _on_rename_files_inputs_changed(self):
        if self._state == self.State.SCANNING_FILES:
            return

        self._rename_files()

    def _rename_files(self):
        if self._scanned_files is None or self._rules is None:
            self._on_rename_files_finished(None)
            return
        if len(self._scanned_files) == 0:
            self._on_rename_files_finished([])
            return

        self._switch_state(self.State.RENAMING_FILES)
        self._start_worker(
            work=lambda check_abort: rename_files(
                self._scanned_files,
                self._rules,
                use_path=self._use_path,
                use_extension=self._use_extension,
                on_progress=lambda progress: self.rename_files_progress.emit(progress),
                check_abort=check_abort,
            ),
            on_finished=self._on_rename_files_finished,
        )

    def _on_rename_files_finished(self, result):
        self._switch_state(self.State.READY)
        self._update_renamed_files_before_overrides(result)

    def _update_renamed_files_before_overrides(self, result):
        if result is not None and not isinstance(result, Exception) and len(result) > 0:
            self._renamed_files_before_overrides = result
        else:
            self._renamed_files_before_overrides = None

        self._on_apply_overrides_inputs_changed()

        if result is None:
            self.not_ready_to_rename.emit()
        elif isinstance(result, Exception):
            self.rename_files_error.emit(result)
        elif len(result) == 0:
            self.no_files_to_rename.emit()
        else:
            self.rename_files_ok.emit()

    def _on_apply_overrides_inputs_changed(self):
        if self._renamed_files_before_overrides is not None:
            renamed_files = apply_rename_overrides(self._renamed_files_before_overrides, self._overrides)
        else:
            renamed_files = None

        self._update_renamed_files(renamed_files)

    def _update_renamed_files(self, renamed_files):
        self._renamed_files = renamed_files

        self.renamed_files_updated.emit(self._renamed_files if self._renamed_files is not None else [])
