# logic/ast/RulesASTNode.py
#
# (C) Copyright 2012-present  Cristian Dinu <goc9000@gmail.com>
#
# This file is part of BAON.
#
# Licensed under the GPL-3

from logic.parsing.ItemWithPositionInSource import ItemWithPositionInSource

from logic.ast.RulesASTNodeField import RulesASTNodeField

import inspect

def ast_node_field(*args, **kwargs):
    return RulesASTNodeField(*args, **kwargs)


class RulesASTNode(ItemWithPositionInSource):
    _ast_node_fields = None

    def __init__(self):
        ItemWithPositionInSource.__init__(self)
        self._init_ast_node_fields()

    def test_repr(self):
        """The representation of this AST item in tests"""
        return\
            (self.__class__.__name__,) +\
            self._test_repr_params() +\
            tuple(child.test_repr() for child in self._test_repr_children())

    def test_repr_with_source_spans(self):
        """The representation of this AST item in tests"""
        return\
            (self.source_start_lineno, self.source_start_colno, self.source_end_lineno, self.source_end_colno) +\
            (self.__class__.__name__,) +\
            self._test_repr_params() +\
            tuple(child.test_repr_with_source_spans() for child in self._test_repr_children())

    def _init_ast_node_fields(self):
        self._ast_node_fields = []
        for field_name, value in inspect.getmembers(self):
            if isinstance(value, RulesASTNodeField):
                value.name = field_name
                self._ast_node_fields.append(value)
                self.__setattr__(field_name, value.default_value)

        self._ast_node_fields.sort(key=lambda field: field.order)

    def _test_repr_params(self):
        values = []
        num_valid = 0

        for index, field in enumerate(self._ast_node_fields):
            value = self.__getattribute__(field.name)

            if field.test_repr is None:
                value_repr = value
            elif hasattr(field.test_repr, '__call__'):
                value_repr = field.test_repr(value)
            else:
                value_repr = field.test_repr

            values.append(value_repr)
            if value != field.hide_for_value:
                num_valid = index

        return tuple(values[0:num_valid+1])

    def _test_repr_children(self):
        return ()
