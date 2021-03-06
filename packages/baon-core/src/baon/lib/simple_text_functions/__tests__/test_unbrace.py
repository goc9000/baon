# baon/lib/simple_text_functions/__tests__/test_unbrace.py
#
# (C) Copyright 2012-present  Cristian Dinu <goc9000@gmail.com>
#
# This file is part of BAON.
#
# Licensed under the GPL-3


from unittest import TestCase

import baon.lib.simple_text_functions.unbrace


class TestUnbrace(TestCase):
    def test_unbrace(self):
        f_u_t = baon.lib.simple_text_functions.unbrace.unbrace

        self.assertEqual(f_u_t('abc'), 'abc')
        self.assertEqual(f_u_t('(some text)'), 'some text')
        self.assertEqual(f_u_t('   (some text)  '), '   some text  ')
        self.assertEqual(f_u_t(' [some text] '), ' some text ')
        self.assertEqual(f_u_t(' {some text} '), ' some text ')
        self.assertEqual(f_u_t('some (text)'), 'some text')
        self.assertEqual(f_u_t('(some) (text)'), 'some text')
        self.assertEqual(f_u_t('(some) [text]'), 'some text')
        self.assertEqual(f_u_t('s({ome [te}}xt)'), 'some text')
