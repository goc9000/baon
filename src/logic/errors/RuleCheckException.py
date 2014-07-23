# logic/errors/RuleCheckException.py
#
# (C) Copyright 2012  Cristian Dinu <goc9000@gmail.com>
# 
# This file is part of BAON.
#
# Licensed under the GPL-3

from logic.parsing.ItemWithPositionInSource import ItemWithPositionInSource


class RuleCheckException(Exception, ItemWithPositionInSource):
    scope = None
    
    def __init__(self, message, scope=None):
        Exception.__init__(self, message)
        self.scope = scope
    
    def __str__(self):
        return self.message

    def test_repr(self):
        return (
            self.__class__.__name__,
            self.message,
            self.source_start_lineno,
            self.source_start_colno,
            self.source_end_lineno,
            self.source_end_colno,
        )

    @staticmethod
    def from_node(node, message, scope=None):
        exception = RuleCheckException(message, scope)
        exception.set_span_from_item(node)
        return exception
