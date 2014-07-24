# logic/ast/actions/CompiledAction.py
#
# (C) Copyright 2012-present  Cristian Dinu <goc9000@gmail.com>
# 
# This file is part of BAON.
#
# Licensed under the GPL-3

from logic.errors.RuleCheckException import RuleCheckException

from logic.ast.actions.Action import Action


class CompiledAction(Action):
    _cached_function = None

    def __init__(self):
        Action.__init__(self)

    def _get_function(self):
        if self._cached_function is not None:
            return self._cached_function

        self._cached_function = self._compile_function()
        return self._cached_function

    def _compile_function(self):
        raise RuntimeError("_compile_function() not implemented in subclass")

    def _semantic_check_before_children(self, scope):
        self._compile_function()

    def execute(self, text, context):
        return self._get_function()(text, context)
