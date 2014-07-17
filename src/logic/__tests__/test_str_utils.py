# logic/__tests__/test_str_utils.py
#
# (C) Copyright 2012-present  Cristian Dinu <goc9000@gmail.com>
#
# This file is part of BAON.
#
# Licensed under the GPL-3


from unittest import TestCase

from logic.str_utils import is_quoted_string


class TestStrUtilsPy(TestCase):
    def test_is_quoted_string(self):
        f_u_t = is_quoted_string
        self.assertTrue(f_u_t(u'"double quotes"'))
        self.assertTrue(f_u_t(u"'single quotes'"))
        self.assertTrue(f_u_t(u'""'))
        self.assertTrue(f_u_t(u'"dodgy"but"allowed"'))
        self.assertFalse(f_u_t(u'unquoted'))
        self.assertFalse(f_u_t(u'"unterminated'))
        self.assertFalse(f_u_t(u'"mismatch\''))
        self.assertFalse(f_u_t(u'"trailing"x'))
        self.assertFalse(f_u_t(u''))
        self.assertFalse(f_u_t(u'x'))
        self.assertFalse(f_u_t(u'"'))
