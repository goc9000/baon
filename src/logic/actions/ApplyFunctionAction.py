# logic/actions/ApplyFunctionAction.py
#
# (C) Copyright 2012  Cristian Dinu <goc9000@gmail.com>
# 
# This file is part of BAON.
#
# Licensed under the GPL-3

import re

from Action import Action
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


class ApplyFunctionAction(Action):
    fn = None
    error = None
    
    def __init__(self, fn_name):
        Action.__init__(self)
        
        if fn_name in FUNC_DICT:
            self.fn = FUNC_DICT[fn_name]
        else:
            self.error = "Unsupported function '{0}'".format(fn_name)
    
    def semanticCheck(self, scope):
        Action.semanticCheck(self, scope)
        
        if not self.error is None:
            raise RuleCheckException(self.error, scope)

    def execute(self, text, context):
        return self.fn(text, context)
