# baon/ui/qt4_gui/forms/MainWindow.py
#
# (C) Copyright 2012-present  Cristian Dinu <goc9000@gmail.com>
# 
# This file is part of BAON.
#
# Licensed under the GPL-3


import platform

import baon.ui.qt4_gui.resources

from PyQt4.QtCore import Qt, pyqtSignal, pyqtSlot
from PyQt4.QtGui import QCheckBox, QDialog, QDialogButtonBox, QGroupBox, QHBoxLayout, QIcon, QSizePolicy, QVBoxLayout,\
    QMessageBox

from baon.core.files.BAONPath import BAONPath
from baon.ui.qt4_gui.BAONStatus import BAONStatus
from baon.ui.qt4_gui.mixins.CenterOnScreenMixin import CenterOnScreenMixin
from baon.ui.qt4_gui.mixins.SetupTabStopsMixin import SetupTabStopsMixin
from baon.ui.qt4_gui.widgets.BasePathPanel import BasePathPanel
from baon.ui.qt4_gui.widgets.RulesEditor import RulesEditor
from baon.ui.qt4_gui.widgets.StatusBox import StatusBox
from baon.ui.qt4_gui.widgets.files_display.FilesDisplay import FilesDisplay
from baon.ui.qt4_gui.widgets.files_display.FilesDisplaySummaryPanel import FilesDisplaySummaryPanel


class MainWindow(QDialog, SetupTabStopsMixin, CenterOnScreenMixin):
    WINDOW_TITLE_TEXT = 'BAON'
    OPTIONS_BOX_TEXT = 'Options'
    SCAN_RECURSIVE_CHECKBOX_TEXT = 'Recursively scan subfolders'
    USE_PATH_CHECKBOX_TEXT = 'Use path'
    USE_EXTENSION_CHECKBOX_TEXT = 'Use extension'
    RULES_BOX_TEXT = 'Rename Rules'
    FILES_BOX_TEXT = 'Renamed Files'

    RENAME_WARNINGS_DIALOG_CAPTION = 'Please Confirm'
    RENAME_WARNINGS_DIALOG_TEXT = 'There are warnings for some of the files. Proceed with the rename operation anyway?'

    RENAME_COMPLETE_DIALOG_CAPTION = 'Rename Complete'
    RENAME_COMPLETE_DIALOG_TEXT =\
        'The files have been renamed successfully. Do you wish to perform another rename operation?'

    DEFAULT_WINDOW_WIDTH = 800
    DEFAULT_WINDOW_HEIGHT = 600
    RULES_BOX_HEIGHT = 112

    base_path_edited = pyqtSignal(str)
    scan_recursive_changed = pyqtSignal(bool)
    rules_text_changed = pyqtSignal(str)
    use_path_changed = pyqtSignal(bool)
    use_extension_changed = pyqtSignal(bool)

    request_add_override = pyqtSignal(BAONPath, BAONPath)
    request_remove_override = pyqtSignal(BAONPath)

    request_do_rename = pyqtSignal()

    request_rescan = pyqtSignal()

    _base_path_panel = None
    _scan_recursive_checkbox = None
    _use_path_checkbox = None
    _use_extension_checkbox = None
    _rules_editor = None
    _files_display = None
    _files_display_summary_panel = None
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
            self._files_display_summary,
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
        self._files_display_summary = FilesDisplaySummaryPanel(box)

        self._files_display.request_add_override.connect(self.request_add_override)
        self._files_display.request_remove_override.connect(self.request_remove_override)

        self._files_display.counts_changed.connect(self._files_display_summary.set_counts)
        self._files_display.is_browsing_category_changed.connect(self._files_display_summary.set_is_browsing_category)
        self._files_display.has_next_in_category_changed.connect(self._files_display_summary.set_has_next_in_category)
        self._files_display.has_prev_in_category_changed.connect(self._files_display_summary.set_has_prev_in_category)

        self._files_display_summary.start_browsing_category.connect(self._files_display.start_browsing_category)
        self._files_display_summary.next_in_category.connect(self._files_display.next_in_category)
        self._files_display_summary.prev_in_category.connect(self._files_display.prev_in_category)

        layout = QVBoxLayout(box)
        layout.addWidget(self._files_display)
        layout.addWidget(self._files_display_summary)

        return box

    def _create_status_box(self):
        self._status_box = StatusBox(self)

        return self._status_box

    def _create_dialog_buttons(self):
        self._dialog_button_box = QDialogButtonBox(self)
        self._dialog_button_box.setOrientation(Qt.Horizontal)
        self._dialog_button_box.setStandardButtons(QDialogButtonBox.Cancel | QDialogButtonBox.Ok)
        self._dialog_button_box.setCenterButtons(True)

        self._dialog_button_box.accepted.connect(self._confirm_rename)
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
    def show_first_time(self):
        self.show()
        self.raise_()

        # We need to do this here as otherwise the operation may fail on some platforms
        self.setWindowIcon(QIcon(':/app_icon.png'))

    @pyqtSlot(str)
    def set_base_path(self, base_path):
        self._base_path_panel.set_base_path(base_path)

    @pyqtSlot(BAONStatus)
    def report_status(self, status):
        files_busy = \
            status.scan_status in [BAONStatus.IN_PROGRESS, BAONStatus.PENDING] or \
            status.rename_status in [BAONStatus.IN_PROGRESS, BAONStatus.PENDING]

        self._files_display.setEnabled(not files_busy)

        if status.rules_status == BAONStatus.ERROR:
            self._rules_editor.show_error(status.rules_status_extra.source_span)
        else:
            self._rules_editor.clear_error()

        self._status_box.show_status(status)

        self._dialog_button_box.button(QDialogButtonBox.Ok).setEnabled(
            status.execute_status in [BAONStatus.WAITING_FOR_USER, BAONStatus.ERROR]
        )

        if status.execute_status == BAONStatus.AVAILABLE:
            self._on_rename_completed()

    @pyqtSlot(list)
    def update_scanned_files(self, files):
        self._files_display.set_original_files(files)

    @pyqtSlot(list)
    def update_renamed_files(self, files):
        self._files_display.set_renamed_files(files)

    @pyqtSlot()
    def _confirm_rename(self):
        if self._files_display.has_rename_warnings():
            if not self._ask_user(self.RENAME_WARNINGS_DIALOG_CAPTION, self.RENAME_WARNINGS_DIALOG_TEXT):
                return

        self.request_do_rename.emit()

    def _on_rename_completed(self):
        self._rules_editor.clear()
        self.request_rescan.emit()

        if self._ask_user(self.RENAME_COMPLETE_DIALOG_CAPTION, self.RENAME_COMPLETE_DIALOG_TEXT):
            pass
        else:
            self.reject()

    def _ask_user(self, caption, text):
        on_mac = platform.system() == 'Darwin'

        dialog = QMessageBox(
            QMessageBox.Question,
            caption,
            text,
            QMessageBox.Yes | QMessageBox.No,
            self,
            Qt.Sheet if on_mac else Qt.Dialog | Qt.MSWindowsFixedSizeDialogHint,
        )
        dialog.setDefaultButton(QMessageBox.No)
        dialog.setWindowModality(Qt.WindowModal)

        return dialog.exec_() == QMessageBox.Yes
