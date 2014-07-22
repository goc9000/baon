# logic/parsing/ItemWithPositionInSource.py
#
# (C) Copyright 2012-present  Cristian Dinu <goc9000@gmail.com>
#
# This file is part of BAON.
#
# Licensed under the GPL-3


class ItemWithPositionInSource(object):
    source_start_lineno = None
    source_start_colno = None
    source_start_pos = None
    source_end_lineno = None
    source_end_colno = None
    source_end_pos = None

    def __init__(self):
        pass

    def set_span_from_item(self, item):
        self.set_span_from_items(item, item)

    def set_span_from_items(self, item_a, item_b):
        self.source_start_lineno = item_a.source_start_lineno
        self.source_start_colno = item_a.source_start_colno
        self.source_start_pos = item_a.source_start_pos
        self.source_end_lineno = item_b.source_end_lineno
        self.source_end_colno = item_b.source_end_colno
        self.source_end_pos = item_b.source_end_pos
