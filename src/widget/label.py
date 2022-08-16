# !/usr/bin/env python3
# -*- coding: utf-8 -*-
# Created by Axel Tremaudant on 07/07/2022

"""
Fichier contenant la classe Label.
"""

from PyQt5 import QtWidgets


class Label(QtWidgets.QLabel):
    """
    Redefinition de QtWidgets.QLabel.
    """
    def __init__(self, text=""):
        """
        Constructeur de Label.
        :param text: str: Texte a ecrire dans le label.
        """
        super(Label, self).__init__(text)
        self.key = None

    def set_key(self, key):
        """
        Definition de la touche correspondant au label.
        :param key: any: Touche
        :return: None
        """
        self.key = key

    def get_key(self):
        """
        Renvoie la touche associee au label
        :return: any: Touche
        """
        return self.key
