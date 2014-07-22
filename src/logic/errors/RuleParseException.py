# logic/errors/RuleParseException.py
#
# (C) Copyright 2012  Cristian Dinu <goc9000@gmail.com>
# 
# This file is part of BAON.
#
# Licensed under the GPL-3

from logic.parsing.ItemWithPositionInSource import ItemWithPositionInSource


class RuleParseException(Exception, ItemWithPositionInSource):
    def __init__(self, message):
        Exception.__init__(self, message)

    def __str__(self):
        return self.message

    def test_repr(self):
        return (
            'PARSE_EXCEPTION',
            self.message,
            self.source_start_lineno,
            self.source_start_colno,
            self.source_end_lineno,
            self.source_end_colno,
        )

    @staticmethod
    def from_token(token, message):
        exception = RuleParseException(message)
        exception.set_span_from_item(token)
        return exception
