# baon/logic/__tests__/test_grammar_utils.py
#
# (C) Copyright 2012-present  Cristian Dinu <goc9000@gmail.com>
#
# This file is part of BAON.
#
# Licensed under the GPL-3


from unittest import TestCase

from baon.logic.grammar_utils import to_title_case, find_words_and_separators, SimplePhrasePart


class TestGrammarUtilsPy(TestCase):
    def test_to_title_case(self):
        f_u_t = to_title_case

        self.assertEqual(f_u_t(u'simple title'), u'Simple Title')
        self.assertEqual(f_u_t(u'SIMPLE TITLE'), u'Simple Title')
        self.assertEqual(f_u_t(u'Simple Title'), u'Simple Title')
        self.assertEqual(f_u_t(u'  sIMPlE TItle'), u'  Simple Title')
        self.assertEqual(f_u_t(u'\u0219tima casei'), u'\u0218tima Casei')  # unicode
        self.assertEqual(f_u_t(u'system of a down'), u'System of a Down')  # particle words
        self.assertEqual(f_u_t(u'system Of A down'), u'System of a Down')  # uncapitalize particle words
        self.assertEqual(f_u_t(u'on a plain'), u'On a Plain')  # particle at start
        self.assertEqual(f_u_t(u'leading me on'), u'Leading Me On')  # particle at end
        self.assertEqual(f_u_t(u'on and off'), u'On and Off')  # particle at start and end
        self.assertEqual(f_u_t(u'flow my tears, the policeman said'),
                         u'Flow My Tears, the Policeman Said')  # particle words around commas
        self.assertEqual(f_u_t(u'Theme by Rimsky-Korsakov'), u'Theme by Rimsky-Korsakov')  # preserve compound names
        self.assertEqual(f_u_t(u"MacCleod's Theme"), u"MacCleod's Theme")  # preserve Mc/Mac names
        self.assertEqual(f_u_t(u"We'll always have VALIS"), u"We'll Always Have VALIS")  # preserve acronyms

    def test_find_words_and_separators(self):
        f_u_t = find_words_and_separators

        self.assertEqual(f_u_t(u"Brazil (1984)"), [
            SimplePhrasePart(is_word=True, content=u'Brazil', ws_before=u'', ws_after=u' '),
            SimplePhrasePart(is_word=False, content=u'(', ws_before=u' ', ws_after=u''),
            SimplePhrasePart(is_word=True, content=u'1984', ws_before=u'', ws_after=u''),
            SimplePhrasePart(is_word=False, content=u')', ws_before=u'', ws_after=u''),
        ])
        self.assertEqual(f_u_t(u"Achille-Claude Debussy"), [
            SimplePhrasePart(is_word=True, content=u'Achille-Claude', ws_before=u'', ws_after=u' '),
            SimplePhrasePart(is_word=True, content=u'Debussy', ws_before=u' ', ws_after=u''),
        ])
        self.assertEqual(f_u_t(u"Allegro assai - Lente -- Moderato"), [
            SimplePhrasePart(is_word=True, content=u'Allegro', ws_before=u'', ws_after=u' '),
            SimplePhrasePart(is_word=True, content=u'assai', ws_before=u' ', ws_after=u' '),
            SimplePhrasePart(is_word=False, content=u'-', ws_before=u' ', ws_after=u' '),
            SimplePhrasePart(is_word=True, content=u'Lente', ws_before=u' ', ws_after=u' '),
            SimplePhrasePart(is_word=False, content=u'--', ws_before=u' ', ws_after=u' '),
            SimplePhrasePart(is_word=True, content=u'Moderato', ws_before=u' ', ws_after=u''),
        ])
        self.assertEqual(f_u_t(u"It's a Wonderful World"), [
            SimplePhrasePart(is_word=True, content=u"It's", ws_before=u'', ws_after=u' '),
            SimplePhrasePart(is_word=True, content=u'a', ws_before=u' ', ws_after=u' '),
            SimplePhrasePart(is_word=True, content=u'Wonderful', ws_before=u' ', ws_after=u' '),
            SimplePhrasePart(is_word=True, content=u'World', ws_before=u' ', ws_after=u''),
        ])
        self.assertEqual(f_u_t(u"Allegro. Lente."), [
            SimplePhrasePart(is_word=True, content=u'Allegro', ws_before=u'', ws_after=u''),
            SimplePhrasePart(is_word=False, content=u'.', ws_before=u'', ws_after=u' '),
            SimplePhrasePart(is_word=True, content=u'Lente', ws_before=u' ', ws_after=u''),
            SimplePhrasePart(is_word=False, content=u'.', ws_before=u'', ws_after=u''),
        ])
        self.assertEqual(f_u_t(u"Spy vs. Spy"), [
            SimplePhrasePart(is_word=True, content=u'Spy', ws_before=u'', ws_after=u' '),
            SimplePhrasePart(is_word=True, content=u'vs.', ws_before=u' ', ws_after=u' '),
            SimplePhrasePart(is_word=True, content=u'Spy', ws_before=u' ', ws_after=u''),
        ])
        self.assertEqual(f_u_t(u"Spy vs. Spy", detect_abbreviations=False), [
            SimplePhrasePart(is_word=True, content=u'Spy', ws_before=u'', ws_after=u' '),
            SimplePhrasePart(is_word=True, content=u'vs', ws_before=u' ', ws_after=u''),
            SimplePhrasePart(is_word=False, content=u'.', ws_before=u'', ws_after=u' '),
            SimplePhrasePart(is_word=True, content=u'Spy', ws_before=u' ', ws_after=u''),
        ])
        self.assertEqual(f_u_t(u"Wait... what?!"), [
            SimplePhrasePart(is_word=True, content=u'Wait', ws_before=u'', ws_after=u''),
            SimplePhrasePart(is_word=False, content=u'...', ws_before=u'', ws_after=u' '),
            SimplePhrasePart(is_word=True, content=u'what', ws_before=u' ', ws_after=u''),
            SimplePhrasePart(is_word=False, content=u'?!', ws_before=u'', ws_after=u''),
        ])
