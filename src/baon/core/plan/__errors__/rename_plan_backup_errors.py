# baon/core/plan/__errors__/rename_plan_backup_errors.py
#
# (C) Copyright 2012-present  Cristian Dinu <goc9000@gmail.com>
# 
# This file is part of BAON.
#
# Licensed under the GPL-3


from abc import ABCMeta, abstractmethod

from baon.core.errors.BAONError import BAONError


class RenamePlanBackupError(BAONError, metaclass=ABCMeta):
    pass


class CannotSaveRenamePlanBackupError(RenamePlanBackupError):
    def __init__(self):
        super().__init__()

    def _get_format_string(self):
        return "Cannot save the rename plan backup. Is BAON installed and configured correctly?"


class CannotLoadRenamePlanBackupError(RenamePlanBackupError):
    def __init__(self):
        super().__init__()

    def _get_format_string(self):
        return "Cannot load the rename plan backup. The application directory may have been corrupted!"


class CannotDeleteRenamePlanBackupError(RenamePlanBackupError):
    def __init__(self):
        super().__init__()

    def _get_format_string(self):
        return "Cannot delete the rename plan backup"
