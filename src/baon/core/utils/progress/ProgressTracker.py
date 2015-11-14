# baon/core/utils/progress/ProgressTracker.py
#
# (C) Copyright 2012-present  Cristian Dinu <goc9000@gmail.com>
# 
# This file is part of BAON.
#
# Licensed under the GPL-3


from baon.core.utils.lang_utils import is_callable
from baon.core.utils.progress.ProgressInfo import ProgressInfo


class ProgressTracker(object):
    """
    This is a helper class for operations that report progress. It fits over a function that receives progress events,
    and provides a friendly API which the caller can use to report progress without constructing ProgressInfo objects
    or tracking the current progress itself.
    """

    _on_progress = None
    _last_reported_done = None
    _last_reported_total = None

    def __init__(self, on_progress=None):
        self._last_reported_done = 0
        self._last_reported_total = 0

        if on_progress is not None:
            assert is_callable(on_progress)
            self._on_progress = on_progress

    def report_progress(self, done, total):
        if self._on_progress is not None:
            self._on_progress(ProgressInfo(done, total))

    def report_indeterminate_progress(self):
        if self._on_progress is not None:
            self._on_progress(ProgressInfo.make_indeterminate())

    def report_more_done(self, amount):
        self._last_reported_done += amount
        self.report_progress(self._last_reported_done, self._last_reported_total)

    def report_more_total(self, amount):
        self._last_reported_total += amount
        self.report_progress(self._last_reported_done, self._last_reported_total)
