# !/usr/bin/env python3
# -*- coding: utf-8 -*-
# Created by Axel Tremaudant on 17/06/22

"""
Fichier contenant la classe ViewWidget.
"""

from PySide6 import QtCore, QtGui
import pyqtgraph.opengl as gl
import data
import widget


class ViewWidget(gl.GLViewWidget):
    """
    Classe qui gere les evenements dans la partie centrale.
    """
    def __init__(self, parent, save_data: data.Save):
        """
        Constructeur de ViewWidget.
        :param parent: ui.MainWindow: Fenetre principale
        :param save_data: data.Save: Donnees de sauvegarde
        """
        super(ViewWidget, self).__init__()
        self.save_data = save_data
        self.init_data = data.Init()
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
        """
        Lorsque la souris est deplacee.
        :param ev: Evenement
        :return: None
        """
        self.setCursor(self.init_data.get_view('moving_cursor'))

        lpos = ev.position() if hasattr(ev, 'position') else ev.localPos()  # Donne la position de la souris
        diff = lpos - self.mousePos
        self.mousePos = lpos

        if ev.buttons() == self.init_data.get_view('rotation_view_key'):
            if ev.modifiers() & self.init_data.get_view('moving_view1'):
                self.pan(diff.x(), diff.y(), 0, relative='view')  # Deplace la vue
            else:
                self.orbit(-diff.x(), diff.y())  # Tourne la vue
        elif ev.buttons() == self.init_data.get_view('moving_view_middle_button'):
            if ev.modifiers() & self.init_data.get_view('moving_view_middle_button1'):
                self.pan(diff.x(), 0, diff.y(), relative='view-upright')
            else:
                self.pan(diff.x(), diff.y(), 0, relative='view-upright')
        elif ev.buttons() == self.init_data.get_view('moving_view2'):
            self.pan(diff.x(), diff.y(), 0, relative='view')

    def keyPressEvent(self, event: QtGui.QKeyEvent) -> None:
        """
        Fonction qui gere l'appui des touches.
        :param event: QtGui.QKeyEvent: Evenement
        :return: None
        """
        if self.getting_key:  # S'il faut renvoyer une touche
            self.key.setText(self.text + widget.KeyDialog.ret_key(event))
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
            # Si c'est une touche pour la sequence mais pas une touche de mouvement
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
            self._go_right(event, elem, mvt, speed)

        elif event.key() == self.save_data.get_gcrubs('keys').get('go_left'):
            self._go_left(event, elem, mvt, speed)

        elif event.key() == self.save_data.get_gcrubs('keys').get('go_down'):
            self._go_down(event, elem, mvt, speed)

        elif event.key() == self.save_data.get_gcrubs('keys').get('go_up'):
            self._go_up(event, elem, mvt, speed)

        elif event.key() == self.save_data.get_gcrubs('keys').get('turn_left'):
            self._turn_left(event, elem, mvt, speed)

        elif event.key() == self.save_data.get_gcrubs('keys').get('turn_right'):
            self._turn_right(event, elem, mvt, speed)

        if invisible:  # Seconde partie du a ne pas virer
            elem.scale(coef, coef, coef)

        self.parent.status_bar.showMessage(
            self.init_data.get_window('position_status_message').format(x=int(elem.get_coord()[0]),
                                                                        y=int(elem.get_coord()[1]),
                                                                        angle=round(elem.get_angle())))

        elem.set_key(event.key())

    def _turn_right(self, event, elem, mvt: list, speed: int):
        """
        Fait tourner le robot sur la droite
        :param event: QtGui.QKeyEvent: Evenement
        :param elem: element.Robot: Robot qui doit tourner
        :param mvt: Deplacements calcules
        :param speed: Vitesse de deplacement
        :return: None
        """
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
                        self.sequence_text = elem.get_window().get_sequence_text()
                        self.parent.do([elem, 0, 0, 0])

                    self.angle += speed
                    self.angle %= 360
                    self.parent.updo([elem, 0, 0, self.angle])

                    elem.get_window().set_sequence_text(self.sequence_text)
                    try:
                        elem.get_window().add_sequence_text(self.save_data.get_gcrubs('cmd_name').get(key).format(
                            angle=self.angle))
                    except KeyError:
                        elem.get_window().add_sequence_text(self.save_data.get_gcrubs('cmd_name').get(key))
                    break

    def _turn_left(self, event, elem, mvt: list, speed: int):
        """
        Fait tourner le robot sur la gauche
        :param event: QtGui.QKeyEvent: Evenement
        :param elem: element.Robot: Robot qui doit tourner
        :param mvt: Deplacements calcules
        :param speed: Vitesse de deplacement
        :return: None
        """
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
                        self.sequence_text = elem.get_window().get_sequence_text()
                        self.parent.do([elem, 0, 0, 0])
                    self.angle += speed
                    self.angle %= 360
                    self.parent.updo([elem, 0, 0, -self.angle])

                    elem.get_window().set_sequence_text(self.sequence_text)
                    try:
                        elem.get_window().add_sequence_text(self.save_data.get_gcrubs('cmd_name').get(key).format(
                            angle=self.angle))
                    except KeyError:
                        elem.get_window().add_sequence_text(self.save_data.get_gcrubs('cmd_name').get(key))
                    break

    def _go_up(self, event, elem, mvt: list, speed: int):
        """
        Fait avancer le robot en haut
        :param event: QtGui.QKeyEvent: Evenement
        :param elem: element.Robot: Robot qui doit avancer
        :param mvt: Deplacements calcules
        :param speed: Vitesse de deplacement
        :return: None
        """
        elem.translate(mvt[1][0] * speed, mvt[1][1] * speed, mvt[1][2] * speed, local=True)
        elem.move(0, speed)
        if elem.is_ready_sequence():
            for key, cmd in zip(self.save_data.get_gcrubs('cmd_key').keys(),
                                self.save_data.get_gcrubs('cmd_key').values()):
                if cmd == event.key():
                    if elem.get_key() != event.key():
                        self.dist = 0
                        self.sequence_text = elem.get_window().get_sequence_text()
                        self.parent.do([elem, 0, 0, 0])
                    self.dist += speed
                    elem.get_window().set_sequence_text(self.sequence_text)
                    self.parent.updo([elem, 0, -self.dist, 0])
                    try:
                        elem.get_window().add_sequence_text(
                            self.save_data.get_gcrubs('cmd_name').get(key).format(dist=self.dist))
                    except KeyError:
                        elem.get_window().add_sequence_text(self.save_data.get_gcrubs('cmd_name').get(key))
                    break

    def _go_down(self, event, elem, mvt: list, speed: int):
        """
        Fait avancer le robot en bas
        :param event: QtGui.QKeyEvent: Evenement
        :param elem: element.Robot: Robot qui doit avancer
        :param mvt: Deplacements calcules
        :param speed: Vitesse de deplacement
        :return: None
        """
        elem.translate(-mvt[1][0] * speed, -mvt[1][1] * speed, -mvt[1][2] * speed, local=True)
        elem.move(0, -speed)
        if elem.is_ready_sequence():
            for key, cmd in zip(self.save_data.get_gcrubs('cmd_key').keys(),
                                self.save_data.get_gcrubs('cmd_key').values()):
                if cmd == event.key():
                    if elem.get_key() != event.key():
                        self.dist = 0
                        self.sequence_text = elem.get_window().get_sequence_text()
                        self.parent.do([elem, 0, 0, 0])
                    self.dist += speed
                    elem.get_window().set_sequence_text(self.sequence_text)
                    self.parent.updo([elem, 0, self.dist, 0])
                    try:
                        elem.get_window().add_sequence_text(
                            self.save_data.get_gcrubs('cmd_name').get(key).format(dist=self.dist))
                    except KeyError:
                        elem.get_window().add_sequence_text(self.save_data.get_gcrubs('cmd_name').get(key))
                    break

    def _go_left(self, event, elem, mvt: list, speed: int):
        """
        Fait avancer le robot vers la gauche
        :param event: QtGui.QKeyEvent: Evenement
        :param elem: element.Robot: Robot qui doit avancer
        :param mvt: Deplacements calcules
        :param speed: Vitesse de deplacement
        :return: None
        """
        elem.translate(-mvt[0][0] * speed, -mvt[0][1] * speed, -mvt[0][2] * speed, local=True)
        elem.move(-speed, 0)
        if elem.is_ready_sequence():
            for key, cmd in zip(self.save_data.get_gcrubs('cmd_key').keys(),
                                self.save_data.get_gcrubs('cmd_key').values()):
                if cmd == event.key():
                    if elem.get_key() != event.key():
                        self.dist = 0
                        self.sequence_text = elem.get_window().get_sequence_text()
                        self.parent.do([elem, 0, 0, 0])
                    self.dist += speed
                    elem.get_window().set_sequence_text(self.sequence_text)
                    self.parent.updo([elem, self.dist, 0, 0])
                    try:
                        elem.get_window().add_sequence_text(
                            self.save_data.get_gcrubs('cmd_name').get(key).format(dist=self.dist))
                    except KeyError:
                        elem.get_window().add_sequence_text(self.save_data.get_gcrubs('cmd_name').get(key))
                    break

    def _go_right(self, event, elem, mvt: list, speed: int):
        """
        Fait avancer le robot vers la droite
        :param event: QtGui.QKeyEvent: Evenement
        :param elem: element.Robot: Robot qui doit avancer
        :param mvt: Deplacements calcules
        :param speed: Vitesse de deplacement
        :return: None
        """
        elem.translate(mvt[0][0] * speed, mvt[0][1] * speed, mvt[0][2] * speed, local=True)
        elem.move(speed, 0)
        if elem.is_ready_sequence():
            for key, cmd in zip(self.save_data.get_gcrubs('cmd_key').keys(),
                                self.save_data.get_gcrubs('cmd_key').values()):
                if cmd == event.key():
                    if elem.get_key() != event.key():
                        self.dist = 0
                        self.sequence_text = elem.get_window().get_sequence_text()
                        self.parent.do([elem, 0, 0, 0])
                    self.dist += speed
                    elem.get_window().set_sequence_text(self.sequence_text)
                    self.parent.updo([elem, -self.dist, 0, 0])
                    try:
                        elem.get_window().add_sequence_text(
                            self.save_data.get_gcrubs('cmd_name').get(key).format(dist=self.dist))
                    except KeyError:
                        elem.get_window().add_sequence_text(self.save_data.get_gcrubs('cmd_name').get(key))
                    break

    def mouseReleaseEvent(self, ev):
        """
        Fonction qui gere le relachement de la touche de la souris
        :param ev: any: Evenement
        :return: None
        """
        self.setCursor(QtCore.Qt.ArrowCursor)

    def get_key(self, where_to_show, write_key):
        """
        Debut de la reception des touches.
        :param where_to_show: QtWidgets.QLabel: La ou doit etre affiche la touche
        :param write_key: any: La ou il faut enregistrer la touche
        :return: None
        """
        self.getting_key = True
        self.key = where_to_show
        self.text = self.key.text()
        self.write_key = write_key

    def stop_get_key(self):
        """
        Arret de la reception des touches.
        :return: None
        """
        self.getting_key = False
