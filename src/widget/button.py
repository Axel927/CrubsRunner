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
Fichier contenant la classe Button.
"""

from PyQt5 import QtWidgets


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
