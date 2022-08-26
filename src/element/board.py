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
Fichier contenant la classe Board, partie objet.
"""

from src import functions
from src import element
from src import ui


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
        self.file = str()
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
            if not functions.object.show_mesh(self):
                self.file = ''
                self.remove(False)
                return

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

    def set_offset(self, value: int):
        """
        Definit la valeur de l'offset pour la hauteur au dessus du plateau a laquelle doit etre le robot.
        :param value: int: Valeur de l'offset
        :return: None
        """
        self.offset = int(value)

    def get_offset(self) -> int:
        """
        Renvoie la valeur de l'offset.
        :return: int: Valeur de l'offset
        """
        return self.offset
