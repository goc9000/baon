# baon/ui/qt4_gui/widgets/files_display/FilesDisplayModel.py
#
# (C) Copyright 2012-present  Cristian Dinu <goc9000@gmail.com>
# 
# This file is part of BAON.
#
# Licensed under the GPL-3


from PyQt4.QtCore import Qt, pyqtSignal, pyqtSlot, QAbstractTableModel, QFileInfo, QObject
from PyQt4.QtGui import QFileIconProvider, QFont, QStyle, QApplication

from baon.core.files.BAONPath import BAONPath
from baon.core.renaming.RenamedFileReference import RenamedFileReference
from baon.core.utils.grammar_utils import format_tally
from baon.ui.qt4_gui.utils.make_qicon_with_overlay import make_qicon_with_overlay
from baon.ui.qt4_gui.utils.parse_qcolor import parse_qcolor


class FilesDisplayModel(QAbstractTableModel):
    COL_INDEX_FROM = 0
    COL_INDEX_TO = 1

    FROM_COLUMN_TEXT = 'From'
    TO_COLUMN_TEXT = 'To'

    ERROR_FOREGROUND_COLOR = parse_qcolor('#ff0000')
    WARNING_FOREGROUND_COLOR = parse_qcolor('#d0b000')
    CHANGED_FOREGROUND_COLOR = parse_qcolor('#0040e0')
    HIGHLIGHT_BACKGROUND_COLOR = parse_qcolor('#ffff00')

    ERROR_ITEM_NAME = 'Error'
    ERROR_ITEM_NAME_PLURAL = 'Errors'
    WARNING_ITEM_NAME = 'Warning'
    WARNING_ITEM_NAME_PLURAL = 'Warnings'

    counts_changed = pyqtSignal(dict)

    request_add_override = pyqtSignal(BAONPath, BAONPath)
    request_remove_override = pyqtSignal(BAONPath)

    _original_files = None
    _renamed_files = None
    _data_cache = None
    _highlighted_row = None

    def __init__(self, parent):
        super().__init__(parent)

        self._original_files = []
        self._renamed_files = []
        self._data_cache = {}

    @pyqtSlot(list)
    def set_original_files(self, files):
        self.beginResetModel()
        self._original_files = files
        self._renamed_files = []
        self._highlighted_row = None
        self._clear_data_cache()
        self.endResetModel()

        self._emit_new_counts()

    @pyqtSlot(list)
    def set_renamed_files(self, renamed_files):
        self._verify_renamed_files(self._original_files, renamed_files)

        self.beginResetModel()
        self._renamed_files = renamed_files
        self._highlighted_row = None
        self._clear_data_cache()
        self.endResetModel()

        self._emit_new_counts()

    @pyqtSlot(int)
    def set_highlighted_row(self, row):
        old_row = self._highlighted_row
        self._highlighted_row = row

        for changed_row in [old_row, row]:
            if changed_row is not None:
                self._clear_data_cache_for_row(changed_row, [Qt.BackgroundRole])
                self.dataChanged.emit(
                    self.index(changed_row, self.COL_INDEX_FROM),
                    self.index(changed_row, self.COL_INDEX_TO),
                )

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

    def setData(self, index, value, role=Qt.EditRole):
        if role != Qt.EditRole:
            return super().setData(index, value, role)

        original_path = self._original_files[index.row()].path

        if value != '':
            self.request_add_override.emit(original_path, original_path.replace_path_text(value))
        else:
            self.request_remove_override.emit(original_path)

        return True

    def flags(self, index):
        item_flags = Qt.ItemIsEnabled

        if (index.column() == self.COL_INDEX_TO) and (len(self._renamed_files) > 0):
            item_flags |= Qt.ItemIsEditable

        return item_flags

    def headerData(self, index, orientation, role=Qt.DisplayRole):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            if index == self.COL_INDEX_FROM:
                return self.FROM_COLUMN_TEXT
            elif index == self.COL_INDEX_TO:
                return self.TO_COLUMN_TEXT

        return super().headerData(index, orientation, role)

    def has_rename_warnings(self):
        return any(file_ref.has_warnings() for file_ref in self._renamed_files)

    def categories_for_item_at(self, index):
        original_file = self._original_files[index]
        renamed_file = self._renamed_files[index] if len(self._renamed_files) > 0 else None

        categories = {'all'}

        if original_file.has_errors():
            categories.add('scan_errors')
        if original_file.has_warnings():
            categories.add('scan_warnings')

        if renamed_file is not None:
            if renamed_file.has_errors():
                categories.add('rename_errors')
            if renamed_file.has_warnings():
                categories.add('rename_warnings')
            if renamed_file.is_changed():
                categories.add('changed')
            if renamed_file.is_override:
                categories.add('overrides')

        return categories

    def _emit_new_counts(self):
        counts = {}

        for index in range(len(self._original_files)):
            for category in self.categories_for_item_at(index):
                counts[category] = 1 + counts.get(category, 0)

        self.counts_changed.emit(counts)

    def _clear_data_cache(self):
        self._data_cache = {}

    def _clear_data_cache_for_row(self, row, roles=None):
        if roles is None:
            roles = [
                Qt.DisplayRole,
                Qt.EditRole,
                Qt.DecorationRole,
                Qt.ForegroundRole,
                Qt.FontRole,
                Qt.BackgroundRole,
                Qt.ToolTipRole,
            ]

        for role in roles:
            self._data_cache.pop((self.index(row, self.COL_INDEX_FROM), role), None)
            self._data_cache.pop((self.index(row, self.COL_INDEX_TO), role), None)

    def _data_impl(self, index, role):
        original_file = self._original_files[index.row()]
        renamed_file = self._renamed_files[index.row()] if len(self._renamed_files) > 0 else None

        key = (index.column(), role)
        if key in self.DATA_GETTERS:
            return self.DATA_GETTERS[key](self, original_file, renamed_file, index.row())

        return None

    def _get_original_text(self, original_file, renamed_file, index):
        return original_file.path.path_text()

    def _get_original_icon(self, original_file, renamed_file, index):
        icon = QFileIconProvider().icon(QFileInfo(original_file.path.real_path()))
        return self._add_icon_overlay_for_problems(icon, original_file)

    def _get_original_foreground(self, original_file, renamed_file, index):
        return self._get_foreground_for_file_info(original_file)

    def _get_original_background(self, original_file, renamed_file, index):
        return self.HIGHLIGHT_BACKGROUND_COLOR if index == self._highlighted_row else None

    def _get_original_tooltip(self, original_file, renamed_file, index):
        return self._get_file_tooltip(original_file.path, original_file.problems)

    def _get_renamed_text(self, original_file, renamed_file, index):
        if renamed_file is None:
            return original_file.path.path_text()

        return renamed_file.path.path_text()

    def _get_renamed_icon(self, original_file, renamed_file, index):
        icon = QFileIconProvider().icon(QFileInfo(original_file.path.real_path()))
        if renamed_file is not None:
            return self._add_icon_overlay_for_problems(icon, renamed_file)

        return icon

    def _get_renamed_foreground(self, original_file, renamed_file, index):
        if renamed_file is not None:
            return self._get_foreground_for_file_info(renamed_file)

        return None

    def _get_renamed_background(self, original_file, renamed_file, index):
        return self.HIGHLIGHT_BACKGROUND_COLOR if index == self._highlighted_row else None

    def _get_renamed_font(self, original_file, renamed_file, index):
        if renamed_file is not None and renamed_file.is_override:
            table = QObject.parent(self)
            font = table.font()

            return QFont(font.family(), font.pointSize(), QFont.Bold)

        return None

    def _get_renamed_tooltip(self, original_file, renamed_file, index):
        if renamed_file is not None:
            return self._get_file_tooltip(renamed_file.path, renamed_file.problems)
        else:
            return self._get_file_tooltip(original_file.path)

    DATA_GETTERS = {
        (COL_INDEX_FROM, Qt.DisplayRole): _get_original_text,
        (COL_INDEX_FROM, Qt.DecorationRole): _get_original_icon,
        (COL_INDEX_FROM, Qt.ForegroundRole): _get_original_foreground,
        (COL_INDEX_FROM, Qt.BackgroundRole): _get_original_background,
        (COL_INDEX_FROM, Qt.ToolTipRole): _get_original_tooltip,
        (COL_INDEX_TO, Qt.DisplayRole): _get_renamed_text,
        (COL_INDEX_TO, Qt.EditRole): _get_renamed_text,
        (COL_INDEX_TO, Qt.DecorationRole): _get_renamed_icon,
        (COL_INDEX_TO, Qt.ForegroundRole): _get_renamed_foreground,
        (COL_INDEX_TO, Qt.FontRole): _get_renamed_font,
        (COL_INDEX_TO, Qt.BackgroundRole): _get_renamed_background,
        (COL_INDEX_TO, Qt.ToolTipRole): _get_renamed_tooltip,
    }

    def _add_icon_overlay_for_problems(self, icon, file_info):
        if file_info.has_errors():
            return make_qicon_with_overlay(
                icon,
                QApplication.style().standardIcon(QStyle.SP_MessageBoxCritical),
            )
        elif file_info.has_warnings():
            return make_qicon_with_overlay(
                icon,
                QApplication.style().standardIcon(QStyle.SP_MessageBoxWarning),
            )
        else:
            return icon

    def _get_foreground_for_file_info(self, file_info):
        if file_info.has_errors():
            return self.ERROR_FOREGROUND_COLOR
        elif file_info.has_warnings():
            return self.WARNING_FOREGROUND_COLOR
        elif isinstance(file_info, RenamedFileReference) and file_info.is_changed():
            return self.CHANGED_FOREGROUND_COLOR
        else:
            return None

    def _get_file_tooltip(self, path, problems=None):
        if problems is None:
            problems = []

        filename_html = '<tt>{0}</tt>'.format('/</tt><br><tt>'.join(
            component.replace(' ', '&nbsp;') for component in path.components
        ))

        return filename_html + ('<hr>' + self._get_problems_html(problems) if len(problems) > 0 else '')

    def _get_problems_html(self, problems):
        num_warnings = len([problem for problem in problems if isinstance(problem, Warning)])
        num_errors = len(problems) - num_warnings

        title = format_tally(
            counts=[num_errors, num_warnings],
            names_singular=[self.ERROR_ITEM_NAME, self.WARNING_ITEM_NAME],
            names_plural=[self.ERROR_ITEM_NAME_PLURAL, self.WARNING_ITEM_NAME_PLURAL],
            and_word=None,
            no_count_if_singleton=True,
        )

        if num_errors > 0:
            title_color = self.ERROR_FOREGROUND_COLOR
        elif num_warnings > 0:
            title_color = self.WARNING_FOREGROUND_COLOR
        else:
            return None

        header_html = '<b><font color="{0}">{1}</font></b><br><br>'.format(title_color.name(), title)

        return header_html + '<br>'.join(
            self._get_problem_html(problem, no_heading=(len(problems) == 1))
            for problem in problems
        )

    def _get_problem_html(self, problem, no_heading=False):
        if isinstance(problem, Warning):
            item_color = self.WARNING_FOREGROUND_COLOR
            item_heading = self.WARNING_ITEM_NAME
        else:
            item_color = self.ERROR_FOREGROUND_COLOR
            item_heading = self.ERROR_ITEM_NAME

        if no_heading:
            item_heading = ''
        else:
            item_heading = '- {0}: '.format(item_heading)

        return '<font color="{0}">{1}{2}</font>'.format(item_color.name(), item_heading, str(problem))

    @staticmethod
    def _verify_renamed_files(original_files, renamed_files):
        """Sanity checks the format of the renamed files list"""
        if len(renamed_files) == 0:
            return

        assert len(original_files) == len(renamed_files)

        for original_file, renamed_file in zip(original_files, renamed_files):
            assert renamed_file.old_file_ref == original_file
