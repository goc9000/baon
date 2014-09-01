# baon/logic/math_utils.py
#
# (C) Copyright 2012-present  Cristian Dinu <goc9000@gmail.com>
#
# This file is part of BAON.
#
# Licensed under the GPL-3


def clamp(value, minimum, maximum):
    if value is None:
        return None
    if minimum is not None and value < minimum:
        return minimum
    if maximum is not None and value > maximum:
        return maximum

    return value
