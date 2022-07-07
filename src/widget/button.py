# !/usr/bin/env python3
# -*- coding: utf-8 -*-
# Created by Axel Tremaudant on 07/07/2022

from PySide6 import QtWidgets


class Button(QtWidgets.QPushButton):
    def __init__(self, parent, number):
        super(Button, self).__init__(parent)
        self.number = number
        self.clicked_ = False

    def get_number(self):
        return self.number

    def set_clicked(self):
        self.clicked_ = True

    def set_unclicked(self):
        self.clicked_ = False

    def is_clicked(self):
        return self.clicked_
