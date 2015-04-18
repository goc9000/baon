# baon/core/__tests__/abort_test_utils.py
#
# (C) Copyright 2012-present  Cristian Dinu <goc9000@gmail.com>
#
# This file is part of BAON.
#
# Licensed under the GPL-3


def abort_after_n_calls(n):
    calls_left = n

    def check_abort():
        nonlocal calls_left

        if calls_left <= 0:
            return True

        calls_left -= 1
        return False

    return check_abort
