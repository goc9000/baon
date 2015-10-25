# baon/core/renaming/rename_files.py
#
# (C) Copyright 2012-present  Cristian Dinu <goc9000@gmail.com>
# 
# This file is part of BAON.
#
# Licensed under the GPL-3


import re
import os

from collections import defaultdict

from baon.core.utils.progress.ProgressTracker import ProgressTracker
from baon.core.utils.lang_utils import is_callable

from baon.core.files.BAONPath import BAONPath
from baon.core.files.baon_paths import all_path_components, all_partial_paths, extend_path, split_path_and_filename

from baon.core.renaming.__errors__.rename_files_errors import UnprintableCharacterInFilenameError, EmptyFilenameError,\
    OnlyDotsFilenameError, EmptyPathComponentError, OnlyDotsPathComponentError, FileCollidesWithFileError,\
    FileCollidesWithDirectoryError, DirectoryCollidesWithFileError, WouldMergeImplicitlyWithOtherFoldersError,\
    ProblematicCharacterInFilenameWarning, PathComponentStartsWithSpaceWarning, PathComponentEndsWithSpaceWarning,\
    PathComponentContainsDoubleSpacesWarning, FilenameStartsWithSpaceWarning, BasenameEndsWithSpaceWarning,\
    FilenameContainsDoubleSpacesWarning, ExtensionContainsSpacesWarning, RenameFilesAbortedError, \
    CannotRenameFileWithErrorsError, RenameFilesError, RenameFilesWarning

from baon.core.renaming.RenamedFileReference import RenamedFileReference


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
    full_filename = file_ref.filename
    problems = []

    try:
        full_filename = _get_renamed_filename(
            full_filename,
            rule_set,
            use_path=use_path,
            use_extension=(use_extension or file_ref.is_dir),
        )
    except Exception as e:
        problems.append(e)

    return RenamedFileReference(file_ref, file_ref.path.replace_path_text(full_filename), problems=problems)


def _get_renamed_filename(full_filename, rule_set, use_path, use_extension):
    input_text = full_filename
    path = ''
    extension = ''

    if not use_path:
        path, input_text = split_path_and_filename(input_text)
    if not use_extension:
        input_text, extension = os.path.splitext(input_text)

    rename_result = rule_set.apply_on(input_text)
    output_text = rename_result.text

    if not use_extension:
        output_text += extension
    if not use_path:
        output_text = extend_path(path, output_text)

    return output_text


def _maybe_apply_override(renamed_ref, overrides):
    new_filename = overrides.get(renamed_ref.old_file_ref.filename)

    if new_filename is not None:
        return RenamedFileReference(
            renamed_ref.old_file_ref,
            renamed_ref.old_file_ref.path.replace_path_text(new_filename),
            is_override=True
        )
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
    full_filename = renamed_fref.filename
    problems = renamed_fref.problems

    if renamed_fref.is_changed() and renamed_fref.old_file_ref.has_errors():
        problems.append(CannotRenameFileWithErrorsError())

    m = NON_PRINTABLE_REGEX.search(full_filename)
    if m is not None:
        problems.append(UnprintableCharacterInFilenameError(ord(m.group(0))))

    path_components = all_path_components(full_filename)
    path_components, filename = path_components[:-1], path_components[-1]

    if filename == '':
        problems.append(EmptyFilenameError())
    if ONLY_DOTS_REGEX.match(filename):
        problems.append(OnlyDotsFilenameError())
    if any(component == '' for component in path_components):
        problems.append(EmptyPathComponentError())
    if any(ONLY_DOTS_REGEX.match(component) for component in path_components):
        problems.append(OnlyDotsPathComponentError())


def _check_for_intrinsic_warnings(renamed_fref):
    full_filename = renamed_fref.filename
    problems = renamed_fref.problems

    path_components = all_path_components(full_filename)

    m = PROBLEM_CHARS_REGEX.search(''.join(path_components))
    if m is not None:
        problems.append(ProblematicCharacterInFilenameWarning(character=m.group(0)))

    path_components, filename = path_components[:-1], path_components[-1]

    for component in path_components:
        if component.startswith(' '):
            problems.append(PathComponentStartsWithSpaceWarning(component=component))
        if component.endswith(' '):
            problems.append(PathComponentEndsWithSpaceWarning(component=component))
        if '  ' in component:
            problems.append(PathComponentContainsDoubleSpacesWarning(component=component))

    basename, extension = os.path.splitext(filename) if not renamed_fref.is_dir else (filename, '')

    if basename.startswith(' '):
        problems.append(FilenameStartsWithSpaceWarning())
    if basename.endswith(' '):
        problems.append(BasenameEndsWithSpaceWarning())
    if '  ' in basename:
        problems.append(FilenameContainsDoubleSpacesWarning())
    if ' ' in extension:
        problems.append(ExtensionContainsSpacesWarning())


def _check_for_collisions(renamed_files):
    file_path_use_counts = defaultdict(int)
    dir_path_use_counts = defaultdict(int)
    partial_dir_paths = set()

    for f in renamed_files:
        if f.is_dir:
            dir_path_use_counts[f.filename] += 1
        else:
            file_path_use_counts[f.filename] += 1

        for path in all_partial_paths(f.filename)[:-1]:
            partial_dir_paths.add(path)

    for f in renamed_files:
        if f.is_dir:
            if file_path_use_counts[f.filename] > 0:
                f.problems.append(DirectoryCollidesWithFileError())
            elif (dir_path_use_counts[f.filename] > 1) or (f.filename in partial_dir_paths):
                f.problems.append(WouldMergeImplicitlyWithOtherFoldersError())
        else:
            if file_path_use_counts[f.filename] > 1:
                f.problems.append(FileCollidesWithFileError())
            elif (dir_path_use_counts[f.filename] > 0) or (f.filename in partial_dir_paths) or \
                    (f.filename in partial_dir_paths):
                f.problems.append(FileCollidesWithDirectoryError())


def _clear_rename_errors(renamed_files):
    for f in renamed_files:
        f.problems = [
            problem for problem in f.problems
            if not isinstance(problem, RenameFilesError) and not isinstance(problem, RenameFilesWarning)
        ]
