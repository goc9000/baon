# baon/core/errors/RuleCheckException.py
#
# (C) Copyright 2012  Cristian Dinu <goc9000@gmail.com>
# 
# This file is part of BAON.
#
# Licensed under the GPL-3


from baon.core.parsing.SourceSpan import SourceSpan


class RuleCheckException(Exception):
    scope = None
    source_span = None
    
    def __init__(self, message, scope=None, source_span=None):
        Exception.__init__(self, message)
        self.scope = scope
        self.source_span = SourceSpan.copy(source_span)
    
    def __str__(self):
        return self.message

    def test_repr(self):
        base_tuple = (self.__class__.__name__, self.message)

        if self.source_span is not None:
            base_tuple += (
                self.source_span.start_line,
                self.source_span.start_column,
                self.source_span.end_line,
                self.source_span.end_column,
            )

        return base_tuple
