# baon/ui/qt_gui/widgets/files_display/FilesDisplaySummaryPanel.py
#
# (C) Copyright 2012-present  Cristian Dinu <goc9000@gmail.com>
#
# This file is part of BAON.
#
# Licensed under the GPL-3


from PyQt4.QtCore import pyqtSignal, pyqtSlot
from PyQt4.QtGui import QHBoxLayout, QLabel, QWidget

from baon.ui.qt_gui.utils.parse_qcolor import parse_qcolor
from baon.ui.qt_gui.mixins.SetupTabStopsMixin import SetupTabStopsMixin


class FilesDisplaySummaryPanel(QWidget, SetupTabStopsMixin):
    NO_ITEMS_TEXT = ''
    ITEM_TEXT = '{0} item'
    ITEM_TEXT_PLURAL = '{0} items'
    SCAN_ERROR_TEXT = '{0} has a scan error'
    SCAN_ERROR_TEXT_PLURAL = '{0} have scan errors'
    SCAN_WARNING_TEXT = '{0} has a scan warning'
    SCAN_WARNING_TEXT_PLURAL = '{0} have scan warnings'
    RENAME_ERROR_TEXT = '{0} has a rename error'
    RENAME_ERROR_TEXT_PLURAL = '{0} have rename errors'
    RENAME_WARNING_TEXT = '{0} has a rename warning'
    RENAME_WARNING_TEXT_PLURAL = '{0} have rename warnings'
    CHANGED_TEXT = '{0} changed'
    CHANGED_TEXT_PLURAL = '{0} changed'
    OVERRIDE_TEXT = '{0} override'
    OVERRIDE_TEXT_PLURAL = '{0} overrides'

    PREVIOUS_LINK_TEXT = 'Prev'
    NEXT_LINK_TEXT = 'Next'

    ERROR_COLOR = parse_qcolor('#ff0000')
    WARNING_COLOR = parse_qcolor('#d0b000')
    CHANGED_COLOR = parse_qcolor('#0040e0')
    OVERRIDE_COLOR = parse_qcolor('#000000')

    CATEGORY_RENDERING = [
        {
            'category': 'all',
            'text': ITEM_TEXT,
            'text_plural': ITEM_TEXT_PLURAL,
            'show_link': False,
        },
        {
            'category': 'scan_errors',
            'text': SCAN_ERROR_TEXT,
            'text_plural': SCAN_ERROR_TEXT_PLURAL,
            'style': {
                'color': ERROR_COLOR.name(),
            },
        },
        {
            'category': 'scan_warnings',
            'text': SCAN_WARNING_TEXT,
            'text_plural': SCAN_WARNING_TEXT_PLURAL,
            'style': {
                'color': WARNING_COLOR.name(),
            },
        },
        {
            'category': 'rename_errors',
            'text': RENAME_ERROR_TEXT,
            'text_plural': RENAME_ERROR_TEXT_PLURAL,
            'style': {
                'color': ERROR_COLOR.name(),
            },
        },
        {
            'category': 'rename_warnings',
            'text': RENAME_WARNING_TEXT,
            'text_plural': RENAME_WARNING_TEXT_PLURAL,
            'style': {
                'color': WARNING_COLOR.name(),
            },
        },
        {
            'category': 'changed',
            'text': CHANGED_TEXT,
            'text_plural': CHANGED_TEXT_PLURAL,
            'style': {
                'color': CHANGED_COLOR.name(),
            },
        },
        {
            'category': 'overrides',
            'text': OVERRIDE_TEXT,
            'text_plural': OVERRIDE_TEXT_PLURAL,
            'style': {
                'color': OVERRIDE_COLOR.name(),
                'font-weight': 'bold',
            },
        },
    ]

    start_browsing_category = pyqtSignal(str)
    prev_in_category = pyqtSignal()
    next_in_category = pyqtSignal()

    _counts = None
    _is_browsing_category = False
    _has_prev_in_category = False
    _has_next_in_category = False

    def __init__(self, parent):
        super().__init__(parent)

        self._counts = {}

        self._summary_label = QLabel('', self)
        self._summary_label.linkActivated.connect(self._on_category_link_clicked)

        self._prev_next_label = QLabel('', self)
        self._prev_next_label.linkActivated.connect(self._on_prev_next_link_clicked)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self._summary_label)
        layout.addStretch()
        layout.addWidget(self._prev_next_label)

        self.setFocusProxy(self._summary_label)

        self._setup_tab_stops(
            self._summary_label,
            self._prev_next_label,
        )

        self._update_summary_label()
        self._update_prev_next_label()

    @pyqtSlot(dict)
    def set_counts(self, counts):
        self._counts = counts.copy()
        self._update_summary_label()

    @pyqtSlot(bool)
    def set_is_browsing_category(self, value):
        self._is_browsing_category = value
        self._update_prev_next_label()

    @pyqtSlot(bool)
    def set_has_prev_in_category(self, value):
        self._has_prev_in_category = value
        self._update_prev_next_label()

    @pyqtSlot(bool)
    def set_has_next_in_category(self, value):
        self._has_next_in_category = value
        self._update_prev_next_label()

    def _update_summary_label(self):
        parts = []

        for category_setup in self.CATEGORY_RENDERING:
            item_count = self._counts.get(category_setup['category'], 0)
            if item_count == 0:
                continue

            part_html = category_setup['text' if item_count == 1 else 'text_plural'].format(item_count)

            if category_setup.get('show_link', True):
                style = '; '.join("{0}: {1}".format(k, v) for k, v in category_setup.get('style', {}).items())

                part_html = '<a href="#{0}" style="{1}">{2}</a>'.format(category_setup['category'], style, part_html)

            parts.append(part_html)

        if len(parts) == 0:
            parts.append(self.NO_ITEMS_TEXT)

        self._summary_label.setText(', '.join(parts))

    def _update_prev_next_label(self):
        parts = []

        if self._is_browsing_category and (self._has_prev_in_category or self._has_next_in_category):
            part_html = self.PREVIOUS_LINK_TEXT
            if self._has_prev_in_category:
                part_html = '<a href="#prev">{0}</a>'.format(part_html)
            parts.append(part_html)

            part_html = self.NEXT_LINK_TEXT
            if self._has_next_in_category:
                part_html = '<a href="#next">{0}</a>'.format(part_html)
            parts.append(part_html)

        self._prev_next_label.setText(' / '.join(parts))

    @pyqtSlot(str)
    def _on_category_link_clicked(self, url):
        self.start_browsing_category.emit(url[1:])

    @pyqtSlot(str)
    def _on_prev_next_link_clicked(self, url):
        if url == '#prev':
            self.prev_in_category.emit()
        elif url == '#next':
            self.next_in_category.emit()
