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
from baon.core.files.__errors__.file_reference_errors import CannotExploreDirectoryError
from baon.core.files.__errors__.scan_files_errors import BasePathDoesNotExistError, BasePathIsNotADirectoryError,\
    CannotScanBasePathOtherError, NoPermissionsForBasePathError, ScanFilesAbortedError
from baon.core.utils.lang_utils import is_callable
from baon.core.utils.progress.ProgressTracker import ProgressTracker


def scan_files(base_path, recursive=True, on_progress=None, check_abort=None):
    progress_tracker = ProgressTracker(on_progress)

    assert check_abort is None or is_callable(check_abort)

    progress_tracker.report_more_total(1)

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

    scan_queue = deque([BAONPath(base_path)])
    files = []

    while len(scan_queue) > 0:
        if check_abort is not None and check_abort():
            raise ScanFilesAbortedError()

        path = scan_queue.popleft()

        problems = []

        is_link = os.path.islink(path.real_path())
        is_dir = os.path.isdir(path.real_path())

        directory_opened = False
        if is_dir and not is_link and (recursive or path.is_root()):
            try:
                files_in_dir = os.listdir(path.real_path())
                scan_queue.extend(path.extend(name) for name in files_in_dir)
                progress_tracker.report_more_total(len(files_in_dir))
                directory_opened = True
            except OSError as e:
                problems.append(CannotExploreDirectoryError(inner_error=e))

        if not directory_opened:
            files.append(
                FileReference(
                    path,
                    is_dir,
                    is_link,
                    problems,
                )
            )

        progress_tracker.report_more_done(1)

    return sorted(files)
