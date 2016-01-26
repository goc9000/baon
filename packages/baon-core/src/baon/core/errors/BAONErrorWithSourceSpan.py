# baon/core/errors/BAONErrorWithSourceSpan.py
#
# (C) Copyright 2012-present  Cristian Dinu <goc9000@gmail.com>
# 
# This file is part of BAON.
#
# Licensed under the GPL-3


from abc import ABCMeta

from baon.core.errors.BAONError import BAONError
from baon.core.parsing.SourceSpan import SourceSpan


class BAONErrorWithSourceSpan(BAONError, metaclass=ABCMeta):
    source_span = None

    def __init__(self, source_span=None, **error_parameters):
        super().__init__(**error_parameters)
        self.source_span = SourceSpan.copy(source_span)

    def test_repr(self):
        base_tuple = super().test_repr()

        if self.source_span is not None:
            base_tuple += (
                self.source_span.start_line,
                self.source_span.start_column,
                self.source_span.end_line,
                self.source_span.end_column,
            )

        return base_tuple
