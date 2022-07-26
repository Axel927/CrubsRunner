# !/usr/bin/env python3
# -*- coding: utf-8 -*-
# Created by Axel Tremaudant on 07/07/2022

"""
Fichier contenant la classe KeyDialog.
"""

from PySide6 import QtWidgets, QtGui, QtCore


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
