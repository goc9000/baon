# baon/core/utils/progress/ProgressInfo.py
#
# (C) Copyright 2012-present  Cristian Dinu <goc9000@gmail.com>
# 
# This file is part of BAON.
#
# Licensed under the GPL-3


class ProgressInfo(object):
    done = None
    total = None

    def __init__(self, done, total):
        if done is not None:
            assert done >= 0
        if total is not None:
            assert total >= 0
        if done is not None and total is not None:
            assert done <= total

        self.done = done
        self.total = total

    def is_indeterminate(self):
        return self.done is None or self.total is None

    def is_complete(self):
        return not self.is_indeterminate() and self.done == self.total

    def test_repr(self):
        if self.is_indeterminate():
            return 'INDETERMINATE'
        else:
            return self.done, self.total

    @staticmethod
    def make_indeterminate():
        return ProgressInfo(None, None)
