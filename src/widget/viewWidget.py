# !/usr/bin/env python3
# -*- coding: utf-8 -*-
# Created by Axel Tremaudant on 17/06/22

"""
Fichier contenant la classe ViewWidget.
"""

from PyQt5 import QtCore, QtGui, QtWidgets
import pyqtgraph.opengl as gl
import numpy as np

from src import widget


class ViewWidget(gl.GLViewWidget):
    """
    Classe qui gere les evenements dans la partie centrale.
    """

    def __init__(self, parent, save_data):
        """
        Constructeur de ViewWidget.
        :param parent: ui.MainWindow: Fenetre principale
        :param save_data: data.Save: Donnees de sauvegarde
        """
        super(ViewWidget, self).__init__()
        self.save_data = save_data
        self.init_data = self.save_data.get_init_data()
        self.mousePos = None
        self.parent = parent
        self.getting_key = False
        self.key = None
        self.text = ""
        self.write_key = None
        self.dist = 0
        self.angle = 0
        self.sequence_text = ""
        self.view_changed = False
        self.view_position = np.zeros(shape=2)
        self.zoom = self.init_data.get_view('start_view_position_distance')

    def wheelEvent(self, event):
        """
        Zoom ou dezoom la vue avec la mollette de la souris.
        :param event: Evenement
        :return: None
        """
        if self.init_data.get_view('min_zoom') < self.zoom + event.angleDelta().y() < \
                self.init_data.get_view('max_zoom'):
            super(ViewWidget, self).wheelEvent(event)
            self.zoom += event.angleDelta().y()

    def panable(self) -> bool:
        """
        Indique si on autorise a deplacer ou non la vue.
        :return: bool: True si ok, False sinon
        """
        w = QtWidgets.QDesktopWidget()
        if self.parent.grid.visible():
            ref = self.parent.grid
        elif self.parent.board.visible():
            ref = self.parent.board
        elif self.parent.vinyl.visible():
            ref = self.parent.vinyl
        else:
            return True

        if ref in self.itemsAt((0, 0, w.screenGeometry().width(), w.screenGeometry().height())):
            return True
        else:
            if self.view_position[0] < 0:
                self.pan(10, 0, 0, relative='view')
            else:
                self.pan(-10, 0, 0, relative='view')
            if self.view_position[1] < 0:
                self.pan(0, 10, 0, relative='view')
            else:
                self.pan(0, -10, 0, relative='view')
            return False

    def mouseMoveEvent(self, ev):
        """
        Lorsque la souris est deplacee, change la vue.
        :param ev: Evenement
        :return: None
        """
        self.setCursor(self.init_data.get_view('moving_cursor'))
        lpos = ev.position() if hasattr(ev, 'position') else ev.localPos()  # Donne la position de la souris
        diff = lpos - self.mousePos
        self.mousePos = lpos

        if diff == QtCore.QPointF(0., 0.):
            self.view_changed = False
        else:
            self.view_changed = True

        if ev.buttons() == self.init_data.get_view('rotation_view_key'):
            if ev.modifiers() & self.init_data.get_view('moving_view1'):
                if self.panable():
                    self.pan(diff.x(), diff.y(), 0, relative='view')  # Deplace la vue
                    self.view_position[0] += diff.x()
                    self.view_position[1] += diff.y()
            else:
                self.setCursor(self.init_data.get_view('orbit_cursor'))
                self.orbit(-diff.x(), diff.y())  # Tourne la vue

        elif ev.buttons() == self.init_data.get_view('moving_view_middle_button'):
            if ev.modifiers() & self.init_data.get_view('moving_view_middle_button1'):
                if self.panable():
                    self.pan(diff.x(), 0, diff.y(), relative='view-upright')
                    self.view_position[0] += diff.x()
                    self.view_position[1] += diff.y()
            else:
                if self.panable():
                    self.pan(diff.x(), diff.y(), 0, relative='view-upright')
                    self.view_position[0] += diff.x()
                    self.view_position[1] += diff.y()

        elif ev.buttons() == self.init_data.get_view('moving_view2'):
            if self.panable():
                self.pan(diff.x(), diff.y(), 0, relative='view')
                self.view_position[0] += diff.x()
                self.view_position[1] += diff.y()

    def keyPressEvent(self, event: QtGui.QKeyEvent) -> None:
        """
        Fonction qui gere l'appui des touches.
        :param event: QtGui.QKeyEvent: Evenement
        :return: None
        """
        if self.parent.running.is_ongoing():  # Si une simulation est en cours, impossible de déplacer un robot
            return

        if self.getting_key:  # S'il faut renvoyer une touche
            self.key.setText(self.text + widget.KeyDialog.ret_key(event))
            self.write_key.set_key(event.key())

        if self.parent.main_robot.is_selected():
            elem = self.parent.main_robot
            axis = self.save_data.get_main_robot('axis_rotation')
            angle = self.save_data.get_main_robot('angle_rotation')
        elif self.parent.second_robot.is_selected():
            elem = self.parent.second_robot
            axis = self.save_data.get_second_robot('axis_rotation')
            angle = self.save_data.get_second_robot('angle_rotation')
        else:
            return

        speed = self.save_data.get_grid('moving_speed')
        mvt = elem.robot_movement(axis, angle)

        for key, cmd in zip(self.save_data.get_gcrubs('cmd_key').keys(),
                            self.save_data.get_gcrubs('cmd_key').values()):
            # Si c'est une touche pour la sequence mais pas une touche de mouvement
            if event.key() == cmd and \
                    event.key() != self.save_data.get_gcrubs('keys').get('go_right') and \
                    event.key() != self.save_data.get_gcrubs('keys').get('go_left') and \
                    event.key() != self.save_data.get_gcrubs('keys').get('go_down') and \
                    event.key() != self.save_data.get_gcrubs('keys').get('go_up') and \
                    event.key() != self.save_data.get_gcrubs('keys').get('turn_right') and \
                    event.key() != self.save_data.get_gcrubs('keys').get('turn_left'):
                elem.get_window().add_sequence_text(self.save_data.get_gcrubs('cmd_name').get(key))
                elem.set_key(None)
                return

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

        self.parent.status_bar.showMessage(
            self.init_data.get_window('position_status_message').format(x=round(elem.get_coord()[0]),
                                                                        y=round(elem.get_coord()[1]),
                                                                        angle=round(elem.get_angle())))

        elem.set_key(event.key()) if elem.is_ready_sequence() else elem.set_key(None)

    def _turn_right(self, event, elem, mvt: tuple, speed: int):
        """
        Fait tourner le robot sur la droite.
        :param event: QtGui.QKeyEvent: Evenement
        :param elem: element.Robot: Robot qui doit tourner
        :param mvt: Deplacements calcules
        :param speed: Vitesse de deplacement
        :return: None
        """
        if elem.is_origined():  # Si l'origine du robot a ete choisie, rotation autour du repere global
            elem.translate(*elem.get_coord() * -1, 0, local=False)
            elem.rotate(-speed, 0, 0, 1, local=False)
            elem.translate(*elem.get_coord(), 0, local=False)

        else:
            elem.rotate(-speed, *mvt[2], local=True)

        elem.turn(-speed)
        if elem.is_ready_sequence():  # Si on enregistre une sequence
            for key, cmd in zip(self.save_data.get_gcrubs('cmd_key').keys(),
                                self.save_data.get_gcrubs('cmd_key').values()):
                if cmd == event.key():
                    if elem.get_key() != event.key():
                        self.angle = 0
                        self.sequence_text = elem.get_window().get_sequence_text()
                        self.parent.do([elem, 0, 0, 0, ""])

                    self.angle += speed
                    self.angle %= 360

                    elem.get_window().set_sequence_text(self.sequence_text)
                    try:
                        elem.get_window().add_sequence_text(self.save_data.get_gcrubs('cmd_name').get(key).format(
                            angle=self.angle))
                    except KeyError:
                        elem.get_window().add_sequence_text(self.save_data.get_gcrubs('cmd_name').get(key))

                    self.parent.updo([elem, 0, 0, self.angle, elem.get_window().get_sequence_text()])
                    break

    def _turn_left(self, event, elem, mvt: tuple, speed: int):
        """
        Fait tourner le robot sur la gauche.
        :param event: QtGui.QKeyEvent: Evenement
        :param elem: element.Robot: Robot qui doit tourner
        :param mvt: Deplacements calcules
        :param speed: Vitesse de deplacement
        :return: None
        """
        if elem.is_origined():  # Si l'origine du robot a ete choisie, rotation autour du repere global
            elem.translate(*elem.get_coord() * -1, 0, local=False)
            elem.rotate(speed, 0, 0, 1, local=False)
            elem.translate(*elem.get_coord(), 0, local=False)

        else:
            elem.rotate(speed, *mvt[2], local=True)

        elem.turn(speed)
        if elem.is_ready_sequence():  # Si on enregistre une sequence
            for key, cmd in zip(self.save_data.get_gcrubs('cmd_key').keys(),
                                self.save_data.get_gcrubs('cmd_key').values()):
                if cmd == event.key():
                    if elem.get_key() != event.key():
                        self.angle = 0
                        self.sequence_text = elem.get_window().get_sequence_text()
                        self.parent.do([elem, 0, 0, 0, ""])

                    self.angle += speed
                    self.angle %= 360

                    elem.get_window().set_sequence_text(self.sequence_text)
                    try:
                        elem.get_window().add_sequence_text(self.save_data.get_gcrubs('cmd_name').get(key).format(
                            angle=self.angle))
                    except KeyError:
                        elem.get_window().add_sequence_text(self.save_data.get_gcrubs('cmd_name').get(key))
                    self.parent.updo([elem, 0, 0, -self.angle, elem.get_window().get_sequence_text()])
                    break

    def _go_up(self, event, elem, mvt: tuple, speed: int):
        """
        Fait avancer le robot en haut.
        :param event: QtGui.QKeyEvent: Evenement
        :param elem: element.Robot: Robot qui doit avancer
        :param mvt: Deplacements calcules
        :param speed: Vitesse de deplacement
        :return: None
        """
        elem.translate(*mvt[1] * speed, local=True)
        elem.move(0, speed)
        if elem.is_ready_sequence():  # Si on enregistre une sequence
            for key, cmd in zip(self.save_data.get_gcrubs('cmd_key').keys(),
                                self.save_data.get_gcrubs('cmd_key').values()):
                if cmd == event.key():
                    if elem.get_key() != event.key():  # Si la touche actuelle est differente de la precedente
                        self.dist = 0
                        self.sequence_text = elem.get_window().get_sequence_text()
                        self.parent.do([elem, 0, 0, 0, ""])
                        elem.get_window().add_track(elem)

                    self.dist += speed
                    if len(elem.get_window().track) != 0:
                        elem.get_window().update_last_track(speed, 0, self.dist)

                    elem.get_window().set_sequence_text(self.sequence_text)
                    try:
                        elem.get_window().add_sequence_text(
                            self.save_data.get_gcrubs('cmd_name').get(key).format(dist=self.dist))
                    except KeyError:
                        elem.get_window().add_sequence_text(self.save_data.get_gcrubs('cmd_name').get(key))

                    self.parent.updo([elem, 0, -self.dist, 0, elem.get_window().get_sequence_text()])
                    break

    def _go_down(self, event, elem, mvt: tuple, speed: int):
        """
        Fait avancer le robot en bas
        :param event: QtGui.QKeyEvent: Evenement
        :param elem: element.Robot: Robot qui doit avancer
        :param mvt: Deplacements calcules
        :param speed: Vitesse de deplacement
        :return: None
        """
        elem.translate(*mvt[1] * -speed, local=True)
        elem.move(0, -speed)
        if elem.is_ready_sequence():
            for key, cmd in zip(self.save_data.get_gcrubs('cmd_key').keys(),
                                self.save_data.get_gcrubs('cmd_key').values()):
                if cmd == event.key():
                    if elem.get_key() != event.key():
                        self.dist = 0
                        self.sequence_text = elem.get_window().get_sequence_text()
                        self.parent.do([elem, 0, 0, 0, ""])
                        elem.get_window().add_track(elem)

                    self.dist += speed
                    if len(elem.get_window().track) != 0:
                        elem.get_window().update_last_track(-speed, 0, self.dist)

                    elem.get_window().set_sequence_text(self.sequence_text)
                    try:
                        elem.get_window().add_sequence_text(
                            self.save_data.get_gcrubs('cmd_name').get(key).format(dist=self.dist))
                    except KeyError:
                        elem.get_window().add_sequence_text(self.save_data.get_gcrubs('cmd_name').get(key))

                    self.parent.updo([elem, 0, self.dist, 0, elem.get_window().get_sequence_text()])
                    break

    def _go_left(self, event, elem, mvt: tuple, speed: int):
        """
        Fait avancer le robot vers la gauche
        :param event: QtGui.QKeyEvent: Evenement
        :param elem: element.Robot: Robot qui doit avancer
        :param mvt: Deplacements calcules
        :param speed: Vitesse de deplacement
        :return: None
        """
        elem.translate(*mvt[0] * -speed, local=True)
        elem.move(-speed, 0)
        if elem.is_ready_sequence():
            for key, cmd in zip(self.save_data.get_gcrubs('cmd_key').keys(),
                                self.save_data.get_gcrubs('cmd_key').values()):
                if cmd == event.key():
                    if elem.get_key() != event.key():
                        self.dist = 0
                        self.sequence_text = elem.get_window().get_sequence_text()
                        self.parent.do([elem, 0, 0, 0, ""])
                        elem.get_window().add_track(elem)

                    self.dist += speed
                    if len(elem.get_window().track) != 0:
                        elem.get_window().update_last_track(-speed, self.dist, 0)

                    elem.get_window().set_sequence_text(self.sequence_text)
                    try:
                        elem.get_window().add_sequence_text(
                            self.save_data.get_gcrubs('cmd_name').get(key).format(dist=self.dist))
                    except KeyError:
                        elem.get_window().add_sequence_text(self.save_data.get_gcrubs('cmd_name').get(key))
                    self.parent.updo([elem, self.dist, 0, 0, elem.get_window().get_sequence_text()])
                    break

    def _go_right(self, event, elem, mvt: tuple, speed: int):
        """
        Fait avancer le robot vers la droite
        :param event: QtGui.QKeyEvent: Evenement
        :param elem: element.Robot: Robot qui doit avancer
        :param mvt: Deplacements calcules
        :param speed: Vitesse de deplacement
        :return: None
        """
        elem.translate(*mvt[0] * speed, local=True)
        elem.move(speed, 0)
        if elem.is_ready_sequence():
            for key, cmd in zip(self.save_data.get_gcrubs('cmd_key').keys(),
                                self.save_data.get_gcrubs('cmd_key').values()):
                if cmd == event.key():
                    if elem.get_key() != event.key():
                        self.dist = 0
                        self.sequence_text = elem.get_window().get_sequence_text()
                        self.parent.do([elem, 0, 0, 0, ""])
                        elem.get_window().add_track(elem)

                    self.dist += speed
                    if len(elem.get_window().track) != 0:
                        elem.get_window().update_last_track(speed, self.dist, 0)

                    elem.get_window().set_sequence_text(self.sequence_text)
                    try:
                        elem.get_window().add_sequence_text(
                            self.save_data.get_gcrubs('cmd_name').get(key).format(dist=self.dist))
                    except KeyError:
                        elem.get_window().add_sequence_text(self.save_data.get_gcrubs('cmd_name').get(key))

                    self.parent.updo([elem, self.dist, 0, 0, elem.get_window().get_sequence_text()])
                    break

    def mouseReleaseEvent(self, ev):
        """
        Fonction qui gere le relachement de la touche de la souris
        :param ev: any: Evenement
        :return: None
        """
        self.setCursor(QtCore.Qt.ArrowCursor)

        if not self.view_changed:
            # Selection du robot
            region = (ev.pos().x() - 5, ev.pos().y() - 5, 10, 10)  # Rectangle de 10 pixels autour de la souris
            if self.parent.main_robot in self.itemsAt(region):  # Si le robot principal se trouve la ou est la souris
                self.parent.main_robot.set_selected(True)
                self.parent.second_robot.set_selected(False)
                self.parent.list_widget.item(
                    self.parent.list_widget.get_content_row(self.parent.main_robot)).setSelected(True)

            elif self.parent.second_robot in self.itemsAt(region):
                self.parent.second_robot.set_selected(True)
                self.parent.main_robot.set_selected(False)
                self.parent.list_widget.item(
                    self.parent.list_widget.get_content_row(self.parent.second_robot)).setSelected(True)

            else:
                self.parent.main_robot.set_selected(False)
                self.parent.second_robot.set_selected(False)
                self.parent.list_widget.item(0).setSelected(True)

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

    def get_view_position(self) -> np.array:
        """
        Donne la position de la vue
        :return: np.array: [x, y]
        """
        return self.view_position

    def reset_view_position(self):
        """
        Reset la valeur de position et du zoom.
        :return: None
        """
        self.view_position = np.zeros(shape=2)
        self.zoom = self.init_data.get_view('start_view_position_distance')
