# logic/ast/actions/ApplyFunctionAction.py
#
# (C) Copyright 2012-present  Cristian Dinu <goc9000@gmail.com>
# 
# This file is part of BAON.
#
# Licensed under the GPL-3

import re

from logic.ast.actions.CompiledAction import CompiledAction

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


FUNC_DICT = {
    'title': lambda s, c: to_title_case(s),
    'trim': lambda s, c: s.strip(),
    'upper': lambda s, c: s.upper(),
    'toupper': lambda s, c: s.upper(),
    'lower': lambda s, c: s.lower(),
    'tolower': lambda s, c: s.lower(),
    'unbrace': lambda s, c: unbrace(s),
    'paras': lambda s, c: add_braces(s, '()'),
    'braces': lambda s, c: add_braces(s, '[]'),
    'curlies': lambda s, c: add_braces(s, '{}'),
    'inparas': lambda s, c: extract_text_from_braces(s, '()', ''),
    'inbraces': lambda s, c: extract_text_from_braces(s, '[]', ''),
    'incurlies': lambda s, c: extract_text_from_braces(s, '{}', '')
}


class ApplyFunctionAction(CompiledAction):
    function_name = None

    def __init__(self, fn_name):
        CompiledAction.__init__(self)

        self.function_name = fn_name

    def _compile_function(self):
        if self.function_name in FUNC_DICT:
            return FUNC_DICT[self.function_name]
        else:
            raise RuleCheckException("Unsupported function '{0}'".format(self.function_name))

    def _test_repr_params(self):
        return self.function_name,
