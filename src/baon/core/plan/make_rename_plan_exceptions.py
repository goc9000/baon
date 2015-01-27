# baon/core/plan/make_rename_plan_exceptions.py
#
# (C) Copyright 2012-present  Cristian Dinu <goc9000@gmail.com>
# 
# This file is part of BAON.
#
# Licensed under the GPL-3


from baon.core.errors.BAONExceptionBase import BAONExceptionBase


class MakeRenamePlanException(BAONExceptionBase):
    def __init__(self, format_string, error_parameters=None):
        BAONExceptionBase.__init__(self, format_string, error_parameters)


class CannotCreateDestinationDirException(MakeRenamePlanException):
    def __init__(self, destination_dir, reason_format_string, reason_parameters=None):
        reason_parameters = dict(reason_parameters or dict())
        reason_parameters['destination_dir'] = destination_dir

        MakeRenamePlanException.__init__(
            self,
            "Cannot create destination directory '{destination_dir}' because " + reason_format_string,
            reason_parameters)


class CannotCreateDestinationDirInaccessibleParentException(CannotCreateDestinationDirException):
    def __init__(self, destination_dir):
        CannotCreateDestinationDirException.__init__(
            self,
            destination_dir,
            "the parent directory is inaccessible")


class CannotCreateDestinationDirUnexpectedNonDirParentException(CannotCreateDestinationDirException):
    def __init__(self, destination_dir):
        CannotCreateDestinationDirException.__init__(
            self,
            destination_dir,
            "the parent entry is unexpectedly not a directory")


class CannotCreateDestinationDirNoReadPermissionForParentException(CannotCreateDestinationDirException):
    def __init__(self, destination_dir):
        CannotCreateDestinationDirException.__init__(
            self,
            destination_dir,
            "we do not have read permission on the parent directory")


class CannotCreateDestinationDirNoTraversePermissionForParentException(CannotCreateDestinationDirException):
    def __init__(self, destination_dir):
        CannotCreateDestinationDirException.__init__(
            self,
            destination_dir,
            "we do not have traverse permission on the parent directory")


class CannotCreateDestinationDirNoWritePermissionForParentException(CannotCreateDestinationDirException):
    def __init__(self, destination_dir):
        CannotCreateDestinationDirException.__init__(
            self,
            destination_dir,
            "we do not have write permission on the parent directory")


class CannotCreateDestinationDirFileInTheWayWillNotMoveException(CannotCreateDestinationDirException):
    def __init__(self, destination_dir):
        CannotCreateDestinationDirException.__init__(
            self,
            destination_dir,
            "a file of the same name is in the way and it is not part of the move")


class RenamedFilesListInvalidMultipleDestinationsException(MakeRenamePlanException):
    def __init__(self, source, destination_1, destination_2):
        MakeRenamePlanException.__init__(
            self,
            "Rename list is invalid: '{source}' is renamed to both '{destination_1}' and '{destination_2}' ",
            {'source': source, 'destination_1': destination_1, 'destination_2': destination_2})


class RenamedFilesListInvalidSameDestinationException(MakeRenamePlanException):
    def __init__(self, destination, source_1, source_2):
        MakeRenamePlanException.__init__(
            self,
            "Rename list is invalid: Both '{source_1}' and '{source_2}' are renamed to '{destination}'",
            {'destination': destination, 'source_1': source_1, 'source_2': source_2})


class CannotMoveFileNoWritePermissionForDirException(MakeRenamePlanException):
    def __init__(self, source, destination, directory):
        MakeRenamePlanException.__init__(
            self,
            "Cannot rename '{source}' to '{destination}' as we do not have write permission on '{directory}'",
            {'source': source, 'destination': destination, 'directory': directory})
