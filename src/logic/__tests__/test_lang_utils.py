# logic/__tests__/test_lang_utils.py
#
# (C) Copyright 2012-present  Cristian Dinu <goc9000@gmail.com>
#
# This file is part of BAON.
#
# Licensed under the GPL-3


from unittest import TestCase
from itertools import count

from logic.lang_utils import is_string, is_arrayish, is_dictish


class TestLangUtilsPy(TestCase):
    def test_is_string(self):
        f_u_t = is_string
        self.assertTrue(f_u_t('string'))
        self.assertTrue(f_u_t(u'unicode\u1234'))
        self.assertFalse(f_u_t(123))
        self.assertFalse(f_u_t(['a', 'b', 'c']))
        self.assertFalse(f_u_t({'a': 'b', 'b': 'c'}))

    def test_is_arrayish(self):
        f_u_t = is_arrayish
        self.assertTrue(f_u_t([1, 2, 3]))
        self.assertTrue(f_u_t((1, 2, 3)))
        self.assertFalse(f_u_t(123))
        self.assertFalse(f_u_t('string'))
        self.assertFalse(f_u_t(count(1)))
        self.assertFalse(f_u_t({'a': 3, 'b': 4}))
        self.assertFalse(f_u_t({0: 1, 1: 2, 2: 3}))

    def test_is_dictish(self):
        f_u_t = is_dictish
        self.assertTrue(f_u_t({'a': 3, 'b': 4}))
        self.assertTrue(f_u_t({0: 1, 1: 2, 2: 3}))
        self.assertFalse(f_u_t([1, 2, 3]))
        self.assertFalse(f_u_t((1, 2, 3)))
        self.assertFalse(f_u_t(123))
        self.assertFalse(f_u_t('string'))
        self.assertFalse(f_u_t(count(1)))
