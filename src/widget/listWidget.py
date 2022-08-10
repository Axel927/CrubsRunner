# !/usr/bin/env python3
# -*- coding: utf-8 -*-
# Created by Axel Tremaudant on 07/07/2022

"""
Fichier contenant la classe ListWidget.
"""

from PySide6 import QtWidgets, QtCore


class ListWidget(QtWidgets.QListWidget):
    """
    Redefinition de QtWidgets.QListWidget.
    """
    def __init__(self):
        """
        Constructeur de ListWidget.
        """
        super(ListWidget, self).__init__()
        self.contents = list()
        self.len = 0

    def add_content(self, elem):
        """
        Ajoute un element a la liste.
        :param elem: any: Element a ajouter
        :return: None
        """
        self.contents.append(elem)
        self.len += 1
        try:
            self.addItem(elem.get_name())
        except AttributeError:
            if isinstance(elem, str):
                self.addItem(elem)

    def get_contents(self) -> list:
        """
        Renvoie tous les elements.
        :return: list: Elements
        """
        return self.contents

    def get_content_row(self, item) -> int:
        """
        Renvoie la position de l'item dans la liste.
        Renvoie 0 si pas dans la liste.
        :param item: Item de la liste
        :return: int: Position
        """
        for i in range(len(self.contents)):
            if item == self.contents[i]:
                return i
        return 0

    def remove_content(self, position: int):
        """
        Supprime l'element a la position entree.
        :param position: int: Position a supprimer
        :return: None
        """
        try:
            self.takeItem(position)
            self.contents.pop(position)
            self.len -= 1
        except IndexError:
            return

    def get_len(self) -> int:
        """
        Renvoie le nombre d'elements
        :return: int: Nombre d'elements
        """
        return self.len

    def clear(self) -> None:
        """
        Supprime tous les elements.
        :return: None
        """
        super(ListWidget, self).clear()
        self.contents = list()
        self.len = 0

    def sortItems(self, order: QtCore.Qt.SortOrder = ...) -> None:
        """
        Trie les elements.
        :param order: QtCore.Qt.SortOrder: Ordre de tri
        :return: None
        """
        super(ListWidget, self).sortItems(order)
        if order == QtCore.Qt.DescendingOrder:
            self.contents.sort(reverse=True)
        else:
            self.contents.sort(reverse=False)
