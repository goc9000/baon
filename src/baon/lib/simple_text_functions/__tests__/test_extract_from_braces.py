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

        self.assertEqual(f_u_t('(abc)'), 'abc')
        self.assertEqual(f_u_t('abc (def)'), 'def')
        self.assertEqual(f_u_t('abc (def)'), 'def')
        self.assertEqual(f_u_t('abc (  def ghi  )'), '  def ghi  ')
        self.assertEqual(f_u_t('abc (def) (ghi)'), 'def')
        self.assertEqual(f_u_t('abc def ghi'), '')
        self.assertEqual(f_u_t('abc [def] {ghi}'), '')
        self.assertEqual(f_u_t('abc ((def))'), 'def')
        self.assertEqual(f_u_t('abc (def'), '')
        self.assertEqual(f_u_t('((abc)'), 'abc')
        self.assertEqual(f_u_t('))()()'), '')

    def test_inbraces(self):
        f_u_t = baon.lib.simple_text_functions.extract_from_braces.inbraces

        self.assertEqual(f_u_t('[abc]'), 'abc')
        self.assertEqual(f_u_t('abc [def]'), 'def')
        self.assertEqual(f_u_t('abc [def]'), 'def')
        self.assertEqual(f_u_t('abc [  def ghi  ]'), '  def ghi  ')
        self.assertEqual(f_u_t('abc [def] [ghi]'), 'def')
        self.assertEqual(f_u_t('abc def ghi'), '')
        self.assertEqual(f_u_t('abc (def) {ghi}'), '')
        self.assertEqual(f_u_t('abc [[def]]'), 'def')
        self.assertEqual(f_u_t('abc [def'), '')
        self.assertEqual(f_u_t('[[abc]'), 'abc')
        self.assertEqual(f_u_t(']][][]'), '')

    def test_incurlies(self):
        f_u_t = baon.lib.simple_text_functions.extract_from_braces.incurlies

        self.assertEqual(f_u_t('{abc}'), 'abc')
        self.assertEqual(f_u_t('abc {def}'), 'def')
        self.assertEqual(f_u_t('abc {def}'), 'def')
        self.assertEqual(f_u_t('abc {  def ghi  }'), '  def ghi  ')
        self.assertEqual(f_u_t('abc {def} {ghi}'), 'def')
        self.assertEqual(f_u_t('abc def ghi'), '')
        self.assertEqual(f_u_t('abc [def] (ghi)'), '')
        self.assertEqual(f_u_t('abc {{def}}'), 'def')
        self.assertEqual(f_u_t('abc {def'), '')
        self.assertEqual(f_u_t('{{abc}'), 'abc')
        self.assertEqual(f_u_t('}}{}{}'), '')
