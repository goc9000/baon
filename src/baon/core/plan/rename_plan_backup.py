# baon/core/plan/rename_plan_backup.py
#
# (C) Copyright 2012-present  Cristian Dinu <goc9000@gmail.com>
#
# This file is part of BAON.
#
# Licensed under the GPL-3


import appdirs
import os

from baon.app_metadata import APP_NAME, APP_AUTHOR

from baon.core.utils.lang_utils import swallow_os_errors

from baon.core.plan.__errors__.rename_plan_backup_errors import CannotSaveRenamePlanBackupError,\
    CannotLoadRenamePlanBackupError

from baon.core.plan.RenamePlan import RenamePlan


def get_rename_plan_backup_filename():
    return os.path.join(appdirs.user_data_dir(appname=APP_NAME, appauthor=APP_AUTHOR), 'rename_plan_backup.json')


def rename_plan_backup_exists():
    return os.path.isfile(get_rename_plan_backup_filename())


def save_rename_plan_backup(rename_plan):
    try:
        rename_plan.save_to_file(get_rename_plan_backup_filename())
    except Exception:
        raise CannotSaveRenamePlanBackupError() from None


def load_rename_plan_backup():
    try:
        return RenamePlan.load_from_file(get_rename_plan_backup_filename())
    except Exception:
        raise CannotLoadRenamePlanBackupError() from None


def delete_rename_plan_backup():
    with swallow_os_errors():
        os.remove(get_rename_plan_backup_filename())
