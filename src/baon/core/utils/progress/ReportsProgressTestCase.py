# baon/core/utils/progress/FileSystemTestCase.py
#
# (C) Copyright 2012-present  Cristian Dinu <goc9000@gmail.com>
# 
# This file is part of BAON.
#
# Licensed under the GPL-3


from contextlib import contextmanager

from baon.core.utils.lang_utils import pairwise

from unittest import TestCase


class ReportsProgressTestCase(TestCase):
    @contextmanager
    def verify_reported_progress(self):
        progress_events = []

        collector = lambda progress_info: progress_events.append(progress_info)
        yield collector

        self.assertTrue(len(progress_events) > 0, 'No progress events received')

        first_non_indeterminate = next(filter(lambda event: not event.is_indeterminate(), progress_events), None)
        if first_non_indeterminate is not None:
            self.assertEqual(first_non_indeterminate.done, 0)

        for a, b in pairwise(progress_events):
            if a.is_indeterminate():
                self.assertTrue(b.is_indeterminate() or b.is_complete())
            elif not b.is_indeterminate():
                self.assertGreaterEqual(b.done, a.done)
                self.assertGreaterEqual(b.total, a.total)

        last_event = progress_events[-1]
        self.assertTrue(last_event.is_indeterminate() or last_event.is_complete())
