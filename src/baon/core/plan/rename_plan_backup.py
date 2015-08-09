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

from baon.core.plan.__errors__.rename_plan_backup_errors import CannotSaveRenamePlanBackupError,\
    CannotLoadRenamePlanBackupError, CannotDeleteRenamePlanBackupError

from baon.core.plan.RenamePlan import RenamePlan


def get_rename_plan_backup_filename():
    return os.path.join(appdirs.user_data_dir(appname=APP_NAME, appauthor=APP_AUTHOR), 'rename_plan_backup.json')


def rename_plan_backup_exists():
    return os.path.isfile(get_rename_plan_backup_filename())


def save_rename_plan_backup(rename_plan):
    try:
        full_filename = get_rename_plan_backup_filename()
        base_dir, _ = os.path.split(full_filename)
        os.makedirs(base_dir, exist_ok=True)

        rename_plan.save_to_file(full_filename)
    except Exception:
        raise CannotSaveRenamePlanBackupError() from None


def load_rename_plan_backup():
    try:
        return RenamePlan.load_from_file(get_rename_plan_backup_filename())
    except Exception:
        raise CannotLoadRenamePlanBackupError() from None


def delete_rename_plan_backup():
    try:
        filename = get_rename_plan_backup_filename()
        if os.path.exists(filename):
            os.remove(filename)
    except Exception:
        raise CannotDeleteRenamePlanBackupError() from None
