# baon/ui/qt_gui/BAONQtCore.py
#
# (C) Copyright 2012-present  Cristian Dinu <goc9000@gmail.com>
#
# This file is part of BAON.
#
# Licensed under the GPL-3


from PyQt4.QtCore import Qt, QObject, QMetaObject, pyqtSlot, pyqtSignal

from baon.ui.qt_gui.mixins.CancellableWorkerMixin import CancellableWorkerMixin

from baon.ui.qt_gui.BAONStatus import BAONStatus

from baon.core.utils.progress.ProgressInfo import ProgressInfo

from baon.core.files.scan_files import scan_files
from baon.core.parsing.parse_rules import parse_rules
from baon.core.renaming.rename_files import rename_files, apply_rename_overrides


class BAONQtCore(CancellableWorkerMixin, QObject):
    prologue_finished = pyqtSignal()

    status_changed = pyqtSignal(BAONStatus)
    scanned_files_updated = pyqtSignal(list)
    renamed_files_updated = pyqtSignal(list)

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
    _defer_status_update_level = 0

    def __init__(self, args):
        super().__init__()

        self._args = args

        self._init_data_flow()

    def status(self):
        status = BAONStatus()
        status.scan_status, status.scan_status_extra = self._scanned_files.extended_status()
        status.rules_status, status.rules_status_extra = self._rules.extended_status()
        status.rename_status, status.rename_status_extra = self._renamed_files_before_overrides.extended_status()

        return status

    @pyqtSlot()
    def start(self):
        self.prologue_finished.emit()

        self._feed_initial_data()

    @pyqtSlot(str)
    def update_base_path(self, base_path):
        self._base_path.set_data(base_path)

    @pyqtSlot(bool)
    def update_scan_recursive(self, scan_recursive):
        self._scan_recursive.set_data(scan_recursive)

    @pyqtSlot(str)
    def update_rules_text(self, rules_text):
        self._rules_text.set_data(rules_text)

    @pyqtSlot(bool)
    def update_use_path(self, use_path):
        self._use_path.set_data(use_path)

    @pyqtSlot(bool)
    def update_use_extension(self, use_extension):
        self._use_extension.set_data(use_extension)

    @pyqtSlot(str, str)
    def add_override(self, original_path, explicit_name):
        self._overrides.set_data(dict(list(self._overrides.value().items()) + [(original_path, explicit_name)]))

    @pyqtSlot(str)
    def remove_override(self, original_path):
        self._overrides.set_data({k: v for k, v in self._overrides.value().items() if k != original_path})

    @pyqtSlot()
    def shutdown(self):
        self._stop_worker()
        self.has_shutdown.emit()

    def _init_data_flow(self):
        self._base_path = InputNode(self, '', debug_name='base path')
        self._scan_recursive = InputNode(self, False, debug_name='scan recursive')
        self._rules_text = InputNode(self, '', debug_name='rules text')
        self._use_extension = InputNode(self, False, debug_name='use extension')
        self._use_path = InputNode(self, False, debug_name='use path')
        self._overrides = InputNode(self, {}, debug_name='overrides')

        self._scanned_files = ScannedFilesNode(self, self._base_path, self._scan_recursive)
        self._scanned_files.updated.connect(self._on_scanned_files_updated)
        self._scanned_files.updated.connect(self._report_updated_status)

        self._rules = RulesNode(self, self._rules_text)
        self._rules.updated.connect(self._report_updated_status)

        self._renamed_files_before_overrides = \
            RenamedFilesBeforeOverridesNode(self, self._scanned_files, self._rules, self._use_path, self._use_extension)
        self._renamed_files_before_overrides.updated.connect(self._report_updated_status)

        self._renamed_files = RenamedFilesNode(self, self._renamed_files_before_overrides, self._overrides)
        self._renamed_files.updated.connect(self._on_renamed_files_updated)
        self._renamed_files.updated.connect(self._report_updated_status)

    @pyqtSlot()
    def _report_updated_status(self):
        # This mechanism will cause a status update to only be emitted after the core has finished processing all other
        # events
        self._defer_status_update_level += 1
        QMetaObject.invokeMethod(self, '_report_updated_status_impl', Qt.QueuedConnection)

    @pyqtSlot()
    def _report_updated_status_impl(self):
        self._defer_status_update_level -= 1
        if self._defer_status_update_level == 0:
            self.status_changed.emit(self.status())

    @pyqtSlot(object)
    def _feed_initial_data(self):
        self._overrides.set_data(self._args.overrides or {})
        self._protect_overrides = True

        self._rules_text.set_data(self._args.rules_text or '')
        self._use_extension.set_data(self._args.use_extension or False)
        self._use_path.set_data(self._args.use_path or False)

        self._base_path.set_data(self._args.base_path or '')
        self._scan_recursive.set_data(self._args.scan_recursive or False)

    @pyqtSlot()
    def _on_scanned_files_updated(self):
        if self._scanned_files.status() not in [BAONStatus.IN_PROGRESS, BAONStatus.PENDING]:
            self.scanned_files_updated.emit(
                self._scanned_files.data() if self._scanned_files.status() == BAONStatus.AVAILABLE else []
            )

            if self._protect_overrides:
                self._protect_overrides = False
            else:
                self._overrides.set_data({})

    @pyqtSlot()
    def _on_renamed_files_updated(self):
        if self._renamed_files.status() not in [BAONStatus.IN_PROGRESS, BAONStatus.PENDING]:
            self.renamed_files_updated.emit(
                self._renamed_files.data() if self._renamed_files.status() == BAONStatus.AVAILABLE else []
            )


class DataFlowNode(QObject):
    will_update = pyqtSignal(object, object)
    updated = pyqtSignal()

    _data = None
    _status = None

    _inputs = None
    _debug_name = None

    def __init__(self, parent, inputs=None, data=None, status=BAONStatus.NOT_AVAILABLE, debug_name=None):
        super().__init__(parent)

        self._inputs = inputs or []
        self._debug_name = debug_name

        self._data = data
        self._status = status

        for input_node in self._inputs:
            input_node.updated.connect(self._recompute)

    def data(self):
        return self._data

    def status(self):
        return self._status

    def extended_status(self):
        return (
            self._status,
            self._data if self._status in [BAONStatus.ERROR, BAONStatus.IN_PROGRESS] else None,
        )

    @pyqtSlot(object)
    def set_data(self, data):
        self._update(data=data, status=BAONStatus.ERROR if isinstance(data, Exception) else BAONStatus.AVAILABLE)

    def _update(self, data=None, status=None):
        if data is None:
            data = self._data
        if status is None:
            status = self._status

        self.will_update.emit(data, status)

        if self._status == BAONStatus.IN_PROGRESS and status != BAONStatus.IN_PROGRESS:
            self.parent()._stop_worker()

        self._data = data
        self._status = status

        self.updated.emit()

    def _input_values(self):
        return [input_node.data() for input_node in self._inputs]

    @pyqtSlot()
    def _recompute(self):
        if not self._handle_inputs_not_ready():
            if not self._recompute_sync():
                self._recompute_async()

    def _handle_inputs_not_ready(self):
        if any(input_node.status() in [BAONStatus.IN_PROGRESS, BAONStatus.PENDING] for input_node in self._inputs):
            self._update(status=BAONStatus.PENDING)
            return True
        if any(input_node.status() in [BAONStatus.ERROR, BAONStatus.NOT_AVAILABLE] for input_node in self._inputs):
            self._update(status=BAONStatus.NOT_AVAILABLE)
            return True

        return False

    def _recompute_sync(self):
        try:
            return self._recompute_sync_impl(*self._input_values())
        except Exception as exc:
            self._update(status=BAONStatus.ERROR, data=exc)
            return True

    def _recompute_async(self):
        self._update(status=BAONStatus.IN_PROGRESS, data=ProgressInfo.make_indeterminate())

        self.parent()._start_worker(
            work=lambda check_abort: self._recompute_async_impl(check_abort, *self._input_values()),
            on_finished=self.set_data,
        )

    def _recompute_sync_impl(self, *args):
        raise NotImplementedError()

    def _recompute_async_impl(self, *args):
        raise NotImplementedError()

    def _on_async_progress(self, progress):
        self._update(status=BAONStatus.IN_PROGRESS, data=progress)


class InputNode(DataFlowNode):
    def __init__(self, parent, data=None, status=BAONStatus.NOT_AVAILABLE, debug_name=None):
        super().__init__(parent, inputs=[], data=data, status=status, debug_name=debug_name)


class RulesNode(DataFlowNode):
    def __init__(self, parent, rules_text_node):
        super().__init__(parent, inputs=[rules_text_node], debug_name='rules')

    def _recompute_sync_impl(self, rules_text):
        self.set_data(parse_rules(rules_text))
        return True


class ScannedFilesNode(DataFlowNode):
    def __init__(self, parent, base_path_node, scan_recursive_node):
        super().__init__(parent, inputs=[base_path_node, scan_recursive_node], debug_name='scanned_files')

    def _recompute_sync_impl(self, base_path, scan_recursive):
        if base_path == '':
            self._update(status=BAONStatus.NOT_AVAILABLE)
            return True

        return False

    def _recompute_async_impl(self, check_abort, base_path, scan_recursive):
        return scan_files(
            base_path,
            scan_recursive,
            on_progress=self._on_async_progress,
            check_abort=check_abort,
        )


class RenamedFilesBeforeOverridesNode(DataFlowNode):
    def __init__(self, parent, scanned_files_node, rules_node, use_path_node, use_extension_node):
        super().__init__(
            parent,
            inputs=[scanned_files_node, rules_node, use_path_node, use_extension_node],
            debug_name='renamed_wo_overrides'
        )

    def _recompute_sync_impl(self, scanned_files, rules, use_path, use_extension):
        if len(scanned_files) == 0:
            self._update(status=BAONStatus.AVAILABLE, data=[])
            return True

        return False

    def _recompute_async_impl(self, check_abort, scanned_files, rules, use_path, use_extension):
        return rename_files(
            scanned_files,
            rules,
            use_path=use_path,
            use_extension=use_extension,
            on_progress=self._on_async_progress,
            check_abort=check_abort,
        )


class RenamedFilesNode(DataFlowNode):
    def __init__(self, parent, renamed_files_before_overrides_node, overrides_node):
        super().__init__(
            parent,
            inputs=[renamed_files_before_overrides_node, overrides_node],
            debug_name='renamed_files'
        )

    def _recompute_sync_impl(self, renamed_files_before_overrides, overrides):
        self._update(
            status=BAONStatus.AVAILABLE,
            data=apply_rename_overrides(renamed_files_before_overrides, overrides)
        )
        return True
