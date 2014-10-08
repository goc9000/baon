# baon/core/ast/actions/ApplyFunctionAction.py
#
# (C) Copyright 2012-present  Cristian Dinu <goc9000@gmail.com>
# 
# This file is part of BAON.
#
# Licensed under the GPL-3

import pkgutil
import inspect

import baon.lib.action_functions
import baon.lib.simple_text_functions

from baon.core.ast.actions.CompiledAction import CompiledAction, wrap_simple_text_function
from baon.core.ast.ASTNode import ast_node_field
from baon.core.errors.RuleCheckException import RuleCheckException


def scan_package_for_functions(package):
    function_dict = {}

    for importer, name, is_package in pkgutil.iter_modules(package.__path__):
        try:
            module = importer.find_module(name).load_module(name)
            is_public_function = lambda f: inspect.isfunction(f) and not f.__name__.startswith('_')
            public_functions = {name: fn for name, fn in inspect.getmembers(module, is_public_function)}

            if name in public_functions:
                function_dict[name] = public_functions[name]
                continue
            else:
                function_dict.update({name: fn for name, fn in public_functions.items() if not name.startswith('_')})
        except ImportError:
            pass

    return function_dict


FUNC_DICT = scan_package_for_functions(baon.lib.action_functions)
SIMPLE_FUNC_DICT = scan_package_for_functions(baon.lib.simple_text_functions)


class ApplyFunctionAction(CompiledAction):
    function_name = ast_node_field()

    def __init__(self, fn_name):
        CompiledAction.__init__(self)

        self.function_name = fn_name

    def _compile_function(self):
        if self.function_name in SIMPLE_FUNC_DICT:
            return wrap_simple_text_function(SIMPLE_FUNC_DICT[self.function_name])
        elif self.function_name in FUNC_DICT:
            return FUNC_DICT[self.function_name]
        else:
            raise RuleCheckException("Unsupported function '{0}'".format(self.function_name))
