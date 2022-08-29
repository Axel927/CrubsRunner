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
Fichier contenant la partie interface de la classe Robot.
"""

from PyQt5 import QtWidgets, QtGui, QtCore
from time import time
import pyqtgraph.opengl as gl
import numpy as np
from platform import system

from src import simulation
from src import widget
from src import element

if system() == 'Windows':
    COEF = -1
else:
    COEF = 1


class Robot:
    """
    Classe pour l'interface des robots.
    """

    def __init__(self, parent, save_data, robot: element):
        """
        Constructeur de Robot.
        :param parent: ui.MainWindow: Fenetre principale.
        :param save_data: data.Save: Donnees de sauvegarde
        :param robot: element.Robot: Robot concerne
        """
        self.parent = parent
        self.save_data = save_data
        self.robot = robot
        self.init_data = self.save_data.get_init_data()
        self.time = 0.
        self.track = list()

        self.window = QtWidgets.QDialog(self.parent)
        self.color_btn = QtWidgets.QPushButton(self.init_data.get_main_robot('color_name'), self.window)
        self.color_dialog = QtWidgets.QColorDialog(self.window)
        self.edge_color_btn = QtWidgets.QPushButton(self.init_data.get_main_robot('edge_color_name'), self.window)
        self.close_btn = QtWidgets.QPushButton(self.init_data.get_board('close_btn_name'), self.window)
        self.reset_btn = QtWidgets.QPushButton(self.init_data.get_board('reset_btn_name'), self.window)
        self.layout = QtWidgets.QVBoxLayout(self.window)
        self.remove_btn = QtWidgets.QPushButton(self.init_data.get_board('remove_btn_name'), self.window)
        self.angle_rotation_sb = QtWidgets.QSpinBox(self.window)
        self.gb_layout = QtWidgets.QGridLayout()
        self.group_box = QtWidgets.QGroupBox(self.init_data.get_main_robot('gb_name'))
        self.speed_gb = QtWidgets.QGroupBox(self.init_data.get_main_robot('gb_speed_name'))
        self.speed_layout = QtWidgets.QGridLayout()

        self.axis_rotation_rb_x = QtWidgets.QRadioButton(self.init_data.get_main_robot('axis_rotation_x_name'),
                                                         self.window)
        self.axis_rotation_rb_y = QtWidgets.QRadioButton(self.init_data.get_main_robot('axis_rotation_y_name'),
                                                         self.window)
        self.axis_rotation_rb_z = QtWidgets.QRadioButton(self.init_data.get_main_robot('axis_rotation_z_name'),
                                                         self.window)
        self.offset_sb = QtWidgets.QSpinBox(self.window)

        self.angle_lbl = QtWidgets.QLabel(self.init_data.get_main_robot('angle_lbl_name'))
        self.axis_lbl = QtWidgets.QLabel(self.init_data.get_main_robot('axis_lbl_name'))
        self.offset_lbl = QtWidgets.QLabel(self.init_data.get_main_robot('offset_lbl_name'))
        self.create_sequence_btn = QtWidgets.QPushButton(self.init_data.get_main_robot('sequence_btn_name'))
        self.import_gcrubs_btn = QtWidgets.QPushButton(self.init_data.get_main_robot('import_gcrubs_btn_name'))
        self.speed_sb = QtWidgets.QSpinBox()
        self.speed_lbl = QtWidgets.QLabel(self.init_data.get_main_robot('speed_lbl'))
        self.speed_rotation_lbl = QtWidgets.QLabel(self.init_data.get_main_robot('speed_rotation_lbl'))
        self.speed_rotation_sb = QtWidgets.QSpinBox()
        self.track_visible_cb = QtWidgets.QCheckBox(self.init_data.get_main_robot('track_visible_cb_name'))

        self.sequence_dialog = QtWidgets.QDialog(self.parent)
        self.sequence_text = QtWidgets.QTextEdit("", self.sequence_dialog)
        self.sequence_layout = QtWidgets.QVBoxLayout()
        self.sequence_splitter = QtWidgets.QSplitter(QtCore.Qt.Vertical)
        self.sequence_save_btn = QtWidgets.QPushButton(self.init_data.get_main_robot('sequence_save_btn_name'))
        self.sequence_cancel_btn = QtWidgets.QPushButton(self.init_data.get_main_robot('sequence_cancel_btn_name'))
        self.sequence_new_btn = QtWidgets.QPushButton(self.init_data.get_main_robot('sequence_new_btn_name'))
        self.sequence_list = widget.ListWidget()
        self.sequence_origin_lbl = QtWidgets.QLabel(self.init_data.get_main_robot('sequence_origin_lbl_text'))
        self.sequence_origin_btn = QtWidgets.QPushButton(self.init_data.get_main_robot('sequence_origin_btn_name'))

    def properties_window(self):
        """
        Cree la fenetre des proprietes
        :return: None
        """
        if self.robot.is_main_robot():
            self.parent.properties_dock.setWindowTitle(self.init_data.get_main_robot('window_title'))
        else:
            self.parent.properties_dock.setWindowTitle(self.init_data.get_second_robot('window_title'))

        self.parent.properties_dock.setWidget(self.window)

        self.color_btn.setCursor(self.init_data.get_board('color_cursor'))
        self.color_btn.setDefault(self.init_data.get_board('color_default'))

        self.edge_color_btn.setCursor(self.init_data.get_board('color_cursor'))
        self.edge_color_btn.setDefault(self.init_data.get_board('edge_color_default'))

        self.close_btn.setCursor(self.init_data.get_board('close_cursor'))
        self.close_btn.setDefault(self.init_data.get_board('close_default'))
        self.reset_btn.setCursor(self.init_data.get_board('reset_cursor'))
        self.reset_btn.setDefault(self.init_data.get_board('reset_default'))
        self.remove_btn.setCursor(self.init_data.get_board('remove_cursor'))
        self.remove_btn.setDefault(self.init_data.get_board('remove_default'))

        self.speed_sb.setMinimum(self.init_data.get_main_robot('speed_min'))
        self.speed_sb.setMaximum(self.init_data.get_main_robot('speed_max'))
        self.speed_sb.setValue(self.robot.get_speed())

        self.speed_rotation_sb.setMaximum(self.init_data.get_main_robot('rotation_max'))
        self.speed_rotation_sb.setMinimum(self.init_data.get_main_robot('rotation_min'))
        self.speed_rotation_sb.setValue(self.robot.get_speed_rotation())

        self.angle_rotation_sb.setMinimum(self.init_data.get_main_robot('angle_rotation_min'))
        self.angle_rotation_sb.setMaximum(self.init_data.get_main_robot('angle_rotation_max'))

        self.offset_sb.setMinimum(self.init_data.get_main_robot('offset_sb_min'))
        self.offset_sb.setMaximum(self.init_data.get_main_robot('offset_sb_max'))
        self.offset_sb.setValue(self.robot.get_offset())

        self.track_visible_cb.setChecked(
            self.track[0].visible() if len(self.track) != 0
            else self.init_data.get_main_robot('track_visible_cb_checked'))

        if self.robot.is_main_robot():
            self.angle_rotation_sb.setValue(self.save_data.get_main_robot('angle_rotation'))
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
            self.angle_rotation_sb.setValue(self.save_data.get_second_robot('angle_rotation'))
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

        self.create_sequence_btn.setCursor(self.init_data.get_main_robot('sequence_btn_cursor'))
        self.create_sequence_btn.setDefault(self.init_data.get_main_robot('sequence_btn_default'))

        self.import_gcrubs_btn.setCursor(self.init_data.get_main_robot('import_gcrubs_btn_cursor'))
        self.import_gcrubs_btn.setDefault(self.init_data.get_main_robot('import_gcrubs_btn_default'))

        self.gb_layout.addWidget(self.angle_lbl, 0, 0)
        self.gb_layout.addWidget(self.angle_rotation_sb, 0, 1)
        self.gb_layout.addWidget(self.axis_lbl, 1, 0)
        self.gb_layout.addWidget(self.axis_rotation_rb_x, 1, 1)
        self.gb_layout.addWidget(self.axis_rotation_rb_y, 2, 1)
        self.gb_layout.addWidget(self.axis_rotation_rb_z, 3, 1)
        self.gb_layout.addWidget(self.offset_lbl, 4, 0)
        self.gb_layout.addWidget(self.offset_sb, 4, 1)
        self.group_box.setLayout(self.gb_layout)

        self.speed_layout.addWidget(self.speed_lbl, 0, 0)
        self.speed_layout.addWidget(self.speed_sb, 0, 1)
        self.speed_layout.addWidget(self.speed_rotation_lbl, 1, 0)
        self.speed_layout.addWidget(self.speed_rotation_sb, 1, 1)
        self.speed_gb.setLayout(self.speed_layout)

        self.layout.addWidget(self.color_btn)
        self.layout.addWidget(self.edge_color_btn)
        self.layout.addWidget(self.speed_gb)
        self.layout.addWidget(self.group_box)
        self.layout.addWidget(self.track_visible_cb)
        self.layout.addWidget(self.close_btn)
        self.layout.addWidget(self.reset_btn)
        self.layout.addWidget(self.remove_btn)
        self.layout.addWidget(self.import_gcrubs_btn)
        self.layout.addWidget(self.create_sequence_btn)

        self._connections()
        self.window.show()

    def _connections(self):
        """
        Cree les connexions entre les widgets et les slots.
        :return: None
        """
        self.color_btn.clicked.connect(self._color_robot)
        self.edge_color_btn.clicked.connect(self._edge_color_robot)
        self.close_btn.clicked.connect(self._close)
        self.reset_btn.clicked.connect(self.reset)
        self.remove_btn.clicked.connect(self._remove)
        self.angle_rotation_sb.valueChanged.connect(self._rotate)
        self.axis_rotation_rb_x.clicked.connect(self._axis_x)
        self.axis_rotation_rb_y.clicked.connect(self._axis_y)
        self.axis_rotation_rb_z.clicked.connect(self._axis_z)
        self.offset_sb.valueChanged.connect(self._offset)
        self.create_sequence_btn.clicked.connect(self.create_sequence)
        self.import_gcrubs_btn.clicked.connect(self.import_gcrubs)
        self.speed_sb.valueChanged.connect(self._speed)
        self.speed_rotation_sb.valueChanged.connect(self._speed_rotation)
        self.track_visible_cb.clicked.connect(self.track_visible)

        self.sequence_save_btn.clicked.connect(self.save_sequence)
        self.sequence_cancel_btn.clicked.connect(self._cancel_sequence)
        self.sequence_origin_btn.clicked.connect(self._set_origin)
        self.sequence_new_btn.clicked.connect(self._new_sequence)

    def is_visible(self) -> bool:
        """
        Indique si la fenetre est visible.
        :return: bool: Fenetre visible
        """
        return self.window.isVisible()

    def _color_robot(self):
        """
        Slot pour choisir la couleur du robot.
        :return: None
        """
        if time() - self.time < 0.2:
            return

        self.color_dialog.open()
        self.color_dialog.setWindowTitle(self.init_data.get_main_robot('color_dialog_title'))

        if self.robot.is_main_robot():
            color = self.save_data.get_main_robot('color')

        else:
            color = self.save_data.get_second_robot('color')
        self.color_dialog.setCurrentColor(QtGui.QColor.fromRgb(*color))

        color = self.color_dialog.getColor()
        if self.robot.is_main_robot():
            self.save_data.set_main_robot('color', (
                color.red() / 255, color.green() / 255, color.blue() / 255, 1.))
            self.robot.setColor(self.save_data.get_main_robot('color'))
        else:
            self.save_data.set_second_robot('color', (
                color.red() / 255, color.green() / 255, color.blue() / 255, 1.))
            self.robot.setColor(self.save_data.get_second_robot('color'))

        for track in self.track:
            track.setColor((color.red(), color.green(), color.blue(), 255))

        self.parent.status_bar.showMessage(self.init_data.get_window('color_status_message').format(r=color.red(),
                                                                                                    v=color.green(),
                                                                                                    b=color.blue()))
        self.color_dialog.close()
        self.time = time()

    def _edge_color_robot(self):
        """
        Slot pour choisir la couleur des arretes.
        :return: None
        """
        if time() - self.time < 0.2:
            return

        self.color_dialog.open()
        self.color_dialog.setWindowTitle(self.init_data.get_main_robot('edge_color_dialog_title'))

        if self.robot.is_main_robot():
            color = self.save_data.get_main_robot('edge_color')

        else:
            color = self.save_data.get_second_robot('edge_color')
        self.color_dialog.setCurrentColor(QtGui.QColor.fromRgb(*color))

        color = self.color_dialog.getColor()
        if self.robot.is_main_robot():
            self.save_data.set_main_robot('edge_color', (
                color.red() / 255, color.green() / 255, color.blue() / 255, 1.))
            self.robot.set_edge_color(self.save_data.get_main_robot('edge_color'))
        else:
            self.save_data.set_second_robot('edge_color', (
                color.red() / 255, color.green() / 255, color.blue() / 255, 1.))
            self.robot.set_edge_color(self.save_data.get_second_robot('edge_color'))

        self.parent.status_bar.showMessage(self.init_data.get_window('color_status_message').format(r=color.red(),
                                                                                                    v=color.green(),
                                                                                                    b=color.blue()))
        self.color_dialog.close()
        self.time = time()

    def _close(self):
        """
        Slot pour fermer la fenetre.
        :return: None
        """
        self.window.close()

    def reset(self):
        """
        Fonction pour remettre le robot dans l'etat initial.
        :return: None
        """
        if self.robot.is_main_robot():
            self.robot.setColor(self.init_data.get_main_robot('color'))
            self.robot.set_edge_color(self.init_data.get_main_robot('edge_color'))
            for track in self.track:
                track.setColor(self.init_data.get_main_robot('color'))

        else:
            self.robot.setColor(self.init_data.get_second_robot('color'))
            self.robot.set_edge_color(self.init_data.get_second_robot('edge_color'))
            for track in self.track:
                track.setColor(self.init_data.get_second_robot('color'))

        self.window.close()

    def import_gcrubs(self, file=''):
        """
        Fonction pour importer un fichier sequentiel.
        :param file: str: Chemin du fichier a ouvrir. Si file vaut '', une fenetre est ouverte pour choisir le fichier.
        :return: None
        """
        if time() - self.time < 0.2:
            return

        if not file:
            file = QtWidgets.QFileDialog.getOpenFileName(self.window,
                                                         self.init_data.get_main_robot('import_gcrubs_title'),
                                                         self.save_data.get_window('directory'),
                                                         self.init_data.get_main_robot('import_gcrubs_extension'))[0]
        if file:
            self.robot.set_gcrubs_file(file)
            self.sequence_text.clear()
            self.track_visible(False)
            self.track.clear()

            try:
                with open(file, 'r') as f:
                    for line in f:
                        self.sequence_text.append(line.replace('\n', '', 1))
            except FileNotFoundError:
                QtWidgets.QMessageBox(self.init_data.get_window('error_open_file_type'),
                                      self.init_data.get_window('error_open_file_title'),
                                      self.init_data.get_window('error_open_file_message').format(
                                          filename=file)).exec()
            if self.robot.is_main_robot():
                self.save_data.set_main_robot('gcrubs_file', file)
                self.robot.set_sequence(self.sequence_text.document().toPlainText())
            else:
                self.save_data.set_second_robot('gcrubs_file', file)
                self.robot.set_sequence(self.sequence_text.document().toPlainText())
            self.draw_track(self.sequence_text.document().toPlainText(), self.robot.is_main_robot())

        self.time = time()

    def _remove(self):
        """
        Slot pour supprimer le robot.
        :return: None
        """
        self.remove(True)

    def remove(self, message=True):
        """
        Fonction pour supprimer le robot.
        :param message: bool: Si True, un message s'affiche
        :return: None
        """
        if time() - self.time < 0.2:
            return

        if message:
            if self.robot.is_main_robot():
                ans = QtWidgets.QMessageBox(self.init_data.get_board('remove_message_box_type'),
                                            self.init_data.get_board('remove_message_box_title'),
                                            self.init_data.get_main_robot('remove_message_box_message'),
                                            self.init_data.get_board('remove_message_box_buttons')).exec()
            else:
                ans = QtWidgets.QMessageBox(self.init_data.get_board('remove_message_box_type'),
                                            self.init_data.get_board('remove_message_box_title'),
                                            self.init_data.get_second_robot('remove_message_box_message'),
                                            self.init_data.get_board('remove_message_box_buttons')).exec()

            if ans == QtWidgets.QMessageBox.No:
                return

        for i in range(self.parent.list_widget.get_len()):  # On retire de la liste a droite
            if self.robot.get_name() == self.parent.list_widget.get_contents()[i].get_name():
                self.parent.list_widget.remove_content(i)
                break

        for track in self.track:  # On retire la trace
            track.setVisible(False)
        self.track = list()

        self.robot.set_file("")
        if self.robot.is_main_robot():
            self.save_data.set_main_robot('file', "")
            self.save_data.set_main_robot('axis_rotation', 'x')
            self.save_data.set_main_robot('angle_rotation', 0)
        else:
            self.save_data.set_second_robot('file', "")
            self.save_data.set_second_robot('axis_rotation', 'x')
            self.save_data.set_second_robot('angle_rotation', 0)
        self.reset()
        self.robot.setVisible(False)
        self.time = time()

    def _speed(self):
        """
        Slot pour modifier la vitesse de deplacement du robot.
        :return: None
        """
        self.robot.set_speed(self.speed_sb.value())
        if self.robot.is_main_robot():
            self.save_data.set_main_robot('speed', self.speed_sb.value())
        else:
            self.save_data.set_second_robot('speed', self.speed_sb.value())

    def _speed_rotation(self):
        """
        Slot pour modifier la vitesse de rotation du robot.
        :return: None
        """
        self.robot.set_speed_rotation(self.speed_rotation_sb.value())
        if self.robot.is_main_robot():
            self.save_data.set_main_robot('speed_rotation', self.speed_rotation_sb.value())
        else:
            self.save_data.set_second_robot('speed_rotation', self.speed_rotation_sb.value())

    def _rotate(self):
        """
        Slot pour faire tourner le robot autour d'un axe.
        :return: None
        """
        self.robot.translate(0, 0, -self.robot.get_offset())  # Retour a la position de depart
        self.robot.rotate(self.angle_rotation_sb.value() - self.robot.get_axis_angle(),
                          int(self.axis_rotation_rb_x.isChecked()),
                          int(self.axis_rotation_rb_y.isChecked()),
                          int(self.axis_rotation_rb_z.isChecked()),
                          local=True)

        self.robot.set_axis_angle(self.angle_rotation_sb.value())
        if self.robot.is_main_robot():
            if self.axis_rotation_rb_x.isChecked():
                self.save_data.set_main_robot('axis_rotation', 'x')
                self.save_data.set_main_robot('angle_rotation', self.angle_rotation_sb.value())
                self.robot.set_offset(self._offset_rotate('x'))
            elif self.axis_rotation_rb_y.isChecked():
                self.save_data.set_main_robot('axis_rotation', 'y')
                self.save_data.set_main_robot('angle_rotation', self.angle_rotation_sb.value())
                self.robot.set_offset(self._offset_rotate('y'))
            else:
                self.save_data.set_main_robot('axis_rotation', 'z')
                self.save_data.set_main_robot('angle_rotation', self.angle_rotation_sb.value())
            self.save_data.set_main_robot('offset', self.robot.get_offset())

        else:
            if self.axis_rotation_rb_x.isChecked():
                self.save_data.set_second_robot('axis_rotation', 'x')
                self.save_data.set_second_robot('angle_rotation', self.angle_rotation_sb.value())
                self.robot.set_offset(self._offset_rotate('x'))
            elif self.axis_rotation_rb_y.isChecked():
                self.save_data.set_second_robot('axis_rotation', 'y')
                self.save_data.set_second_robot('angle_rotation', self.angle_rotation_sb.value())
                self.robot.set_offset(self._offset_rotate('y'))
            else:
                self.save_data.set_second_robot('axis_rotation', 'z')
                self.save_data.set_second_robot('angle_rotation', self.angle_rotation_sb.value())
            self.save_data.set_second_robot('offset', self.robot.get_offset())

        self.robot.translate(0, 0, self.robot.get_offset())
        self.offset_sb.setValue(self.robot.get_offset())

    def _offset_rotate(self, axis: str) -> float:
        """
        Fonction qui determine la hauteur a laquelle doit etre place le robot pour etre sur le plateau.
        :param axis: str: Axe de rotation
        :return: float: Distance a parcourir
        """
        if axis == 'x':
            if self.robot.get_axis_angle() == 90:
                return -self.robot.get_min_max()[1][0]
            elif self.robot.get_axis_angle() == 180 or self.robot.get_axis_angle() == -180:
                return self.robot.get_min_max()[2][1]
            elif self.robot.get_axis_angle() == -90:
                return self.robot.get_min_max()[1][1]
            elif self.robot.get_axis_angle() == 0:
                return -self.robot.get_min_max()[2][0]
            else:
                return self.robot.get_offset()

        elif axis == 'y':
            if self.robot.get_axis_angle() == 90:
                return self.robot.get_min_max()[0][1]
            elif self.robot.get_axis_angle() == 180 or self.robot.get_axis_angle() == -180:
                return self.robot.get_min_max()[2][1]
            elif self.robot.get_axis_angle() == -90:
                return -self.robot.get_min_max()[0][0]
            elif self.robot.get_axis_angle() == 0:
                return -self.robot.get_min_max()[2][0]
            else:
                return self.robot.get_offset()

        elif axis == 'z':
            return self.robot.get_offset()
        else:
            return 0.

    def _axis_x(self):
        """
        Slot si l'axe x est selectionne.
        :return: None
        """
        self.robot.set_axis_angle(0)
        if self.robot.is_main_robot():
            if self.save_data.get_main_robot('axis_rotation') == 'y':
                self.robot.rotate(-self.angle_rotation_sb.value(), 0, 1, 0, local=True)
            elif self.save_data.get_main_robot('axis_rotation') == 'z':
                self.robot.rotate(-self.angle_rotation_sb.value(), 0, 0, 1, local=True)
            elif self.save_data.get_main_robot('axis_rotation') == 'x':
                self.robot.rotate(-self.angle_rotation_sb.value(), 1, 0, 0, local=True)

            self.save_data.set_main_robot('angle_rotation', 0)
            self.save_data.set_main_robot('offset', -self.robot.get_min_max()[2][0])

        else:
            if self.save_data.get_second_robot('axis_rotation') == 'y':
                self.robot.rotate(-self.angle_rotation_sb.value(), 0, 1, 0, local=True)
            elif self.save_data.get_second_robot('axis_rotation') == 'z':
                self.robot.rotate(-self.angle_rotation_sb.value(), 0, 0, 1, local=True)
            elif self.save_data.get_main_robot('axis_rotation') == 'x':
                self.robot.rotate(-self.angle_rotation_sb.value(), 1, 0, 0, local=True)

            self.save_data.set_second_robot('angle_rotation', 0)
            self.save_data.set_second_robot('offset', -self.robot.get_min_max()[2][0])

        self.angle_rotation_sb.setValue(0)
        self.robot.translate(0, 0, -self.robot.get_offset() - self.robot.get_min_max()[2][0])
        self.robot.set_offset(-self.robot.get_min_max()[2][0])
        self.offset_sb.setValue(self.robot.get_offset())

    def _axis_y(self):
        """
        Slot si l'axe y est selectionne.
        :return: None
        """
        self.robot.set_axis_angle(0)
        if self.robot.is_main_robot():
            if self.save_data.get_main_robot('axis_rotation') == 'x':
                self.robot.rotate(-self.angle_rotation_sb.value(), 1, 0, 0, local=True)
            elif self.save_data.get_main_robot('axis_rotation') == 'z':
                self.robot.rotate(-self.angle_rotation_sb.value(), 0, 0, 1, local=True)
            elif self.save_data.get_main_robot('axis_rotation') == 'y':
                self.robot.rotate(-self.angle_rotation_sb.value(), 0, 1, 0, local=True)

            self.save_data.set_main_robot('angle_rotation', 0)
            self.save_data.set_main_robot('offset', -self.robot.get_min_max()[2][0])

        else:
            if self.save_data.get_second_robot('axis_rotation') == 'x':
                self.robot.rotate(-self.angle_rotation_sb.value(), 1, 0, 0, local=True)
            elif self.save_data.get_second_robot('axis_rotation') == 'z':
                self.robot.rotate(-self.angle_rotation_sb.value(), 0, 0, 1, local=True)
            elif self.save_data.get_main_robot('axis_rotation') == 'y':
                self.robot.rotate(-self.angle_rotation_sb.value(), 0, 1, 0, local=True)

            self.save_data.set_second_robot('angle_rotation', 0)
            self.save_data.set_second_robot('offset', -self.robot.get_min_max()[2][0])

        self.angle_rotation_sb.setValue(0)
        self.robot.translate(0, 0, -self.robot.get_offset() - self.robot.get_min_max()[2][0])
        self.robot.set_offset(-self.robot.get_min_max()[2][0])
        self.offset_sb.setValue(self.robot.get_offset())

    def _axis_z(self):
        """
        Slot si l'axe z est selectionne.
        :return: None
        """
        self.robot.set_axis_angle(0)
        if self.robot.is_main_robot():
            if self.save_data.get_main_robot('axis_rotation') == 'y':
                self.robot.rotate(-self.angle_rotation_sb.value(), 0, 1, 0, local=True)
            elif self.save_data.get_main_robot('axis_rotation') == 'x':
                self.robot.rotate(-self.angle_rotation_sb.value(), 1, 0, 0, local=True)
            elif self.save_data.get_main_robot('axis_rotation') == 'z':
                self.robot.rotate(-self.angle_rotation_sb.value(), 0, 0, 1, local=True)

            self.save_data.set_main_robot('angle_rotation', 0)
            self.save_data.set_main_robot('offset', -self.robot.get_min_max()[2][0])

        else:
            if self.save_data.get_second_robot('axis_rotation') == 'y':
                self.robot.rotate(-self.angle_rotation_sb.value(), 0, 1, 0, local=True)
            elif self.save_data.get_second_robot('axis_rotation') == 'x':
                self.robot.rotate(-self.angle_rotation_sb.value(), 1, 0, 0, local=True)
            elif self.save_data.get_main_robot('axis_rotation') == 'z':
                self.robot.rotate(-self.angle_rotation_sb.value(), 0, 0, 1, local=True)

            self.save_data.set_second_robot('angle_rotation', 0)
            self.save_data.set_second_robot('offset', -self.robot.get_min_max()[2][0])

        self.angle_rotation_sb.setValue(0)
        self.robot.translate(0, 0, -self.robot.get_offset() - self.robot.get_min_max()[2][0])
        self.robot.set_offset(-self.robot.get_min_max()[2][0])
        self.offset_sb.setValue(self.robot.get_offset())

    def _offset(self):
        """
        Slot pour deplacer le robot selon la valeur de l'offset
        :return: None
        """
        self.robot.translate(0, 0, (self.offset_sb.value() - self.robot.get_offset()) * COEF)
        self.robot.set_offset(self.offset_sb.value())
        if self.robot.is_main_robot():
            self.save_data.set_main_robot('offset', self.robot.get_offset())
        else:
            self.save_data.set_second_robot('offset', self.robot.get_offset())

    def create_sequence(self):
        """
        Fonction pour creer la fenetre pour creer la sequence.
        :return: None
        """
        self._close()
        self.robot.set_origined(False)

        if self.robot.is_main_robot():
            self.parent.sequence_dock.setWindowTitle(self.init_data.get_main_robot('sequence_dialog_title'))
        else:
            self.parent.sequence_dock.setWindowTitle(self.init_data.get_second_robot('sequence_dialog_title'))
        self.sequence_text.setText(self.robot.get_sequence())

        self.parent.sequence_dock.setWidget(self.sequence_dialog)
        self.sequence_list_update()

        self.sequence_save_btn.setCursor(self.init_data.get_main_robot('sequence_save_btn_cursor'))
        self.sequence_save_btn.setDefault(self.init_data.get_main_robot('sequence_save_btn_default'))
        self.sequence_cancel_btn.setCursor(self.init_data.get_main_robot('sequence_cancel_btn_cursor'))
        self.sequence_cancel_btn.setDefault(self.init_data.get_main_robot('sequence_cancel_btn_default'))
        self.sequence_new_btn.setCursor(self.init_data.get_main_robot('sequence_new_btn_cursor'))
        self.sequence_new_btn.setDefault(self.init_data.get_main_robot('sequence_new_btn_default'))

        self.sequence_origin_btn.setCursor(self.init_data.get_main_robot('sequence_origin_btn_cursor'))
        self.sequence_origin_btn.setDefault(self.init_data.get_main_robot('sequence_origin_btn_default'))
        self.sequence_origin_lbl.setText(self.init_data.get_main_robot('sequence_origin_lbl_text'))

        self.sequence_splitter.addWidget(self.sequence_text)
        self.sequence_splitter.addWidget(self.sequence_list)
        self.sequence_layout.addWidget(self.sequence_splitter)
        self.sequence_layout.addWidget(self.sequence_origin_lbl)
        self.sequence_layout.addWidget(self.sequence_save_btn)
        self.sequence_layout.addWidget(self.sequence_cancel_btn)
        self.sequence_layout.addWidget(self.sequence_new_btn)
        self.sequence_layout.addWidget(self.sequence_origin_btn)

        self.sequence_dialog.setLayout(self.sequence_layout)
        self.sequence_list.itemDoubleClicked.connect(self._set_sequence)
        self.sequence_dialog.show()

        self.robot.go_to_origin()  # Place le robot a l'origine

        self.sequence_list.setVisible(False)
        self.sequence_text.setVisible(False)
        self.sequence_save_btn.setVisible(False)
        self.sequence_cancel_btn.setVisible(False)
        self.sequence_new_btn.setVisible(False)
        self.parent.board.setVisible(False)
        self.parent.vinyl.setVisible(False)

        self.sequence_origin_btn.setVisible(True)
        self.sequence_origin_lbl.setVisible(True)

        if not self.save_data.get_grid('coord_sys_visible'):
            self.parent.x_coord_sys.setVisible(True)
            self.parent.y_coord_sys.setVisible(True)
            self.parent.z_coord_sys.setVisible(True)

    def sequence_list_update(self):
        """
        Met a jour la liste qui contient les commandes.
        :return: None
        """
        self.sequence_list.clear()
        for key in self.save_data.get_gcrubs('cmd_name').keys():
            self.sequence_list.add_content(key)

        self.sequence_list.sortItems(self.init_data.get_main_robot('list_sorting_order'))

    def _cancel_sequence(self):
        """
        Slot pour annuler la sequence.
        :return: None
        """
        self.robot.set_sequence(self.sequence_text.document().toPlainText()) \
            if self.robot.is_main_robot() \
            else self.robot.set_sequence(self.sequence_text.document().toPlainText())

        self.sequence_dialog.close()
        self.sequence_list.setVisible(False)
        self.robot.set_ready_sequence(False)
        self.robot.set_key(None)

    def _new_sequence(self):
        """
        Cree une nouvelle sequence.
        :return: None
        """
        self.track_visible(False)
        self.track.clear()
        self.robot.set_key(None)
        self.sequence_text.clear()
        if self.robot.is_main_robot():
            self.save_data.set_main_robot('gcrubs_file', '')
        else:
            self.save_data.set_second_robot('gcrubs_file', '')

        self.robot.set_sequence('') if self.robot.is_main_robot \
            else self.robot.set_sequence('')

        self.sequence_list.setVisible(False)
        self.sequence_text.setVisible(False)
        self.sequence_save_btn.setVisible(False)
        self.sequence_cancel_btn.setVisible(False)
        self.sequence_new_btn.setVisible(False)

        self.sequence_origin_btn.setVisible(True)
        self.sequence_origin_lbl.setVisible(True)
        self.robot.set_ready_sequence(False)

        self.parent.status_bar.showMessage(
            self.init_data.get_window('position_status_message').format(x=round(self.robot.get_coord()[0]),
                                                                        y=round(self.robot.get_coord()[1]),
                                                                        angle=self.robot.get_angle()))
        self.sequence_origin_lbl.setText(self.init_data.get_main_robot('sequence_origin_lbl_text_start'))
        self.parent.board.setVisible(True)
        self.parent.vinyl.setVisible(True)

    def save_sequence(self):
        """
        Fonction pour sauvegarder la sequence.
        :return: None
        """
        if time() - self.time < 0.2:
            return

        if self.robot.is_main_robot():
            if self.save_data.get_main_robot('gcrubs_file') == '':
                filename = \
                    QtWidgets.QFileDialog.getSaveFileName(self.parent,
                                                          self.init_data.get_main_robot('save_sequence_title'),
                                                          self.save_data.get_window('directory') + '/' +
                                                          self.init_data.get_window('project_default_name') +
                                                          self.init_data.get_extension('sequence'),
                                                          self.save_data.get_gcrubs('extension'))[0]
                self.save_data.set_main_robot('gcrubs_file', filename)
            else:
                filename = self.save_data.get_main_robot('gcrubs_file')
        else:
            if self.save_data.get_second_robot('gcrubs_file') == '':
                filename = \
                    QtWidgets.QFileDialog.getSaveFileName(self.parent,
                                                          self.init_data.get_main_robot('save_sequence_title'),
                                                          self.save_data.get_window('directory') + '/' +
                                                          self.init_data.get_window('project_default_name') +
                                                          self.init_data.get_extension('sequence'),
                                                          self.save_data.get_gcrubs('extension'))[0]
                self.save_data.set_second_robot('gcrubs_file', filename)
            else:
                filename = self.save_data.get_second_robot('gcrubs_file')

        if filename:
            if filename.split('.')[-1] != self.init_data.get_extension('sequence')[1:]:
                filename = filename.split('.')[0] + self.init_data.get_extension('sequence')

            with open(filename, 'w') as file:
                file.write(self.sequence_text.document().toPlainText())
                file.write('\n')

            self.robot.set_sequence(self.sequence_text.document().toPlainText()) \
                if self.robot.is_main_robot() \
                else self.robot.set_sequence(self.sequence_text.document().toPlainText())

            self.robot.set_gcrubs_file(filename)
        self.time = time()

    def _set_sequence(self):
        """
        Slot pour ajouter la commande selectionnee dans la sequence
        :return:
        """
        if time() - self.time < 0.2:
            return
        self.sequence_text.append(self.save_data.get_gcrubs("cmd_name").get(
            self.sequence_list.get_contents()[self.sequence_list.currentRow()]))

        self.parent.do([self.robot, self.save_data.get_gcrubs("cmd_name").get(
            self.sequence_list.get_contents()[self.sequence_list.currentRow()])])
        self.key = None
        self.time = time()

    def add_sequence_text(self, text: str):
        """
        Fonction pour ajouter du texte a la sequence.
        :param text: Texte a ajouter
        :return: None
        """
        self.sequence_text.append(text)

    def get_sequence_text(self) -> str:
        """
        Renvoie le text sequentiel actuel.
        :return: str: text
        """
        return self.sequence_text.document().toPlainText()

    def set_sequence_text(self, text: str):
        """
        Definit le texte de la sequence.
        :param text: str: text
        :return: None
        """
        self.sequence_text.setText(text)

    def _set_origin(self):
        """
        Slot pour placer le robot a l'origine et au point de depart.
        :return: None
        """
        if time() - self.time < 0.2:
            # Permet d'eviter un bug d'affichage lors de la deuxieme ouverture de sequence_dialog
            return

        if self.robot.is_origined():  # Si la position de depart du robot vient d'etre choisie
            self.sequence_origin_btn.setVisible(False)
            self.sequence_origin_lbl.setVisible(False)

            self.sequence_list.setVisible(True)
            self.sequence_text.setVisible(True)
            self.sequence_save_btn.setVisible(True)
            self.sequence_cancel_btn.setVisible(True)
            self.sequence_new_btn.setVisible(True)

            if not self.save_data.get_grid('coord_sys_visible'):
                self.parent.x_coord_sys.setVisible(False)
                self.parent.y_coord_sys.setVisible(False)
                self.parent.z_coord_sys.setVisible(False)

            if self.robot.is_main_robot():
                if self.robot.get_sequence() == '':
                    self.sequence_text.setText(self.init_data.get_main_robot('sequence_text').format(
                        comment=self.save_data.get_gcrubs('cmd_name').get("Commentaire"),
                        date=QtCore.QDate.currentDate().toString(self.init_data.get_main_robot('date_format'))))
                    self.sequence_text.append(self.init_data.get_main_robot('start_sequence_text').format(
                        comment=self.save_data.get_gcrubs('cmd_name').get("Commentaire"),
                        x=round(self.robot.get_coord()[0]),
                        y=round(self.robot.get_coord()[1]),
                        angle=round(self.robot.get_angle())))
                else:
                    self.sequence_text.setText(self.robot.get_sequence())
                    for line in self.robot.get_sequence().split('\n'):
                        if self.init_data.get_main_robot('position_text') in line:
                            coord = simulation.Run.go_to_start(self.robot, line)
                            self.parent.status_bar.showMessage(
                                self.init_data.get_window('position_status_message').format(
                                    x=round(coord[0]), y=round(coord[1]), angle=round(coord[2])))
                            break

            else:  # Second_robot
                if self.robot.get_sequence() == '':
                    self.sequence_text.setText(self.init_data.get_second_robot('sequence_text').format(
                        comment=self.save_data.get_gcrubs('cmd_name').get("Commentaire"),
                        date=QtCore.QDate.currentDate().toString(self.init_data.get_main_robot('date_format'))))
                    self.sequence_text.append(self.init_data.get_main_robot('start_sequence_text').format(
                        comment=self.save_data.get_gcrubs('cmd_name').get("Commentaire"),
                        x=round(self.robot.get_coord()[0]),
                        y=round(self.robot.get_coord()[1]),
                        angle=round(self.robot.get_angle())))
                else:
                    self.sequence_text.setText(self.robot.get_sequence())
                    for line in self.robot.get_sequence().split('\n'):
                        if self.init_data.get_main_robot('position_text') in line:
                            coord = simulation.Run.go_to_start(self.robot, line)
                            self.parent.status_bar.showMessage(
                                self.init_data.get_window('position_status_message').format(
                                    x=round(coord[0]), y=round(coord[1]), angle=round(coord[2])))
                            break

            self.robot.set_ready_sequence(True)

        else:  # Si l'origine du robot vient d'etre choisie
            self.robot.set_origined(True)
            self.robot.set_origin()
            if self.robot.is_running():
                self._cancel_sequence()
            else:
                self.parent.status_bar.showMessage(
                    self.init_data.get_window('position_status_message').format(x=round(self.robot.get_coord()[0]),
                                                                                y=round(self.robot.get_coord()[1]),
                                                                                angle=self.robot.get_angle()))
                self.sequence_origin_lbl.setText(self.init_data.get_main_robot('sequence_origin_lbl_text_start'))
                self.parent.board.setVisible(True)
                self.parent.vinyl.setVisible(True)
                self.time = time()

                if self.robot.is_main_robot():
                    if self.robot.get_sequence() != "":
                        while time() - self.time < 0.2:
                            pass
                        self._set_origin()
                else:
                    if self.robot.get_sequence() != "":
                        while time() - self.time < 0.2:
                            pass
                        self._set_origin()

    def add_track(self, robot: element.Robot):
        """
        Ajoute un element de chemin a la position du robot.
        :param robot: element.Robot: Robot dont on trace le chemin
        :return: None
        """
        color = self.save_data.get_main_robot('color') if self.robot.is_main_robot() \
            else self.save_data.get_second_robot('color')
        track_width = self.init_data.get_main_robot('track_width')

        self.track.append(gl.GLSurfacePlotItem(x=np.append(-track_width / 2, track_width / 2),
                                               y=np.append(-track_width / 2, track_width / 2),
                                               z=np.full((2, 2), 1),  # Hauteur de 1 mm
                                               colors=np.full((4, 4), color)))  # Couleur du robot

        self.parent.viewer.addItem(self.track[-1])
        self.track[-1].translate(*robot.get_coord(), 0)  # Place a la position du robot
        self.track[-1].rotate(robot.get_angle(), 0, 0, 1, True)  # Met dans le sens du robot

        if not self.track_visible_cb.isChecked():
            self.track[-1].setVisible(False)

    def update_last_track(self, speed: int, width=0, height=0):
        """
        Met a jour la position et les dimensions pour la derniere trace.
        :param speed: int: Vitesse de deplacement du robot
        :param width: int: Deplacement total de la commande gcrubs selon x
        :param height: int: Deplacement total de la commande gcrubs selon y
        :return: None
        """
        color = self.save_data.get_main_robot('color') if self.robot.is_main_robot() \
            else self.save_data.get_second_robot('color')
        track_width = self.init_data.get_main_robot('track_width')

        if width == 0:
            self.track[-1].setData(x=np.append(-track_width / 2, track_width / 2),
                                   y=np.append(-height / 2, height / 2),
                                   z=np.full((2, 2), 1),
                                   colors=np.full((4, 4), color))
            self.track[-1].translate(0, speed / 2, 0, True)

        elif height == 0:
            self.track[-1].setData(x=np.append(-width / 2, width / 2),
                                   y=np.append(-track_width / 2, track_width / 2),
                                   z=np.full((2, 2), 1),
                                   colors=np.full((4, 4), color))
            self.track[-1].translate(speed / 2, 0, 0, True)

    def track_visible(self, visible=None):
        """
        Rend la trace visible ou non selon si la check box est est checkee ou non ou force la visibilite si visible
        True ou False.
        :param visible: bool: Trace visible
        :return: None
        """
        if visible is None:
            for track in self.track:
                track.setVisible(self.track_visible_cb.isChecked())
        else:
            for track in self.track:
                track.setVisible(visible)

    def remove_last_track(self):
        """
        Supprime la derniere trace.
        :return: None
        """
        self.track[-1].setVisible(False)
        self.track.pop(-1)

    def draw_track(self, sequence: str, main_robot=True):
        """
        Dessine la trace depuis la sequence.
        :param sequence: str: Contenu du fichier sequentiel
        :param main_robot: bool: Robot principal ou non
        :return: None
        """
        robot = element.Robot(self.save_data, self.parent, main_robot)
        robot.setVisible(False)
        name = self.save_data.get_gcrubs('cmd_name')  # On recupere les commandes

        for line in sequence.split('\n'):
            if self.init_data.get_main_robot('position_text') in line:
                simulation.Run.go_to_start(robot, line)
                continue

            sep = name.get('Se deplacer en avant').find('{')
            if line[:sep] == name.get('Se deplacer en avant')[:sep]:
                self.add_track(robot)
                movement = self.move(robot, line, 'Se deplacer en avant', sep, self.save_data)
                if movement[0] == 0:
                    self.update_last_track(movement[1], 0, movement[1])
                elif movement[1] == 0:
                    self.update_last_track(movement[0], movement[0], 0)
                continue

            sep = name.get('Se deplacer en arriere').find('{')
            if line[:sep] == name.get('Se deplacer en arriere')[:sep]:
                self.add_track(robot)
                movement = self.move(robot, line, 'Se deplacer en arriere', sep, self.save_data)
                if movement[0] == 0:
                    self.update_last_track(movement[1], 0, movement[1])
                elif movement[1] == 0:
                    self.update_last_track(movement[0], movement[0], 0)
                continue

            sep = name.get('Tourner a droite').find('{')
            if line[:sep] == name.get('Tourner a droite')[:sep]:
                self.move(robot, line, 'Tourner a droite', sep, self.save_data)
                continue

            sep = name.get('Tourner a gauche').find('{')
            if line[:sep] == name.get('Tourner a gauche')[:sep]:
                self.move(robot, line, 'Tourner a gauche', sep, self.save_data)
                continue

            # Pour toutes les autres commandes, on verifie que la touche correspondante n'est pas la meme
            # qu'une touche definie par un mouvement
            for key, value in zip(self.save_data.get_gcrubs('cmd_key').keys(),
                                  self.save_data.get_gcrubs('cmd_key').values()):
                if value == self.save_data.get_gcrubs('keys').get('go_up') and \
                        (key != 'Se deplacer en avant' and key != 'Se deplacer en arriere' and
                         key != 'Tourner a gauche' and key != 'Tourner a droite'):
                    sep = name.get(key).find('{')
                    if line[:sep] == name.get(key)[:sep]:
                        self.add_track(robot)
                        movement = self.move(robot, line, key, sep, self.save_data)
                        if movement[0] == 0:
                            self.update_last_track(movement[1], 0, movement[1])
                        elif movement[1] == 0:
                            self.update_last_track(movement[0], movement[0], 0)
                        break
                elif value == self.save_data.get_gcrubs('keys').get('go_down') and \
                        (key != 'Se deplacer en avant' and key != 'Se deplacer en arriere' and
                         key != 'Tourner a gauche' and key != 'Tourner a droite'):
                    sep = name.get(key).find('{')
                    if line[:sep] == name.get(key)[:sep]:
                        self.add_track(robot)
                        movement = self.move(robot, line, key, sep, self.save_data)
                        if movement[0] == 0:
                            self.update_last_track(movement[1], 0, movement[1])
                        elif movement[1] == 0:
                            self.update_last_track(movement[0], movement[0], 0)
                        break
                elif value == self.save_data.get_gcrubs('keys').get('go_right') and \
                        (key != 'Se deplacer en avant' and key != 'Se deplacer en arriere' and
                         key != 'Tourner a gauche' and key != 'Tourner a droite'):
                    sep = name.get(key).find('{')
                    if line[:sep] == name.get(key)[:sep]:
                        self.add_track(robot)
                        movement = self.move(robot, line, key, sep, self.save_data)
                        if movement[0] == 0:
                            self.update_last_track(movement[1], 0, movement[1])
                        elif movement[1] == 0:
                            self.update_last_track(movement[0], movement[0], 0)
                        break
                elif value == self.save_data.get_gcrubs('keys').get('go_left') and \
                        (key != 'Se deplacer en avant' and key != 'Se deplacer en arriere' and
                         key != 'Tourner a gauche' and key != 'Tourner a droite'):
                    sep = name.get(key).find('{')
                    if line[:sep] == name.get(key)[:sep]:
                        self.add_track(robot)
                        movement = self.move(robot, line, key, sep, self.save_data)
                        if movement[0] == 0:
                            self.update_last_track(movement[1], 0, movement[1])
                        elif movement[1] == 0:
                            self.update_last_track(movement[0], movement[0], 0)
                        break

    @staticmethod
    def move(robot, cmd, key, sep, save_data) -> np.array:
        """
        Deplace le robot d'apres la commande et la touche.
        :param robot: element.Robot: Robot a deplacer
        :param cmd: str: Commande sequentielle
        :param key: str: Touche qui correspond a la commande
        :param sep: int: Position du debut de la distance a lire:
        :param save_data: data.Save: Donnees de sauvegarde
        :return: np.array: Deplacement du robot [dx, dy, rz]
        """
        cmd_key = save_data.get_gcrubs('cmd_key')

        if cmd_key.get(key) == save_data.get_gcrubs('keys').get('go_up'):
            move = np.array([0, 1, 0])
        elif cmd_key.get(key) == save_data.get_gcrubs('keys').get('go_down'):
            move = np.array([0, -1, 0])
        elif cmd_key.get(key) == save_data.get_gcrubs('keys').get('go_right'):
            move = np.array([1, 0, 0])
        elif cmd_key.get(key) == save_data.get_gcrubs('keys').get('go_left'):
            move = np.array([-1, 0, 0])
        elif cmd_key.get(key) == save_data.get_gcrubs('keys').get('turn_right'):
            move = np.array([0, 0, -1])
        elif cmd_key.get(key) == save_data.get_gcrubs('keys').get('turn_left'):
            move = np.array([0, 0, 1])
        else:
            return np.zeros(shape=3)

        end_sep = sep
        for char in cmd[sep:]:
            if not char.isdigit():
                break  # Obtention de la position de la fin de la valeur
            end_sep += 1

        movement = int(cmd[sep:end_sep])  # Obtention de la distance a parcourir
        robot.move_robot(*move * movement)

        return move * movement
