# baon/ui/qt_gui/widgets/files_display/FilesDisplayModel.py
#
# (C) Copyright 2012-present  Cristian Dinu <goc9000@gmail.com>
# 
# This file is part of BAON.
#
# Licensed under the GPL-3


from PyQt4.QtCore import Qt, pyqtSlot, QAbstractTableModel, QFileInfo
from PyQt4.QtGui import QFileIconProvider


class FilesDisplayModel(QAbstractTableModel):
    COL_INDEX_FROM = 0
    COL_INDEX_TO = 1

    FROM_COLUMN_TEXT = 'From'
    TO_COLUMN_TEXT = 'To'

    _original_files = None
    _data_cache = None

    def __init__(self, parent):
        super().__init__(parent)

        self._original_files = []
        self._data_cache = {}

    @pyqtSlot(list)
    def set_original_files(self, files):
        self.beginResetModel()
        self._original_files = files
        self._clear_data_cache()
        self.endResetModel()

    def rowCount(self, *args):
        return len(self._original_files)

    def columnCount(self, *args):
        return 2

    def data(self, index, role=Qt.DisplayRole):
        if (index, role) in self._data_cache:
            return self._data_cache[(index, role)]

        value = self._data_impl(index, role)
        self._data_cache[(index, role)] = value

        return value

    def flags(self, index):
        item_flags = Qt.ItemIsEnabled

        if index.column() == self.COL_INDEX_TO:
            item_flags |= Qt.ItemIsEditable

        return item_flags

    def headerData(self, index, orientation, role=Qt.DisplayRole):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            if index == self.COL_INDEX_FROM:
                return self.FROM_COLUMN_TEXT
            elif index == self.COL_INDEX_TO:
                return self.TO_COLUMN_TEXT

        return super().headerData(index, orientation, role)

    def _clear_data_cache(self):
        self._data_cache = {}

    def _data_impl(self, index, role):
        original_file = self._original_files[index.row()]

        key = (index.column(), role)
        if key in self.DATA_GETTERS:
            return self.DATA_GETTERS[key](self, original_file, renamed_file)

        return None

    def _get_original_text(self, original_file, renamed_file):
        return original_file.filename

    def _get_original_icon(self, original_file, renamed_file):
        return QFileIconProvider().icon(QFileInfo(original_file.full_path))

    DATA_GETTERS = {
        (COL_INDEX_FROM, Qt.DisplayRole): _get_original_text,
        (COL_INDEX_FROM, Qt.DecorationRole): _get_original_icon,
        (COL_INDEX_TO, Qt.DisplayRole): _get_original_text,
        (COL_INDEX_TO, Qt.DecorationRole): _get_original_icon,
    }
