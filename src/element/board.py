# !/usr/bin/env python3
# -*- coding: utf-8 -*-
# Created by Axel Tremaudant on 07/07/2022

"""
Fichier contenant la classe Board, partie objet.
"""

import functions
import element
import data
import ui


class Board(element.CoordSys):
    """
    Classe qui gere la partie 3D du plateau.
    """
    def __init__(self, save_data: data.Save, parent):
        """
        Constructeur de Board.
        :param save_data: data.Save: Les donnees de sauvegarde y sont recuperees et ecrites
        :param parent: ui.MainWindow: Fenetre principale
        """
        super(Board, self).__init__(save_data)

        self.parent = parent
        self.file = self.init_data.get_board('file')
        self.name = self.init_data.get_board('name')
        self.window = ui.Board(self.parent, self.save_data, self)

    def properties(self):
        """
        Cree la fenetre de proprietes du plateau.
        :return: None
        """
        self.window.properties_window()

    def update_(self):
        """
        Met a jour les donnees du plateau a partir des donnees de sauvegarde.
        :return: None
        """
        if self.file == '':
            self.file = self.save_data.get_board('file')
            functions.object.show_stl(self)

        self.setColor(self.save_data.get_board('color'))
        self.set_edge_color(self.save_data.get_board('edge_color'))
        if self.file == "":
            self.remove(False)

    def remove(self, message: bool):
        """
        Retire l'element.
        :param message: bool: Si True, affiche un message
        :return: None
        """
        self.window.remove(message)
