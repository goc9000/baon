# baon/gui/qt_utils.py
#
# (C) Copyright 2012-present  Cristian Dinu <goc9000@gmail.com>
# 
# This file is part of BAON.
#
# Licensed under the GPL-3


import re

from PyQt4.QtGui import QTextCharFormat, QFont, QBrush, QColor

from baon.core.utils.lang_utils import is_string, is_arrayish, is_dictish


def qstr_to_unicode(qstring):
    return unicode(qstring.toUtf8(), 'utf-8')


def parse_qcolor(color_spec):
    try:
        if is_string(color_spec):
            return _parse_qcolor_string(color_spec)
        elif is_arrayish(color_spec):
            return _parse_qcolor_arrayish(color_spec)
        elif is_dictish(color_spec):
            return _parse_qcolor_dictish(color_spec)

        raise RuntimeError('Unsupported format')
    except Exception as e:
        message = 'Invalid QColor spec "{0}"'.format(color_spec)
        if e.message != '':
            message += ' - ' + e.message

        raise RuntimeError(message)


def _parse_qcolor_string(color_spec):
    if re.match(r'#?[0-9a-f]{2,}', color_spec):
        return _parse_qcolor_html(color_spec)
    elif QColor.isValidColor(color_spec):
        color = QColor()
        color.setNamedColor(color_spec)
        return color

    raise RuntimeError('Color name not recognized and not a HTML format')


def _parse_qcolor_html(color_spec):
    digits = color_spec[1:] if color_spec.startswith('#') else color_spec

    if len(digits) not in [6, 8]:
        raise RuntimeError('Invalid length for HTML format')

    components = [int(digits[i:i+2], 16) for i in xrange(0, len(digits), 2)]

    return QColor.fromRgb(*components)


def _parse_qcolor_dictish(color_spec):
    found_components = {}

    for component, value in color_spec.items():
        found_role = False
        for role in ['red', 'green', 'blue', 'alpha']:
            if (component.lower() == role) or (component.lower() == role[0]):
                if role in found_components:
                    raise RuntimeError('Duplicate value for {0}'.format(role))

                found_components[role] = value
                found_role = True
                break

        if not found_role:
            raise RuntimeError('Invalid component "{0}"'.format(component))

    new_spec = []
    for role in ['red', 'green', 'blue', 'alpha']:
        if role in found_components:
            new_spec.append(found_components[role])
        elif role != 'alpha':
            raise RuntimeError('Missing value for {0}'.format(role))

    return _parse_qcolor_arrayish(new_spec)


def _parse_qcolor_arrayish(color_spec):
    if len(color_spec) < 3 or len(color_spec) > 4:
        raise RuntimeError('Expecting an array of length 3 or 4')

    if len(set(type(x) for x in color_spec)) > 1:
        raise RuntimeError('All components must have the same type')

    comp_type = type(color_spec[0])

    if comp_type == int:
        if not all(0 <= x <= 255 for x in color_spec):
            raise RuntimeError('Integer components must be in the [0..255] range')

        return QColor.fromRgb(*color_spec)
    elif comp_type == float:
        if not all(0.0 <= x <= 1.0 for x in color_spec):
            raise RuntimeError('Float components must be in the [0.0..1.0] range')

        return QColor.fromRgbF(*color_spec)

    raise RuntimeError('Only int and float components are supported')


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
            raise RuntimeError("Unsupported underline style: '{0}'".format(ul))

    if ul_color is not None:
        text_format.setUnderlineColor(parse_qcolor(ul_color))

    return text_format
