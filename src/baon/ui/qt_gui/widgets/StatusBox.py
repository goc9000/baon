# baon/ui/qt_gui/widgets/StatusBox.py
#
# (C) Copyright 2012-present  Cristian Dinu <goc9000@gmail.com>
# 
# This file is part of BAON.
#
# Licensed under the GPL-3


from PyQt4.QtGui import QGroupBox, QHBoxLayout, QLabel, QProgressBar


class StatusBox(QGroupBox):
    STATUS_BOX_TEXT = 'Status'

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

    def show_message(self, format_string, *args, **kwargs):
        self._show_raw_message(format_string.format(*args, **kwargs))

    def show_progress(self, progress, text):
        self._show_raw_message(text, progress=progress)

    def show_error(self, error, caption=None):
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
