# baon/core/errors/RuleCheckException.py
#
# (C) Copyright 2012-present  Cristian Dinu <goc9000@gmail.com>
# 
# This file is part of BAON.
#
# Licensed under the GPL-3


from baon.core.errors.ExceptionWithSourceSpan import ExceptionWithSourceSpan


class RuleCheckException(ExceptionWithSourceSpan):
    scope = None
    
    def __init__(self, message, scope=None, source_span=None):
        ExceptionWithSourceSpan.__init__(self, message, source_span)
        self.scope = scope
