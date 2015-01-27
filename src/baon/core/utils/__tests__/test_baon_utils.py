# baon/core/utils/__tests__/test_baon_utils.py
#
# (C) Copyright 2012-present  Cristian Dinu <goc9000@gmail.com>
#
# This file is part of BAON.
#
# Licensed under the GPL-3


from unittest import TestCase

from baon.core.utils.baon_utils import decode_baon_string_literal
from baon.core.parsing.rule_parse_exceptions import StringLiteralNotQuotedProperlyException


class TestBaonUtilsPy(TestCase):
    def test_decode_baon_string_literal(self):
        f_u_t = decode_baon_string_literal

        self.assertEqual(f_u_t('"double quotes"'), 'double quotes')
        self.assertEqual(f_u_t("'single quotes'"), 'single quotes')
        self.assertEqual(f_u_t('"dodgy"quote"'), 'dodgy"quote')
        self.assertEqual(f_u_t('"escaped\\"quote"'), 'escaped"quote')
        self.assertEqual(f_u_t('"escape\\\\char"'), 'escape\\char')
        self.assertEqual(f_u_t('"valid\\n\\tescapes"'), 'valid\n\tescapes')
        self.assertEqual(f_u_t('"raw\n\tspace"'), 'raw\n\tspace')
        self.assertEqual(f_u_t('"invalid\\escape"'), 'invalid\\escape')
        self.assertEqual(f_u_t('"end escape\\"'), 'end escape\\')
        self.assertEqual(f_u_t('"octal\\040escape"'), 'octal escape')
        self.assertEqual(f_u_t('"invalid\\840octal"'), 'invalid\\840octal')
        self.assertEqual(f_u_t('"unicode\\u1234escape"'), 'unicode\u1234escape')
        self.assertEqual(f_u_t('"raw\u1234unicode"'), 'raw\u1234unicode')
        self.assertEqual(f_u_t('"invalid\\u12g4unicode"'), 'invalid\\u12g4unicode')
        self.assertEqual(f_u_t('"invalid_uni\\u123"'), 'invalid_uni\\u123')

        with self.assertRaises(StringLiteralNotQuotedProperlyException):
            f_u_t('unquoted')
        with self.assertRaises(StringLiteralNotQuotedProperlyException):
            f_u_t('"unterminated')
        with self.assertRaises(StringLiteralNotQuotedProperlyException):
            f_u_t('"mismatch\'')
