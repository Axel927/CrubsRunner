# !/usr/bin/env python3
# -*- coding: utf-8 -*-
# Created by Axel Tremaudant on 07/07/2022

from PySide6 import QtWidgets, QtCore


class ListWidget(QtWidgets.QListWidget):
    def __init__(self):
        super(ListWidget, self).__init__()
        self.contents = list()
        self.len = 0

    def add_content(self, elem):
        self.contents.append(elem)
        self.len += 1
        try:
            self.addItem(elem.get_name())
        except AttributeError:
            pass

    def get_contents(self) -> list:
        return self.contents

    def remove_content(self, position: int):
        try:
            self.takeItem(position)
            self.contents.pop(position)
            self.len -= 1
        except IndexError:
            return

    def get_len(self) -> int:
        return self.len

    def clear(self) -> None:
        super(ListWidget, self).clear()
        self.contents = list()
        self.len = 0

    def sortItems(self, order: QtCore.Qt.SortOrder = ...) -> None:
        super(ListWidget, self).sortItems(order)
        if order == QtCore.Qt.DescendingOrder:
            self.contents.sort(reverse=True)
        else:
            self.contents.sort(reverse=False)
