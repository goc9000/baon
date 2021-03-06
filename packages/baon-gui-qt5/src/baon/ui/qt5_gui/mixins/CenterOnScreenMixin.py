# baon/ui/qt5_gui/mixins/CenterOnScreenMixin.py
#
# (C) Copyright 2012-present  Cristian Dinu <goc9000@gmail.com>
#
# This file is part of BAON.
#
# Licensed under the GPL-3


from PyQt5.QtWidgets import QDesktopWidget, QWidget


class CenterOnScreenMixin(object):
    """Mixin that provides a method for windows and dialogs so that they can center themselves on the screen."""

    def _center_on_screen(self):
        assert isinstance(self, QWidget)

        desktop = QDesktopWidget().availableGeometry()
        self.move((desktop.width() / 2) - (self.frameSize().width() / 2),
                  (desktop.height() / 2) - (self.frameSize().height() / 2))
