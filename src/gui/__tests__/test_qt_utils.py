# gui/__tests__/test_qt_utils.py
#
# (C) Copyright 2012-present  Cristian Dinu <goc9000@gmail.com>
#
# This file is part of BAON.
#
# Licensed under the GPL-3


from unittest import TestCase

from gui.qt_utils import parse_qcolor


class TestQtUtilsPy(TestCase):
    def test_parse_qcolor(self):
        f_u_t = parse_qcolor
        self.assertEqual(f_u_t((64, 128, 255)).getRgb(), (64, 128, 255, 255))
        self.assertEqual(f_u_t((64, 128, 255, 32)).getRgb(), (64, 128, 255, 32))
        self.assertEqual(f_u_t((0.25, 0.5, 1.0)).getRgb(), (64, 128, 255, 255))
        self.assertEqual(f_u_t('#4080ff').getRgb(), (64, 128, 255, 255))
        self.assertEqual(f_u_t('#4080ff20').getRgb(), (64, 128, 255, 32))
        self.assertEqual(f_u_t('#4080Ff').getRgb(), (64, 128, 255, 255))
        self.assertEqual(f_u_t('4080ff').getRgb(), (64, 128, 255, 255))
        self.assertEqual(f_u_t('red').getRgb(), (255, 0, 0, 255))
        self.assertEqual(f_u_t('Red').getRgb(), (255, 0, 0, 255))
        self.assertEqual(f_u_t({'r': 64, 'g': 128, 'b': 255}).getRgb(), (64, 128, 255, 255))
        self.assertEqual(f_u_t({'r': 64, 'g': 128, 'b': 255, 'a': 32}).getRgb(), (64, 128, 255, 32))
        self.assertEqual(f_u_t({'r': 64, 'G': 128, 'b': 255, 'A': 32}).getRgb(), (64, 128, 255, 32))
        self.assertEqual(f_u_t({'reD': 64, 'Green': 128, 'bLuE': 255, 'ALPHA': 32}).getRgb(), (64, 128, 255, 32))
        self.assertEqual(f_u_t({'r': 0.25, 'g': 0.5, 'b': 1.0}).getRgb(), (64, 128, 255, 255))
        self.assertEqual(f_u_t({'red': 64, 'g': 128, 'b': 255, 'alpha': 32}).getRgb(), (64, 128, 255, 32))

        with self.assertRaises(RuntimeError):
            f_u_t(123)
        with self.assertRaises(RuntimeError):
            f_u_t((64, 128))
        with self.assertRaises(RuntimeError):
            f_u_t((64, 128, 255, 32, 250))
        with self.assertRaises(RuntimeError):
            f_u_t((64, 128.0, 255))
        with self.assertRaises(RuntimeError):
            f_u_t((64, -1, 255))
        with self.assertRaises(RuntimeError):
            f_u_t((64, 0, 256))
        with self.assertRaises(RuntimeError):
            f_u_t(('64', '128', '255'))
        with self.assertRaises(RuntimeError):
            f_u_t('#4080gf')
        with self.assertRaises(RuntimeError):
            f_u_t('#4080')
        with self.assertRaises(RuntimeError):
            f_u_t('bogusname')
        with self.assertRaises(RuntimeError):
            f_u_t('#4080ff80ff')
        with self.assertRaises(RuntimeError):
            f_u_t({'r': 64, 'b': 255})
        with self.assertRaises(RuntimeError):
            f_u_t({'r': 64, 'g': 100, 'b': 255, 'extra': 4})
        with self.assertRaises(RuntimeError):
            f_u_t({'r': 64, 'red': 32, 'g': 100, 'b': 255})
        with self.assertRaises(RuntimeError):
            f_u_t({'r': 64, 'g': 128.0, 'b': 255})
