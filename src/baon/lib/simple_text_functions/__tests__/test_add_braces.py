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
    def test_paras(self):
        f_u_t = baon.lib.simple_text_functions.add_braces.paras

        self.assertEqual(f_u_t(u'abc'), u'(abc)')
        self.assertEqual(f_u_t(u'  some text   '), u'  (some text)   ')
        self.assertEqual(f_u_t(u'   '), u'   ()')
        self.assertEqual(f_u_t(u'  (abc)  '), u'  ((abc))  ')

    def test_braces(self):
        f_u_t = baon.lib.simple_text_functions.add_braces.braces

        self.assertEqual(f_u_t(u'abc'), u'[abc]')
        self.assertEqual(f_u_t(u'  some text   '), u'  [some text]   ')
        self.assertEqual(f_u_t(u'   '), u'   []')
        self.assertEqual(f_u_t(u'  [abc]  '), u'  [[abc]]  ')

    def test_curlies(self):
        f_u_t = baon.lib.simple_text_functions.add_braces.curlies

        self.assertEqual(f_u_t(u'abc'), u'{abc}')
        self.assertEqual(f_u_t(u'  some text   '), u'  {some text}   ')
        self.assertEqual(f_u_t(u'   '), u'   {}')
        self.assertEqual(f_u_t(u'  {abc}  '), u'  {{abc}}  ')
