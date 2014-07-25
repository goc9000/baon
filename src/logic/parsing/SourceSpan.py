# logic/parsing/SourceSpan.py
#
# (C) Copyright 2012-present  Cristian Dinu <goc9000@gmail.com>
#
# This file is part of BAON.
#
# Licensed under the GPL-3


def compute_line_col(pos, text):
    line_no = 1
    line_start_pos = 0

    for line in text.split(u"\n"):
        line_end_pos = line_start_pos + len(line)

        if pos <= line_end_pos:
            return line_no, 1 + pos - line_start_pos

        line_no += 1
        line_start_pos = line_end_pos + 1

    return line_no - 1, line_start_pos - 1


class SourceSpan(object):
    start_pos = None
    end_pos = None
    start_line = None
    start_column = None
    end_line = None
    end_column = None

    def __init__(self, start_pos, end_pos, start_line, start_column, end_line, end_column):
        self.start_pos = start_pos
        self.end_pos = end_pos
        self.start_line = start_line
        self.start_column = start_column
        self.end_line = end_line
        self.end_column = end_column

    def __getattribute__(self, item):
        if item == 'length':
            return self.end_pos - self.start_pos + 1
        else:
            return object.__getattribute__(self, item)

    @staticmethod
    def copy(other):
        if other is None:
            return None

        return SourceSpan(
            other.start_pos,
            other.end_pos,
            other.start_line,
            other.start_column,
            other.end_line,
            other.end_column,
        )

    @staticmethod
    def from_to(from_span, to_span):
        return SourceSpan(
            from_span.start_pos if from_span is not None else None,
            to_span.end_pos if to_span is not None else None,
            from_span.start_line if from_span is not None else None,
            from_span.start_column if from_span is not None else None,
            to_span.end_line if to_span is not None else None,
            to_span.end_column if to_span is not None else None,
        )

    @staticmethod
    def right_after(other):
        if other is None:
            return None

        return SourceSpan(
            other.end_pos + 1,
            other.end_pos,
            other.end_line,
            other.end_column + 1,
            other.end_line,
            other.end_column,
        )

    @staticmethod
    def at_beginning():
        return SourceSpan(0, -1, 1, 1, 1, 0)

    @staticmethod
    def from_start_end(start_pos, end_pos, text):
        start_line, start_column = compute_line_col(start_pos, text)
        end_line, end_column = compute_line_col(end_pos, text)

        return SourceSpan(
            start_pos,
            end_pos,
            start_line,
            start_column,
            end_line,
            end_column,
        )

    @staticmethod
    def at_end_of_source(text):
        return SourceSpan.from_start_end(len(text), len(text) - 1, text)
