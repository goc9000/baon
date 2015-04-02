# baon/gui/qt/widgets/MainWindow.py
#
# (C) Copyright 2012-present  Cristian Dinu <goc9000@gmail.com>
# 
# This file is part of BAON.
#
# Licensed under the GPL-3


from PyQt4.QtCore import Qt, pyqtSignal
from PyQt4.QtGui import QCheckBox, QDialog, QDialogButtonBox, QFont, QGroupBox, QHBoxLayout, QLabel, QLineEdit,\
    QProgressBar, QPushButton, QSizePolicy, QSpacerItem, QTextEdit, QVBoxLayout

from baon.gui.qt.utils.CenterWindowOnScreenTrait import CenterWindowOnScreenTrait

from baon.gui.qt.widgets.FilesDisplay import FilesDisplay


class MainWindow(CenterWindowOnScreenTrait, QDialog):
    WINDOW_TITLE_TEXT = 'BAON'
    BASE_PATH_LABEL_TEXT = 'Base Path'
    BROWSE_BUTTON_TEXT = 'Browse...'
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

    scan_recursive_changed = pyqtSignal(bool)
    use_path_changed = pyqtSignal(bool)
    use_extension_changed = pyqtSignal(bool)

    _base_path_editor = None
    _browse_button = None
    _scan_recursive_checkbox = None
    _use_path_checkbox = None
    _use_extension_checkbox = None
    _rules_editor = None
    _files_display = None
    _status_label = None
    _status_progressbar = None

    def __init__(self):
        QDialog.__init__(self)

        self.init_ui()
        self.center_on_screen()

    def init_ui(self):
        self.setWindowTitle(self.WINDOW_TITLE_TEXT)
        self.resize(self.DEFAULT_WINDOW_WIDTH, self.DEFAULT_WINDOW_HEIGHT)

        main_layout = QVBoxLayout(self)
        main_layout.addLayout(self._create_base_path_widgets())
        main_layout.addWidget(self._create_options_box())
        main_layout.addWidget(self._create_rules_box())
        main_layout.addWidget(self._create_files_box())
        main_layout.addWidget(self._create_status_box())
        main_layout.addWidget(self._create_dialog_buttons())

    def _create_base_path_widgets(self):
        self._base_path_editor = QLineEdit(self)
        self._browse_button = QPushButton(self.BROWSE_BUTTON_TEXT, self)

        layout = QHBoxLayout()
        layout.addWidget(QLabel(self.BASE_PATH_LABEL_TEXT, self))
        layout.addWidget(self._base_path_editor)
        layout.addWidget(self._browse_button)

        return layout

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
        layout.addItem(QSpacerItem(0, 0, QSizePolicy.Expanding, QSizePolicy.Minimum))

        return box

    def _create_rules_box(self):
        box = QGroupBox(self.RULES_BOX_TEXT, self)
        box.setMaximumHeight(self.RULES_BOX_HEIGHT)

        mono_font = QFont()
        mono_font.setFixedPitch(True)

        self._rules_editor = QTextEdit(box)
        self._rules_editor.setFont(mono_font)
        self._rules_editor.setAcceptRichText(False)

        layout = QHBoxLayout(box)
        layout.addWidget(self._rules_editor)

        return box

    def _create_files_box(self):
        box = QGroupBox(self.FILES_BOX_TEXT, self)
        box.setSizePolicy(QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding))

        self._files_display = FilesDisplay(self)

        layout = QHBoxLayout(box)
        layout.addWidget(self._files_display)

        return box

    def _create_status_box(self):
        box = QGroupBox(self.STATUS_BOX_TEXT, self)

        self._status_label = QLabel(self)
        self._status_progressbar = QProgressBar(box)
        self._status_progressbar.setVisible(False)

        layout = QHBoxLayout(box)
        layout.addWidget(self._status_label)
        layout.addWidget(self._status_progressbar)

        return box

    def _create_dialog_buttons(self):
        button_box = QDialogButtonBox(self)
        button_box.setOrientation(Qt.Horizontal)
        button_box.setStandardButtons(QDialogButtonBox.Cancel | QDialogButtonBox.Ok)
        button_box.setCenterButtons(True)

        return button_box
