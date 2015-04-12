# baon/ui/qt_gui/utils/parse_qcolor.py
#
# (C) Copyright 2012-present  Cristian Dinu <goc9000@gmail.com>
# 
# This file is part of BAON.
#
# Licensed under the GPL-3


import re

from PyQt4.QtGui import QColor

from baon.core.utils.lang_utils import is_string, is_arrayish, is_dictish


def parse_qcolor(color_spec):
    try:
        if is_string(color_spec):
            return _parse_qcolor_string(color_spec)
        elif is_arrayish(color_spec):
            return _parse_qcolor_arrayish(color_spec)
        elif is_dictish(color_spec):
            return _parse_qcolor_dictish(color_spec)

        raise ValueError('Unsupported format')
    except Exception as e:
        message = 'Invalid QColor spec "{0}" - {1}'.format(color_spec, e)

        raise ValueError(message) from None


def _parse_qcolor_string(color_spec):
    if re.match(r'#?[0-9a-f]{2,}', color_spec):
        return _parse_qcolor_html(color_spec)
    elif QColor.isValidColor(color_spec):
        color = QColor()
        color.setNamedColor(color_spec)
        return color

    raise ValueError('Color name not recognized and not a HTML format')


def _parse_qcolor_html(color_spec):
    digits = color_spec[1:] if color_spec.startswith('#') else color_spec

    if len(digits) not in [6, 8]:
        raise ValueError('Invalid length for HTML format')

    components = [int(digits[i:i+2], 16) for i in range(0, len(digits), 2)]

    return QColor.fromRgb(*components)


def _parse_qcolor_dictish(color_spec):
    found_components = {}

    for component, value in color_spec.items():
        found_role = False
        for role in ['red', 'green', 'blue', 'alpha']:
            if (component.lower() == role) or (component.lower() == role[0]):
                if role in found_components:
                    raise ValueError('Duplicate value for {0}'.format(role))

                found_components[role] = value
                found_role = True
                break

        if not found_role:
            raise ValueError('Invalid component "{0}"'.format(component))

    new_spec = []
    for role in ['red', 'green', 'blue', 'alpha']:
        if role in found_components:
            new_spec.append(found_components[role])
        elif role != 'alpha':
            raise ValueError('Missing value for {0}'.format(role))

    return _parse_qcolor_arrayish(new_spec)


def _parse_qcolor_arrayish(color_spec):
    if len(color_spec) < 3 or len(color_spec) > 4:
        raise ValueError('Expecting an array of length 3 or 4')

    if len(set(type(x) for x in color_spec)) > 1:
        raise ValueError('All components must have the same type')

    comp_type = type(color_spec[0])

    if comp_type == int:
        if not all(0 <= x <= 255 for x in color_spec):
            raise ValueError('Integer components must be in the [0..255] range')

        return QColor.fromRgb(*color_spec)
    elif comp_type == float:
        if not all(0.0 <= x <= 1.0 for x in color_spec):
            raise ValueError('Float components must be in the [0.0..1.0] range')

        return QColor.fromRgbF(*color_spec)

    raise ValueError('Only int and float components are supported')
