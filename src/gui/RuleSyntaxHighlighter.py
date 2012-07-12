from PyQt4.QtGui import QSyntaxHighlighter, QTextCharFormat, QFont, QBrush, QColor

import antlr3, string

from genparsers.RulesLexer import *

FMT_LITERAL = QTextCharFormat()
FMT_LITERAL.setBackground(QBrush(QColor(232,232,240)))
FMT_LITERAL.setForeground(QBrush(QColor(0,0,240)))

FMT_PATTERN = QTextCharFormat()
FMT_PATTERN.setForeground(QBrush(QColor(0,174,0)))

FMT_BETWEEN = QTextCharFormat()
FMT_BETWEEN.setForeground(QBrush(QColor(0,174,0)))
FMT_BETWEEN.setFontWeight(QFont.Bold)

FMT_OP = QTextCharFormat()

FMT_PARA = QTextCharFormat()
FMT_PARA.setFontWeight(QFont.Bold)

FMT_ID = QTextCharFormat()
FMT_ID.setForeground(QBrush(QColor(96,96,128)))
FMT_ID.setFontWeight(QFont.Bold)

FORMAT_DICT = {
    STRING_LITERAL: FMT_LITERAL,
    
    FORMAT_SPEC: FMT_PATTERN,
    REGEX: FMT_PATTERN,
    ANCHOR_START: FMT_PATTERN,
    ANCHOR_END: FMT_PATTERN,
    OP_BETWEEN: FMT_BETWEEN,
    
    ID: FMT_ID,
    
    OP_OR: FMT_OP,
    OP_XFORM: FMT_OP,
    OP_INSERT: FMT_OP,
    OP_DELETE: FMT_OP,
    OP_SEARCH: FMT_OP,
    OP_SAVE: FMT_OP,
    OP_PLUS: FMT_OP,
    OP_STAR: FMT_OP,
    OP_OPTIONAL: FMT_OP,
    RULE_SEP: FMT_OP,
    
    OP_OPEN_PARA: FMT_PARA,
    OP_CLOSE_PARA: FMT_PARA
}

class RuleSyntaxHighlighter(QSyntaxHighlighter):
    _lexer = None
    _err_line = None
    _err_col = None
    
    def __init__(self, document):
        QSyntaxHighlighter.__init__(self, document)
        self._lexer = RulesLexer()
        self._lexer.lenient = True
    
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
        tokens = self.tokenizeText(text)
            
        for tok in tokens:
            fmt = None
            if tok.type in FORMAT_DICT:
                fmt = FORMAT_DICT[tok.type]

            if fmt is not None:
                self.setFormat(tok.start, 1 + tok.stop - tok.start, fmt)
        
        if self._err_line is not None:
            if self.currentBlock().firstLineNumber() == self._err_line:
                self.markErrorAtChar(self._err_col, text, tokens)

    def markErrorAtChar(self, char, text, tokens):
        token_starts = set([tok.start for tok in tokens])
        token_ends = set([tok.stop for tok in tokens])
        
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
            fmt = self.format(col)
            fmt.setForeground(QBrush(QColor(255,0,0)))
            fmt.setFontWeight(QFont.Bold)
            fmt.setUnderlineColor(QColor(255,0,0))
            fmt.setUnderlineStyle(QTextCharFormat.SpellCheckUnderline)
            self.setFormat(col, 1, fmt)
    
    def tokenizeText(self, text):
        tokens = []
        
        try:
            chrStream = antlr3.ANTLRStringStream(text)
            self._lexer.setCharStream(chrStream)
            self._lexer.errors = []
            
            while True:
                tok = self._lexer.nextToken()
                if tok.channel != antlr3.DEFAULT_CHANNEL:
                    continue
                if tok.type == antlr3.EOF:
                    break
                tokens.append(tok)
        except:
            pass
        
        return tokens
