# baon/core/parsing/__tests__/test_tokenize_rules.py
#
# (C) Copyright 2012-present  Cristian Dinu <goc9000@gmail.com>
#
# This file is part of BAON.
#
# Licensed under the GPL-3


from unittest import TestCase

from baon.core.parsing.tokenize_rules import tokenize_rules


class TestTokenizeRules(TestCase):

    def test_parse_id(self):
        self.assertEqual(self.parse_result('ident'),
                         [(0, 'ID', 'ident', 1, 1)])
        self.assertEqual(self.parse_result('CasedID'),
                         [(0, 'ID', 'CasedID', 1, 1)])
        self.assertEqual(self.parse_result('a b c'),
                         [(0, 'ID', 'a', 1, 1),
                          (2, 'ID', 'b', 1, 3),
                          (4, 'ID', 'c', 1, 5)])
        self.assertEqual(self.parse_result('num123b_3'),
                         [(0, 'ID', 'num123b_3', 1, 1)])
        self.assertEqual(self.parse_result('_x'),
                         [(0, 'ID', '_x', 1, 1)])
        self.assertEqual(self.parse_result('a-b'),
                         [(0, 'ID', 'a', 1, 1),
                          (1, 'error', '-', 1, 2),
                          (2, 'ID', 'b', 1, 3)])
        self.assertEqual(self.parse_result('0ident'),
                         [(0, 'error', '0', 1, 1),
                          (1, 'ID', 'ident', 1, 2)])

    def test_parse_single_char_operators(self):
        self.assertEqual(self.parse_result(' (@^|$!) '),
                         [(1, 'PARA_OPEN', '(', 1, 2),
                          (2, 'OP_SEARCH', '@', 1, 3),
                          (3, 'ANCHOR_START', '^', 1, 4),
                          (4, 'OP_OR', '|', 1, 5),
                          (5, 'ANCHOR_END', '$', 1, 6),
                          (6, 'OP_DELETE', '!', 1, 7),
                          (7, 'PARA_CLOSE', ')', 1, 8)])

    def test_parse_two_char_operators(self):
        self.assertEqual(self.parse_result('->-<<>><>.....'),
                         [(0, 'OP_XFORM', '->', 1, 1),
                          (2, 'error', '-', 1, 3),
                          (3, 'OP_INSERT', '<<', 1, 4),
                          (5, 'OP_SAVE', '>>', 1, 6),
                          (7, 'error', '<>', 1, 8),
                          (9, 'BETWEEN', '..', 1, 10),
                          (11, 'BETWEEN', '..', 1, 12),
                          (13, 'error', '.', 1, 14)])

    def test_parse_rule_sep(self):
        self.assertEqual(self.parse_result('rule; rule\nrule\n\nrule;;'),
                         [(0, 'ID', 'rule', 1, 1),
                          (4, 'RULE_SEP', ';', 1, 5),
                          (6, 'ID', 'rule', 1, 7),
                          (10, 'RULE_SEP', '\n', 1, 11),
                          (11, 'ID', 'rule', 2, 1),
                          (15, 'RULE_SEP', '\n', 2, 5),
                          (16, 'RULE_SEP', '\n', 3, 1),
                          (17, 'ID', 'rule', 4, 1),
                          (21, 'RULE_SEP', ';', 4, 5),
                          (22, 'RULE_SEP', ';', 4, 6)])

    def test_parse_repeat_operator(self):
        self.assertEqual(self.parse_result('x+ x * x??'),
                         [(0, 'ID', 'x', 1, 1),
                          (1, 'OP_REPEAT', '+', 1, 2, {'max': None, 'min': 1}),
                          (3, 'ID', 'x', 1, 4),
                          (5, 'OP_REPEAT', '*', 1, 6, {'max': None, 'min': 0}),
                          (7, 'ID', 'x', 1, 8),
                          (8, 'OP_REPEAT', '?', 1, 9, {'max': 1, 'min': 0}),
                          (9, 'OP_REPEAT', '?', 1, 10, {'max': 1, 'min': 0})])

    def test_parse_fmt_specifier(self):
        self.assertEqual(self.parse_result('%d'),
                         [(0, 'FORMAT_SPEC', '%d', 1, 1, {'specifier': 'd'})])
        self.assertEqual(self.parse_result('%s%d'),
                         [(0, 'FORMAT_SPEC', '%s', 1, 1, {'specifier': 's'}),
                          (2, 'FORMAT_SPEC', '%d', 1, 3, {'specifier': 'd'})])
        self.assertEqual(self.parse_result('%para'),
                         [(0, 'FORMAT_SPEC', '%para', 1, 1, {'specifier': 'para'})])
        self.assertEqual(self.parse_result('%4c'),
                         [(0, 'FORMAT_SPEC', '%4c', 1, 1, {'width': 4, 'specifier': 'c'})])
        self.assertEqual(self.parse_result('%123c'),
                         [(0, 'FORMAT_SPEC', '%123c', 1, 1, {'width': 123, 'specifier': 'c'})])
        self.assertEqual(self.parse_result('%05str'),
                         [(0, 'FORMAT_SPEC', '%05str', 1, 1,
                           {'specifier': 'str', 'width': 5, 'leading_zeros': True})])
        self.assertEqual(self.parse_result('%'),
                         [(0, 'FORMAT_SPEC', '%', 1, 1, {'specifier': None})])
        self.assertEqual(self.parse_result('%-11z'),
                         [(0, 'FORMAT_SPEC', '%', 1, 1, {'specifier': None}),
                         (1, 'error', '-11', 1, 2),
                         (4, 'ID', 'z', 1, 5)])
        self.assertEqual(self.parse_result('% d'),
                         [(0, 'FORMAT_SPEC', '%', 1, 1, {'specifier': None}),
                          (2, 'ID', 'd', 1, 3)])
        self.assertEqual(self.parse_result('%5'),
                         [(0, 'FORMAT_SPEC', '%5', 1, 1, {'width': 5, 'specifier': None})])

    def test_parse_string_literal(self):
        self.assertEqual(self.parse_result('"double quotes"'),
                         [(0, 'STRING_LITERAL', '"double quotes"', 1, 1, {'value': 'double quotes'})])
        self.assertEqual(self.parse_result("'single quotes'"),
                         [(0, 'STRING_LITERAL', "'single quotes'", 1, 1, {'value': 'single quotes'})])
        self.assertEqual(self.parse_result('"two" "literals"'),
                         [(0, 'STRING_LITERAL', '"two"', 1, 1, {'value': 'two'}),
                          (6, 'STRING_LITERAL', '"literals"', 1, 7, {'value': 'literals'})])
        self.assertEqual(self.parse_result('"embedded""quotes"'),
                         [(0, 'STRING_LITERAL', '"embedded""quotes"', 1, 1, {'value': 'embedded"quotes'})])
        self.assertEqual(self.parse_result('"unterminated'),
                         [(0, 'STRING_LITERAL', '"unterminated', 1, 1, {'unterminated': True})])
        self.assertEqual(self.parse_result('"unterminated\nnext line'),
                         [(0, 'STRING_LITERAL', '"unterminated', 1, 1, {'unterminated': True}),
                          (13, 'RULE_SEP', '\n', 1, 14),
                          (14, 'ID', 'next', 2, 1),
                          (19, 'ID', 'line', 2, 6)])
        self.assertEqual(self.parse_result('"unterm w ""embedded'),
                         [(0, 'STRING_LITERAL', '"unterm w ""embedded', 1, 1, {'unterminated': True})])
        self.assertEqual(self.parse_result('"with"trailer'),
                         [(0, 'STRING_LITERAL', '"with"', 1, 1, {'value': 'with'}),
                          (6, 'ID', 'trailer', 1, 7)])

    def test_parse_regex(self):
        self.assertEqual(self.parse_result('/normal regex/'),
                         [(0, 'REGEX', '/normal regex/', 1, 1, {'pattern': 'normal regex'})])
        self.assertEqual(self.parse_result("/regex w flags/igm"),
                         [(0, 'REGEX', '/regex w flags/igm', 1, 1, {'pattern': 'regex w flags',
                                                                    'flags': {'i', 'g', 'm'}})])
        self.assertEqual(self.parse_result('/two/i/regexes/'),
                         [(0, 'REGEX', '/two/i', 1, 1, {'pattern': 'two', 'flags': {'i'}}),
                          (6, 'REGEX', '/regexes/', 1, 7, {'pattern': 'regexes'})])
        self.assertEqual(self.parse_result('/with//escape/'),
                         [(0, 'REGEX', '/with//escape/', 1, 1, {'pattern': 'with/escape'})])
        self.assertEqual(self.parse_result('/unterminated'),
                         [(0, 'REGEX', '/unterminated', 1, 1, {'unterminated': True})])
        self.assertEqual(self.parse_result('/unterminated\nnext line'),
                         [(0, 'REGEX', '/unterminated', 1, 1, {'unterminated': True}),
                          (13, 'RULE_SEP', '\n', 1, 14),
                          (14, 'ID', 'next', 2, 1),
                          (19, 'ID', 'line', 2, 6)])
        self.assertEqual(self.parse_result('/unterm w escape//'),
                         [(0, 'REGEX', '/unterm w escape//', 1, 1, {'unterminated': True})])
        self.assertEqual(self.parse_result('/unterm w escape//\nnext line'),
                         [(0, 'REGEX', '/unterm w escape//', 1, 1, {'unterminated': True}),
                          (18, 'RULE_SEP', '\n', 1, 19),
                          (19, 'ID', 'next', 2, 1),
                          (24, 'ID', 'line', 2, 6)])

    def test_parse_error(self):
        self.assertEqual(self.parse_result('#'),
                         [(0, 'error', '#', 1, 1)])
        self.assertEqual(self.parse_result('#::##:#'),
                         [(0, 'error', '#::##:#', 1, 1)])
        self.assertEqual(self.parse_result('###recover'),
                         [(0, 'error', '###', 1, 1),
                          (3, 'ID', 'recover', 1, 4)])
        self.assertEqual(self.parse_result('  ###   ####  '),
                         [(2, 'error', '###', 1, 3),
                          (8, 'error', '####', 1, 9)])
        self.assertEqual(self.parse_result('  ### \n  ####  '),
                         [(2, 'error', '###', 1, 3),
                          (6, 'RULE_SEP', '\n', 1, 7),
                          (9, 'error', '####', 2, 3)])

    def test_parse_complete(self):
        text = '  %d+ ->"abc" ("efg""def"*->title->%4c ; ..! #:## @(/[a-z]/i->(<<abc|"x"?)))\n  $'
        self.assertEqual(self.parse_result(text),
                         [(2, 'FORMAT_SPEC', '%d', 1, 3, {'specifier': 'd'}),
                          (4, 'OP_REPEAT', '+', 1, 5, {'max': None, 'min': 1}),
                          (6, 'OP_XFORM', '->', 1, 7),
                          (8, 'STRING_LITERAL', '"abc"', 1, 9, {'value': 'abc'}),
                          (14, 'PARA_OPEN', '(', 1, 15),
                          (15, 'STRING_LITERAL', '"efg""def"', 1, 16, {'value': 'efg"def'}),
                          (25, 'OP_REPEAT', '*', 1, 26, {'max': None, 'min': 0}),
                          (26, 'OP_XFORM', '->', 1, 27),
                          (28, 'ID', 'title', 1, 29),
                          (33, 'OP_XFORM', '->', 1, 34),
                          (35, 'FORMAT_SPEC', '%4c', 1, 36, {'width': 4, 'specifier': 'c'}),
                          (39, 'RULE_SEP', ';', 1, 40),
                          (41, 'BETWEEN', '..', 1, 42),
                          (43, 'OP_DELETE', '!', 1, 44),
                          (45, 'error', '#:##', 1, 46),
                          (50, 'OP_SEARCH', '@', 1, 51),
                          (51, 'PARA_OPEN', '(', 1, 52),
                          (52, 'REGEX', '/[a-z]/i', 1, 53, {'pattern': '[a-z]', 'flags': {'i'}}),
                          (60, 'OP_XFORM', '->', 1, 61),
                          (62, 'PARA_OPEN', '(', 1, 63),
                          (63, 'OP_INSERT', '<<', 1, 64),
                          (65, 'ID', 'abc', 1, 66),
                          (68, 'OP_OR', '|', 1, 69),
                          (69, 'STRING_LITERAL', '"x"', 1, 70, {'value': 'x'}),
                          (72, 'OP_REPEAT', '?', 1, 73, {'max': 1, 'min': 0}),
                          (73, 'PARA_CLOSE', ')', 1, 74),
                          (74, 'PARA_CLOSE', ')', 1, 75),
                          (75, 'PARA_CLOSE', ')', 1, 76),
                          (76, 'RULE_SEP', '\n', 1, 77),
                          (79, 'ANCHOR_END', '$', 2, 3)])

    def parse_result(self, text_input):
        return [token.test_repr() for token in tokenize_rules(text_input)]
