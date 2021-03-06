# baon/core/utils/__tests__/test_str_utils.py
#
# (C) Copyright 2012-present  Cristian Dinu <goc9000@gmail.com>
#
# This file is part of BAON.
#
# Licensed under the GPL-3


from unittest import TestCase

from baon.core.utils.str_utils import is_quoted_string


class TestStrUtilsPy(TestCase):
    def test_is_quoted_string(self):
        f_u_t = is_quoted_string
        self.assertTrue(f_u_t('"double quotes"'))
        self.assertTrue(f_u_t("'single quotes'"))
        self.assertTrue(f_u_t('""'))
        self.assertTrue(f_u_t('"dodgy"but"allowed"'))
        self.assertFalse(f_u_t('unquoted'))
        self.assertFalse(f_u_t('"unterminated'))
        self.assertFalse(f_u_t('"mismatch\''))
        self.assertFalse(f_u_t('"trailing"x'))
        self.assertFalse(f_u_t(''))
        self.assertFalse(f_u_t('x'))
        self.assertFalse(f_u_t('"'))
