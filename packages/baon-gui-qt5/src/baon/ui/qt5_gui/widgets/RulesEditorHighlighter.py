# baon/ui/qt5_gui/widgets/RulesEditorHighlighter.py
#
# (C) Copyright 2012-present  Cristian Dinu <goc9000@gmail.com>
# 
# This file is part of BAON.
#
# Licensed under the GPL-3


from collections import defaultdict

from PyQt5.QtGui import QSyntaxHighlighter

from baon.core.parsing.SourceSpan import SourceSpan
from baon.core.parsing.tokenize_rules import tokenize_rules
from baon.core.utils.math_utils import clamp
from baon.ui.qt5_gui.utils.mk_txt_fmt import mk_txt_fmt


class RulesEditorHighlighter(QSyntaxHighlighter):
    LITERAL_FORMAT = {'fg': '#0000f0', 'bg': '#e8e8f0'}
    PATTERN_FORMAT = {'fg': '#00ae00'}
    BETWEEN_FORMAT = {'fg': '#00ae00', 'bold': True}
    OPERATOR_FORMAT = {}
    PARA_FORMAT = {'bold': True}
    ID_FORMAT = {'fg': '#606080', 'bold': True}
    ERROR_FORMAT = {'fg': '#ff0000', 'ul': 'spellcheck', 'ul_color': '#ff0000'}

    _FORMAT_DICT = {
        'STRING_LITERAL': LITERAL_FORMAT,

        'FORMAT_SPEC': PATTERN_FORMAT,
        'REGEX': PATTERN_FORMAT,
        'ANCHOR_START': PATTERN_FORMAT,
        'ANCHOR_END': PATTERN_FORMAT,
        'BETWEEN': BETWEEN_FORMAT,

        'ID': ID_FORMAT,

        'OP_OR': OPERATOR_FORMAT,
        'OP_XFORM': OPERATOR_FORMAT,
        'OP_INSERT': OPERATOR_FORMAT,
        'OP_DELETE': OPERATOR_FORMAT,
        'OP_SEARCH': OPERATOR_FORMAT,
        'OP_SAVE': OPERATOR_FORMAT,
        'OP_REPEAT': OPERATOR_FORMAT,
        'RULE_SEP': OPERATOR_FORMAT,

        'PARA_OPEN': PARA_FORMAT,
        'PARA_CLOSE': PARA_FORMAT,

        'error': ERROR_FORMAT,
    }

    _error_span = None

    def __init__(self, document):
        QSyntaxHighlighter.__init__(self, document)

    def set_error_span(self, error_span):
        self._error_span = error_span
        self.rehighlight()

    def highlightBlock(self, text):
        self._apply_highlight_events(self._get_highlight_events(text))

    def _apply_highlight_events(self, events):
        current_format = None
        error_on = False
        last_cursor = 0

        for cursor in sorted(events.keys()):
            if cursor > last_cursor:
                format = current_format
                if error_on:
                    format = format.copy() if format is not None else {}
                    format.update(self.ERROR_FORMAT)

                if format is not None:
                    self.setFormat(last_cursor, cursor - last_cursor, mk_txt_fmt(**format))

            events_here = events[cursor]
            if 'format' in events_here:
                current_format = events_here['format']
            if 'error' in events_here:
                error_on = events_here['error']

            last_cursor = cursor

    def _get_highlight_events(self, text):
        events = defaultdict(dict)

        for token in tokenize_rules(text):
            format = self._FORMAT_DICT.get(token.type)
            if format is not None:
                events[token.source_span.start_pos]['format'] = format
                events[token.source_span.end_pos + 1]['format'] = None

        error_span = self._get_block_level_adjusted_error_span()
        if error_span is not None:
            events[error_span.start_pos]['error'] = True
            events[error_span.end_pos + 1]['error'] = False

        events[len(text)]['format'] = None
        events[len(text)]['error'] = False

        return events

    def _get_document_level_adjusted_error_span(self):
        if self._error_span is None:
            return None

        source = self.document().toPlainText() + "\n"
        start = clamp(self._error_span.start_pos, 0, len(source) - 1)
        end = clamp(self._error_span.end_pos, start, len(source) - 1)

        # An error that occurs between two tokens will be extended backwards until it touches the last character in
        # the first token; this is so that we can be sure it shows up in the highlighter
        while start > 0 and str.isspace(source[start]):
            start -= 1

        while end > start and source[end] == "\n":
            end -= 1

        return SourceSpan.from_start_end(start, end, source)

    def _get_block_level_adjusted_error_span(self):
        block_start = self.currentBlock().position()
        block_end = self.currentBlock().position() + self.currentBlock().length() - 2
        if block_start > block_end:
            return None

        error_span = self._get_document_level_adjusted_error_span()
        if error_span is None:
            return None

        start = clamp(error_span.start_pos, block_start, block_end + 1) - block_start
        end = clamp(error_span.end_pos, block_start - 1, block_end) - block_start
        if start > end:
            return None

        return SourceSpan.from_start_end(start, end, self.currentBlock().text())
