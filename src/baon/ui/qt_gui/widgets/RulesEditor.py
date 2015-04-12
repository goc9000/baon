# baon/ui/qt_gui/widgets/RulesEditor.py
#
# (C) Copyright 2012-present  Cristian Dinu <goc9000@gmail.com>
# 
# This file is part of BAON.
#
# Licensed under the GPL-3


from PyQt4.QtGui import QFont, QTextEdit


class RulesEditor(QTextEdit):
    def __init__(self, parent):
        super().__init__(parent)

        mono_font = QFont()
        mono_font.setFixedPitch(True)

        self.setFont(mono_font)
        self.setAcceptRichText(False)
