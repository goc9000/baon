# gui/RuleSyntaxHighlighter.py
#
# (C) Copyright 2012  Cristian Dinu <goc9000@gmail.com>
# 
# This file is part of BAON.
#
# Licensed under the GPL-3


from PyQt4.QtGui import QSyntaxHighlighter

from gui.qt_utils import mk_txt_fmt, qstr_to_unicode

from logic.parsing.RulesLexer import RulesLexer
from logic.parsing.SourceSpan import SourceSpan

from logic.math_utils import clamp


FMT_LITERAL = mk_txt_fmt(fg=(0, 0, 240), bg=(232, 232, 240))
FMT_PATTERN = mk_txt_fmt(fg=(0, 174, 0))
FMT_BETWEEN = mk_txt_fmt(fg=(0, 174, 0), bold=True)
FMT_OP = mk_txt_fmt()
FMT_PARA = mk_txt_fmt(bold=True)
FMT_ID = mk_txt_fmt(fg=(96, 96, 128), bold=True)
FMT_ERROR_SPEC = {'fg': (255, 0, 0), 'ul': 'spellcheck', 'ul_color': (255, 0, 0)}


FORMAT_DICT = {
    'STRING_LITERAL': FMT_LITERAL,
    
    'FORMAT_SPEC': FMT_PATTERN,
    'REGEX': FMT_PATTERN,
    'ANCHOR_START': FMT_PATTERN,
    'ANCHOR_END': FMT_PATTERN,
    'BETWEEN': FMT_BETWEEN,
    
    'ID': FMT_ID,
    
    'OP_OR': FMT_OP,
    'OP_XFORM': FMT_OP,
    'OP_INSERT': FMT_OP,
    'OP_DELETE': FMT_OP,
    'OP_SEARCH': FMT_OP,
    'OP_SAVE': FMT_OP,
    'OP_REPEAT': FMT_OP,
    'RULE_SEP': FMT_OP,
    
    'PARA_OPEN': FMT_PARA,
    'PARA_CLOSE': FMT_PARA,
}


class RuleSyntaxHighlighter(QSyntaxHighlighter):
    _error_span = None
    
    def __init__(self, document):
        QSyntaxHighlighter.__init__(self, document)
    
    def show_error(self, error_span):
        self._error_span = self._adjust_error_span(error_span)
        self.rehighlight()
    
    def clear_error(self):
        if self._error_span is not None:
            self.show_error(None)

    def highlightBlock(self, text):
        text = qstr_to_unicode(text)

        tokens = list(RulesLexer.tokenize(text))
        for token in tokens:
            fmt = None
            if token.type in FORMAT_DICT:
                fmt = FORMAT_DICT[token.type]

            if fmt is not None:
                self.setFormat(
                    token.source_span.start_pos,
                    token.source_span.length,
                    fmt,
                )

        if self._error_span is not None:
            start = clamp(self._error_span.start_pos - self.currentBlock().position(), 0, len(text))
            end = clamp(self._error_span.end_pos - self.currentBlock().position(), -1, len(text) - 1)

            for pos in xrange(start, end + 1):
                self.setFormat(pos, 1, mk_txt_fmt(derive=self.format(pos), **FMT_ERROR_SPEC))

    def _adjust_error_span(self, error_span):
        if error_span is None:
            return None

        source = qstr_to_unicode(self.document().toPlainText()) + u"\n"
        start = clamp(error_span.start_pos, 0, len(source) - 1)
        end = clamp(error_span.end_pos, start, len(source) - 1)

        while start > 0 and unicode.isspace(source[start]):
            start -= 1
        while end > start and source[end] == u"\n":
            end -= 1

        return SourceSpan.from_start_end(start, end, source)

