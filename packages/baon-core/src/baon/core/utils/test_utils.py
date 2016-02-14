# baon/core/test_utils.py
#
# (C) Copyright 2012-present  Cristian Dinu <goc9000@gmail.com>
#
# This file is part of BAON.
#
# Licensed under the GPL-3


from baon.core.utils.lang_utils import is_string, is_arrayish, is_dictish


def normalize_structure(structure, *scalar_replace_functions):
    def _replace_scalar(value):
        for replace_function in scalar_replace_functions:
            value = replace_function(value)
        return value

    def _replace_rec(value):
        if is_string(value):
            return _replace_scalar(value)
        elif is_arrayish(value):
            return tuple(_replace_rec(subitem) for subitem in value)
        elif is_dictish(value):
            return {key: _replace_rec(value) for key, value in value.items()}
        else:
            return value

    return _replace_rec(structure)
