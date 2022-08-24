#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# © 2022 Tremaudant Axel
# axel.tremaudant@gmail.com

# This software is a computer program whose purpose is to easily and precisely generate sequential file for robots
# used in the Coupe de France de robotique.

# This software is governed by the CeCILL license under French law and abiding by the rules of distribution of free
# software. You can use, modify and/ or redistribute the software under the terms of the CeCILL license as circulated
# by CEA, CNRS and INRIA at the following URL "http://www.cecill.info".
# As a counterpart to the access to the source code and rights to copy, modify and redistribute granted by the license,
# users are provided only with a limited warranty and the software's author, the holder of the economic rights,
# and the successive licensors have only limited liability.
# In this respect, the user's attention is drawn to the risks associated with loading, using, modifying
# and/or developing or reproducing the software by the user in light of its specific status of free software,
# that may mean that it is complicated to manipulate, and that also
# therefore means that it is reserved for developers and experienced professionals having in-depth computer knowledge.
# Users are therefore encouraged to load and test the software's suitability as regards their requirements in conditions
# enabling the security of their systems and/or data to be ensured and, more generally, to use and operate it
# in the same conditions as regards security.
# The fact that you are presently reading this means that you have had knowledge of the CeCILL license
# and that you accept its terms.


"""
Fichier contenant la classe ListWidget.
"""

from PyQt5 import QtWidgets, QtCore


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
