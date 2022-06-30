# !/usr/bin/env python3
# -*- coding: utf-8 -*-
# Created by Axel Tremaudant on 17/06/22

from PySide6 import QtWidgets, QtCore, QtGui
from math import cos, sin, radians
import pyqtgraph.opengl as gl
import data


class Button(QtWidgets.QPushButton):
    def __init__(self, parent, number):
        super(Button, self).__init__(parent)
        self.number = number
        self.clicked_ = False

    def get_number(self):
        return self.number

    def set_clicked(self):
        self.clicked_ = True

    def set_unclicked(self):
        self.clicked_ = False

    def is_clicked(self):
        return self.clicked_


class LineEdit(QtWidgets.QLineEdit):
    def __init__(self, parent):
        super(LineEdit, self).__init__(parent)
        self.key = QtCore.Qt.Key(0)

    def set_key(self, value):
        if value is None:
            self.key = QtCore.Qt.Key(0)
        else:
            self.key = QtCore.Qt.Key(value)

    def get_key(self):
        return self.key


class ListWidget(QtWidgets.QListWidget):
    def __init__(self):
        super(ListWidget, self).__init__()
        self.contents = list()
        self.len = 0

    def add_content(self, elem):
        self.contents.append(elem)
        self.len += 1

    def get_contents(self) -> list:
        return self.contents

    def remove_content(self, position: int):
        self.contents.pop(position)
        self.len -= 1

    def get_len(self) -> int:
        return self.len

    def clear(self) -> None:
        super(ListWidget, self).clear()
        self.contents = list()
        self.len = 0

    def sortItems(self, order: QtCore.Qt.SortOrder = ...) -> None:
        super(ListWidget, self).sortItems(order)
        if order == QtCore.Qt.DescendingOrder:
            self.contents.sort(reverse=True)
        else:
            self.contents.sort(reverse=False)


class GlViewWidget(gl.GLViewWidget):
    # Redefinition de methodes de pyqtgraph.opengl.GLViewWidget

    def __init__(self, parent, save_data: data.SaveData):
        super(GlViewWidget, self).__init__()
        self.save_data = save_data
        self.init_data = data.InitData()
        self.mousePos = None
        self.parent = parent
        self.getting_key = False
        self.key = None
        self.text = ""
        self.write_key = None
        self.dist = 0
        self.angle = 0
        self.sequence_text = ""

    @staticmethod
    def robot_movement(axis: str, angle: int) -> list:
        """
        Permet de deplacer le robot avec les memes touches quelle que soit la rotation subie lors de la mise en place.

        :param axis: Axe de rotation du robot lors de la mise en place
        :param angle: Angle de rotation du robot lors de la mise en place
        :return: La liste des deplacements a effectuer [mvt vertical, mvt horizontal, rotation]
                 Chacun contient une liste [dx, dy, dy] pour les deplacements ou [rx, ry, rz] pour la rotation
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

    def mouseMoveEvent(self, ev):
        self.setCursor(self.init_data.get_view('moving_cursor'))
        lpos = ev.position() if hasattr(ev, 'position') else ev.localPos()
        diff = lpos - self.mousePos
        self.mousePos = lpos

        if ev.buttons() == self.init_data.get_view('rotation_view_key'):
            if ev.modifiers() & self.init_data.get_view('moving_view1'):
                self.pan(diff.x(), diff.y(), 0, relative='view')
            else:
                self.orbit(-diff.x(), diff.y())
        elif ev.buttons() == self.init_data.get_view('moving_view_middle_button'):
            if ev.modifiers() & self.init_data.get_view('moving_view_middle_button1'):
                self.pan(diff.x(), 0, diff.y(), relative='view-upright')
            else:
                self.pan(diff.x(), diff.y(), 0, relative='view-upright')
        elif ev.buttons() == self.init_data.get_view('moving_view2'):
            self.pan(diff.x(), diff.y(), 0, relative='view')

    def keyPressEvent(self, event: QtGui.QKeyEvent) -> None:
        if self.getting_key:
            self.key.setText(self.text + self.ret_key(event))
            self.write_key.set_key(event.key())

        if self.parent.main_robot.is_selected():
            elem = self.parent.main_robot
            axis = self.save_data.get_main_robot('axis_rotation')
            angle = self.save_data.get_main_robot('angle_rotation')
            invisible = self.save_data.get_main_robot('invisible')
        elif self.parent.second_robot.is_selected():
            elem = self.parent.second_robot
            axis = self.save_data.get_second_robot('axis_rotation')
            angle = self.save_data.get_second_robot('angle_rotation')
            invisible = self.save_data.get_second_robot('invisible')
        else:
            return

        speed = self.save_data.get_grid('moving_speed')
        mvt = self.robot_movement(axis, angle)

        for key, cmd in zip(self.save_data.get_gcrubs('cmd_key').keys(),
                            self.save_data.get_gcrubs('cmd_key').values()):
            if event.key() == cmd and event.key() != QtCore.Qt.Key_Right and event.key() != QtCore.Qt.Key_Left and \
                    event.key() != QtCore.Qt.Key_Down and event.key() != QtCore.Qt.Key_Up and \
                    event.key() != QtCore.Qt.Key_D and event.key() != QtCore.Qt.Key_Q:
                elem.add_sequence_text(self.save_data.get_gcrubs('cmd_name').get(key))
                elem.set_key(None)
                return

        coef = self.init_data.get_main_robot('invisible_coef')
        if invisible:  # Ne pas chercher mais laisser meme si ca parait inutile, pb lors des deplacements sinon
            elem.scale(1 / coef, 1 / coef, 1 / coef)

        if event.key() == QtCore.Qt.Key_Right:
            elem.translate(mvt[0][0] * speed, mvt[0][1] * speed, mvt[0][2] * speed, local=True)
            elem.move(speed, 0)
            for key, cmd in zip(self.save_data.get_gcrubs('cmd_key').keys(),
                                self.save_data.get_gcrubs('cmd_key').values()):
                if cmd == event.key():
                    if elem.get_key() != event.key():
                        self.dist = 0
                        self.sequence_text = elem.get_sequence_text()
                        self.parent.do([elem, 0, 0, 0])
                    self.dist += speed
                    elem.set_sequence_text(self.sequence_text)
                    self.parent.updo([elem, -self.dist, 0, 0])
                    try:
                        elem.add_sequence_text(self.save_data.get_gcrubs('cmd_name').get(key).format(dist=self.dist))
                    except KeyError:
                        elem.add_sequence_text(self.save_data.get_gcrubs('cmd_name').get(key))
                    break

        elif event.key() == QtCore.Qt.Key_Left:
            elem.translate(-mvt[0][0] * speed, -mvt[0][1] * speed, -mvt[0][2] * speed, local=True)
            elem.move(-speed, 0)
            for key, cmd in zip(self.save_data.get_gcrubs('cmd_key').keys(),
                                self.save_data.get_gcrubs('cmd_key').values()):
                if cmd == event.key():
                    if elem.get_key() != event.key():
                        self.dist = 0
                        self.sequence_text = elem.get_sequence_text()
                        self.parent.do([elem, 0, 0, 0])
                    self.dist += speed
                    elem.set_sequence_text(self.sequence_text)
                    self.parent.updo([elem, self.dist, 0, 0])
                    try:
                        elem.add_sequence_text(self.save_data.get_gcrubs('cmd_name').get(key).format(dist=self.dist))
                    except KeyError:
                        elem.add_sequence_text(self.save_data.get_gcrubs('cmd_name').get(key))
                    break

        elif event.key() == QtCore.Qt.Key_Down:
            elem.translate(-mvt[1][0] * speed, -mvt[1][1] * speed, -mvt[1][2] * speed, local=True)
            elem.move(0, -speed)
            for key, cmd in zip(self.save_data.get_gcrubs('cmd_key').keys(),
                                self.save_data.get_gcrubs('cmd_key').values()):
                if cmd == event.key():
                    if elem.get_key() != event.key():
                        self.dist = 0
                        self.sequence_text = elem.get_sequence_text()
                        self.parent.do([elem, 0, 0, 0])
                    self.dist += speed
                    elem.set_sequence_text(self.sequence_text)
                    self.parent.updo([elem, 0, self.dist, 0])
                    try:
                        elem.add_sequence_text(self.save_data.get_gcrubs('cmd_name').get(key).format(dist=self.dist))
                    except KeyError:
                        elem.add_sequence_text(self.save_data.get_gcrubs('cmd_name').get(key))
                    break

        elif event.key() == QtCore.Qt.Key_Up:
            elem.translate(mvt[1][0] * speed, mvt[1][1] * speed, mvt[1][2] * speed, local=True)
            elem.move(0, speed)
            for key, cmd in zip(self.save_data.get_gcrubs('cmd_key').keys(),
                                self.save_data.get_gcrubs('cmd_key').values()):
                if cmd == event.key():
                    if elem.get_key() != event.key():
                        self.dist = 0
                        self.sequence_text = elem.get_sequence_text()
                        self.parent.do([elem, 0, 0, 0])
                    self.dist += speed
                    elem.set_sequence_text(self.sequence_text)
                    self.parent.updo([elem, 0, -self.dist, 0])
                    try:
                        elem.add_sequence_text(self.save_data.get_gcrubs('cmd_name').get(key).format(dist=self.dist))
                    except KeyError:
                        elem.add_sequence_text(self.save_data.get_gcrubs('cmd_name').get(key))
                    break

        elif event.key() == QtCore.Qt.Key_Q:
            if elem.is_origined():
                elem.translate(-elem.get_coord()[0], -elem.get_coord()[1], 0, local=False)
                elem.rotate(speed, 0, 0, 1, local=False)
                elem.translate(elem.get_coord()[0], elem.get_coord()[1], 0, local=False)

            else:
                elem.rotate(speed, mvt[2][0], mvt[2][1], mvt[2][2], local=True)

            elem.turn(speed)

            for key, cmd in zip(self.save_data.get_gcrubs('cmd_key').keys(),
                                self.save_data.get_gcrubs('cmd_key').values()):
                if cmd == event.key():
                    if elem.get_key() != event.key():
                        self.angle = 0
                        self.sequence_text = elem.get_sequence_text()
                        self.parent.do([elem, 0, 0, 0])
                    self.angle += speed
                    self.angle %= 360
                    self.parent.updo([elem, 0, 0, -self.angle])

                    elem.set_sequence_text(self.sequence_text)
                    try:
                        elem.add_sequence_text(self.save_data.get_gcrubs('cmd_name').get(key).format(
                            angle=self.angle))
                    except KeyError:
                        elem.add_sequence_text(self.save_data.get_gcrubs('cmd_name').get(key))
                    break

        elif event.key() == QtCore.Qt.Key_D:
            if elem.is_origined():
                elem.translate(-elem.get_coord()[0], -elem.get_coord()[1], 0, local=False)
                elem.rotate(-speed, 0, 0, 1, local=False)
                elem.translate(elem.get_coord()[0], elem.get_coord()[1], 0, local=False)

            else:
                elem.rotate(-speed, mvt[2][0], mvt[2][1], mvt[2][2], local=True)

            elem.turn(-speed)

            for key, cmd in zip(self.save_data.get_gcrubs('cmd_key').keys(),
                                self.save_data.get_gcrubs('cmd_key').values()):
                if cmd == event.key():
                    if elem.get_key() != event.key():
                        self.angle = 0
                        self.sequence_text = elem.get_sequence_text()
                        self.parent.do([elem, 0, 0, 0])
                    self.angle += speed
                    self.angle %= 360
                    self.parent.updo([elem, 0, 0, self.angle])

                    elem.set_sequence_text(self.sequence_text)
                    try:
                        elem.add_sequence_text(self.save_data.get_gcrubs('cmd_name').get(key).format(
                            angle=self.angle))
                    except KeyError:
                        elem.add_sequence_text(self.save_data.get_gcrubs('cmd_name').get(key))
                    break

        if invisible:
            elem.scale(coef, coef, coef)

        self.parent.status_bar.showMessage(
            self.init_data.get_window('position_status_message').format(x=int(elem.get_coord()[0]),
                                                                        y=int(elem.get_coord()[1]),
                                                                        angle=elem.get_angle()))

        elem.set_key(event.key())

    @staticmethod
    def ret_key(event: QtGui.QKeyEvent) -> str:
        if event.key() == QtCore.Qt.Key_Up:
            return "Fleche du haut"
        elif event.key() == QtCore.Qt.Key_Down:
            return "Fleche du bas"
        elif event.key() == QtCore.Qt.Key_Right:
            return "Fleche de droite"
        elif event.key() == QtCore.Qt.Key_Left:
            return "Fleche de gauche"
        else:
            return str(event.text())

    def mouseReleaseEvent(self, ev):
        self.setCursor(QtCore.Qt.ArrowCursor)

    def get_key(self, where_to_show, write_key):
        self.getting_key = True
        self.key = where_to_show
        self.text = self.key.text()
        self.write_key = write_key

    def stop_get_key(self):
        self.getting_key = False
