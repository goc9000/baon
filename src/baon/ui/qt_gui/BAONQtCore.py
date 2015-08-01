# baon/ui/qt_gui/BAONQtCore.py
#
# (C) Copyright 2012-present  Cristian Dinu <goc9000@gmail.com>
#
# This file is part of BAON.
#
# Licensed under the GPL-3


from PyQt4.QtCore import QObject, pyqtSlot, pyqtSignal

from baon.ui.qt_gui.mixins.CancellableWorkerMixin import CancellableWorkerMixin

from baon.core.utils.symbol import symbol

from baon.core.utils.progress.ProgressInfo import ProgressInfo

from baon.core.files.scan_files import scan_files
from baon.core.parsing.parse_rules import parse_rules
from baon.core.renaming.rename_files import rename_files, apply_rename_overrides


class BAONQtCore(CancellableWorkerMixin, QObject):
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
    _base_path = None
    _scan_recursive = None
    _rules_text = None
    _use_extension = None
    _use_path = None
    _overrides = None

    # Intermediary data
    _scanned_files = None
    _rules = None
    _renamed_files_before_overrides = None
    _renamed_files = None

    # Other state
    _args = None
    _protect_overrides = False

    def __init__(self, args):
        super().__init__()

        self._args = args

        self._init_data_flow()

    @pyqtSlot()
    def start(self):
        self.prologue_finished.emit()

        self._feed_initial_data()

    @pyqtSlot(str)
    def update_base_path(self, base_path):
        self._base_path.update_value(base_path)

    @pyqtSlot(bool)
    def update_scan_recursive(self, scan_recursive):
        self._scan_recursive.update_value(scan_recursive)

    @pyqtSlot(str)
    def update_rules_text(self, rules_text):
        self._rules_text.update_value(rules_text)

    @pyqtSlot(bool)
    def update_use_path(self, use_path):
        self._use_path.update_value(use_path)

    @pyqtSlot(bool)
    def update_use_extension(self, use_extension):
        self._use_extension.update_value(use_extension)

    @pyqtSlot(str, str)
    def add_override(self, original_path, explicit_name):
        self._overrides.update_value(dict(list(self._overrides.value().items()) + [(original_path, explicit_name)]))

    @pyqtSlot(str)
    def remove_override(self, original_path):
        self._overrides.update_value({k: v for k, v in self._overrides.value().items() if k != original_path})

    @pyqtSlot()
    def shutdown(self):
        self._stop_worker()
        self.has_shutdown.emit()

    def _init_data_flow(self):
        self._base_path = DataFlowNode(self, '', debug_name='base path')
        self._scan_recursive = DataFlowNode(self, False, debug_name='scan recursive')
        self._rules_text = DataFlowNode(self, '', debug_name='rules text')
        self._use_extension = DataFlowNode(self, False, debug_name='use extension')
        self._use_path = DataFlowNode(self, False, debug_name='use path')
        self._overrides = DataFlowNode(self, {}, debug_name='overrides')

        self._scanned_files = ScannedFilesNode(self, self._base_path, self._scan_recursive)
        self._scanned_files.value_updated.connect(self._maybe_clear_overrides)
        self._scanned_files.value_updated.connect(self._do_check_ready)
        self._scanned_files.value_updated.connect(self._report_scan_status)

        self._rules = RulesNode(self, self._rules_text)
        self._rules.value_updated.connect(self._report_rules_status)

        self._renamed_files_before_overrides = \
            RenamedFilesBeforeOverridesNode(self, self._scanned_files, self._rules, self._use_path, self._use_extension)
        self._renamed_files_before_overrides.value_updated.connect(self._do_check_ready)
        self._renamed_files_before_overrides.value_updated.connect(self._report_rename_status)

        self._renamed_files = RenamedFilesNode(self, self._renamed_files_before_overrides, self._overrides)
        self._renamed_files.value_updated.connect(self._report_renamed_files)

    @pyqtSlot(object)
    def _feed_initial_data(self):
        self._overrides.update_value(self._args.overrides or {})
        self._protect_overrides = True

        self._rules_text.update_value(self._args.rules_text or '')
        self._use_extension.update_value(self._args.use_extension or False)
        self._use_path.update_value(self._args.use_path or False)

        self._base_path.update_value(self._args.base_path or '')
        self._scan_recursive.update_value(self._args.scan_recursive or False)

    @pyqtSlot()
    def _maybe_clear_overrides(self):
        if not self._scanned_files.is_pending_value():
            if self._protect_overrides:
                self._protect_overrides = False
            else:
                self._overrides.update_value({})

    @pyqtSlot()
    def _do_check_ready(self):
        if not self._scanned_files.is_pending_value() and not self._renamed_files_before_overrides.is_pending_value():
            self.ready.emit()

    @pyqtSlot()
    def _report_scan_status(self):
        value = self._scanned_files.value()

        if value == WAITING_FOR_DEPENDENTS:
            pass
        elif value == COMPUTING_VALUE:
            self.started_scanning_files.emit()
        elif value == NOT_AVAILABLE:
            self.base_path_required.emit()
            self.scanned_files_updated.emit([])
        elif isinstance(value, Exception):
            self.scan_files_error.emit(value)
            self.scanned_files_updated.emit([])
        else:
            self.scan_files_ok.emit()
            self.scanned_files_updated.emit(value)

    @pyqtSlot()
    def _report_rules_status(self):
        value = self._rules.value()

        if isinstance(value, Exception):
            self.rules_error.emit(value)
        else:
            self.rules_ok.emit()

    @pyqtSlot()
    def _report_rename_status(self):
        value = self._renamed_files_before_overrides.value()

        if value == WAITING_FOR_DEPENDENTS:
            pass
        elif value == COMPUTING_VALUE:
            self.started_renaming_files.emit()
        elif value == NOT_AVAILABLE:
            self.not_ready_to_rename.emit()
        elif isinstance(value, Exception):
            self.rename_files_error.emit(value)
        elif len(value) == 0:
            self.no_files_to_rename.emit()
        else:
            self.rename_files_ok.emit()

    @pyqtSlot()
    def _report_renamed_files(self):
        value = self._renamed_files.value()

        if value == WAITING_FOR_DEPENDENTS:
            pass
        elif value == NOT_AVAILABLE:
            self.renamed_files_updated.emit([])
        else:
            self.renamed_files_updated.emit(value)


CONTINUE_PROCESSING = symbol('CONTINUE_PROCESSING')
COMPUTING_VALUE = symbol('COMPUTING_VALUE')
WAITING_FOR_DEPENDENTS = symbol('WAITING_FOR_DEPENDENTS')
NOT_AVAILABLE = symbol('NOT_AVAILABLE')


class DataFlowNode(QObject):
    value_updated = pyqtSignal()

    _value = None
    _inputs = None
    _debug_name = None

    def __init__(self, parent, value=NOT_AVAILABLE, inputs=None, debug_name=None):
        super().__init__(parent)

        self._value = value
        self._inputs = inputs or []
        self._debug_name = debug_name

        for input_node in self._inputs:
            input_node.value_updated.connect(self._on_inputs_updated)

    @pyqtSlot(object)
    def update_value(self, new_value):
        self._value = new_value

        self.value_updated.emit()

    def value(self):
        return self._value

    def is_pending_value(self):
        return self._value == COMPUTING_VALUE or self._value == WAITING_FOR_DEPENDENTS

    @pyqtSlot()
    def _on_inputs_updated(self):
        input_values = [input_node.value() for input_node in self._inputs]

        value = self._compute_new_value(input_values)
        if self._value == COMPUTING_VALUE and value != COMPUTING_VALUE:
            self.parent()._stop_worker()

        self.update_value(value)

    def _compute_new_value(self, input_values):
        value = self._do_standard_input_processing(input_values)
        if value != CONTINUE_PROCESSING:
            return value

        try:
            value = self._compute_sync_value(*input_values)
        except Exception as exc:
            value = exc

        if value != CONTINUE_PROCESSING:
            return value

        self.parent()._start_worker(
            work=lambda check_abort: self._compute_async_value(check_abort, *input_values),
            on_finished=self.update_value,
        )

        return COMPUTING_VALUE

    def _do_standard_input_processing(self, input_values):
        if len(input_values) == 0:
            return CONTINUE_PROCESSING

        for value in input_values:
            if value == COMPUTING_VALUE or value == WAITING_FOR_DEPENDENTS:
                return WAITING_FOR_DEPENDENTS
            elif value == NOT_AVAILABLE or isinstance(value, Exception):
                return NOT_AVAILABLE

        return CONTINUE_PROCESSING

    def _compute_sync_value(self, *input_values):
        return NOT_AVAILABLE


class RulesNode(DataFlowNode):
    def __init__(self, parent, rules_text_node):
        super().__init__(parent, inputs=[rules_text_node], debug_name='rules')

    def _compute_sync_value(self, rules_text):
        return parse_rules(rules_text)


class ScannedFilesNode(DataFlowNode):
    def __init__(self, parent, base_path_node, scan_recursive_node):
        super().__init__(parent, inputs=[base_path_node, scan_recursive_node], debug_name='scanned_files')

    def _compute_sync_value(self, base_path, scan_recursive):
        if base_path == '':
            return NOT_AVAILABLE

        return CONTINUE_PROCESSING

    def _compute_async_value(self, check_abort, base_path, scan_recursive):
        return scan_files(
            base_path,
            scan_recursive,
            on_progress=lambda progress: self.parent().scan_files_progress.emit(progress),
            check_abort=check_abort,
        )


class RenamedFilesBeforeOverridesNode(DataFlowNode):
    def __init__(self, parent, scanned_files_node, rules_node, use_path_node, use_extension_node):
        super().__init__(
            parent,
            inputs=[scanned_files_node, rules_node, use_path_node, use_extension_node],
            debug_name='renamed_wo_overrides'
        )

    def _compute_sync_value(self, scanned_files, rules, use_path, use_extension):
        if len(scanned_files) == 0:
            return list()

        return CONTINUE_PROCESSING

    def _compute_async_value(self, check_abort, scanned_files, rules, use_path, use_extension):
        return rename_files(
            scanned_files,
            rules,
            use_path=use_path,
            use_extension=use_extension,
            on_progress=lambda progress: self.parent().rename_files_progress.emit(progress),
            check_abort=check_abort,
        )


class RenamedFilesNode(DataFlowNode):
    def __init__(self, parent, renamed_files_before_overrides_node, overrides_node):
        super().__init__(
            parent,
            inputs=[renamed_files_before_overrides_node, overrides_node],
            debug_name='renamed_files'
        )

    def _compute_sync_value(self, renamed_files_before_overrides, overrides):
        return apply_rename_overrides(renamed_files_before_overrides, overrides)
