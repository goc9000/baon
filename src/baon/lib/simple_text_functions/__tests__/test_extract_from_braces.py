# baon/lib/simple_text_functions/__tests__/test_extract_from_braces.py
#
# (C) Copyright 2012-present  Cristian Dinu <goc9000@gmail.com>
#
# This file is part of BAON.
#
# Licensed under the GPL-3


from unittest import TestCase

import baon.lib.simple_text_functions.extract_from_braces


class TestExtractFromBracesFunctions(TestCase):
    def test_inparas(self):
        f_u_t = baon.lib.simple_text_functions.extract_from_braces.inparas

        self.assertEqual(f_u_t(u'(abc)'), u'abc')
        self.assertEqual(f_u_t(u'abc (def)'), u'def')
        self.assertEqual(f_u_t(u'abc (def)'), u'def')
        self.assertEqual(f_u_t(u'abc (  def ghi  )'), u'  def ghi  ')
        self.assertEqual(f_u_t(u'abc (def) (ghi)'), u'def')
        self.assertEqual(f_u_t(u'abc def ghi'), u'')
        self.assertEqual(f_u_t(u'abc [def] {ghi}'), u'')
        self.assertEqual(f_u_t(u'abc ((def))'), u'def')
        self.assertEqual(f_u_t(u'abc (def'), u'')
        self.assertEqual(f_u_t(u'((abc)'), u'abc')
        self.assertEqual(f_u_t(u'))()()'), u'')

    def test_inbraces(self):
        f_u_t = baon.lib.simple_text_functions.extract_from_braces.inbraces

        self.assertEqual(f_u_t(u'[abc]'), u'abc')
        self.assertEqual(f_u_t(u'abc [def]'), u'def')
        self.assertEqual(f_u_t(u'abc [def]'), u'def')
        self.assertEqual(f_u_t(u'abc [  def ghi  ]'), u'  def ghi  ')
        self.assertEqual(f_u_t(u'abc [def] [ghi]'), u'def')
        self.assertEqual(f_u_t(u'abc def ghi'), u'')
        self.assertEqual(f_u_t(u'abc (def) {ghi}'), u'')
        self.assertEqual(f_u_t(u'abc [[def]]'), u'def')
        self.assertEqual(f_u_t(u'abc [def'), u'')
        self.assertEqual(f_u_t(u'[[abc]'), u'abc')
        self.assertEqual(f_u_t(u']][][]'), u'')

    def test_incurlies(self):
        f_u_t = baon.lib.simple_text_functions.extract_from_braces.incurlies

        self.assertEqual(f_u_t(u'{abc}'), u'abc')
        self.assertEqual(f_u_t(u'abc {def}'), u'def')
        self.assertEqual(f_u_t(u'abc {def}'), u'def')
        self.assertEqual(f_u_t(u'abc {  def ghi  }'), u'  def ghi  ')
        self.assertEqual(f_u_t(u'abc {def} {ghi}'), u'def')
        self.assertEqual(f_u_t(u'abc def ghi'), u'')
        self.assertEqual(f_u_t(u'abc [def] (ghi)'), u'')
        self.assertEqual(f_u_t(u'abc {{def}}'), u'def')
        self.assertEqual(f_u_t(u'abc {def'), u'')
        self.assertEqual(f_u_t(u'{{abc}'), u'abc')
        self.assertEqual(f_u_t(u'}}{}{}'), u'')
