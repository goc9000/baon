# baon/core/utils/ReportsProgress.py
#
# (C) Copyright 2012-present  Cristian Dinu <goc9000@gmail.com>
# 
# This file is part of BAON.
#
# Licensed under the GPL-3


class ReportsProgress(object):
    on_progress = None

    def __init__(self, on_progress=None):
        self.on_progress = on_progress

    def _report_progress(self, processed, total):
        if self.on_progress is not None:
            self.on_progress(processed, total)
