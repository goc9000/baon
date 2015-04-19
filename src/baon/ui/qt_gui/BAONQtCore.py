# baon/ui/qt_gui/BAONQtCore.py
#
# (C) Copyright 2012-present  Cristian Dinu <goc9000@gmail.com>
# 
# This file is part of BAON.
#
# Licensed under the GPL-3


from PyQt4.QtCore import QObject, pyqtSlot, pyqtSignal


class BAONQtCore(QObject):
    prologue_finished = pyqtSignal()
    has_shutdown = pyqtSignal()

    # Inputs
    _base_path = ''
    _scan_recursive = False
    _rules_text = ''
    _use_extension = False
    _use_path = False

    def __init__(self, args):
        super().__init__()

        self._init_inputs(args)

    def _init_inputs(self, args):
        if args.base_path is not None:
            self._base_path = args.base_path
        if args.scan_recursive is not None:
            self._scan_recursive = args.scan_recursive
        if args.rules_text is not None:
            self._rules_text = args.rules_text
        if args.use_extension is not None:
            self._use_extension = args.use_extension
        if args.use_path is not None:
            self._use_path = args.use_path

    @pyqtSlot()
    def start(self):
        self.prologue_finished.emit()

    @pyqtSlot()
    def shutdown(self):
        self.has_shutdown.emit()
