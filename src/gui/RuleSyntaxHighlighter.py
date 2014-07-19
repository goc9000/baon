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


FMT_LITERAL = mk_txt_fmt(fg=(0, 0, 240), bg=(232, 232, 240))
FMT_PATTERN = mk_txt_fmt(fg=(0, 174, 0))
FMT_BETWEEN = mk_txt_fmt(fg=(0, 174, 0), bold=True)
FMT_OP = mk_txt_fmt()
FMT_PARA = mk_txt_fmt(bold=True)
FMT_ID = mk_txt_fmt(fg=(96, 96, 128), bold=True)
FMT_ERROR = mk_txt_fmt(fg=(255, 0, 0), bold=True, ul='spellcheck', ul_color=(255, 0, 0))


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
    _lexer = None
    _err_line = None
    _err_col = None
    
    def __init__(self, document):
        QSyntaxHighlighter.__init__(self, document)
    
    def showError(self, line, col):
        self._err_line = line
        self._err_col = col
        self.rehighlight()
    
    def clearError(self):
        if self._err_line is not None:
            self._err_line = None
            self._err_col = None
            self.rehighlight()
    
    def highlightBlock(self, text):
        text = qstr_to_unicode(text)

        tokens = list(RulesLexer.tokenize(text))
        for token in tokens:
            fmt = None
            if token.type in FORMAT_DICT:
                fmt = FORMAT_DICT[token.type]

            if fmt is not None:
                self.setFormat(token.start, token.length, fmt)
        
        if self._err_line is not None:
            if self.currentBlock().firstLineNumber() == self._err_line:
                self.markErrorAtChar(self._err_col, text, tokens)

    def markErrorAtChar(self, char, text, tokens):
        token_starts = set([tok.start for tok in tokens])
        token_ends = set([tok.end for tok in tokens])
        
        if len(text) == 0:
            return
        if char == len(text):
            char = len(text)-1
        
        char_from = char
        while char_from > 0:
            if char_from in token_starts:
                break
            if char_from-1 in token_ends:
                break
            char_from -= 1
        
        char_to = char
        while char_to < len(text)-1:
            if char_to in token_ends:
                break
            if char_to+1 in token_starts:
                break
            char_to += 1
        
        for col in xrange(char_from, char_to+1):
            self.setFormat(col, 1, FMT_ERROR)
