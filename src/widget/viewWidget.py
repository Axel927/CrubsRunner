# !/usr/bin/env python3
# -*- coding: utf-8 -*-
# Created by Axel Tremaudant on 17/06/22

from PySide6 import QtCore, QtGui
import pyqtgraph.opengl as gl
from data.initData import InitData
from data.saveData import SaveData
from widget.keyDialog import KeyDialog


class GlViewWidget(gl.GLViewWidget):
    def __init__(self, parent, save_data: SaveData):
        super(GlViewWidget, self).__init__()
        self.save_data = save_data
        self.init_data = InitData()
        self.mousePos = None
        self.parent = parent
        self.getting_key = False
        self.key = None
        self.text = ""
        self.write_key = None
        self.dist = 0
        self.angle = 0
        self.sequence_text = ""

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
            self.key.setText(self.text + KeyDialog.ret_key(event))
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
        mvt = self.parent.main_robot.robot_movement(axis, angle)

        for key, cmd in zip(self.save_data.get_gcrubs('cmd_key').keys(),
                            self.save_data.get_gcrubs('cmd_key').values()):
            if event.key() == cmd and event.key() != self.save_data.get_gcrubs('keys').get('go_right') and\
                    event.key() != self.save_data.get_gcrubs('keys').get('go_left') and \
                    event.key() != self.save_data.get_gcrubs('keys').get('go_down') and \
                    event.key() != self.save_data.get_gcrubs('keys').get('go_up') and \
                    event.key() != self.save_data.get_gcrubs('keys').get('turn_right') and \
                    event.key() != self.save_data.get_gcrubs('keys').get('turn_left'):

                elem.add_sequence_text(self.save_data.get_gcrubs('cmd_name').get(key))
                elem.set_key(None)
                return

        coef = self.init_data.get_main_robot('invisible_coef')
        if invisible:  # Ne pas chercher mais laisser meme si ca parait inutile, pb lors des deplacements sinon
            elem.scale(1 / coef, 1 / coef, 1 / coef)

        if event.key() == self.save_data.get_gcrubs('keys').get('go_right'):
            elem.translate(mvt[0][0] * speed, mvt[0][1] * speed, mvt[0][2] * speed, local=True)
            elem.move(speed, 0)
            if elem.is_ready_sequence():
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
                            elem.add_sequence_text(
                                self.save_data.get_gcrubs('cmd_name').get(key).format(dist=self.dist))
                        except KeyError:
                            elem.add_sequence_text(self.save_data.get_gcrubs('cmd_name').get(key))
                        break

        elif event.key() == self.save_data.get_gcrubs('keys').get('go_left'):
            elem.translate(-mvt[0][0] * speed, -mvt[0][1] * speed, -mvt[0][2] * speed, local=True)
            elem.move(-speed, 0)
            if elem.is_ready_sequence():
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
                            elem.add_sequence_text(
                                self.save_data.get_gcrubs('cmd_name').get(key).format(dist=self.dist))
                        except KeyError:
                            elem.add_sequence_text(self.save_data.get_gcrubs('cmd_name').get(key))
                        break

        elif event.key() == self.save_data.get_gcrubs('keys').get('go_down'):
            elem.translate(-mvt[1][0] * speed, -mvt[1][1] * speed, -mvt[1][2] * speed, local=True)
            elem.move(0, -speed)
            if elem.is_ready_sequence():
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
                            elem.add_sequence_text(
                                self.save_data.get_gcrubs('cmd_name').get(key).format(dist=self.dist))
                        except KeyError:
                            elem.add_sequence_text(self.save_data.get_gcrubs('cmd_name').get(key))
                        break

        elif event.key() == self.save_data.get_gcrubs('keys').get('go_up'):
            elem.translate(mvt[1][0] * speed, mvt[1][1] * speed, mvt[1][2] * speed, local=True)
            elem.move(0, speed)
            if elem.is_ready_sequence():
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
                            elem.add_sequence_text(
                                self.save_data.get_gcrubs('cmd_name').get(key).format(dist=self.dist))
                        except KeyError:
                            elem.add_sequence_text(self.save_data.get_gcrubs('cmd_name').get(key))
                        break

        elif event.key() == self.save_data.get_gcrubs('keys').get('turn_left'):
            if elem.is_origined():
                elem.translate(-elem.get_coord()[0], -elem.get_coord()[1], 0, local=False)
                elem.rotate(speed, 0, 0, 1, local=False)
                elem.translate(elem.get_coord()[0], elem.get_coord()[1], 0, local=False)

            else:
                elem.rotate(speed, mvt[2][0], mvt[2][1], mvt[2][2], local=True)

            elem.turn(speed)
            if elem.is_ready_sequence():
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

        elif event.key() == self.save_data.get_gcrubs('keys').get('turn_right'):
            if elem.is_origined():
                elem.translate(-elem.get_coord()[0], -elem.get_coord()[1], 0, local=False)
                elem.rotate(-speed, 0, 0, 1, local=False)
                elem.translate(elem.get_coord()[0], elem.get_coord()[1], 0, local=False)

            else:
                elem.rotate(-speed, mvt[2][0], mvt[2][1], mvt[2][2], local=True)

            elem.turn(-speed)
            if elem.is_ready_sequence():
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
                                                                        angle=round(elem.get_angle())))

        elem.set_key(event.key())

    def mouseReleaseEvent(self, ev):
        self.setCursor(QtCore.Qt.ArrowCursor)

    def get_key(self, where_to_show, write_key):
        self.getting_key = True
        self.key = where_to_show
        self.text = self.key.text()
        self.write_key = write_key

    def stop_get_key(self):
        self.getting_key = False
