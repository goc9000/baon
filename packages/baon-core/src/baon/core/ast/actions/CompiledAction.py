# baon/core/ast/actions/CompiledAction.py
#
# (C) Copyright 2012-present  Cristian Dinu <goc9000@gmail.com>
# 
# This file is part of BAON.
#
# Licensed under the GPL-3


from abc import abstractmethod

from baon.core.ast.actions.Action import Action


def wrap_simple_text_function(function):
    def wrapper(action_context):
        new_text = function(action_context.text)
        if new_text is False:
            return False
        return action_context._replace(text=new_text)

    return wrapper


class CompiledAction(Action):
    _cached_function = None

    def __init__(self):
        Action.__init__(self)

    def _get_function(self):
        if self._cached_function is not None:
            return self._cached_function

        self._cached_function = self._compile_function()
        return self._cached_function

    @abstractmethod
    def _compile_function(self):
        return lambda x: x

    def _semantic_check_before_children(self, scope):
        self._compile_function()

    def execute(self, context):
        return self._get_function()(context)
