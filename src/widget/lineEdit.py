# !/usr/bin/env python3
# -*- coding: utf-8 -*-
# Created by Axel Tremaudant on 07/07/2022

"""
Fichier contenant la classe LineEdit.
"""

from PyQt5 import QtWidgets, QtCore


class LineEdit(QtWidgets.QLineEdit):
    """
    Redefinition de QtWidgets.QLineEdit.
    """
    def __init__(self, parent):
        """
        Constructeur de LineEdit.
        :param parent: PySide6: Fenetre parente
        """
        super(LineEdit, self).__init__(parent)
        self.key = QtCore.Qt.Key(0)

    def set_key(self, value):
        """
        Definition de la touche correspondant a la ligne.
        :param value: any: Touche
        :return: None
        """
        if value is None:
            self.key = QtCore.Qt.Key(0)
        else:
            self.key = QtCore.Qt.Key(value)

    def get_key(self):
        """
        Renvoie la touche associee a la ligne
        :return: any: Touche
        """
        return self.key
