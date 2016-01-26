# baon/ui/qt4_gui/utils/__tests__/test_parse_qcolor.py
#
# (C) Copyright 2012-present  Cristian Dinu <goc9000@gmail.com>
#
# This file is part of BAON.
#
# Licensed under the GPL-3


from unittest import TestCase

from baon.ui.qt4_gui.utils.parse_qcolor import parse_qcolor


class TestParseQColorPy(TestCase):
    def test_parse_qcolor(self):
        for spec, expected_rgba in (
            ((64, 128, 255), (64, 128, 255, 255)),
            ((64, 128, 255, 32), (64, 128, 255, 32)),
            ((0.25, 0.5, 1.0), (64, 128, 255, 255)),
            ('#4080ff', (64, 128, 255, 255)),
            ('#4080ff20', (64, 128, 255, 32)),
            ('#4080Ff', (64, 128, 255, 255)),
            ('4080ff', (64, 128, 255, 255)),
            ('red', (255, 0, 0, 255)),
            ('Red', (255, 0, 0, 255)),
            ({'r': 64, 'g': 128, 'b': 255}, (64, 128, 255, 255)),
            ({'r': 64, 'g': 128, 'b': 255, 'a': 32}, (64, 128, 255, 32)),
            ({'r': 64, 'G': 128, 'b': 255, 'A': 32}, (64, 128, 255, 32)),
            ({'reD': 64, 'Green': 128, 'bLuE': 255, 'ALPHA': 32}, (64, 128, 255, 32)),
            ({'r': 0.25, 'g': 0.5, 'b': 1.0}, (64, 128, 255, 255)),
            ({'red': 64, 'g': 128, 'b': 255, 'alpha': 32}, (64, 128, 255, 32)),
        ):
            with self.subTest(color_spec=spec, expected_rgba=expected_rgba):
                self.assertEqual(parse_qcolor(spec).getRgb(), expected_rgba)

    def test_parse_qcolor_invalid(self):
        for spec in (
            123,
            (64, 128),
            (64, 128, 255, 32, 250),
            (64, 128.0, 255),
            (64, -1, 255),
            (64, 0, 256),
            ('64', '128', '255'),
            '#4080gf',
            '#4080',
            'bogusname',
            '#4080ff80ff',
            {'r': 64, 'b': 255},
            {'r': 64, 'g': 100, 'b': 255, 'extra': 4},
            {'r': 64, 'red': 32, 'g': 100, 'b': 255},
            {'r': 64, 'g': 128.0, 'b': 255},
        ):
            with self.subTest(color_spec=spec):
                with self.assertRaises(ValueError):
                    parse_qcolor(spec)
