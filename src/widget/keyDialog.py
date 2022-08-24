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
Fichier contenant la classe KeyDialog.
"""

from PyQt5 import QtWidgets, QtGui, QtCore


class KeyDialog(QtWidgets.QDialog):
    """
    Classe qui redefinit PySide6.QtWidgets.QDialog.
    """
    def __init__(self, save_data, parent=None):
        """
        Constructeur de KeyDialog.
        :param save_data: data.Save: Donnees de sauvegarde
        :param parent: PySide6: Fenetre parente
        """
        super(KeyDialog, self).__init__(parent)
        self.save_data = save_data
        self.init_data = self.save_data.get_init_data()
        self.movement = ''
        self.key = None
        self.to_write = None
        self.movements = list(self.save_data.get_gcrubs('keys').keys())

    def set_movement(self, movement: str):
        """
        Definit le mouvement (vers la droite, vers la gauche, vers le haut, vers le bas,
        tourner a droite, tourner a gauche, ...).
        :param movement: str: Mouvement
        :return: None
        """
        self.movement = movement

    def get_key(self, to_write):
        """
        Ecrit la touche appuyee dans to_write
        :param to_write: any: La ou est enregistree la touche
        :return: None
        """
        self.to_write = to_write

    def keyReleaseEvent(self, event: QtGui.QKeyEvent) -> None:
        """
        Methode qui detecte lorsqu'une touche est relachee.
        :param event: QtGui.QKeyEvent: Evenement
        :return: None
        """
        if self.movement in self.movements:
            self.key = event.key()
            self.to_write.setText(self.init_data.get_window('keys_lbl_key').format(key=self.ret_key(event)))
            self.to_write.set_key(event.key())

    @staticmethod
    def ret_key(event) -> str:
        """
        Renvoie une string pour des touches du clavier.
        :param event: any: Evenement
        :return: None
        """

        try:
            if event.key() == QtCore.Qt.Key_Up:
                return "Fleche du haut"
            elif event.key() == QtCore.Qt.Key_Down:
                return "Fleche du bas"
            elif event.key() == QtCore.Qt.Key_Right:
                return "Fleche de droite"
            elif event.key() == QtCore.Qt.Key_Left:
                return "Fleche de gauche"
            else:
                return str(event.text()).upper()
        except AttributeError:
            if event == QtCore.Qt.Key_Up:
                return "Fleche du haut"
            elif event == QtCore.Qt.Key_Down:
                return "Fleche du bas"
            elif event == QtCore.Qt.Key_Right:
                return "Fleche de droite"
            elif event == QtCore.Qt.Key_Left:
                return "Fleche de gauche"
            else:
                try:
                    return str(chr(event))
                except (ValueError, TypeError):
                    return ""
