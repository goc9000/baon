# baon/core/utils/progress/DummyProgressReceiver.py
#
# (C) Copyright 2012-present  Cristian Dinu <goc9000@gmail.com>
# 
# This file is part of BAON.
#
# Licensed under the GPL-3


from baon.core.utils.progress.ProgressReceiver import ProgressReceiver


class DummyProgressReceiver(ProgressReceiver):

    def on_progress(self, done, total):
        pass

    def on_indeterminate_progress(self):
        pass
