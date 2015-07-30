# baon/ui/qt_gui/utils/DataFlowNode.py
#
# (C) Copyright 2012-present  Cristian Dinu <goc9000@gmail.com>
#
# This file is part of BAON.
#
# Licensed under the GPL-3


from PyQt4.QtCore import QObject, pyqtSlot


class DataFlowNode(QObject):
    _value = None
    _debug_name = None

    def __init__(self, parent, value=None, debug_name=None):
        super().__init__(parent)

        self._value = value
        self._debug_name = debug_name

    @pyqtSlot(object)
    def update_value(self, new_value):
        self._value = new_value

    def value(self):
        return self._value

    def valid_value(self):
        return self._value is not None and not isinstance(self._value, Exception)
