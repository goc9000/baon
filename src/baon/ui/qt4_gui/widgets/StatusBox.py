# baon/ui/qt4_gui/widgets/StatusBox.py
#
# (C) Copyright 2012-present  Cristian Dinu <goc9000@gmail.com>
# 
# This file is part of BAON.
#
# Licensed under the GPL-3


from PyQt4.QtCore import pyqtSlot
from PyQt4.QtGui import QGroupBox, QHBoxLayout, QLabel, QProgressBar

from baon.core.plan.__errors__.make_rename_plan_errors import MakeRenamePlanError
from baon.ui.qt4_gui.BAONStatus import BAONStatus


class StatusBox(QGroupBox):
    STATUS_BOX_TEXT = 'Status'

    BASE_PATH_REQUIRED_MESSAGE_TEXT = 'Fill in the base path to start scanning for files to be renamed.'
    SCAN_FILES_PROGRESS_TEXT = 'Scanning files'
    SCAN_FILES_ERROR_CAPTION_TEXT = 'Error scanning files'

    RULES_ERROR_CAPTION_TEXT = 'Error in rules'

    NO_FILES_TO_RENAME_MESSAGE_TEXT = 'No files to rename.'
    RENAME_FILES_PROGRESS_TEXT = 'Renaming files'
    RENAME_FILES_ERROR_CAPTION_TEXT = 'Error renaming files'

    NO_FILES_RENAMED_MESSAGE_TEXT = 'No files changed.'
    READY_TO_RENAME_MESSAGE_TEXT = 'Ready to rename.'
    RENAME_PROGRESS_TEXT = 'Executing rename'
    PLANNING_RENAME_ERROR_CAPTION_TEXT = 'Error while planning rename'
    RENAME_ERROR_CAPTION_TEXT = 'Error while executing rename'

    RENAME_COMPLETE_MESSAGE_TEXT = 'Rename completed.'

    READY_MESSAGE_TEXT = 'Ready.'

    ERROR_COLOR = '#ff0000'

    _status_label = None
    _status_progressbar = None

    def __init__(self, parent):
        super().__init__(self.STATUS_BOX_TEXT, parent)

        self._status_label = QLabel(self)
        self._status_progressbar = QProgressBar(self)
        self._status_progressbar.setVisible(False)
        self._status_progressbar.setMinimum(0)

        layout = QHBoxLayout(self)
        layout.addWidget(self._status_label)
        layout.addWidget(self._status_progressbar)

    @pyqtSlot(BAONStatus)
    def show_status(self, status):
        if status.scan_status == BAONStatus.IN_PROGRESS:
            self._show_progress(status.scan_status_extra, self.SCAN_FILES_PROGRESS_TEXT)
        elif status.rename_status == BAONStatus.IN_PROGRESS:
            self._show_progress(status.rename_status_extra, self.RENAME_FILES_PROGRESS_TEXT)
        elif status.execute_status == BAONStatus.IN_PROGRESS:
            self._show_progress(status.execute_status_extra, self.RENAME_PROGRESS_TEXT)
        elif status.scan_status == BAONStatus.ERROR:
            self._show_error(status.scan_status_extra, self.SCAN_FILES_ERROR_CAPTION_TEXT)
        elif status.rules_status == BAONStatus.ERROR:
            self._show_error(status.rules_status_extra, self.RULES_ERROR_CAPTION_TEXT)
        elif status.rename_status == BAONStatus.ERROR:
            self._show_error(status.rename_status_extra, self.RENAME_FILES_ERROR_CAPTION_TEXT)
        elif status.execute_status == BAONStatus.ERROR:
            if isinstance(status.execute_status_extra, MakeRenamePlanError):
                self._show_error(status.execute_status_extra, self.PLANNING_RENAME_ERROR_CAPTION_TEXT)
            else:
                self._show_error(status.execute_status_extra, self.RENAME_ERROR_CAPTION_TEXT)
        elif status.scan_status == BAONStatus.NOT_AVAILABLE:
            self._show_message(self.BASE_PATH_REQUIRED_MESSAGE_TEXT)
        elif status.rename_status == BAONStatus.NOT_AVAILABLE:
            self._show_message(self.NO_FILES_TO_RENAME_MESSAGE_TEXT)
        elif status.execute_status == BAONStatus.NOT_AVAILABLE:
            self._show_message(self.NO_FILES_RENAMED_MESSAGE_TEXT)
        elif status.execute_status == BAONStatus.WAITING_FOR_USER:
            self._show_message(self.READY_TO_RENAME_MESSAGE_TEXT)
        elif status.execute_status == BAONStatus.AVAILABLE:
            self._show_message(self.RENAME_COMPLETE_MESSAGE_TEXT)
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
