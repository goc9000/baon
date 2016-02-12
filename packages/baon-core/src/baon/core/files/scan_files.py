# baon/core/files/scan_files.py
#
# (C) Copyright 2012-present  Cristian Dinu <goc9000@gmail.com>
# 
# This file is part of BAON.
#
# Licensed under the GPL-3


import os
from collections import deque

from baon.core.files.BAONPath import BAONPath
from baon.core.files.FileReference import FileReference
from baon.core.files.__errors__.file_reference_errors import CannotAccessFileEntryError, CannotExploreDirectoryError
from baon.core.files.__errors__.scan_files_errors import BasePathDoesNotExistError, BasePathIsNotADirectoryError,\
    CannotScanBasePathOtherError, NoPermissionsForBasePathError, ScanFilesAbortedError
from baon.core.utils.file_utils import stat_file
from baon.core.utils.lang_utils import is_callable
from baon.core.utils.progress.ProgressTracker import ProgressTracker


def scan_files(base_path, recursive=True, on_progress=None, check_abort=None):
    progress_tracker = ProgressTracker(on_progress)

    assert check_abort is None or is_callable(check_abort)

    progress_tracker.report_more_total(1)

    _do_base_path_checks(base_path)

    scan_queue = deque([BAONPath(base_path)])
    files = []

    while len(scan_queue) > 0:
        if check_abort is not None and check_abort():
            raise ScanFilesAbortedError()

        path = scan_queue.popleft()
        file_ref = _scan_single_entry(path)

        directory_opened = False
        if file_ref.is_dir and not file_ref.is_link and (recursive or path.is_root()):
            try:
                files_in_dir = os.listdir(path.real_path())
                scan_queue.extend(path.extend(name) for name in files_in_dir)
                progress_tracker.report_more_total(len(files_in_dir))
                directory_opened = True
            except OSError as e:
                file_ref.problems.append(CannotExploreDirectoryError(inner_error=e))

        if not directory_opened:
            files.append(file_ref)

        progress_tracker.report_more_done(1)

    return sorted(files)


def _do_base_path_checks(base_path):
    try:
        os.listdir(base_path)
    except PermissionError:
        raise NoPermissionsForBasePathError(path=base_path) from None
    except FileNotFoundError:
        raise BasePathDoesNotExistError(path=base_path) from None
    except NotADirectoryError:
        raise BasePathIsNotADirectoryError(path=base_path) from None
    except OSError as e:
        raise CannotScanBasePathOtherError(path=base_path, inner_error=e) from None


def _scan_single_entry(path):
    try:
        file_info = stat_file(path.real_path())
        return FileReference(path, file_info.is_dir, file_info.is_link)
    except OSError as e:
        return FileReference(path, False, False, [CannotAccessFileEntryError(inner_error=e)])
