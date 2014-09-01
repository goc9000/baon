# baon/logic/parsing/RulesToken.py
#
# (C) Copyright 2012-present  Cristian Dinu <goc9000@gmail.com>
#
# This file is part of BAON.
#
# Licensed under the GPL-3


from baon.logic.parsing.SourceSpan import SourceSpan


class RulesToken(object):
    type = None
    text = None
    extras = None
    source_span = None

    def __init__(self, lex_token=None, **extras):
        if lex_token is not None:
            self.type = lex_token.type
            self.text = lex_token.value
            self.extras = extras if len(extras) > 0 else None

            line, curr_line_start_pos = lex_token.lineno
            start_pos = lex_token.lexpos
            column = 1 + start_pos - curr_line_start_pos
            length = len(lex_token.value)

            self.source_span = SourceSpan(
                start_pos,
                start_pos + length - 1,
                line,
                column,
                line,
                column + length - 1,
            )

    def __getattribute__(self, item):
        if item == 'value':
            return self
        elif item == 'lineno':
            return self.source_span.start_line
        elif item == 'lexpos':
            return self.source_span.start_pos

        return object.__getattribute__(self, item)

    def test_repr(self):
        """The representation of this token in tests"""
        base_tuple = (
            self.lexpos,
            self.type,
            self.text,
        )

        if self.source_span is not None:
            base_tuple += (self.source_span.start_line, self.source_span.start_column)

        return base_tuple if self.extras is None else base_tuple + (self.extras,)
