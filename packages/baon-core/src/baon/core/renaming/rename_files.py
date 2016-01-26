# baon/core/renaming/rename_files.py
#
# (C) Copyright 2012-present  Cristian Dinu <goc9000@gmail.com>
# 
# This file is part of BAON.
#
# Licensed under the GPL-3


import os
import re
from collections import defaultdict

from baon.core.errors.BAONError import BAONError
from baon.core.renaming.RenamedFileReference import RenamedFileReference
from baon.core.renaming.__errors__.rename_files_errors import UnprintableCharacterInFilenameError, EmptyFilenameError,\
    OnlyDotsFilenameError, EmptyPathComponentError, OnlyDotsPathComponentError, FileCollidesWithFileError,\
    FileCollidesWithDirectoryError, DirectoryCollidesWithFileError, WouldMergeImplicitlyWithOtherFoldersError,\
    ProblematicCharacterInFilenameWarning, PathComponentStartsWithSpaceWarning, PathComponentEndsWithSpaceWarning,\
    PathComponentContainsDoubleSpacesWarning, FilenameStartsWithSpaceWarning, FilenameEndsWithSpaceWarning,\
    FilenameContainsDoubleSpacesWarning, ExtensionContainsSpacesWarning, RenameFilesAbortedError, \
    CannotRenameFileWithErrorsError, RenameFilesError, RenameFilesWarning
from baon.core.utils.lang_utils import is_callable
from baon.core.utils.progress.ProgressTracker import ProgressTracker


NON_PRINTABLE_REGEX = re.compile(r'[\u0000-\u001f]')
PROBLEM_CHARS_REGEX = re.compile(r'["*:<>?\\/]')
ONLY_DOTS_REGEX = re.compile(r'^[.]+$')


def rename_files(files, rule_set, use_path=False, use_extension=False, on_progress=None, check_abort=None):
    progress_tracker = ProgressTracker(on_progress)

    assert check_abort is None or is_callable(check_abort)

    progress_tracker.report_more_total(len(files))
    renamed_files = []

    for file_ref in files:
        if check_abort is not None and check_abort():
            raise RenameFilesAbortedError()

        renamed_files.append(
            _rename_file(
                file_ref,
                rule_set,
                use_path=use_path,
                use_extension=use_extension,
            )
        )
        progress_tracker.report_more_done(1)

    _verify_renamed_files(renamed_files)

    return renamed_files


def apply_rename_overrides(renamed_files, overrides):
    renamed_files = [_maybe_apply_override(renamed_ref, overrides) for renamed_ref in renamed_files]

    _verify_renamed_files(renamed_files)

    return renamed_files


def _rename_file(file_ref, rule_set, use_path=False, use_extension=False):
    try:
        if use_path:
            input_text = file_ref.path.path_text()
        else:
            input_text = file_ref.path.basename()

        saved_extension = None
        if not (use_extension or file_ref.is_dir):
            input_text, saved_extension = os.path.splitext(input_text)

        rename_result = rule_set.apply_on(input_text)
        output_text = rename_result.text

        if saved_extension is not None:
            output_text += saved_extension

        if use_path:
            renamed_path = file_ref.path.replace_path_text(output_text)
        else:
            renamed_path = file_ref.path.parent_path().extend_with_path_text(output_text)

        return RenamedFileReference(file_ref, renamed_path)
    except BAONError as e:
        return RenamedFileReference(file_ref, file_ref.path, problems=[e])


def _maybe_apply_override(renamed_ref, overrides):
    new_path = overrides.get(renamed_ref.old_file_ref.path)

    if new_path is not None:
        return RenamedFileReference(renamed_ref.old_file_ref, new_path, is_override=True)
    else:
        return renamed_ref


def _verify_renamed_files(renamed_files):
    """
    Performs verifications.

    Note: by design, the renamer will only perform verifications that do
    not require further accesses to the filesystem. Errors that can only be
    detected by using such information will be caught in the planning phase.
    """

    _clear_rename_errors(renamed_files)

    for renamed_fref in renamed_files:
        _check_for_intrinsic_errors(renamed_fref)
        _check_for_intrinsic_warnings(renamed_fref)

    _check_for_collisions(renamed_files)


def _check_for_intrinsic_errors(renamed_fref):
    problems = renamed_fref.problems

    if renamed_fref.is_changed() and renamed_fref.old_file_ref.has_errors():
        problems.append(CannotRenameFileWithErrorsError())

    m = NON_PRINTABLE_REGEX.search(renamed_fref.path.path_text())
    if m is not None:
        problems.append(UnprintableCharacterInFilenameError(ord(m.group(0))))

    path_components = renamed_fref.path.parent_path().components
    basename = renamed_fref.path.basename()

    if basename == '':
        problems.append(EmptyFilenameError())
    if ONLY_DOTS_REGEX.match(basename):
        problems.append(OnlyDotsFilenameError())
    if any(component == '' for component in path_components):
        problems.append(EmptyPathComponentError())
    if any(ONLY_DOTS_REGEX.match(component) for component in path_components):
        problems.append(OnlyDotsPathComponentError())


def _check_for_intrinsic_warnings(renamed_fref):
    problems = renamed_fref.problems

    m = PROBLEM_CHARS_REGEX.search(''.join(renamed_fref.path.components))
    if m is not None:
        problems.append(ProblematicCharacterInFilenameWarning(character=m.group(0)))

    for component in renamed_fref.path.parent_path().components:
        if component.startswith(' '):
            problems.append(PathComponentStartsWithSpaceWarning(component=component))
        if component.endswith(' '):
            problems.append(PathComponentEndsWithSpaceWarning(component=component))
        if '  ' in component:
            problems.append(PathComponentContainsDoubleSpacesWarning(component=component))

    if not renamed_fref.is_dir:
        name, extension = os.path.splitext(renamed_fref.path.basename())
    else:
        name, extension = renamed_fref.path.basename(), ''

    if name.startswith(' '):
        problems.append(FilenameStartsWithSpaceWarning())
    if name.endswith(' '):
        problems.append(FilenameEndsWithSpaceWarning())
    if '  ' in name:
        problems.append(FilenameContainsDoubleSpacesWarning())
    if ' ' in extension:
        problems.append(ExtensionContainsSpacesWarning())


def _check_for_collisions(renamed_files):
    file_path_use_counts = defaultdict(int)
    dir_path_use_counts = defaultdict(int)
    partial_dir_paths = set()

    for f in renamed_files:
        if f.is_dir:
            dir_path_use_counts[f.path] += 1
        else:
            file_path_use_counts[f.path] += 1

        partial_dir_paths.update(f.path.parent_paths())

    for f in renamed_files:
        if f.is_dir:
            if file_path_use_counts[f.path] > 0:
                f.problems.append(DirectoryCollidesWithFileError())
            elif (dir_path_use_counts[f.path] > 1) or (f.path in partial_dir_paths):
                f.problems.append(WouldMergeImplicitlyWithOtherFoldersError())
        else:
            if file_path_use_counts[f.path] > 1:
                f.problems.append(FileCollidesWithFileError())
            elif (dir_path_use_counts[f.path] > 0) or (f.path in partial_dir_paths):
                f.problems.append(FileCollidesWithDirectoryError())


def _clear_rename_errors(renamed_files):
    for f in renamed_files:
        f.problems = [
            problem for problem in f.problems
            if not isinstance(problem, RenameFilesError) and not isinstance(problem, RenameFilesWarning)
        ]
