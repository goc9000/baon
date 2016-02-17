# baon/core/utils/__tests__/test_baon_utils.py
#
# (C) Copyright 2012-present  Cristian Dinu <goc9000@gmail.com>
#
# This file is part of BAON.
#
# Licensed under the GPL-3


from unittest import TestCase

from baon.core.parsing.__errors__.rule_parse_errors import StringLiteralNotQuotedProperlyError
from baon.core.utils.baon_utils import decode_baon_string_literal


class TestBaonUtilsPy(TestCase):
    def test_decode_baon_string_literal(self):
        for input, output in (
            ('"double quotes"', 'double quotes'),
            ("'single quotes'", 'single quotes'),
            ('"dodgy"quote"', 'dodgy"quote'),
            ('"escaped""double quote"', 'escaped"double quote'),
            ("'escaped'single quote'", "escaped'single quote"),
            ('"raw\n\tchars\u1234"', "raw\n\tchars\u1234"),
            ('"backslash\\does\\not\\escape\\"', "backslash\\does\\not\\escape\\"),
            ('"no unicode\\u1234escape"', 'no unicode\\u1234escape'),
        ):
            with self.subTest(input=input):
                self.assertEqual(decode_baon_string_literal(input), output)

        with self.assertRaises(StringLiteralNotQuotedProperlyError):
            decode_baon_string_literal('unquoted')
        with self.assertRaises(StringLiteralNotQuotedProperlyError):
            decode_baon_string_literal('"unterminated')
        with self.assertRaises(StringLiteralNotQuotedProperlyError):
            decode_baon_string_literal('"mismatch\'')
