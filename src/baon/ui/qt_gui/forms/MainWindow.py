# baon/ui/qt_gui/forms/MainWindow.py
#
# (C) Copyright 2012-present  Cristian Dinu <goc9000@gmail.com>
# 
# This file is part of BAON.
#
# Licensed under the GPL-3


from PyQt4.QtCore import Qt, pyqtSignal
from PyQt4.QtGui import QCheckBox, QDialog, QDialogButtonBox, QGroupBox, QHBoxLayout, QLabel, QProgressBar,\
    QSizePolicy, QVBoxLayout

from baon.ui.qt_gui.utils.WindowWithCenterOnScreenTrait import WindowWithCenterOnScreenTrait
from baon.ui.qt_gui.utils.WidgetWithSetupTabStopsTrait import WidgetWithSetupTabStopsTrait

from baon.ui.qt_gui.widgets.BasePathPanel import BasePathPanel
from baon.ui.qt_gui.widgets.FilesDisplay import FilesDisplay
from baon.ui.qt_gui.widgets.RulesEditor import RulesEditor


class MainWindow(WidgetWithSetupTabStopsTrait, WindowWithCenterOnScreenTrait, QDialog):
    WINDOW_TITLE_TEXT = 'BAON'
    OPTIONS_BOX_TEXT = 'Options'
    SCAN_RECURSIVE_CHECKBOX_TEXT = 'Recursively scan subfolders'
    USE_PATH_CHECKBOX_TEXT = 'Use path'
    USE_EXTENSION_CHECKBOX_TEXT = 'Use extension'
    RULES_BOX_TEXT = 'Rename Rules'
    FILES_BOX_TEXT = 'Renamed Files'
    STATUS_BOX_TEXT = 'Status'

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
    _status_label = None
    _status_progressbar = None
    _dialog_button_box = None

    def __init__(self):
        QDialog.__init__(self)

        self.init_ui()
        self.center_on_screen()

    def init_ui(self):
        self.setWindowTitle(self.WINDOW_TITLE_TEXT)
        self.resize(self.DEFAULT_WINDOW_WIDTH, self.DEFAULT_WINDOW_HEIGHT)

        main_layout = QVBoxLayout(self)
        main_layout.addWidget(self._create_base_path_panel())
        main_layout.addWidget(self._create_options_box())
        main_layout.addWidget(self._create_rules_box())
        main_layout.addWidget(self._create_files_box())
        main_layout.addWidget(self._create_status_box())
        main_layout.addWidget(self._create_dialog_buttons())

        self.setup_tab_stops(
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
        box = QGroupBox(self.STATUS_BOX_TEXT, self)

        self._status_label = QLabel(box)
        self._status_progressbar = QProgressBar(box)
        self._status_progressbar.setVisible(False)

        layout = QHBoxLayout(box)
        layout.addWidget(self._status_label)
        layout.addWidget(self._status_progressbar)

        return box

    def _create_dialog_buttons(self):
        self._dialog_button_box = QDialogButtonBox(self)
        self._dialog_button_box.setOrientation(Qt.Horizontal)
        self._dialog_button_box.setStandardButtons(QDialogButtonBox.Cancel | QDialogButtonBox.Ok)
        self._dialog_button_box.setCenterButtons(True)

        return self._dialog_button_box
