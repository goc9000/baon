# logic/ast/actions/ApplyFunctionAction.py
#
# (C) Copyright 2012-present  Cristian Dinu <goc9000@gmail.com>
# 
# This file is part of BAON.
#
# Licensed under the GPL-3

import re

from logic.ast.actions.CompiledAction import CompiledAction, wrap_simple_text_function
from logic.ast.ASTNode import ast_node_field

from logic.errors.RuleCheckException import RuleCheckException

from logic.grammar_utils import to_title_case


PAT_BRACE = re.compile(r"[()\[\]{}]")


def unbrace(text):
    return PAT_BRACE.sub('', text)


def add_braces(text, braces):
    mid_text = text.lstrip()
    left_space = text[0:len(text) - len(mid_text)]
    mid_text = mid_text.rstrip()
    right_space = text[len(left_space) + len(mid_text):]
    
    return left_space + braces[0] + mid_text + braces[1] + right_space


def extract_text_from_braces(text, braces, fail_value=None):
    idx_from = text.find(braces[0])
    if idx_from == -1:
        return fail_value
    idx_to = text.find(braces[1], idx_from + 1)
    if idx_to == -1:
        return fail_value
    
    return text[idx_from + 1:idx_to]


SIMPLE_FUNC_DICT = {
    'title': to_title_case,
    'trim': lambda s: s.strip(),
    'upper': lambda s: s.upper(),
    'toupper': lambda s: s.upper(),
    'lower': lambda s: s.lower(),
    'tolower': lambda s: s.lower(),
    'unbrace': unbrace,
    'paras': lambda s: add_braces(s, u'()'),
    'braces': lambda s: add_braces(s, u'[]'),
    'curlies': lambda s: add_braces(s, u'{}'),
    'inparas': lambda s: extract_text_from_braces(s, u'()', u''),
    'inbraces': lambda s: extract_text_from_braces(s, u'[]', u''),
    'incurlies': lambda s: extract_text_from_braces(s, u'{}', u''),
}

FUNC_DICT = {
}


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
