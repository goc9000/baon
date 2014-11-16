# baon/core/renaming/rename_files_exceptions.py
#
# (C) Copyright 2012-present  Cristian Dinu <goc9000@gmail.com>
# 
# This file is part of BAON.
#
# Licensed under the GPL-3


from baon.core.errors.BAONExceptionBase import BAONExceptionBase
from baon.core.errors.BAONWarningBase import BAONWarningBase


class RenameFilesException(BAONExceptionBase):
    def __init__(self, format_string, error_parameters=None):
        BAONExceptionBase.__init__(self, format_string, error_parameters)


class UnprintableCharacterInFilenameException(RenameFilesException):
    def __init__(self, character_code):
        RenameFilesException.__init__(
            self, u"Non-printable character \\u{character_code:04x} present in filename",
            {'character_code': character_code})


class EmptyFilenameException(RenameFilesException):
    def __init__(self):
        RenameFilesException.__init__(self, u"Filename is empty")


class OnlyDotsFilenameException(RenameFilesException):
    def __init__(self):
        RenameFilesException.__init__(self, u"Filename may not be . or ..")


class EmptyPathComponentException(RenameFilesException):
    def __init__(self):
        RenameFilesException.__init__(self, u"Path has empty component")


class OnlyDotsPathComponentException(RenameFilesException):
    def __init__(self):
        RenameFilesException.__init__(self, u"Path may not contain a . or .. component")


class FileCollidesWithFileException(RenameFilesException):
    def __init__(self):
        RenameFilesException.__init__(self, u"Collides with other file")


class FileCollidesWithDirectoryException(RenameFilesException):
    def __init__(self):
        RenameFilesException.__init__(self, u"Collides with directory")


class DirectoryCollidesWithFileException(RenameFilesException):
    def __init__(self):
        RenameFilesException.__init__(self, u"Collides with other directory")


class WouldMergeImplicitlyWithOtherFoldersException(RenameFilesException):
    def __init__(self):
        RenameFilesException.__init__(self, u"Would merge implicitly with other folders")


class RenameFilesWarning(BAONWarningBase):
    def __init__(self, format_string, error_parameters=None):
        BAONWarningBase.__init__(self, format_string, error_parameters)


class ProblematicCharacterInFilenameWarning(RenameFilesWarning):
    def __init__(self, character):
        RenameFilesWarning.__init__(
            self, u"Problematic character present in filename: {character}",
            {'character': character})


class PathComponentStartsWithSpaceWarning(RenameFilesWarning):
    def __init__(self, component):
        RenameFilesWarning.__init__(
            self, u"Path component '{component}' starts with spaces",
            {'component': component})


class PathComponentEndsWithSpaceWarning(RenameFilesWarning):
    def __init__(self, component):
        RenameFilesWarning.__init__(
            self, u"Path component '{component}' ends with spaces",
            {'component': component})


class PathComponentContainsDoubleSpacesWarning(RenameFilesWarning):
    def __init__(self, component):
        RenameFilesWarning.__init__(
            self, u"Path component '{component}' contains double spaces",
            {'component': component})


class FilenameStartsWithSpaceWarning(RenameFilesWarning):
    def __init__(self):
        RenameFilesWarning.__init__(self, u"Filename starts with spaces")


class BasenameEndsWithSpaceWarning(RenameFilesWarning):
    def __init__(self):
        RenameFilesWarning.__init__(self, u"Filename contains spaces before the extension")


class FilenameContainsDoubleSpacesWarning(RenameFilesWarning):
    def __init__(self):
        RenameFilesWarning.__init__(self, u"Filename contains double spaces")


class ExtensionContainsSpacesWarning(RenameFilesWarning):
    def __init__(self):
        RenameFilesWarning.__init__(self, u"Extension contains spaces")
