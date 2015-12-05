# baon/core/plan/make_rename_plan_new.py
#
# (C) Copyright 2012-present  Cristian Dinu <goc9000@gmail.com>
#
# This file is part of BAON.
#
# Licensed under the GPL-3


from baon.core.plan.RenamePlan import RenamePlan


def make_rename_plan(renamed_files):
    return MakeRenamePlanInstance(renamed_files).run()


class MakeRenamePlanInstance(object):
    renamed_files = None
    steps = []

    def __init__(self, renamed_files):
        self.renamed_files = renamed_files

    def run(self):
        self._keep_only_changed_files()
        if len(self.renamed_files) > 0:
            pass

        return RenamePlan(self.steps)

    def _keep_only_changed_files(self):
        self.renamed_files = [f for f in self.renamed_files if f.is_changed()]
