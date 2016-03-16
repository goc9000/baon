# baon/ui/qt4_gui/widgets/BasePathPanel.py
#
# (C) Copyright 2012-present  Cristian Dinu <goc9000@gmail.com>
# 
# This file is part of BAON.
#
# Licensed under the GPL-3


import os

from PyQt4.QtCore import Qt, QTimer, pyqtSignal, pyqtSlot
from PyQt4.QtGui import QFileDialog, QHBoxLayout, QLabel, QLineEdit, QPushButton, QWidget

from baon.ui.qt4_gui.mixins.SetupTabStopsMixin import SetupTabStopsMixin


class BasePathPanel(QWidget, SetupTabStopsMixin):
    BASE_PATH_LABEL_TEXT = 'Base Path'
    BROWSE_BUTTON_TEXT = 'Browse...'
    BROWSE_DIALOG_CAPTION_TEXT = 'Choose Base Directory'

    BASE_PATH_EDITOR_QUIESCENCE_TIME_MSEC = 1000

    path_edited = pyqtSignal(str)

    _base_path_editor = None
    _base_path_editor_quiescence_timer = None
    _browse_button = None

    _last_emitted_path = ''

    def __init__(self, parent):
        super().__init__(parent)

        self._base_path_editor_quiescence_timer = QTimer(self)
        self._base_path_editor_quiescence_timer.setSingleShot(True)
        self._base_path_editor_quiescence_timer.setInterval(self.BASE_PATH_EDITOR_QUIESCENCE_TIME_MSEC)
        self._base_path_editor_quiescence_timer.timeout.connect(self._on_base_path_editor_quiescence_timer_timeout)

        self._base_path_editor = QLineEdit(self)
        self._base_path_editor.editingFinished.connect(self._on_base_path_editor_finished)
        self._base_path_editor.textEdited.connect(self._base_path_editor_quiescence_timer.start)

        self._browse_button = QPushButton(self.BROWSE_BUTTON_TEXT, self)
        self._browse_button.pressed.connect(self._on_browse_button_pressed)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(QLabel(self.BASE_PATH_LABEL_TEXT, self))
        layout.addWidget(self._base_path_editor)
        layout.addWidget(self._browse_button)

        self.setFocusProxy(self._base_path_editor)

        self._setup_tab_stops(
            self._base_path_editor,
            self._browse_button,
        )

    def base_path(self):
        return self._base_path_editor.text()

    @pyqtSlot()
    def set_base_path(self, base_path):
        self._base_path_editor_quiescence_timer.stop()
        self._base_path_editor.setText(base_path)
        self._maybe_emit_path_edited()

    @pyqtSlot()
    def _on_base_path_editor_finished(self):
        self._base_path_editor_quiescence_timer.stop()
        self._maybe_emit_path_edited()

    @pyqtSlot()
    def _on_base_path_editor_quiescence_timer_timeout(self):
        self._maybe_emit_path_edited()

    @pyqtSlot()
    def _on_browse_button_pressed(self):
        self._base_path_editor_quiescence_timer.stop()

        directory = QFileDialog.getExistingDirectory(
            parent=self.window(),
            caption=self.BROWSE_DIALOG_CAPTION_TEXT,
            directory=self.base_path() or os.path.expanduser('~'),
        )
        if directory != '':
            self._base_path_editor.setText(directory)

        self._maybe_emit_path_edited()

    @pyqtSlot()
    def _maybe_emit_path_edited(self):
        if self.base_path() != self._last_emitted_path:
            self._last_emitted_path = self.base_path()
            self.path_edited.emit(self.base_path())
