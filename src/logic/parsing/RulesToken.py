# logic/parsing/RulesToken.py
#
# (C) Copyright 2012-present  Cristian Dinu <goc9000@gmail.com>
#
# This file is part of BAON.
#
# Licensed under the GPL-3


class RulesToken(object):
    type = None
    text = None
    lexpos = None
    lineno = None
    colno = None
    extras = None

    def __init__(self, lex_token=None, **extras):
        if lex_token is not None:
            self.type = lex_token.type
            self.text = lex_token.value
            self.lexpos = lex_token.lexpos
            self.lineno = lex_token.lineno[0]
            self.colno = 1 + lex_token.lexpos - lex_token.lineno[1]
            self.extras = extras if len(extras) > 0 else None

    def __getattribute__(self, item):
        if item == 'length':
            return len(self.text)
        elif item == 'value':
            return self
        elif item == 'start':
            return self.lexpos
        elif item == 'end':
            return self.lexpos + len(self.text)

        return object.__getattribute__(self, item)

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
