# baon/core/utils/__tests__/test_grammar_utils.py
#
# (C) Copyright 2012-present  Cristian Dinu <goc9000@gmail.com>
#
# This file is part of BAON.
#
# Licensed under the GPL-3


from unittest import TestCase

from baon.core.utils.grammar_utils import to_title_case, find_words_and_separators, SimplePhrasePart


class TestGrammarUtilsPy(TestCase):
    def test_to_title_case(self):
        f_u_t = to_title_case

        self.assertEqual(f_u_t('simple title'), 'Simple Title')
        self.assertEqual(f_u_t('SIMPLE TITLE'), 'Simple Title')
        self.assertEqual(f_u_t('Simple Title'), 'Simple Title')
        self.assertEqual(f_u_t('  sIMPlE TItle'), '  Simple Title')
        self.assertEqual(f_u_t('\u0219tima casei'), '\u0218tima Casei')  # unicode
        self.assertEqual(f_u_t('system of a down'), 'System of a Down')  # particle words
        self.assertEqual(f_u_t('system Of A down'), 'System of a Down')  # uncapitalize particle words
        self.assertEqual(f_u_t('on a plain'), 'On a Plain')  # particle at start
        self.assertEqual(f_u_t('leading me on'), 'Leading Me On')  # particle at end
        self.assertEqual(f_u_t('on and off'), 'On and Off')  # particle at start and end
        self.assertEqual(f_u_t('flow my tears, the policeman said'),
                         'Flow My Tears, the Policeman Said')  # particle words around commas
        self.assertEqual(f_u_t('Theme by Rimsky-Korsakov'), 'Theme by Rimsky-Korsakov')  # preserve compound names
        self.assertEqual(f_u_t("MacCleod's Theme"), "MacCleod's Theme")  # preserve Mc/Mac names
        self.assertEqual(f_u_t("We'll always have VALIS"), "We'll Always Have VALIS")  # preserve acronyms

    def test_find_words_and_separators(self):
        f_u_t = find_words_and_separators

        self.assertEqual(f_u_t("Brazil (1984)"), [
            SimplePhrasePart(is_word=True, content='Brazil', ws_before='', ws_after=' '),
            SimplePhrasePart(is_word=False, content='(', ws_before=' ', ws_after=''),
            SimplePhrasePart(is_word=True, content='1984', ws_before='', ws_after=''),
            SimplePhrasePart(is_word=False, content=')', ws_before='', ws_after=''),
        ])
        self.assertEqual(f_u_t("Achille-Claude Debussy"), [
            SimplePhrasePart(is_word=True, content='Achille-Claude', ws_before='', ws_after=' '),
            SimplePhrasePart(is_word=True, content='Debussy', ws_before=' ', ws_after=''),
        ])
        self.assertEqual(f_u_t("Allegro assai - Lente -- Moderato"), [
            SimplePhrasePart(is_word=True, content='Allegro', ws_before='', ws_after=' '),
            SimplePhrasePart(is_word=True, content='assai', ws_before=' ', ws_after=' '),
            SimplePhrasePart(is_word=False, content='-', ws_before=' ', ws_after=' '),
            SimplePhrasePart(is_word=True, content='Lente', ws_before=' ', ws_after=' '),
            SimplePhrasePart(is_word=False, content='--', ws_before=' ', ws_after=' '),
            SimplePhrasePart(is_word=True, content='Moderato', ws_before=' ', ws_after=''),
        ])
        self.assertEqual(f_u_t("It's a Wonderful World"), [
            SimplePhrasePart(is_word=True, content="It's", ws_before='', ws_after=' '),
            SimplePhrasePart(is_word=True, content='a', ws_before=' ', ws_after=' '),
            SimplePhrasePart(is_word=True, content='Wonderful', ws_before=' ', ws_after=' '),
            SimplePhrasePart(is_word=True, content='World', ws_before=' ', ws_after=''),
        ])
        self.assertEqual(f_u_t("Allegro. Lente."), [
            SimplePhrasePart(is_word=True, content='Allegro', ws_before='', ws_after=''),
            SimplePhrasePart(is_word=False, content='.', ws_before='', ws_after=' '),
            SimplePhrasePart(is_word=True, content='Lente', ws_before=' ', ws_after=''),
            SimplePhrasePart(is_word=False, content='.', ws_before='', ws_after=''),
        ])
        self.assertEqual(f_u_t("Spy vs. Spy"), [
            SimplePhrasePart(is_word=True, content='Spy', ws_before='', ws_after=' '),
            SimplePhrasePart(is_word=True, content='vs.', ws_before=' ', ws_after=' '),
            SimplePhrasePart(is_word=True, content='Spy', ws_before=' ', ws_after=''),
        ])
        self.assertEqual(f_u_t("Spy vs. Spy", detect_abbreviations=False), [
            SimplePhrasePart(is_word=True, content='Spy', ws_before='', ws_after=' '),
            SimplePhrasePart(is_word=True, content='vs', ws_before=' ', ws_after=''),
            SimplePhrasePart(is_word=False, content='.', ws_before='', ws_after=' '),
            SimplePhrasePart(is_word=True, content='Spy', ws_before=' ', ws_after=''),
        ])
        self.assertEqual(f_u_t("Wait... what?!"), [
            SimplePhrasePart(is_word=True, content='Wait', ws_before='', ws_after=''),
            SimplePhrasePart(is_word=False, content='...', ws_before='', ws_after=' '),
            SimplePhrasePart(is_word=True, content='what', ws_before=' ', ws_after=''),
            SimplePhrasePart(is_word=False, content='?!', ws_before='', ws_after=''),
        ])
