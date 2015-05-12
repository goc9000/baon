# baon/ui/qt_gui/forms/MainWindow.py
#
# (C) Copyright 2012-present  Cristian Dinu <goc9000@gmail.com>
# 
# This file is part of BAON.
#
# Licensed under the GPL-3


from PyQt4.QtCore import Qt, pyqtSignal, pyqtSlot
from PyQt4.QtGui import QCheckBox, QDialog, QDialogButtonBox, QGroupBox, QHBoxLayout, QSizePolicy, QVBoxLayout

from baon.ui.qt_gui.mixins.CenterOnScreenMixin import CenterOnScreenMixin
from baon.ui.qt_gui.mixins.SetupTabStopsMixin import SetupTabStopsMixin

from baon.ui.qt_gui.widgets.BasePathPanel import BasePathPanel
from baon.ui.qt_gui.widgets.files_display.FilesDisplay import FilesDisplay
from baon.ui.qt_gui.widgets.RulesEditor import RulesEditor
from baon.ui.qt_gui.widgets.StatusBox import StatusBox

from baon.core.errors.BAONError import BAONError

from baon.core.utils.progress.ProgressInfo import ProgressInfo


class MainWindow(QDialog, SetupTabStopsMixin, CenterOnScreenMixin):
    WINDOW_TITLE_TEXT = 'BAON'
    OPTIONS_BOX_TEXT = 'Options'
    SCAN_RECURSIVE_CHECKBOX_TEXT = 'Recursively scan subfolders'
    USE_PATH_CHECKBOX_TEXT = 'Use path'
    USE_EXTENSION_CHECKBOX_TEXT = 'Use extension'
    RULES_BOX_TEXT = 'Rename Rules'
    FILES_BOX_TEXT = 'Renamed Files'

    DEFAULT_WINDOW_WIDTH = 800
    DEFAULT_WINDOW_HEIGHT = 600
    RULES_BOX_HEIGHT = 112

    base_path_edited = pyqtSignal(str)
    scan_recursive_changed = pyqtSignal(bool)
    rules_text_changed = pyqtSignal(str)
    use_path_changed = pyqtSignal(bool)
    use_extension_changed = pyqtSignal(bool)

    _base_path_panel = None
    _scan_recursive_checkbox = None
    _use_path_checkbox = None
    _use_extension_checkbox = None
    _rules_editor = None
    _files_display = None
    _status_box = None
    _dialog_button_box = None

    def __init__(self, args):
        super().__init__()

        self._init_ui()
        self._fill_in_controls(args)
        self._center_on_screen()

    def _init_ui(self):
        self.setWindowTitle(self.WINDOW_TITLE_TEXT)
        self.resize(self.DEFAULT_WINDOW_WIDTH, self.DEFAULT_WINDOW_HEIGHT)

        main_layout = QVBoxLayout(self)
        main_layout.addWidget(self._create_base_path_panel())
        main_layout.addWidget(self._create_options_box())
        main_layout.addWidget(self._create_rules_box())
        main_layout.addWidget(self._create_files_box())
        main_layout.addWidget(self._create_status_box())
        main_layout.addWidget(self._create_dialog_buttons())

        self._setup_tab_stops(
            self._base_path_panel,
            self._scan_recursive_checkbox,
            self._use_path_checkbox,
            self._use_extension_checkbox,
            self._rules_editor,
            self._files_display,
            self._dialog_button_box,
        )

    def _create_base_path_panel(self):
        self._base_path_panel = BasePathPanel(self)
        self._base_path_panel.path_edited.connect(self.base_path_edited)

        return self._base_path_panel

    def _create_options_box(self):
        box = QGroupBox(self.OPTIONS_BOX_TEXT, self)

        self._scan_recursive_checkbox = QCheckBox(self.SCAN_RECURSIVE_CHECKBOX_TEXT, box)
        self._scan_recursive_checkbox.toggled.connect(self.scan_recursive_changed)

        self._use_path_checkbox = QCheckBox(self.USE_PATH_CHECKBOX_TEXT, box)
        self._use_path_checkbox.toggled.connect(self.use_path_changed)

        self._use_extension_checkbox = QCheckBox(self.USE_EXTENSION_CHECKBOX_TEXT, box)
        self._use_extension_checkbox.toggled.connect(self.use_extension_changed)

        layout = QHBoxLayout(box)
        layout.addWidget(self._scan_recursive_checkbox)
        layout.addWidget(self._use_path_checkbox)
        layout.addWidget(self._use_extension_checkbox)
        layout.addStretch()

        return box

    def _create_rules_box(self):
        box = QGroupBox(self.RULES_BOX_TEXT, self)
        box.setMaximumHeight(self.RULES_BOX_HEIGHT)

        self._rules_editor = RulesEditor(box)
        self._rules_editor.rules_edited.connect(self.rules_text_changed)

        layout = QHBoxLayout(box)
        layout.addWidget(self._rules_editor)

        return box

    def _create_files_box(self):
        box = QGroupBox(self.FILES_BOX_TEXT, self)
        box.setSizePolicy(QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding))

        self._files_display = FilesDisplay(box)

        layout = QHBoxLayout(box)
        layout.addWidget(self._files_display)

        return box

    def _create_status_box(self):
        self._status_box = StatusBox(self)

        return self._status_box

    def _create_dialog_buttons(self):
        self._dialog_button_box = QDialogButtonBox(self)
        self._dialog_button_box.setOrientation(Qt.Horizontal)
        self._dialog_button_box.setStandardButtons(QDialogButtonBox.Cancel | QDialogButtonBox.Ok)
        self._dialog_button_box.setCenterButtons(True)

        self._dialog_button_box.rejected.connect(self.reject)

        return self._dialog_button_box

    def _fill_in_controls(self, args):
        if args.base_path is not None:
            self._base_path_panel.set_base_path(args.base_path)
        if args.scan_recursive is not None:
            self._scan_recursive_checkbox.setChecked(args.scan_recursive)
        if args.use_extension is not None:
            self._use_extension_checkbox.setChecked(args.use_extension)
        if args.use_path is not None:
            self._use_path_checkbox.setChecked(args.use_path)
        if args.rules_text is not None:
            self._rules_editor.set_rules(args.rules_text)

    @pyqtSlot()
    def report_base_path_required(self):
        self._status_box.show_base_path_required()

    @pyqtSlot()
    def report_started_scanning_files(self):
        self._files_display.setEnabled(False)

    @pyqtSlot(ProgressInfo)
    def report_scan_files_progress(self, progress):
        self._status_box.show_scan_files_progress(progress)

    @pyqtSlot()
    def report_scan_files_ok(self):
        self._status_box.clear_scan_files_error()

    @pyqtSlot(BAONError)
    def report_scan_files_error(self, error):
        self._status_box.show_scan_files_error(error)

    @pyqtSlot(list)
    def update_scanned_files(self, files):
        self._files_display.set_original_files(files)

    @pyqtSlot()
    def report_rules_ok(self):
        self._rules_editor.clear_error()
        self._status_box.clear_rules_error()

    @pyqtSlot(BAONError)
    def report_rules_error(self, error):
        self._rules_editor.show_error(error.source_span)
        self._status_box.show_rules_error(error)

    @pyqtSlot()
    def report_ready(self):
        self._files_display.setEnabled(True)
        self._status_box.stop_showing_progress()
