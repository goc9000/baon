# baon/core/ast/matches/pattern/__tests__/test_FormatMatch.py
#
# (C) Copyright 2012-present  Cristian Dinu <goc9000@gmail.com>
#
# This file is part of BAON.
#
# Licensed under the GPL-3


from baon.core.ast.matches.__tests__.MatchTestCase import MatchTestCase
from baon.core.ast.matches.pattern.FormatMatch import FormatMatch


class TestFormatMatch(MatchTestCase):

    def test_format_match_ws(self):
        self._test_unique_match(
            text='abcdef',
            match=FormatMatch('ws'),
            expected_solution={'matched_text': '', 'position': 0})
        self._test_unique_match(
            text='    abcdef',
            match=FormatMatch('ws'),
            expected_solution={'matched_text': '    ', 'position': 4})
        self._test_no_match(
            text='abcdef',
            match=FormatMatch('ws', 3))
        self._test_unique_match(
            text='    abcdef',
            match=FormatMatch('ws', 3),
            expected_solution={'matched_text': '   ', 'position': 3})

    def test_format_match_d(self):
        self._test_unique_match(
            text='0123.',
            match=FormatMatch('d'),
            expected_solution={'matched_text': '0123', 'position': 4})
        self._test_unique_match(
            text='0123.',
            match=FormatMatch('d', 2),
            expected_solution={'matched_text': '01', 'position': 2})
        self._test_no_match(
            text='0123.',
            match=FormatMatch('d', 5))
        self._test_no_match(
            text='',
            match=FormatMatch('d'))
        self._test_no_match(
            text='abc0123.',
            match=FormatMatch('d'))
        self._test_unique_match(
            text='   123.',
            match=FormatMatch('d'),
            expected_solution={'matched_text': '   123', 'position': 6})
        self._test_unique_match(
            text='   123.',
            match=FormatMatch('d', 2),
            expected_solution={'matched_text': '   12', 'position': 5})
        self._test_no_match(
            text='   123.',
            match=FormatMatch('d', 5))

    def test_format_match_c(self):
        self._test_unique_match(
            text='abc',
            match=FormatMatch('c'),
            expected_solution={'matched_text': 'a', 'position': 1})
        self._test_unique_match(
            text=' ',
            match=FormatMatch('c'),
            expected_solution={'matched_text': ' ', 'position': 1})
        self._test_unique_match(
            text=' ef',
            match=FormatMatch('c'),
            expected_solution={'matched_text': ' ', 'position': 1})
        self._test_no_match(
            text='',
            match=FormatMatch('c'))
        self._test_unique_match(
            text='abcdef',
            match=FormatMatch('c', 3),
            expected_solution={'matched_text': 'abc', 'position': 3})
        self._test_unique_match(
            text=' efg',
            match=FormatMatch('c', 3),
            expected_solution={'matched_text': ' ef', 'position': 3})
        self._test_no_match(
            text='ab',
            match=FormatMatch('c', 3))

    def test_format_match_s(self):
        self._test_unique_match(
            text='abcdef  ghi',
            match=FormatMatch('s'),
            expected_solution={'matched_text': 'abcdef', 'position': 6})
        self._test_unique_match(
            text='abc123-q.xy  ghi',
            match=FormatMatch('s'),
            expected_solution={'matched_text': 'abc123-q.xy', 'position': 11})
        self._test_unique_match(
            text='   abcdef  ghi',
            match=FormatMatch('s'),
            expected_solution={'matched_text': '   abcdef', 'position': 9})
        self._test_no_match(
            text='',
            match=FormatMatch('s'))
        self._test_no_match(
            text='   ',
            match=FormatMatch('s'))
        self._test_unique_match(
            text='abcdef  ghi',
            match=FormatMatch('s', 3),
            expected_solution={'matched_text': 'abc', 'position': 3})
        self._test_unique_match(
            text='   abcdef  ghi',
            match=FormatMatch('s', 3),
            expected_solution={'matched_text': '   abc', 'position': 6})
        self._test_no_match(
            text='abc defghi',
            match=FormatMatch('s', 5))
        self._test_no_match(
            text='   abc defghi',
            match=FormatMatch('s', 5))
        self._test_no_match(
            text='    ',
            match=FormatMatch('s', 3))

    def test_format_match_paras(self):
        self._test_unique_match(
            text='(abc def)hij',
            match=FormatMatch('paras'),
            expected_solution={'matched_text': '(abc def)', 'position': 9})
        self._test_unique_match(
            text='()',
            match=FormatMatch('paras'),
            expected_solution={'matched_text': '()', 'position': 2})
        self._test_unique_match(
            text='   (abc def)hij',
            match=FormatMatch('paras'),
            expected_solution={'matched_text': '   (abc def)', 'position': 12})
        self._test_unique_match(
            text='   (abc def)hij',
            match=FormatMatch('paras', 7),
            expected_solution={'matched_text': '   (abc def)', 'position': 12})
        self._test_no_match(
            text='   (abc def)hij',
            match=FormatMatch('paras', 6))
        self._test_no_match(
            text='   (abc def)hij',
            match=FormatMatch('paras', 8))
        self._test_no_match(
            text='abc',
            match=FormatMatch('paras'))
        self._test_no_match(
            text='abc(1934)',
            match=FormatMatch('paras'))
        self._test_no_match(
            text='(abc',
            match=FormatMatch('paras'))

    def test_format_match_braces(self):
        self._test_unique_match(
            text='[abc def]hij',
            match=FormatMatch('braces'),
            expected_solution={'matched_text': '[abc def]', 'position': 9})
        self._test_unique_match(
            text='[]',
            match=FormatMatch('braces'),
            expected_solution={'matched_text': '[]', 'position': 2})
        self._test_unique_match(
            text='   [abc def]hij',
            match=FormatMatch('braces'),
            expected_solution={'matched_text': '   [abc def]', 'position': 12})
        self._test_unique_match(
            text='   [abc def]hij',
            match=FormatMatch('braces', 7),
            expected_solution={'matched_text': '   [abc def]', 'position': 12})
        self._test_no_match(
            text='   [abc def]hij',
            match=FormatMatch('braces', 6))
        self._test_no_match(
            text='   [abc def]hij',
            match=FormatMatch('braces', 8))
        self._test_no_match(
            text='abc',
            match=FormatMatch('braces'))
        self._test_no_match(
            text='abc[1934]',
            match=FormatMatch('braces'))
        self._test_no_match(
            text='[abc',
            match=FormatMatch('braces'))

    def test_format_match_curlies(self):
        self._test_unique_match(
            text='{abc def}hij',
            match=FormatMatch('curlies'),
            expected_solution={'matched_text': '{abc def}', 'position': 9})
        self._test_unique_match(
            text='{}',
            match=FormatMatch('curlies'),
            expected_solution={'matched_text': '{}', 'position': 2})
        self._test_unique_match(
            text='   {abc def}hij',
            match=FormatMatch('curlies'),
            expected_solution={'matched_text': '   {abc def}', 'position': 12})
        self._test_unique_match(
            text='   {abc def}hij',
            match=FormatMatch('curlies', 7),
            expected_solution={'matched_text': '   {abc def}', 'position': 12})
        self._test_no_match(
            text='   {abc def}hij',
            match=FormatMatch('curlies', 6))
        self._test_no_match(
            text='   {abc def}hij',
            match=FormatMatch('curlies', 8))
        self._test_no_match(
            text='abc',
            match=FormatMatch('curlies'))
        self._test_no_match(
            text='abc{1934}',
            match=FormatMatch('curlies'))
        self._test_no_match(
            text='{abc',
            match=FormatMatch('curlies'))

    def test_format_match_inparas(self):
        self._test_no_match(
            text='ab(cde fg)hi',
            match=FormatMatch('inparas'))
        self._test_unique_match(
            text='ab(cde fg)hi',
            position=3,
            match=FormatMatch('inparas'),
            expected_solution={'matched_text': 'cde fg', 'position': 9})
        self._test_unique_match(
            text='ab(cde fg)hi',
            position=3,
            match=FormatMatch('inparas', 6),
            expected_solution={'matched_text': 'cde fg', 'position': 9})
        self._test_no_match(
            text='ab(cde fg)hi',
            position=3,
            match=FormatMatch('inparas', 5))
        self._test_no_match(
            text='ab(cde fg)hi',
            position=3,
            match=FormatMatch('inparas', 7))

    def test_format_match_inbraces(self):
        self._test_no_match(
            text='ab[cde fg]hi',
            match=FormatMatch('inbraces'))
        self._test_unique_match(
            text='ab[cde fg]hi',
            position=3,
            match=FormatMatch('inbraces'),
            expected_solution={'matched_text': 'cde fg', 'position': 9})
        self._test_unique_match(
            text='ab[cde fg]hi',
            position=3,
            match=FormatMatch('inbraces', 6),
            expected_solution={'matched_text': 'cde fg', 'position': 9})
        self._test_no_match(
            text='ab[cde fg]hi',
            position=3,
            match=FormatMatch('inbraces', 5))
        self._test_no_match(
            text='ab[cde fg]hi',
            position=3,
            match=FormatMatch('inbraces', 7))

    def test_format_match_incurlies(self):
        self._test_no_match(
            text='ab{cde fg}hi',
            match=FormatMatch('incurlies'))
        self._test_unique_match(
            text='ab{cde fg}hi',
            position=3,
            match=FormatMatch('incurlies'),
            expected_solution={'matched_text': 'cde fg', 'position': 9})
        self._test_unique_match(
            text='ab{cde fg}hi',
            position=3,
            match=FormatMatch('incurlies', 6),
            expected_solution={'matched_text': 'cde fg', 'position': 9})
        self._test_no_match(
            text='ab{cde fg}hi',
            position=3,
            match=FormatMatch('incurlies', 5))
        self._test_no_match(
            text='ab{cde fg}hi',
            position=3,
            match=FormatMatch('incurlies', 7))

    def test_format_path(self):
        self._test_no_match(
            text='filename',
            match=FormatMatch('path'))
        self._test_unique_match(
            text='dir1/dir2/filename',
            match=FormatMatch('path'),
            expected_solution={'matched_text': 'dir1/dir2/', 'position': 10})
        self._test_unique_match(
            text='/dir1/filename',
            match=FormatMatch('path'),
            expected_solution={'matched_text': '/dir1/', 'position': 6})
        self._test_unique_match(
            text='   /dir1/filename',
            match=FormatMatch('path'),
            expected_solution={'matched_text': '   /dir1/', 'position': 9})
