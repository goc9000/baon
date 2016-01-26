# baon/ui/qt4_gui/widgets/RulesEditor.py
#
# (C) Copyright 2012-present  Cristian Dinu <goc9000@gmail.com>
# 
# This file is part of BAON.
#
# Licensed under the GPL-3


from PyQt4.QtCore import QTimer, pyqtSignal, pyqtSlot
from PyQt4.QtGui import QFont, QTextEdit

from baon.ui.qt4_gui.widgets.RulesEditorHighlighter import RulesEditorHighlighter


class RulesEditor(QTextEdit):
    QUIESCENCE_TIME_MSEC = 1000

    rules_edited = pyqtSignal(str)

    _highlighter = None

    _quiescence_timer = None
    _last_emitted_text = ''
    _performing_programmatic_change = False

    def __init__(self, parent):
        super().__init__(parent)

        mono_font = QFont()
        mono_font.setFixedPitch(True)

        self.setFont(mono_font)
        self.setAcceptRichText(False)
        self.setTabChangesFocus(True)

        self._highlighter = RulesEditorHighlighter(self.document())

        self._quiescence_timer = QTimer(self)
        self._quiescence_timer.setSingleShot(True)
        self._quiescence_timer.setInterval(self.QUIESCENCE_TIME_MSEC)
        self._quiescence_timer.timeout.connect(self._on_quiescence_timer_timeout)

        self.document().contentsChanged.connect(self._on_contents_changed)

    def rules(self):
        return self.document().toPlainText()

    @pyqtSlot()
    def set_rules(self, rules_text):
        self._quiescence_timer.stop()
        self._last_emitted_text = rules_text
        self.document().setPlainText(rules_text)
        self.clear_error()

    @pyqtSlot()
    def show_error(self, error_span):
        self._performing_programmatic_change = True
        self._highlighter.set_error_span(error_span)
        self._performing_programmatic_change = False

    @pyqtSlot()
    def clear_error(self):
        self._performing_programmatic_change = True
        self._highlighter.set_error_span(None)
        self._performing_programmatic_change = False

    def setDocument(self, document):
        assert False, 'setDocument() should not be called directly on the rules editor'

    def focusOutEvent(self, event):
        self._quiescence_timer.stop()
        self._maybe_emit_rules_edited()
        super().focusOutEvent(event)

    @pyqtSlot()
    def _on_contents_changed(self):
        if self._performing_programmatic_change:
            return

        self._quiescence_timer.start()
        self.clear_error()

    @pyqtSlot()
    def _on_quiescence_timer_timeout(self):
        self._maybe_emit_rules_edited()

    def _maybe_emit_rules_edited(self):
        if self.rules() != self._last_emitted_text:
            self._last_emitted_text = self.rules()
            self.rules_edited.emit(self.rules())
