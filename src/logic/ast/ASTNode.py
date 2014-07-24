# logic/ast/ASTNode.py
#
# (C) Copyright 2012-present  Cristian Dinu <goc9000@gmail.com>
#
# This file is part of BAON.
#
# Licensed under the GPL-3

import inspect

from logic.errors.RuleCheckException import RuleCheckException

from logic.parsing.ItemWithPositionInSource import ItemWithPositionInSource

from logic.ast.ASTNodeField import ASTNodeField
from logic.ast.ASTNodeChildRef import ASTNodeChildRef
from logic.ast.ASTNodeChildList import ASTNodeChildList


def ast_node_field(*args, **kwargs):
    return ASTNodeField(*args, **kwargs)


def ast_node_child(*args, **kwargs):
    return ASTNodeChildRef(*args, **kwargs)


def ast_node_children(*args, **kwargs):
    return ASTNodeChildList(*args, **kwargs)


class ASTNode(ItemWithPositionInSource):
    _ast_node_fields = None
    _ast_node_child_refs = None
    _ast_node_child_lists = None

    def __init__(self):
        ItemWithPositionInSource.__init__(self)
        self._init_ast_node_fields()
        self._init_ast_node_child_refs()
        self._init_ast_node_child_lists()

    def semantic_check(self, scope):
        try:
            self._semantic_check_before_children(scope)
            for child in self.iter_ast_children():
                child.semantic_check(scope)
            self._semantic_check_after_children(scope)
        except RuleCheckException as e:
            if e.scope is None:
                e.scope = scope
            if e.source_start_lineno is None:
                e.set_span_from_item(self)
            raise e

    def iter_ast_children(self):
        for child in [self.__getattribute__(child_ref.name) for child_ref in self._ast_node_child_refs]:
            if child is not None:
                yield child

        for child_list in self._ast_node_child_lists:
            for child in self.__getattribute__(child_list.name):
                yield child

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
            if isinstance(value, ASTNodeField):
                value.name = field_name
                self._ast_node_fields.append(value)
                self.__setattr__(field_name, value.default_value)

        self._ast_node_fields.sort(key=lambda field: field.order)

    def _init_ast_node_child_refs(self):
        self._ast_node_child_refs = []
        for child_ref_name, value in inspect.getmembers(self):
            if isinstance(value, ASTNodeChildRef):
                value.name = child_ref_name
                self._ast_node_child_refs.append(value)
                self.__setattr__(child_ref_name, None)

        self._ast_node_child_refs.sort(key=lambda child_ref: child_ref.order)

    def _init_ast_node_child_lists(self):
        self._ast_node_child_lists = []
        for child_list_name, value in inspect.getmembers(self):
            if isinstance(value, ASTNodeChildList):
                value.name = child_list_name
                self._ast_node_child_lists.append(value)
                self.__setattr__(child_list_name, [])

        self._ast_node_child_lists.sort(key=lambda child_list: child_list.order)

    def _semantic_check_before_children(self, scope):
        pass

    def _semantic_check_after_children(self, scope):
        pass

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
        children = [self.__getattribute__(child_ref.name) for child_ref in self._ast_node_child_refs]

        for child_list in self._ast_node_child_lists:
            children.extend(self.__getattribute__(child_list.name))

        return tuple(children)
