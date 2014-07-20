# logic/parsing/__tests__/test_RulesLexer.py
#
# (C) Copyright 2012-present  Cristian Dinu <goc9000@gmail.com>
#
# This file is part of BAON.
#
# Licensed under the GPL-3


from unittest import TestCase

from logic.parsing.RulesLexer import RulesLexer


class TestRulesLexer(TestCase):

    def test_parse_id(self):
        self.assertEqual(self.parse_result(u'ident'),
                         [(0, 'ID', u'ident', 1, 1)])
        self.assertEqual(self.parse_result(u'CasedID'),
                         [(0, 'ID', u'CasedID', 1, 1)])
        self.assertEqual(self.parse_result(u'a b c'),
                         [(0, 'ID', u'a', 1, 1),
                          (2, 'ID', u'b', 1, 3),
                          (4, 'ID', u'c', 1, 5)])
        self.assertEqual(self.parse_result(u'num123b_3'),
                         [(0, 'ID', u'num123b_3', 1, 1)])
        self.assertEqual(self.parse_result(u'_x'),
                         [(0, 'ID', u'_x', 1, 1)])
        self.assertEqual(self.parse_result(u'a-b'),
                         [(0, 'ID', u'a', 1, 1),
                          (1, 'error', u'-', 1, 2),
                          (2, 'ID', u'b', 1, 3)])
        self.assertEqual(self.parse_result(u'0ident'),
                         [(0, 'error', u'0', 1, 1),
                          (1, 'ID', u'ident', 1, 2)])

    def test_parse_single_char_operators(self):
        self.assertEqual(self.parse_result(u' (@^|$!) '),
                         [(1, 'PARA_OPEN', u'(', 1, 2),
                          (2, 'OP_SEARCH', u'@', 1, 3),
                          (3, 'ANCHOR_START', u'^', 1, 4),
                          (4, 'OP_OR', u'|', 1, 5),
                          (5, 'ANCHOR_END', u'$', 1, 6),
                          (6, 'OP_DELETE', u'!', 1, 7),
                          (7, 'PARA_CLOSE', u')', 1, 8)])

    def test_parse_two_char_operators(self):
        self.assertEqual(self.parse_result(u'->-<<>><>.....'),
                         [(0, 'OP_XFORM', u'->', 1, 1),
                          (2, 'error', u'-', 1, 3),
                          (3, 'OP_INSERT', u'<<', 1, 4),
                          (5, 'OP_SAVE', u'>>', 1, 6),
                          (7, 'error', u'<>', 1, 8),
                          (9, 'BETWEEN', u'..', 1, 10),
                          (11, 'BETWEEN', u'..', 1, 12),
                          (13, 'error', u'.', 1, 14)])

    def test_parse_rule_sep(self):
        self.assertEqual(self.parse_result(u'rule; rule\nrule\n\nrule;;'),
                         [(0, 'ID', u'rule', 1, 1),
                          (4, 'RULE_SEP', u';', 1, 5),
                          (6, 'ID', u'rule', 1, 7),
                          (10, 'RULE_SEP', u'\n', 1, 11),
                          (11, 'ID', u'rule', 2, 1),
                          (15, 'RULE_SEP', u'\n', 2, 5),
                          (16, 'RULE_SEP', u'\n', 3, 1),
                          (17, 'ID', u'rule', 4, 1),
                          (21, 'RULE_SEP', u';', 4, 5),
                          (22, 'RULE_SEP', u';', 4, 6)])

    def test_parse_repeat_operator(self):
        self.assertEqual(self.parse_result(u'x+ x * x??'),
                         [(0, 'ID', u'x', 1, 1),
                          (1, 'OP_REPEAT', u'+', 1, 2, {'max': None, 'min': 1}),
                          (3, 'ID', u'x', 1, 4),
                          (5, 'OP_REPEAT', u'*', 1, 6, {'max': None, 'min': 0}),
                          (7, 'ID', u'x', 1, 8),
                          (8, 'OP_REPEAT', u'?', 1, 9, {'max': 1, 'min': 0}),
                          (9, 'OP_REPEAT', u'?', 1, 10, {'max': 1, 'min': 0})])

    def test_parse_fmt_specifier(self):
        self.assertEqual(self.parse_result(u'%d'),
                         [(0, 'FORMAT_SPEC', u'%d', 1, 1, {'specifier': u'd'})])
        self.assertEqual(self.parse_result(u'%s%d'),
                         [(0, 'FORMAT_SPEC', u'%s', 1, 1, {'specifier': u's'}),
                          (2, 'FORMAT_SPEC', u'%d', 1, 3, {'specifier': u'd'})])
        self.assertEqual(self.parse_result(u'%para'),
                         [(0, 'FORMAT_SPEC', u'%para', 1, 1, {'specifier': u'para'})])
        self.assertEqual(self.parse_result(u'%4c'),
                         [(0, 'FORMAT_SPEC', u'%4c', 1, 1, {'width': 4, 'specifier': u'c'})])
        self.assertEqual(self.parse_result(u'%123c'),
                         [(0, 'FORMAT_SPEC', u'%123c', 1, 1, {'width': 123, 'specifier': u'c'})])
        self.assertEqual(self.parse_result(u'%05str'),
                         [(0, 'FORMAT_SPEC', u'%05str', 1, 1,
                           {'specifier': u'str', 'width': 5, 'leading_zeros': True})])
        self.assertEqual(self.parse_result(u'%'),
                         [(0, 'FORMAT_SPEC', u'%', 1, 1, {'specifier': None})])
        self.assertEqual(self.parse_result(u'%-11z'),
                         [(0, 'FORMAT_SPEC', u'%', 1, 1, {'specifier': None}),
                         (1, 'error', u'-11', 1, 2),
                         (4, 'ID', u'z', 1, 5)])
        self.assertEqual(self.parse_result(u'% d'),
                         [(0, 'FORMAT_SPEC', u'%', 1, 1, {'specifier': None}),
                          (2, 'ID', u'd', 1, 3)])
        self.assertEqual(self.parse_result(u'%5'),
                         [(0, 'FORMAT_SPEC', u'%5', 1, 1, {'width': 5, 'specifier': None})])

    def test_parse_string_literal(self):
        self.assertEqual(self.parse_result(u'"double quotes"'),
                         [(0, 'STRING_LITERAL', u'"double quotes"', 1, 1, {'value': u'double quotes'})])
        self.assertEqual(self.parse_result(u"'single quotes'"),
                         [(0, 'STRING_LITERAL', u"'single quotes'", 1, 1, {'value': u'single quotes'})])
        self.assertEqual(self.parse_result(u'"two" "literals"'),
                         [(0, 'STRING_LITERAL', u'"two"', 1, 1, {'value': u'two'}),
                          (6, 'STRING_LITERAL', u'"literals"', 1, 7, {'value': u'literals'})])
        self.assertEqual(self.parse_result(u'"with\\\\escapes\\""'),
                         [(0, 'STRING_LITERAL', u'"with\\\\escapes\\""', 1, 1, {'value': u'with\\escapes"'})])
        self.assertEqual(self.parse_result(u'"unterminated'),
                         [(0, 'STRING_LITERAL', u'"unterminated', 1, 1, {'unterminated': True})])
        self.assertEqual(self.parse_result(u'"unterminated\nnext line'),
                         [(0, 'STRING_LITERAL', u'"unterminated', 1, 1, {'unterminated': True}),
                          (13, 'RULE_SEP', u'\n', 1, 14),
                          (14, 'ID', u'next', 2, 1),
                          (19, 'ID', u'line', 2, 6)])
        self.assertEqual(self.parse_result(u'"unterm w escape\\'),
                         [(0, 'STRING_LITERAL', u'"unterm w escape\\', 1, 1, {'unterminated': True})])
        self.assertEqual(self.parse_result(u'"unterm w escape\\\nnext line'),
                         [(0, 'STRING_LITERAL', u'"unterm w escape\\', 1, 1, {'unterminated': True}),
                         (17, 'RULE_SEP', u'\n', 1, 18),
                         (18, 'ID', u'next', 2, 1),
                         (23, 'ID', u'line', 2, 6)])
        self.assertEqual(self.parse_result(u'"unterm w escape\\"'),
                         [(0, 'STRING_LITERAL', u'"unterm w escape\\"', 1, 1, {'unterminated': True})])
        self.assertEqual(self.parse_result(u'"unterm w escape\\"\nnext line'),
                         [(0, 'STRING_LITERAL', u'"unterm w escape\\"', 1, 1, {'unterminated': True}),
                          (18, 'RULE_SEP', u'\n', 1, 19),
                          (19, 'ID', u'next', 2, 1),
                          (24, 'ID', u'line', 2, 6)])

    def test_parse_regex(self):
        self.assertEqual(self.parse_result(u'/normal regex/'),
                         [(0, 'REGEX', u'/normal regex/', 1, 1, {'pattern': u'normal regex'})])
        self.assertEqual(self.parse_result(u"/regex w flags/igm"),
                         [(0, 'REGEX', u'/regex w flags/igm', 1, 1, {'pattern': u'regex w flags',
                                                                     'flags': {u'i', u'g', u'm'}})])
        self.assertEqual(self.parse_result(u'/two/i/regexes/'),
                         [(0, 'REGEX', u'/two/i', 1, 1, {'pattern': u'two', 'flags': {u'i'}}),
                          (6, 'REGEX', u'/regexes/', 1, 7, {'pattern': u'regexes'})])
        self.assertEqual(self.parse_result(u'/with//escape/'),
                         [(0, 'REGEX', u'/with//escape/', 1, 1, {'pattern': u'with/escape'})])
        self.assertEqual(self.parse_result(u'/unterminated'),
                         [(0, 'REGEX', u'/unterminated', 1, 1, {'unterminated': True})])
        self.assertEqual(self.parse_result(u'/unterminated\nnext line'),
                         [(0, 'REGEX', u'/unterminated', 1, 1, {'unterminated': True}),
                          (13, 'RULE_SEP', u'\n', 1, 14),
                          (14, 'ID', u'next', 2, 1),
                          (19, 'ID', u'line', 2, 6)])
        self.assertEqual(self.parse_result(u'/unterm w escape//'),
                         [(0, 'REGEX', u'/unterm w escape//', 1, 1, {'unterminated': True})])
        self.assertEqual(self.parse_result(u'/unterm w escape//\nnext line'),
                         [(0, 'REGEX', u'/unterm w escape//', 1, 1, {'unterminated': True}),
                          (18, 'RULE_SEP', u'\n', 1, 19),
                          (19, 'ID', u'next', 2, 1),
                          (24, 'ID', u'line', 2, 6)])

    def test_parse_error(self):
        self.assertEqual(self.parse_result(u'#'),
                         [(0, 'error', u'#', 1, 1)])
        self.assertEqual(self.parse_result(u'#::##:#'),
                         [(0, 'error', u'#::##:#', 1, 1)])
        self.assertEqual(self.parse_result(u'###recover'),
                         [(0, 'error', u'###', 1, 1),
                          (3, 'ID', u'recover', 1, 4)])
        self.assertEqual(self.parse_result(u'  ###   ####  '),
                         [(2, 'error', u'###', 1, 3),
                          (8, 'error', u'####', 1, 9)])
        self.assertEqual(self.parse_result(u'  ### \n  ####  '),
                         [(2, 'error', u'###', 1, 3),
                          (6, 'RULE_SEP', u'\n', 1, 7),
                          (9, 'error', u'####', 2, 3)])

    def test_parse_complete(self):
        text = u'  %d+ ->"abc" ("efg\\"def"*->title->%4c ; ..! #:## @(/[a-z]/i->(<<abc|"x"?)))\n  $'
        self.assertEqual(self.parse_result(text),
                         [(2, 'FORMAT_SPEC', u'%d', 1, 3, {'specifier': u'd'}),
                          (4, 'OP_REPEAT', u'+', 1, 5, {'max': None, 'min': 1}),
                          (6, 'OP_XFORM', u'->', 1, 7),
                          (8, 'STRING_LITERAL', u'"abc"', 1, 9, {'value': u'abc'}),
                          (14, 'PARA_OPEN', u'(', 1, 15),
                          (15, 'STRING_LITERAL', u'"efg\\"def"', 1, 16, {'value': u'efg"def'}),
                          (25, 'OP_REPEAT', u'*', 1, 26, {'max': None, 'min': 0}),
                          (26, 'OP_XFORM', u'->', 1, 27),
                          (28, 'ID', u'title', 1, 29),
                          (33, 'OP_XFORM', u'->', 1, 34),
                          (35, 'FORMAT_SPEC', u'%4c', 1, 36, {'width': 4, 'specifier': u'c'}),
                          (39, 'RULE_SEP', u';', 1, 40),
                          (41, 'BETWEEN', u'..', 1, 42),
                          (43, 'OP_DELETE', u'!', 1, 44),
                          (45, 'error', u'#:##', 1, 46),
                          (50, 'OP_SEARCH', u'@', 1, 51),
                          (51, 'PARA_OPEN', u'(', 1, 52),
                          (52, 'REGEX', u'/[a-z]/i', 1, 53, {'pattern': u'[a-z]', 'flags': {u'i'}}),
                          (60, 'OP_XFORM', u'->', 1, 61),
                          (62, 'PARA_OPEN', u'(', 1, 63),
                          (63, 'OP_INSERT', u'<<', 1, 64),
                          (65, 'ID', u'abc', 1, 66),
                          (68, 'OP_OR', u'|', 1, 69),
                          (69, 'STRING_LITERAL', u'"x"', 1, 70, {'value': u'x'}),
                          (72, 'OP_REPEAT', u'?', 1, 73, {'max': 1, 'min': 0}),
                          (73, 'PARA_CLOSE', u')', 1, 74),
                          (74, 'PARA_CLOSE', u')', 1, 75),
                          (75, 'PARA_CLOSE', u')', 1, 76),
                          (76, 'RULE_SEP', u'\n', 1, 77),
                          (79, 'ANCHOR_END', u'$', 2, 3)])

    def parse_result(self, text_input):
        return [token.test_repr() for token in RulesLexer.tokenize(text_input)]
