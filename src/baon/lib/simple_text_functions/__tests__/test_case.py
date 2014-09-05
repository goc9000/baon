# baon/lib/simple_text_functions/__tests__/test_case.py
#
# (C) Copyright 2012-present  Cristian Dinu <goc9000@gmail.com>
#
# This file is part of BAON.
#
# Licensed under the GPL-3


from unittest import TestCase

import baon.lib.simple_text_functions.case


class TestCaseFunctions(TestCase):
    def test_upper(self):
        f_u_t = baon.lib.simple_text_functions.case.upper

        self.assertEqual(f_u_t(u'abc'), u'ABC')
        self.assertEqual(f_u_t(u'  SoMe woRDs  '), u'  SOME WORDS  ')
        self.assertEqual(f_u_t(u"\u00e2\u0103\u00ee\u0219\u021b\u00c2\u0102\u00ce\u0218\u021a"),
                         u"\u00c2\u0102\u00ce\u0218\u021a\u00c2\u0102\u00ce\u0218\u021a")

    def test_lower(self):
        f_u_t = baon.lib.simple_text_functions.case.lower

        self.assertEqual(f_u_t(u'ABC'), u'abc')
        self.assertEqual(f_u_t(u'  SoMe woRDs  '), u'  some words  ')
        self.assertEqual(f_u_t(u"\u00e2\u0103\u00ee\u0219\u021b\u00c2\u0102\u00ce\u0218\u021a"),
                         u"\u00e2\u0103\u00ee\u0219\u021b\u00e2\u0103\u00ee\u0219\u021b")

    def test_title(self):
        f_u_t = baon.lib.simple_text_functions.case.title
        # TODO: test title
