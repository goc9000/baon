# logic/parsing/RulesToken.py
#
# (C) Copyright 2012-present  Cristian Dinu <goc9000@gmail.com>
#
# This file is part of BAON.
#
# Licensed under the GPL-3

from logic.parsing.ItemWithPositionInSource import ItemWithPositionInSource


class RulesToken(ItemWithPositionInSource):
    type = None
    text = None
    extras = None

    def __init__(self, lex_token=None, **extras):
        ItemWithPositionInSource.__init__(self)

        if lex_token is not None:
            self.type = lex_token.type
            self.text = lex_token.value
            self.extras = extras if len(extras) > 0 else None

            line, curr_line_start_pos = lex_token.lineno
            start_pos = lex_token.lexpos
            length = len(lex_token.value)

            self.source_start_lineno = line
            self.source_start_colno = 1 + start_pos - curr_line_start_pos
            self.source_start_pos = start_pos
            self.source_end_lineno = self.source_start_lineno
            self.source_end_colno = self.source_start_colno + length - 1
            self.source_end_pos = self.source_start_pos + length - 1

            self.lexpos = lex_token.lexpos
            self.lineno = lex_token.lineno[0]
            self.colno = 1 + lex_token.lexpos - lex_token.lineno[1]


    def __getattribute__(self, item):
        if item == 'value':
            return self
        elif item == 'lineno':
            return self.source_start_lineno
        elif item == 'colno':
            return self.source_start_colno
        elif item == 'start' or item == 'lexpos':
            return self.source_start_pos
        elif item == 'end':
            return self.source_end_pos
        elif item == 'length':
            return 1 + self.source_end_pos - self.source_start_pos

        return ItemWithPositionInSource.__getattribute__(self, item)

    def test_repr(self):
        """The representation of this token in tests"""
        base_tuple = (
            self.start,
            self.type,
            self.text,
            self.lineno,
            self.colno,
        )

        return base_tuple if self.extras is None else base_tuple + (self.extras,)
