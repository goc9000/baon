# baon/core/__tests__/FileSystemTestCase.py
#
# (C) Copyright 2012-present  Cristian Dinu <goc9000@gmail.com>
# 
# This file is part of BAON.
#
# Licensed under the GPL-3


from unittest import TestCase


class ReportsProgressTestCase(TestCase):
    def _progress_collector(self, progress_events):
        return lambda count, total: progress_events.append((count, total))

    def _verify_reported_progress(self, progress_events):
        self.assertFalse(len(progress_events) == 0, 'No progress reported!')

        first_event = progress_events[0]
        self.assertEquals(first_event[0], 0)

        for a, b in zip(progress_events[:-1], progress_events[1:]):
            self.assertLessEqual(a[0], a[1])
            self.assertLessEqual(a[0], b[0])
            self.assertLessEqual(a[1], b[1])

        last_event = progress_events[-1]
        self.assertEquals(last_event[0], last_event[1])
