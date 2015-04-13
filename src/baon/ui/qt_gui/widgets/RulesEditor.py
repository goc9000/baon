# baon/ui/qt_gui/widgets/RulesEditor.py
#
# (C) Copyright 2012-present  Cristian Dinu <goc9000@gmail.com>
# 
# This file is part of BAON.
#
# Licensed under the GPL-3


from PyQt4.QtGui import QFont, QTextEdit

from baon.ui.qt_gui.widgets.RulesEditorHighlighter import RulesEditorHighlighter


class RulesEditor(QTextEdit):
    _highlighter = None

    def __init__(self, parent):
        super().__init__(parent)

        mono_font = QFont()
        mono_font.setFixedPitch(True)

        self.setFont(mono_font)
        self.setAcceptRichText(False)

        self._highlighter = RulesEditorHighlighter(self.document())

    def setDocument(self, document):
        super().setDocument(document)
        self._highlighter.setDocument(document)

    def show_error(self, error_span):
        self._highlighter.set_error_span(error_span)

    def clear_error(self):
        self._highlighter.set_error_span(None)
