# !/usr/bin/env python3
# -*- coding: utf-8 -*-
# Created by Axel Tremaudant on 07/07/2022

"""
Fichier contenant la classe Board, partie objet.
"""

import functions
import element
import ui


class Board(element.CoordSys):
    """
    Classe qui gere la partie 3D du plateau.
    """
    def __init__(self, save_data, parent):
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
        self.axis_angle = 0
        self.offset = 0
        self.is_updated = False

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
            functions.object.show_mesh(self)

        self.setColor(self.save_data.get_board('color'))
        self.set_edge_color(self.save_data.get_board('edge_color'))

        self.offset = self.save_data.get_board('offset')
        self.translate(0, 0, self.offset)

        self.axis_angle = self.save_data.get_board('angle_rotation')
        if self.save_data.get_board('axis_rotation') == 'x':
            self.window.axis_rotation_rb_x.setChecked(True)
            self.window.axis_rotation_rb_y.setChecked(False)
            self.window.axis_rotation_rb_z.setChecked(False)
        elif self.save_data.get_board('axis_rotation') == 'y':
            self.window.axis_rotation_rb_x.setChecked(False)
            self.window.axis_rotation_rb_y.setChecked(True)
            self.window.axis_rotation_rb_z.setChecked(False)
        elif self.save_data.get_board('axis_rotation') == 'z':
            self.window.axis_rotation_rb_x.setChecked(False)
            self.window.axis_rotation_rb_y.setChecked(False)
            self.window.axis_rotation_rb_z.setChecked(True)

        if self.file == "":
            self.remove(False)

        if not self.is_updated:  # Si le plateau n'a pas deja ete mis a jour
            self.is_updated = True
            self.rotate(self.axis_angle, int(self.window.axis_rotation_rb_x.isChecked()),
                        int(self.window.axis_rotation_rb_y.isChecked()),
                        int(self.window.axis_rotation_rb_z.isChecked()), local=True)

    def remove(self, message: bool):
        """
        Retire l'element.
        :param message: bool: Si True, affiche un message
        :return: None
        """
        self.window.remove(message)

    def get_axis_angle(self) -> int:
        """
        Renvoie l'angle de rotation autour de l'axe (lors de la mise en place)
        :return: int: angle
        """
        return self.axis_angle

    def set_axis_angle(self, angle: int):
        """
        Definit l'angle de rotation autour de l'axe (lors de la mise en place)
        :param angle: int: angle
        :return: None
        """
        self.axis_angle = angle

    def set_offset(self, value: float):
        """
        Definit la valeur de l'offset pour la hauteur au dessus du plateau a laquelle doit etre le robot.
        :param value: float: Valeur de l'offset
        :return: None
        """
        self.offset = value

    def get_offset(self) -> float:
        """
        Renvoie la valeur de l'offset.
        :return: float: Valeur de l'offset
        """
        return self.offset
