# baon/core/utils/progress/FileSystemTestCase.py
#
# (C) Copyright 2012-present  Cristian Dinu <goc9000@gmail.com>
# 
# This file is part of BAON.
#
# Licensed under the GPL-3


from contextlib import contextmanager

from unittest import TestCase

from baon.core.utils.progress.ProgressReceiver import ProgressReceiver


class ReportsProgressTestCase(TestCase):
    @contextmanager
    def verify_reported_progress(self):
        test = self

        class ProgressCollectorForTest(ProgressReceiver):

            any_event_received = False
            last_done = None
            last_total = None
            last_was_indeterminate = False

            def on_progress(self, done, total):
                test.assertGreaterEqual(done, 0)
                test.assertGreaterEqual(total, 0)
                test.assertLessEqual(done, total)

                if self.last_done is None:
                    test.assertEqual(done, 0)
                if self.last_was_indeterminate:
                    test.assertEqual(done, total, 'Only 100% progress can follow after indeterminate progress')
                if self.last_done is not None:
                    test.assertGreaterEqual(done, self.last_done)
                    test.assertGreaterEqual(total, self.last_total)

                self.last_done, self.last_total = done, total
                self.any_event_received = True
                self.last_was_indeterminate = False

            def on_indeterminate_progress(self):
                self.any_event_received = True
                self.last_was_indeterminate = True

            def do_final_checks(self):
                test.assertTrue(self.any_event_received, 'No progress events received')

                if not self.last_was_indeterminate and not self.last_done == self.last_total:
                    test.fail('Last progress recorded should be 100% or indeterminate')

        collector = ProgressCollectorForTest()

        yield collector

        collector.do_final_checks()
