# logic/__tests__/test_baon_utils.py
#
# (C) Copyright 2012-present  Cristian Dinu <goc9000@gmail.com>
#
# This file is part of BAON.
#
# Licensed under the GPL-3


from unittest import TestCase

from logic.baon_utils import decode_baon_string_literal


class TestBaonUtilsPy(TestCase):
    def test_decode_baon_string_literal(self):
        f_u_t = decode_baon_string_literal

        self.assertEqual(f_u_t(u'"double quotes"'), u'double quotes')
        self.assertEqual(f_u_t(u"'single quotes'"), u'single quotes')
        self.assertEqual(f_u_t(u'"dodgy"quote"'), u'dodgy"quote')
        self.assertEqual(f_u_t(u'"escaped\\"quote"'), u'escaped"quote')
        self.assertEqual(f_u_t(u'"escape\\\\char"'), u'escape\\char')
        self.assertEqual(f_u_t(u'"valid\\n\\tescapes"'), u'valid\n\tescapes')
        self.assertEqual(f_u_t(u'"raw\n\tspace"'), u'raw\n\tspace')
        self.assertEqual(f_u_t(u'"invalid\\escape"'), u'invalid\\escape')
        self.assertEqual(f_u_t(u'"end escape\\"'), u'end escape\\')
        self.assertEqual(f_u_t(u'"octal\\040escape"'), u'octal escape')
        self.assertEqual(f_u_t(u'"invalid\\840octal"'), u'invalid\\840octal')
        self.assertEqual(f_u_t(u'"unicode\\u1234escape"'), u'unicode\u1234escape')
        self.assertEqual(f_u_t(u'"raw\u1234unicode"'), u'raw\u1234unicode')
        self.assertEqual(f_u_t(u'"invalid\\u12g4unicode"'), u'invalid\\u12g4unicode')
        self.assertEqual(f_u_t(u'"invalid_uni\\u123"'), u'invalid_uni\\u123')

        with self.assertRaises(RuntimeError):
            f_u_t(u'unquoted')
        with self.assertRaises(RuntimeError):
            f_u_t(u'"unterminated')
        with self.assertRaises(RuntimeError):
            f_u_t(u'"mismatch\'')
