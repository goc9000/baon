# baon/core/utils/progress/ProgressReceiver.py
#
# (C) Copyright 2012-present  Cristian Dinu <goc9000@gmail.com>
# 
# This file is part of BAON.
#
# Licensed under the GPL-3


from abc import ABCMeta, abstractmethod


class ProgressReceiver(object, metaclass=ABCMeta):
    _last_reported_done = None
    _last_reported_total = None

    def __init__(self):
        self._last_reported_done = 0
        self._last_reported_total = 0

    @abstractmethod
    def on_progress(self, done, total):
        pass

    @abstractmethod
    def on_indeterminate_progress(self):
        pass

    def on_more_done(self, amount):
        self._last_reported_done += amount
        self.on_progress(self._last_reported_done, self._last_reported_total)

    def on_more_total(self, amount):
        self._last_reported_total += amount
        self.on_progress(self._last_reported_done, self._last_reported_total)
