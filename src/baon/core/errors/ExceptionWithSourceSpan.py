# baon/core/errors/ExceptionWithSourceSpan.py
#
# (C) Copyright 2012-present  Cristian Dinu <goc9000@gmail.com>
# 
# This file is part of BAON.
#
# Licensed under the GPL-3


from baon.core.errors.BAONExceptionBase import BAONExceptionBase
from baon.core.parsing.SourceSpan import SourceSpan


class ExceptionWithSourceSpan(BAONExceptionBase):
    source_span = None

    def __init__(self, format_string, error_parameters, source_span=None):
        BAONExceptionBase.__init__(self, format_string, error_parameters)
        self.source_span = SourceSpan.copy(source_span)

    def test_repr(self):
        base_tuple = BAONExceptionBase.test_repr(self)

        if self.source_span is not None:
            base_tuple += (
                self.source_span.start_line,
                self.source_span.start_column,
                self.source_span.end_line,
                self.source_span.end_column,
            )

        return base_tuple
