# !/usr/bin/env python3
# -*- coding: utf-8 -*-
# Created by Axel Tremaudant on 07/06/2022

from PySide6 import QtCore
from math import cos, sin, radians

import data
import element
import ui


class Robot(element.Board):
    def __init__(self, save_data: data.SaveData, parent, main_robot: bool):
        super(Robot, self).__init__(save_data, parent)
        self.element_type = "robot"
        self.main_robot = main_robot
        self.selected = False
        self.origined = False
        self.coord = [0., 0.]
        self.angle = 0
        self.key = None
        self.moving = [0., 0., 0]
        self.on_moving = False
        self.invisible = False
        self.running = False
        self.gcrubs_file = ""
        self.is_updated = False
        self.ready_sequence = False
        self.axis_angle = 0
        self.offset = 0

        if self.main_robot:
            self.speed = self.save_data.get_main_robot('speed')
            self.speed_rotation = self.save_data.get_main_robot('speed_rotation')
            self.name = self.init_data.get_main_robot('name')
        else:
            self.speed = self.save_data.get_second_robot('speed')
            self.speed_rotation = self.save_data.get_second_robot('speed_rotation')
            self.name = self.init_data.get_second_robot('name')
        self.window = ui.Robot(self.parent, self.save_data, self)

    def is_ready_sequence(self) -> bool:
        return self.ready_sequence

    def properties(self):
        self.window.properties_window()

    def is_selected(self) -> bool:
        return self.selected

    def set_selected(self, selected: bool):
        self.selected = selected

    def is_main_robot(self) -> bool:
        return self.main_robot

    def set_on_moving(self, moving: bool):
        self.on_moving = moving

    def is_on_moving(self) -> bool:
        return self.on_moving

    def set_offset(self, value: float):
        self.offset = value

    def get_offset(self) -> float:
        return self.offset

    def is_origined(self) -> bool:
        return self.origined

    def set_origined(self, origined: bool):
        self.origined = origined

    def get_coord(self) -> list:
        return self.coord

    def move(self, dx: int, dy: int):
        """
        Calcule les coordonnees du robot dans le repere global par rapport au deplacement.
        :param dx: Deplacement selon x du repere du robot
        :param dy: Deplacement selon y du repere du robot
        :return: None
        """

        self.coord[0] += dx * cos(radians(self.angle)) - dy * sin(radians(self.angle))
        self.coord[1] += dx * sin(radians(self.angle)) + dy * cos(radians(self.angle))

    def get_angle(self) -> int:
        return self.angle

    def turn(self, angle: int):
        self.angle += angle
        self.angle %= 360

    def set_key(self, key: QtCore.Qt):
        self.key = key

    def get_key(self) -> QtCore.Qt:
        return self.key

    def add_sequence_text(self, text: str):
        self.sequence_text.append(text)

    def get_sequence_text(self) -> str:
        return self.sequence_text.document().toPlainText()

    def set_sequence_text(self, text: str):
        self.sequence_text.setText(text)

    def set_moving(self, dx=0, dy=0, rz=0):
        self.moving[0] += dx
        self.moving[1] += dy
        self.moving[2] += rz

    def update_(self):
        if self.file == '':
            if self.main_robot:
                self.file = self.save_data.get_main_robot('file')
            else:
                self.file = self.save_data.get_second_robot('file')
            self.parent.show_stl(self)
            if self.is_invisible():
                coef = self.init_data.get_main_robot('invisible_coef')
                self.scale(coef, coef, coef)

        if self.main_robot:
            self.setColor(self.save_data.get_main_robot('color'))
            self.set_edge_color(self.save_data.get_main_robot('edge_color'))
            self.axis_angle = self.save_data.get_main_robot('angle_rotation')
            self.offset = self.save_data.get_main_robot('offset')
            self.speed = self.save_data.get_main_robot('speed')
            self.speed_rotation = self.save_data.get_main_robot('speed_rotation')
            self.gcrubs_file = self.save_data.get_main_robot('gcrubs_file')
            self.sequence_text.setText(self.save_data.get_main_robot('sequence'))

            if self.save_data.get_main_robot('axis_rotation') == 'x':
                self.axis_rotation_rb_x.setChecked(True)
                self.axis_rotation_rb_y.setChecked(False)
                self.axis_rotation_rb_z.setChecked(False)
            elif self.save_data.get_main_robot('axis_rotation') == 'y':
                self.axis_rotation_rb_x.setChecked(False)
                self.axis_rotation_rb_y.setChecked(True)
                self.axis_rotation_rb_z.setChecked(False)
            elif self.save_data.get_main_robot('axis_rotation') == 'z':
                self.axis_rotation_rb_x.setChecked(False)
                self.axis_rotation_rb_y.setChecked(False)
                self.axis_rotation_rb_z.setChecked(True)
        else:
            self.setColor(self.save_data.get_second_robot('color'))
            self.set_edge_color(self.save_data.get_second_robot('edge_color'))
            self.axis_angle = self.save_data.get_second_robot('angle_rotation')
            self.offset = self.save_data.get_second_robot('offset')
            self.speed = self.save_data.get_second_robot('speed')
            self.speed_rotation = self.save_data.get_second_robot('speed_rotation')
            self.gcrubs_file = self.save_data.get_second_robot('gcrubs_file')
            self.sequence_text.setText(self.save_data.get_second_robot('sequence'))

            if self.save_data.get_second_robot('axis_rotation') == 'x':
                self.axis_rotation_rb_x.setChecked(True)
                self.axis_rotation_rb_y.setChecked(False)
                self.axis_rotation_rb_z.setChecked(False)
            elif self.save_data.get_second_robot('axis_rotation') == 'y':
                self.axis_rotation_rb_x.setChecked(False)
                self.axis_rotation_rb_y.setChecked(True)
                self.axis_rotation_rb_z.setChecked(False)
            elif self.save_data.get_second_robot('axis_rotation') == 'z':
                self.axis_rotation_rb_x.setChecked(False)
                self.axis_rotation_rb_y.setChecked(False)
                self.axis_rotation_rb_z.setChecked(True)

        if not self.is_updated:
            self.is_updated = True
            self.rotate(self.axis_angle, int(self.axis_rotation_rb_x.isChecked()),
                        int(self.axis_rotation_rb_y.isChecked()), int(self.axis_rotation_rb_z.isChecked()), local=True)

            self.translate(0, 0, self.offset)

    def move_robot(self, dx: float, dy: float, rz: float):
        """
        Deplace le robot et le fait tourner.
        :param dx: Deplacement selon x du repere du robot
        :param dy: Deplacement selon y du repere du robot
        :param rz: Rotation selon z
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

        if self.invisible:
            self.scale(coef, coef, coef)

        self.parent.status_bar.showMessage(
            self.init_data.get_window('position_status_message').format(x=int(self.get_coord()[0]),
                                                                        y=int(self.get_coord()[1]),
                                                                        angle=round(self.get_angle())))

    def set_invisible(self, invisible: bool):
        self.invisible = invisible
        if self.main_robot:
            self.save_data.set_main_robot('invisible', invisible)
        else:
            self.save_data.set_second_robot('invisible', invisible)

    def is_invisible(self) -> bool:
        return self.invisible

    def is_running(self) -> bool:
        return self.running

    def set_running(self, run: bool):
        self.running = run

    def get_gcrubs_file(self) -> str:
        return self.gcrubs_file

    def get_speed(self) -> int:
        return self.speed

    def set_speed(self, speed: int):
        self.speed = speed

    def get_speed_rotation(self) -> int:
        return self.speed_rotation

    def set_speed_rotation(self, speed: int):
        self.speed_rotation = speed

    def set_gcrubs_file(self, file: str):
        self.gcrubs_file = file

    def set_ready_sequence(self, ready: bool):
        self.ready_sequence = ready

    def sequence_list_update(self):
        self.window.sequence_list_update()

    @staticmethod
    def robot_movement(axis: str, angle: int) -> list:
        """
        Calcule le deplacement par rapport a l'angle de rotation pour rester dans le plan.
        :param axis: Axe de rotation du robot lors de la mise en place
        :param angle: Angle de rotation du robot lors de la mise en place
        :return: La liste des deplacements a effectuer [mvt vertical, mvt horizontal, rotation]
                 Chacun contient une liste [dx, dy, dz] pour les deplacements ou [rx, ry, rz] pour la rotation
        """

        if angle == '0':
            return [[1, 0, 0],
                    [0, 1, 0],
                    [0, 0, 1]
                    ]

        if axis == 'x':
            return [[1, 0, 0],
                    [0, cos(radians(angle)), -sin(radians(angle))],
                    [0, sin(radians(angle)), cos(radians(angle))]
                    ]

        elif axis == 'y':
            return [[cos(radians(angle)), 0, sin(radians(angle))],
                    [0, 1, 0],
                    [-sin(radians(angle)), 0, cos(radians(angle))]
                    ]

        elif axis == 'z':
            return [[cos(radians(angle)), -sin(radians(angle)), 0],
                    [sin(radians(angle)), cos(radians(angle)), 0],
                    [0, 0, 1]
                    ]
