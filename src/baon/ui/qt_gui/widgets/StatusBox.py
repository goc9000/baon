# baon/ui/qt_gui/widgets/StatusBox.py
#
# (C) Copyright 2012-present  Cristian Dinu <goc9000@gmail.com>
# 
# This file is part of BAON.
#
# Licensed under the GPL-3


from PyQt4.QtCore import pyqtSlot
from PyQt4.QtGui import QGroupBox, QHBoxLayout, QLabel, QProgressBar

from baon.core.utils.progress.ProgressInfo import ProgressInfo


class StatusBox(QGroupBox):
    STATUS_BOX_TEXT = 'Status'

    BASE_PATH_REQUIRED_MESSAGE_TEXT = 'Fill in the base path to start scanning for files to be renamed.'
    SCAN_FILES_PROGRESS_TEXT = 'Scanning files'
    SCAN_FILES_ERROR_CAPTION_TEXT = 'Error scanning files'

    RULES_ERROR_CAPTION_TEXT = 'Error in rules'

    NO_FILES_TO_RENAME_MESSAGE_TEXT = 'No files to rename.'
    RENAME_FILES_PROGRESS_TEXT = 'Renaming files'
    RENAME_FILES_ERROR_CAPTION_TEXT = 'Error renaming files'

    READY_MESSAGE_TEXT = 'Ready.'

    ERROR_COLOR = '#ff0000'

    _status_label = None
    _status_progressbar = None

    _show_base_path_required = False
    _scan_files_error = None
    _rules_error = None
    _show_no_files_to_rename = False
    _rename_files_error = None

    def __init__(self, parent):
        super().__init__(self.STATUS_BOX_TEXT, parent)

        self._status_label = QLabel(self)
        self._status_progressbar = QProgressBar(self)
        self._status_progressbar.setVisible(False)
        self._status_progressbar.setMinimum(0)

        layout = QHBoxLayout(self)
        layout.addWidget(self._status_label)
        layout.addWidget(self._status_progressbar)

        self._update_display()

    @pyqtSlot(ProgressInfo)
    def show_scan_files_progress(self, progress):
        self._show_progress(progress, self.SCAN_FILES_PROGRESS_TEXT)

    @pyqtSlot()
    def show_base_path_required(self):
        self._show_base_path_required = True
        self._scan_files_error = None
        self._update_display()

    @pyqtSlot(Exception)
    def show_scan_files_error(self, error):
        self._show_base_path_required = False
        self._scan_files_error = error
        self._update_display()

    @pyqtSlot()
    def clear_scan_files_error(self):
        self._show_base_path_required = False
        self._scan_files_error = None
        self._update_display()

    @pyqtSlot(Exception)
    def show_rules_error(self, error):
        self._rules_error = error
        self._update_display()

    @pyqtSlot()
    def clear_rules_error(self):
        self._rules_error = None
        self._update_display()

    @pyqtSlot(ProgressInfo)
    def show_rename_files_progress(self, progress):
        self._show_progress(progress, self.RENAME_FILES_PROGRESS_TEXT)

    @pyqtSlot()
    def show_no_files_to_rename(self):
        self._show_no_files_to_rename = True
        self._rename_files_error = None
        self._update_display()

    @pyqtSlot(Exception)
    def show_rename_files_error(self, error):
        self._show_no_files_to_rename = False
        self._rename_files_error = error
        self._update_display()

    @pyqtSlot()
    def clear_rename_files_error(self):
        self._show_no_files_to_rename = False
        self._rename_files_error = None
        self._update_display()

    @pyqtSlot()
    def stop_showing_progress(self):
        self._status_progressbar.setVisible(False)
        self._update_display()

    def _update_display(self):
        if self._status_progressbar.isVisible():
            return

        if self._rules_error is not None:
            self._show_error(self._rules_error, self.RULES_ERROR_CAPTION_TEXT)
        elif self._scan_files_error is not None:
            self._show_error(self._scan_files_error, self.SCAN_FILES_ERROR_CAPTION_TEXT)
        elif self._show_base_path_required:
            self._show_message(self.BASE_PATH_REQUIRED_MESSAGE_TEXT)
        elif self._rename_files_error is not None:
            self._show_error(self._rename_files_error, self.RENAME_FILES_ERROR_CAPTION_TEXT)
        elif self._show_no_files_to_rename:
            self._show_message(self.NO_FILES_TO_RENAME_MESSAGE_TEXT)
        else:
            self._show_message(self.READY_MESSAGE_TEXT)

    def _show_message(self, format_string, *args, **kwargs):
        self._show_raw_message(format_string.format(*args, **kwargs))

    def _show_progress(self, progress, text):
        self._show_raw_message(text, progress=progress)

    def _show_error(self, error, caption=None):
        text = str(error)
        if caption is not None:
            text = caption + ': ' + text

        self._show_raw_message(text, is_error=True)

    def _show_raw_message(self, text, is_error=False, progress=None):
        self._status_label.setText(text)
        self._status_label.setStyleSheet("QLabel {{ color: {0} }}".format(self.ERROR_COLOR) if is_error else "")

        self._status_progressbar.setVisible(progress is not None)

        if progress is not None:
            if progress.is_indeterminate():
                self._status_progressbar.setMaximum(0)
            else:
                self._status_progressbar.setMaximum(progress.total)
                self._status_progressbar.setValue(progress.done)
