# baon/ui/qt_gui/BAONQtApplication.py
#
# (C) Copyright 2012-present  Cristian Dinu <goc9000@gmail.com>
# 
# This file is part of BAON.
#
# Licensed under the GPL-3


import sys

from PyQt4.QtCore import Qt, QThread, QMetaObject
from PyQt4.QtGui import QApplication

from baon.ui.qt_gui.BAONQtCore import BAONQtCore
from baon.ui.qt_gui.forms.MainWindow import MainWindow


class BAONQtApplication(QApplication):
    _main_window = None
    _core = None

    _core_thread = None

    def __init__(self, args):
        super().__init__(sys.argv)

        # Actually we do quit when the last window is closed, but we need to do this in a more controlled way
        self.setQuitOnLastWindowClosed(False)

        self._init_threads()
        self._init_main_objects(args)
        self._connect_main_objects()
        self._start_core()

    def _init_threads(self):
        self._core_thread = QThread()
        self._core_thread.start()

    def _init_main_objects(self, args):
        self._main_window = MainWindow(args)

        self._core = BAONQtCore(args)
        self._core.moveToThread(self._core_thread)

    def _connect_main_objects(self):
        self.aboutToQuit.connect(self._on_quit)

        self._core.prologue_finished.connect(self._main_window.show)

        self._core.status_changed.connect(self._main_window.report_status)
        self._core.scanned_files_updated.connect(self._main_window.update_scanned_files)
        self._core.renamed_files_updated.connect(self._main_window.update_renamed_files)

        self._core.has_shutdown.connect(self.quit)

        self._main_window.base_path_edited.connect(self._core.update_base_path)
        self._main_window.scan_recursive_changed.connect(self._core.update_scan_recursive)

        self._main_window.rules_text_changed.connect(self._core.update_rules_text)
        self._main_window.use_path_changed.connect(self._core.update_use_path)
        self._main_window.use_extension_changed.connect(self._core.update_use_extension)

        self._main_window.request_add_override.connect(self._core.add_override)
        self._main_window.request_remove_override.connect(self._core.remove_override)

        self._main_window.request_do_rename.connect(self._core.do_rename)
        self._main_window.request_rescan.connect(self._core.rescan)

        self._main_window.rejected.connect(self._core.shutdown)

    def _start_core(self):
        QMetaObject.invokeMethod(self._core, 'start', Qt.QueuedConnection)

    def _on_quit(self):
        self._core_thread.quit()
        self._core_thread.wait()
