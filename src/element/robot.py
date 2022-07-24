# !/usr/bin/env python3
# -*- coding: utf-8 -*-
# Created by Axel Tremaudant on 07/06/2022

"""
Fichier de la classe Robot.
"""

from PySide6 import QtCore
from math import cos, sin, radians

import data
import element
import functions
import ui


class Robot(element.Board):
    """
    Classe qui gere la partie 3D des robots.
    """
    def __init__(self, save_data: data.Save, parent, main_robot: bool):
        """
        Constructeur de Robot.
        :param save_data: data.Save: Les donnees de sauvegarde y sont recuperees et ecrites
        :param parent: ui.MainWindow: Fenetre principale
        :param main_robot: bool: Indique s'il s'agit du robot principal.
        """
        super(Robot, self).__init__(save_data, parent)
        self.element_type = "robot"
        self.main_robot = main_robot
        self.selected = False
        self.origined = False
        self.coord = [0., 0.]
        self.angle = 0
        self.key = None
        self.moving = [0., 0., 0]
        self.invisible = False
        self.running = False
        self.gcrubs_file = ""
        self.ready_sequence = False

        if self.main_robot:
            self.speed = self.save_data.get_main_robot('speed')
            self.speed_rotation = self.save_data.get_main_robot('speed_rotation')
            self.name = self.init_data.get_main_robot('name')
        else:
            self.speed = self.save_data.get_second_robot('speed')
            self.speed_rotation = self.save_data.get_second_robot('speed_rotation')
            self.name = self.init_data.get_second_robot('name')
        self.window = ui.Robot(self.parent, self.save_data, self)

    def is_selected(self) -> bool:
        """
        Indique si le robot est selectionne.
        :return: bool: selected
        """
        return self.selected

    def set_selected(self, selected: bool):
        """
        Definit si le robot est selectionne.
        :param selected: bool: selected
        :return: None
        """
        self.selected = selected

    def is_main_robot(self) -> bool:
        """
        Indique s'il s'agit du robot principal.
        :return: bool: main_robot
        """
        return self.main_robot

    def is_origined(self) -> bool:
        """
        Indique si l'origine du robot a ete definie.
        :return: bool: Origine definie
        """
        return self.origined

    def set_origined(self, origined: bool):
        """
        Definit si l'origine du robot est definie.
        :param origined: bool: Origine definie
        :return: None
        """
        self.origined = origined

    def get_coord(self) -> list:
        """
        Renvoie les coordonnees du robot dans le repere global.
        :return: list: [x, y] contient des flottants
        """
        return self.coord

    def move(self, dx: int, dy: int):
        """
        Calcule les coordonnees du robot dans le repere global par rapport au deplacement.
        :param dx: int: Deplacement selon x du repere du robot
        :param dy: int: Deplacement selon y du repere du robot
        :return: None
        """

        self.coord[0] += dx * cos(radians(self.angle)) - dy * sin(radians(self.angle))
        self.coord[1] += dx * sin(radians(self.angle)) + dy * cos(radians(self.angle))

    def get_angle(self) -> int:
        """
        Renvoie l'angle de rotation du robot en degres.
        :return: int: angle
        """
        return self.angle

    def turn(self, angle: int):
        """
        Tourne le robot d'une variation d'angle angle en degres.
        :param angle: int: Variation d'angle
        :return: None
        """
        self.angle += angle
        self.angle %= 360

    def set_key(self, key: QtCore.Qt):
        """
        Definit la touche du robot qui l'a fait se deplacer.
        :param key: PySide6.QtCore.Qt: cle
        :return: None
        """
        self.key = key

    def get_key(self) -> QtCore.Qt:
        """
        Renvoie la derniere touche du robot qui l'a fait se deplacer.
        :return: PySide6.QtCore.Qt: cle
        """
        return self.key

    def get_window(self):
        """
        Renvoie la fenetre des proprietes du robot.
        :return: ui.Robot: window
        """
        return self.window

    def set_moving(self, dx=0., dy=0., rz=0.):
        """
        Fait bouger le robot selon dx, dy et rz dans le repere local.
        :param dx: float: Deplacement selon x
        :param dy: float: Deplacement selon y
        :param rz: float: Rotation selon z
        :return: None
        """
        self.moving[0] += dx
        self.moving[1] += dy
        self.moving[2] += rz

    def update_(self):
        """
        Met les donnees du robot a jour.
        :return: None
        """
        if self.file == '':
            if self.main_robot:
                self.file = self.save_data.get_main_robot('file')
            else:
                self.file = self.save_data.get_second_robot('file')
            functions.object.show_stl(self)

            if self.is_invisible():  # Si le robot est minuscule
                coef = self.init_data.get_main_robot('invisible_coef')
                self.scale(coef, coef, coef)  # Agrandit le robot

        if self.main_robot:
            self.setColor(self.save_data.get_main_robot('color'))
            self.set_edge_color(self.save_data.get_main_robot('edge_color'))
            self.axis_angle = self.save_data.get_main_robot('angle_rotation')
            self.offset = self.save_data.get_main_robot('offset')
            self.speed = self.save_data.get_main_robot('speed')
            self.speed_rotation = self.save_data.get_main_robot('speed_rotation')
            self.gcrubs_file = self.save_data.get_main_robot('gcrubs_file')

            if self.save_data.get_main_robot('axis_rotation') == 'x':
                self.window.axis_rotation_rb_x.setChecked(True)
                self.window.axis_rotation_rb_y.setChecked(False)
                self.window.axis_rotation_rb_z.setChecked(False)
            elif self.save_data.get_main_robot('axis_rotation') == 'y':
                self.window.axis_rotation_rb_x.setChecked(False)
                self.window.axis_rotation_rb_y.setChecked(True)
                self.window.axis_rotation_rb_z.setChecked(False)
            elif self.save_data.get_main_robot('axis_rotation') == 'z':
                self.window.axis_rotation_rb_x.setChecked(False)
                self.window.axis_rotation_rb_y.setChecked(False)
                self.window.axis_rotation_rb_z.setChecked(True)
        else:
            self.setColor(self.save_data.get_second_robot('color'))
            self.set_edge_color(self.save_data.get_second_robot('edge_color'))
            self.axis_angle = self.save_data.get_second_robot('angle_rotation')
            self.offset = self.save_data.get_second_robot('offset')
            self.speed = self.save_data.get_second_robot('speed')
            self.speed_rotation = self.save_data.get_second_robot('speed_rotation')
            self.gcrubs_file = self.save_data.get_second_robot('gcrubs_file')

            if self.save_data.get_second_robot('axis_rotation') == 'x':
                self.window.axis_rotation_rb_x.setChecked(True)
                self.window.axis_rotation_rb_y.setChecked(False)
                self.window.axis_rotation_rb_z.setChecked(False)
            elif self.save_data.get_second_robot('axis_rotation') == 'y':
                self.window.axis_rotation_rb_x.setChecked(False)
                self.window.axis_rotation_rb_y.setChecked(True)
                self.window.axis_rotation_rb_z.setChecked(False)
            elif self.save_data.get_second_robot('axis_rotation') == 'z':
                self.window.axis_rotation_rb_x.setChecked(False)
                self.window.axis_rotation_rb_y.setChecked(False)
                self.window.axis_rotation_rb_z.setChecked(True)

        if self.file == "":
            self.remove(False)

        if not self.is_updated:  # Si le robot n'a pas deja ete mis a jour
            self.is_updated = True
            self.rotate(self.axis_angle, int(self.window.axis_rotation_rb_x.isChecked()),
                        int(self.window.axis_rotation_rb_y.isChecked()),
                        int(self.window.axis_rotation_rb_z.isChecked()), local=True)

            self.translate(0, 0, self.offset)

    def move_robot(self, dx: float, dy: float, rz: float):
        """
        Deplace le robot et le fait tourner.
        :param dx: float: Deplacement selon x du repere du robot
        :param dy: float: Deplacement selon y du repere du robot
        :param rz: float: Rotation selon z
        :return: None
        """

        coef = self.init_data.get_main_robot('invisible_coef')
        # Ne pas chercher mais laisser meme si ca parait inutile, pb lors des deplacements sinon
        if self.invisible:
            self.scale(1 / coef, 1 / coef, 1 / coef)

        if self.main_robot:
            mvt = self.robot_movement(self.save_data.get_main_robot('axis_rotation'),
                                      self.save_data.get_main_robot('angle_rotation'))
        else:
            mvt = self.robot_movement(self.save_data.get_second_robot('axis_rotation'),
                                      self.save_data.get_second_robot('angle_rotation'))

        self.translate(dx * mvt[0][0] + dy * mvt[1][0], dx * mvt[0][1] + dy * mvt[1][1],
                       dx * mvt[0][2] + dy * mvt[1][2], local=True)
        self.move(dx, dy)

        self.translate(-self.get_coord()[0], -self.get_coord()[1], 0, local=False)
        self.rotate(rz % 360, 0, 0, 1, local=False)
        self.turn(rz % 360)
        self.translate(self.get_coord()[0], self.get_coord()[1], 0, local=False)

        if self.invisible:  # Seconde partie de ce qu'il ne faut pas enlever
            self.scale(coef, coef, coef)

        self.parent.status_bar.showMessage(
            self.init_data.get_window('position_status_message').format(x=int(self.get_coord()[0]),
                                                                        y=int(self.get_coord()[1]),
                                                                        angle=round(self.get_angle())))

    def set_invisible(self, invisible: bool):
        """
        Definit si le robot est minuscule.
        :param invisible: bool: invisible
        :return: None
        """
        self.invisible = invisible
        if self.main_robot:
            self.save_data.set_main_robot('invisible', invisible)
        else:
            self.save_data.set_second_robot('invisible', invisible)

    def is_invisible(self) -> bool:
        """
        Indique si le robot est minuscule a la creation.
        :return: bool: invisible
        """
        return self.invisible

    def is_running(self) -> bool:
        """
        Indique si le robot fait la simulation.
        :return: bool: running
        """
        return self.running

    def set_running(self, run: bool):
        """
        Definit si le robot fait la simulation.
        :param run: bool: running
        :return: None
        """
        self.running = run

    def get_gcrubs_file(self) -> str:
        """
        Renvoie le fichier sequentiel.
        :return: str: Fichier
        """
        return self.gcrubs_file

    def set_gcrubs_file(self, file: str):
        """
        Definit le fichier sequentiel.
        :param file: str: Fichier
        :return: None
        """
        self.gcrubs_file = file

    def get_speed(self) -> int:
        """
        Renvoie la vitesse de deplacement du robot en mm/s.
        :return: int: Vitesse
        """
        return self.speed

    def set_speed(self, speed: int):
        """
        Definit la vitesse de deplacement du robot en mm/s.
        :param speed: int: Vitesse
        :return: None
        """
        self.speed = speed

    def get_speed_rotation(self) -> int:
        """
        Renvoie la vitesse de rotation du robot en degres/s.
        :return: int: Vitesse
        """
        return self.speed_rotation

    def set_speed_rotation(self, speed: int):
        """
        Definit la vitesse de rotation du robot en degres/s.
        :param speed: int: Vitesse de rotation
        :return: None
        """
        self.speed_rotation = speed

    def is_ready_sequence(self) -> bool:
        """
        Indique si le robot est pret a creer la sequence.
        :return: bool: ready_sequence
        """
        return self.ready_sequence

    def set_ready_sequence(self, ready: bool):
        """
        Definit si le robot est pret a creer la sequence.
        :param ready: bool: ready_sequence
        :return: None
        """
        self.ready_sequence = ready

    def sequence_list_update(self):
        """
        Met a jour la sequence_list de la fenetre de proprietes
        :return: None
        """
        self.window.sequence_list_update()

    @staticmethod
    def robot_movement(axis: str, angle: int) -> tuple:
        """
        Calcule le deplacement par rapport a l'angle de rotation pour rester dans le plan.

        Liste des axes :
            x, y, z

        :param axis: str: Axe de rotation du robot lors de la mise en place
        :param angle: int: Angle de rotation du robot lors de la mise en place
        :return: Le tuple des deplacements a effectuer (mvt vertical, mvt horizontal, rotation)
                 Chacun contient un tuple (dx, dy, dz) pour les deplacements ou (rx, ry, rz) pour la rotation
        """

        if angle == 0:
            return ((1, 0, 0),
                    (0, 1, 0),
                    (0, 0, 1)
                    )

        if axis == 'x':
            return ((1, 0, 0),
                    (0, cos(radians(angle)), -sin(radians(angle))),
                    (0, sin(radians(angle)), cos(radians(angle)))
                    )

        elif axis == 'y':
            return ((cos(radians(angle)), 0, sin(radians(angle))),
                    (0, 1, 0),
                    (-sin(radians(angle)), 0, cos(radians(angle)))
                    )

        elif axis == 'z':
            return ((cos(radians(angle)), -sin(radians(angle)), 0),
                    (sin(radians(angle)), cos(radians(angle)), 0),
                    (0, 0, 1)
                    )

        else:
            return None
