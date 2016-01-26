# baon/ui/qt4_gui/utils/make_qicon_with_overlay.py
#
# (C) Copyright 2012-present  Cristian Dinu <goc9000@gmail.com>
# 
# This file is part of BAON.
#
# Licensed under the GPL-3


from PyQt4.QtCore import Qt
from PyQt4.QtGui import QIcon, QPainter, QPixmap


_MODES = [QIcon.Normal, QIcon.Disabled, QIcon.Active, QIcon.Selected]
_STATES = [QIcon.On, QIcon.Off]


def make_qicon_with_overlay(base_icon, overlay_icon, align=Qt.AlignRight | Qt.AlignBottom, relative_size=0.75):
    overlay_aspect_ratio = _get_qicon_aspect_ratio(overlay_icon)

    new_icon = QIcon()

    for mode in _MODES:
        for state in _STATES:
            for size in base_icon.availableSizes(mode, state):
                pixmap = QPixmap(base_icon.pixmap(size, mode, state))

                overlay_height = min(
                    size.height() * relative_size,
                    size.width() * relative_size / overlay_aspect_ratio,
                )
                overlay_width = int(overlay_height * overlay_aspect_ratio)
                overlay_height = int(overlay_height)

                painter = QPainter(pixmap)

                x = 0
                if align & Qt.AlignHCenter:
                    x = int((size.width() - overlay_width) / 2)
                elif align & Qt.AlignRight:
                    x = size.width() - overlay_width

                y = 0
                if align & Qt.AlignVCenter:
                    y = int((size.height() - overlay_height) / 2)
                elif align & Qt.AlignBottom:
                    y = size.height() - overlay_height

                overlay_icon.paint(painter, x, y, overlay_width - 1, overlay_height - 1, mode=mode, state=state)

                del painter

                new_icon.addPixmap(pixmap, mode, state)

    return new_icon


def _get_qicon_aspect_ratio(icon):
    for mode in _MODES:
        for state in _STATES:
            sizes = icon.availableSizes(mode, state)
            if len(sizes) > 0:
                return sizes[-1].width() / sizes[-1].height()

    return None
