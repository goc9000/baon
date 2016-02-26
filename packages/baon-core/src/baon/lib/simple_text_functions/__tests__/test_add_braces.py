# baon/lib/simple_text_functions/__tests__/test_add_braces.py
#
# (C) Copyright 2012-present  Cristian Dinu <goc9000@gmail.com>
#
# This file is part of BAON.
#
# Licensed under the GPL-3


from unittest import TestCase

import baon.lib.simple_text_functions.add_braces


class TestAddBracesFunctions(TestCase):
    def test_parens(self):
        f_u_t = baon.lib.simple_text_functions.add_braces.parens

        self.assertEqual(f_u_t('abc'), '(abc)')
        self.assertEqual(f_u_t('  some text   '), '  (some text)   ')
        self.assertEqual(f_u_t('   '), '   ()')
        self.assertEqual(f_u_t('  (abc)  '), '  ((abc))  ')

    def test_braces(self):
        f_u_t = baon.lib.simple_text_functions.add_braces.braces

        self.assertEqual(f_u_t('abc'), '[abc]')
        self.assertEqual(f_u_t('  some text   '), '  [some text]   ')
        self.assertEqual(f_u_t('   '), '   []')
        self.assertEqual(f_u_t('  [abc]  '), '  [[abc]]  ')

    def test_curlies(self):
        f_u_t = baon.lib.simple_text_functions.add_braces.curlies

        self.assertEqual(f_u_t('abc'), '{abc}')
        self.assertEqual(f_u_t('  some text   '), '  {some text}   ')
        self.assertEqual(f_u_t('   '), '   {}')
        self.assertEqual(f_u_t('  {abc}  '), '  {{abc}}  ')
