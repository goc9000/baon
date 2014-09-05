# baon/lib/simple_text_functions/__tests__/test_whitespace.py
#
# (C) Copyright 2012-present  Cristian Dinu <goc9000@gmail.com>
#
# This file is part of BAON.
#
# Licensed under the GPL-3


from unittest import TestCase

import baon.lib.simple_text_functions.whitespace


class TestWhitespaceFunctions(TestCase):
    def test_trim(self):
        f_u_t = baon.lib.simple_text_functions.whitespace.trim

        self.assertEqual(f_u_t(u' abc  '), u'abc')
        self.assertEqual(f_u_t(u'  some text   '), u'some text')
        self.assertEqual(f_u_t(u'inner   space   '), u'inner   space')