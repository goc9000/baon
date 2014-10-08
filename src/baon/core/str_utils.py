# baon/core/str_utils.py
#
# (C) Copyright 2012-present  Cristian Dinu <goc9000@gmail.com>
#
# This file is part of BAON.
#
# Licensed under the GPL-3


def is_quoted_string(s):
    return (len(s) >= 2) and (s[0] == s[-1]) and (s[0] in ['"', "'"])
