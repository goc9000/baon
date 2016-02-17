# baon/core/baon_utils.py
#
# (C) Copyright 2012-present  Cristian Dinu <goc9000@gmail.com>
# 
# This file is part of BAON.
#
# Licensed under the GPL-3


from baon.core.files.BAONPath import BAONPath
from baon.core.parsing.__errors__.rule_parse_errors import StringLiteralNotQuotedProperlyError
from baon.core.utils.str_utils import is_quoted_string


def decode_baon_string_literal(literal):
    if not is_quoted_string(literal):
        raise StringLiteralNotQuotedProperlyError()

    return literal[1:-1].replace(literal[0] * 2, literal[0])


def convert_raw_overrides(raw_overrides, base_path):
    """Converts a dict of str->str to a dict of BAONPath->BAONPath"""

    return {
        BAONPath.from_path_text(base_path, path_from): BAONPath.from_path_text(base_path, path_to)
        for path_from, path_to in raw_overrides.items()
    }
