# !/usr/bin/env python3
# -*- coding: utf-8 -*-
# Created by Axel Tremaudant on 07/07/2022

from PySide6 import QtWidgets


class Label(QtWidgets.QLabel):
    def __init__(self, text=""):
        super(Label, self).__init__(text)
        self.key = None

    def set_key(self, key):
        self.key = key

    def get_key(self):
        return self.key
