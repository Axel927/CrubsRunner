# !/usr/bin/env python3
# -*- coding: utf-8 -*-
# Created by Axel Tremaudant on 07/07/2022

from PySide6 import QtWidgets, QtCore


class LineEdit(QtWidgets.QLineEdit):
    def __init__(self, parent):
        super(LineEdit, self).__init__(parent)
        self.key = QtCore.Qt.Key(0)

    def set_key(self, value):
        if value is None:
            self.key = QtCore.Qt.Key(0)
        else:
            self.key = QtCore.Qt.Key(value)

    def get_key(self):
        return self.key
