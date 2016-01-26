# baon/ui/qt4_gui/utils/mk_txt_fmt.py
#
# (C) Copyright 2012-present  Cristian Dinu <goc9000@gmail.com>
# 
# This file is part of BAON.
#
# Licensed under the GPL-3


from PyQt4.QtGui import QTextCharFormat, QFont, QBrush

from baon.ui.qt4_gui.utils.parse_qcolor import parse_qcolor


UNDERLINE_STYLES = {
    'single': QTextCharFormat.SingleUnderline,
    'dash': QTextCharFormat.DashUnderline,
    'dot': QTextCharFormat.DotLine,
    'squiggly': QTextCharFormat.WaveUnderline,
    'spellcheck': QTextCharFormat.SpellCheckUnderline,
}


def mk_txt_fmt(derive=None, fg=None, bg=None, bold=False, ul=None, ul_color=None):
    text_format = QTextCharFormat(derive) if derive is not None else QTextCharFormat()

    if fg is not None:
        text_format.setForeground(QBrush(parse_qcolor(fg)))
    if bg is not None:
        text_format.setBackground(QBrush(parse_qcolor(bg)))

    if bold:
        text_format.setFontWeight(QFont.Bold)

    if ul is not None:
        if ul is True:
            text_format.setUnderlineStyle(QTextCharFormat.SingleUnderline)
        elif ul in UNDERLINE_STYLES:
            text_format.setUnderlineStyle(UNDERLINE_STYLES[ul])
        else:
            raise ValueError("Unsupported underline style: '{0}'".format(ul))

    if ul_color is not None:
        text_format.setUnderlineColor(parse_qcolor(ul_color))

    return text_format
