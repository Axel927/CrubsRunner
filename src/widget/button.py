# !/usr/bin/env python3
# -*- coding: utf-8 -*-
# Created by Axel Tremaudant on 07/07/2022

"""
Fichier contenant la classe Button.
"""

from PySide6 import QtWidgets


class Button(QtWidgets.QPushButton):
    """
    Redefinition de PySide6.QtWidgets.QPushButton.
    """
    def __init__(self, parent, number: int):
        """
        Constructeur de Button.
        :param parent: PySide6: Fenetre parente
        :param number: int: Numero du bouton
        """
        super(Button, self).__init__(parent)
        self.number = number
        self.clicked_ = False

    def get_number(self) -> int:
        """
        Renvoie le numero du bouton.
        :return: int: Numero
        """
        return self.number

    def set_clicked(self):
        """
        Definit l'etat du bouton en tant que clicke.
        :return: None
        """
        self.clicked_ = True

    def set_unclicked(self):
        """
        Definit l'etat du bouton en tant que non clicke.
        :return: None
        """
        self.clicked_ = False

    def is_clicked(self) -> bool:
        """
        Indique si le robot est clicke.
        :return: bool: clicked
        """
        return self.clicked_
