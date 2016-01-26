# baon/ui/qt4_gui/widgets/files_display/FilesDisplay.py
#
# (C) Copyright 2012-present  Cristian Dinu <goc9000@gmail.com>
# 
# This file is part of BAON.
#
# Licensed under the GPL-3


from PyQt4.QtCore import pyqtSignal, pyqtSlot, QSize, QTimer
from PyQt4.QtGui import QAbstractItemView, QHeaderView, QTableView

from baon.core.files.BAONPath import BAONPath
from baon.ui.qt4_gui.widgets.files_display.FilesDisplayModel import FilesDisplayModel


class FilesDisplay(QTableView):
    DEFAULT_ROW_HEIGHT = 20
    DEFAULT_ICON_SIZE = DEFAULT_ROW_HEIGHT - 2

    HIGHLIGHT_TIME_MSEC = 1000

    counts_changed = pyqtSignal(dict)
    is_browsing_category_changed = pyqtSignal(bool)
    has_next_in_category_changed = pyqtSignal(bool)
    has_prev_in_category_changed = pyqtSignal(bool)

    request_add_override = pyqtSignal(BAONPath, BAONPath)
    request_remove_override = pyqtSignal(BAONPath)

    _is_browsing_category = False
    _indexes_in_category = None
    _category_cursor = None
    _clear_highlight_timer = None

    def __init__(self, parent):
        super().__init__(parent)

        model = FilesDisplayModel(self)
        model.counts_changed.connect(self.counts_changed)
        model.request_add_override.connect(self.request_add_override)
        model.request_remove_override.connect(self.request_remove_override)

        self.setModel(model)
        self.setSelectionMode(QAbstractItemView.NoSelection)

        self.setShowGrid(False)
        self.setAlternatingRowColors(True)
        self.setIconSize(QSize(self.DEFAULT_ICON_SIZE, self.DEFAULT_ICON_SIZE))

        self.horizontalHeader().setResizeMode(QHeaderView.Stretch)

        self.verticalHeader().hide()
        self.verticalHeader().setDefaultSectionSize(self.DEFAULT_ROW_HEIGHT)

        self._clear_highlight_timer = QTimer(self)
        self._clear_highlight_timer.setSingleShot(True)
        self._clear_highlight_timer.setInterval(self.HIGHLIGHT_TIME_MSEC)
        self._clear_highlight_timer.timeout.connect(self._on_clear_highlight_timer_timeout)

    def has_rename_warnings(self):
        return self.model().has_rename_warnings()

    @pyqtSlot(list)
    def set_original_files(self, files):
        self.stop_browsing_category()
        self.model().set_original_files(files)

    @pyqtSlot(list)
    def set_renamed_files(self, files):
        self.stop_browsing_category()
        self.model().set_renamed_files(files)

    @pyqtSlot(str)
    def start_browsing_category(self, category):
        self._indexes_in_category = [
            i for i in range(self.model().rowCount()) if category in self.model().categories_for_item_at(i)
        ]

        if len(self._indexes_in_category) == 0:
            self.stop_browsing_category()
            return

        self._is_browsing_category = True
        self.is_browsing_category_changed.emit(True)
        self._set_category_cursor(0)

    @pyqtSlot()
    def stop_browsing_category(self):
        if self._is_browsing_category:
            self._is_browsing_category = False
            self.is_browsing_category_changed.emit(False)
            self._set_category_cursor(None)

    @pyqtSlot()
    def next_in_category(self):
        if self._is_browsing_category:
            self._set_category_cursor(self._category_cursor + 1)

    @pyqtSlot()
    def prev_in_category(self):
        if self._is_browsing_category:
            self._set_category_cursor(self._category_cursor - 1)

    def _set_category_cursor(self, new_cursor):
        if new_cursor is not None:
            row_no = self._indexes_in_category[new_cursor]

            self.model().set_highlighted_row(row_no)
            self._clear_highlight_timer.start()

            self.scrollTo(self.model().index(row_no, 0))

            self.has_prev_in_category_changed.emit(new_cursor > 0)
            self.has_next_in_category_changed.emit(new_cursor < len(self._indexes_in_category) - 1)
        else:
            self._clear_highlight_timer.stop()

        self._category_cursor = new_cursor

    def _on_clear_highlight_timer_timeout(self):
        self.model().set_highlighted_row(None)
