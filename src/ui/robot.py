# !/usr/bin/env python3
# -*- coding: utf-8 -*-
# Created by Axel Tremaudant on 08/07/2022

"""
Fichier contenant la partie interface de la classe Robot.
"""

from PySide6 import QtWidgets, QtGui, QtCore
from time import time
import data
import widget


class Robot:
    """
    Classe pour l'interface des robots.
    """
    def __init__(self, parent, save_data: data.Save, robot):
        """
        Constructeur de Robot.
        :param parent: ui.MainWindow: Fenetre principale.
        :param save_data: data.Save: Donnees de sauvegarde
        :param robot: element.Robot: Robot concerne
        """
        self.parent = parent
        self.save_data = save_data
        self.robot = robot
        self.init_data = data.Init()
        self.time = 0.

        self.window = QtWidgets.QDialog(self.parent)
        self.color_btn = QtWidgets.QPushButton(self.init_data.get_main_robot('color_name'), self.window)
        self.color_dialog = QtWidgets.QColorDialog(self.window)
        self.edge_color_btn = QtWidgets.QPushButton(self.init_data.get_main_robot('edge_color_name'), self.window)
        self.close_btn = QtWidgets.QPushButton(self.init_data.get_board('close_btn_name'), self.window)
        self.reset_btn = QtWidgets.QPushButton(self.init_data.get_board('reset_btn_name'), self.window)
        self.layout = QtWidgets.QGridLayout(self.window)
        self.remove_btn = QtWidgets.QPushButton(self.init_data.get_board('remove_btn_name'), self.window)
        self.angle_rotation_sb = QtWidgets.QSpinBox(self.window)

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

        self.sequence_dialog = QtWidgets.QDialog(self.parent)
        self.sequence_text = QtWidgets.QTextEdit("", self.sequence_dialog)
        self.sequence_layout = QtWidgets.QVBoxLayout()
        self.sequence_save_btn = QtWidgets.QPushButton(self.init_data.get_main_robot('sequence_save_btn_name'))
        self.sequence_cancel_btn = QtWidgets.QPushButton(self.init_data.get_main_robot('sequence_cancel_btn_name'))
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
        self.color_dialog.setVisible(False)

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

        gb_layout = QtWidgets.QGridLayout()
        gb_layout.addWidget(self.angle_lbl, 0, 0)
        gb_layout.addWidget(self.angle_rotation_sb, 0, 1)
        gb_layout.addWidget(self.axis_lbl, 1, 0)
        gb_layout.addWidget(self.axis_rotation_rb_x, 1, 1)
        gb_layout.addWidget(self.axis_rotation_rb_y, 2, 1)
        gb_layout.addWidget(self.axis_rotation_rb_z, 3, 1)
        gb_layout.addWidget(self.offset_lbl, 4, 0)
        gb_layout.addWidget(self.offset_sb, 4, 1)
        group_box = QtWidgets.QGroupBox(self.init_data.get_main_robot('gb_name'), self.window)
        group_box.setLayout(gb_layout)

        speed_gb = QtWidgets.QGroupBox(self.init_data.get_main_robot('gb_speed_name'))
        speed_layout = QtWidgets.QGridLayout()
        speed_layout.addWidget(self.speed_lbl, 0, 0)
        speed_layout.addWidget(self.speed_sb, 0, 1)
        speed_layout.addWidget(self.speed_rotation_lbl, 1, 0)
        speed_layout.addWidget(self.speed_rotation_sb, 1, 1)
        speed_gb.setLayout(speed_layout)

        self.layout.addWidget(self.color_btn, 0, 0)
        self.layout.addWidget(self.edge_color_btn, 1, 0)
        self.layout.addWidget(speed_gb, 2, 0)
        self.layout.addWidget(group_box, 3, 0)
        self.layout.addWidget(self.close_btn, 4, 0)
        self.layout.addWidget(self.reset_btn, 5, 0)
        self.layout.addWidget(self.remove_btn, 6, 0)
        self.layout.addWidget(self.import_gcrubs_btn, 7, 0)
        self.layout.addWidget(self.create_sequence_btn, 8, 0)

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

        self.sequence_save_btn.clicked.connect(self.save_sequence)
        self.sequence_cancel_btn.clicked.connect(self._cancel_sequence)
        self.sequence_origin_btn.clicked.connect(self._set_origin)

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
        self.color_dialog.setCurrentColor(QtGui.QColor.fromRgb(color[0], color[1], color[2], color[3]))

        color = self.color_dialog.getColor()
        if self.robot.is_main_robot():
            self.save_data.set_main_robot('color', (
                color.red() / 255, color.green() / 255, color.blue() / 255, 1.))
            self.robot.setColor(self.save_data.get_main_robot('color'))
        else:
            self.save_data.set_second_robot('color', (
                color.red() / 255, color.green() / 255, color.blue() / 255, 1.))
            self.robot.setColor(self.save_data.get_second_robot('color'))

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
        self.color_dialog.setCurrentColor(QtGui.QColor.fromRgb(color[0], color[1], color[2], color[3]))

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

        else:
            self.robot.setColor(self.init_data.get_second_robot('color'))
            self.robot.set_edge_color(self.init_data.get_second_robot('edge_color'))

        self.window.close()

    def import_gcrubs(self):
        """
        fonction pour importer un fichier sequentiel.
        :return: None
        """
        if time() - self.time < 0.2:
            return

        file = QtWidgets.QFileDialog.getOpenFileName(self.window,
                                                     self.init_data.get_main_robot('import_gcrubs_title'),
                                                     self.save_data.get_window('directory'),
                                                     self.init_data.get_main_robot('import_gcrubs_extension'))[0]
        self.robot.set_gcrubs_file(file)
        self.sequence_text.clear()

        try:
            with open(file, 'r') as f:
                lines = f.readlines()
                for line in lines:
                    self.sequence_text.append(line.replace('\n', '', 1))
        except FileNotFoundError:
            QtWidgets.QMessageBox(self.init_data.get_window('error_open_file_type'),
                                  self.init_data.get_window('error_open_file_title'),
                                  self.init_data.get_window('error_open_file_message').format(
                                      filename=file)).exec()
        if self.robot.is_main_robot():
            self.save_data.set_main_robot('gcrubs_file', file)
            self.save_data.set_main_robot('sequence', self.sequence_text.document().toPlainText())
        else:
            self.save_data.set_second_robot('gcrubs_file', file)
            self.save_data.set_second_robot('sequence', self.sequence_text.document().toPlainText())

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

        for i in range(self.parent.list_widget.get_len()):
            if self.robot.get_name() == self.parent.list_widget.get_contents()[i].get_name():
                self.parent.list_widget.remove_content(i)
                break

        self.robot.set_file("")
        if self.robot.is_main_robot():
            self.save_data.set_main_robot('file', "")
        else:
            self.save_data.set_second_robot('file', "")
        self.reset()
        self.robot.setVisible(False)
        del self

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
        self.robot.translate(0, 0, self.offset_sb.value() - self.robot.get_offset())
        self.robot.set_offset(self.offset_sb.value())
        if self.robot.is_main_robot():
            self.save_data.set_main_robot('offset', self.robot.get_offset())
        else:
            self.save_data.set_second_robot('offset', self.robot.get_offset())

    def create_sequence(self):
        """
        Fonction pour cree la fenetre pour creer la sequence.
        :return: None
        """
        self._close()
        self.robot.set_origined(False)

        if self.robot.is_main_robot():
            self.parent.sequence_dock.setWindowTitle(self.init_data.get_main_robot('sequence_dialog_title'))
            self.sequence_text.setText(self.save_data.get_main_robot('sequence'))
        else:
            self.parent.sequence_dock.setWindowTitle(self.init_data.get_second_robot('sequence_dialog_title'))
            self.sequence_text.setText(self.save_data.get_second_robot('sequence'))

        self.parent.sequence_dock.setWidget(self.sequence_dialog)
        self.sequence_list_update()

        self.sequence_save_btn.setCursor(self.init_data.get_main_robot('sequence_save_btn_cursor'))
        self.sequence_save_btn.setDefault(self.init_data.get_main_robot('sequence_save_btn_default'))
        self.sequence_cancel_btn.setCursor(self.init_data.get_main_robot('sequence_cancel_btn_cursor'))
        self.sequence_cancel_btn.setDefault(self.init_data.get_main_robot('sequence_cancel_btn_default'))

        self.sequence_origin_btn.setCursor(self.init_data.get_main_robot('sequence_origin_btn_cursor'))
        self.sequence_origin_btn.setDefault(self.init_data.get_main_robot('sequence_origin_btn_default'))
        self.sequence_origin_lbl.setText(self.init_data.get_main_robot('sequence_origin_lbl_text'))

        self.sequence_layout.addWidget(self.sequence_text)
        self.sequence_layout.addWidget(self.sequence_origin_lbl)
        self.sequence_layout.addWidget(self.sequence_list)
        self.sequence_layout.addWidget(self.sequence_save_btn)
        self.sequence_layout.addWidget(self.sequence_cancel_btn)
        self.sequence_layout.addWidget(self.sequence_origin_btn)

        self.sequence_dialog.setLayout(self.sequence_layout)
        self.sequence_list.itemDoubleClicked.connect(self._set_sequence)
        self.sequence_dialog.show()

        self.sequence_list.setVisible(False)
        self.sequence_text.setVisible(False)
        self.sequence_save_btn.setVisible(False)
        self.sequence_cancel_btn.setVisible(False)
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
        Met a jour la liste qui contient les commandes
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
        if self.robot.is_main_robot():
            self.save_data.set_main_robot('sequence', self.sequence_text.document().toPlainText())
        else:
            self.save_data.set_second_robot('sequence', self.sequence_text.document().toPlainText())
        self.sequence_text.clear()
        self.sequence_dialog.close()
        self.sequence_list.setVisible(False)
        self.ready_sequence = False

    def save_sequence(self):
        """
        Fonction pour sauvegarder la sequence.
        :return: None
        """
        if self.robot.is_main_robot():
            if self.save_data.get_main_robot('gcrubs_file') == '':
                filename = \
                    QtWidgets.QFileDialog.getSaveFileName(self.parent,
                                                          self.init_data.get_main_robot('save_sequence_title'),
                                                          self.save_data.get_window('directory'),
                                                          self.save_data.get_gcrubs('extension'))[0]
            else:
                filename = self.save_data.get_main_robot('gcrubs_file')
        else:
            if self.save_data.get_second_robot('gcrubs_file') == '':
                filename = \
                    QtWidgets.QFileDialog.getSaveFileName(self.parent,
                                                          self.init_data.get_main_robot('save_sequence_title'),
                                                          self.save_data.get_window('directory'),
                                                          self.save_data.get_gcrubs('extension'))[0]
            else:
                filename = self.save_data.get_second_robot('gcrubs_file')

        if filename:
            filename += self.init_data.get_extension('sequence')
            with open(filename, 'w') as file:
                file.write(self.sequence_text.document().toPlainText())
                file.write('\n')

            if self.robot.is_main_robot():
                self.save_data.set_main_robot('sequence', self.sequence_text.document().toPlainText())
            else:
                self.save_data.set_second_robot('sequence', self.sequence_text.document().toPlainText())

            self.robot.set_gcrubs_file(filename)

    def _set_sequence(self):
        """
        Slot pour ajouter la commande selectionnee dans la sequence
        :return:
        """
        if time() - self.time < 0.2:
            return
        self.sequence_text.append(self.save_data.get_gcrubs("cmd_name").get(
            self.sequence_list.get_contents()[self.sequence_list.currentRow()]))

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
        if self.robot.is_origined():  # Si l'origine du robot a deja ete choisie
            if time() - self.time < 0.2:
                # Permet d'eviter un bug d'affichage lors de la deuxieme ouverture de sequence_dialog
                return

            self.sequence_origin_btn.setVisible(False)
            self.sequence_origin_lbl.setVisible(False)

            self.sequence_list.setVisible(True)
            self.sequence_text.setVisible(True)
            self.sequence_save_btn.setVisible(True)
            self.sequence_cancel_btn.setVisible(True)

            if not self.save_data.get_grid('coord_sys_visible'):
                self.parent.x_coord_sys.setVisible(False)
                self.parent.y_coord_sys.setVisible(False)
                self.parent.z_coord_sys.setVisible(False)

            if self.robot.is_main_robot():
                if self.save_data.get_main_robot('sequence') == '':
                    self.sequence_text.setText(self.init_data.get_main_robot('sequence_text').format(
                        comment=self.save_data.get_gcrubs('cmd_name').get("Commentaire"),
                        date=QtCore.QDate.currentDate().toString(self.init_data.get_main_robot('date_format'))))
                    self.sequence_text.append(self.init_data.get_main_robot('start_sequence_text').format(
                        comment=self.save_data.get_gcrubs('cmd_name').get("Commentaire"),
                        x=int(self.robot.get_coord()[0]),
                        y=int(self.robot.get_coord()[1]),
                        angle=self.robot.get_angle()))
                else:
                    self.sequence_text.setText(self.save_data.get_main_robot('sequence'))

            else:  # Second_robot
                if self.save_data.get_second_robot('sequence') == '':
                    self.sequence_text.setText(self.init_data.get_second_robot('sequence_text').format(
                        comment=self.save_data.get_gcrubs('cmd_name').get("Commentaire"),
                        date=QtCore.QDate.currentDate().toString(self.init_data.get_main_robot('date_format'))))
                    self.sequence_text.append(self.init_data.get_main_robot('start_sequence_text').format(
                        comment=self.save_data.get_gcrubs('cmd_name').get("Commentaire"),
                        x=int(self.robot.get_coord()[0]),
                        y=int(self.robot.get_coord()[1]),
                        angle=self.robot.get_angle()))
                else:
                    self.sequence_text.setText(self.save_data.get_second_robot('sequence'))

            self.robot.set_ready_sequence(True)

        else:
            self.robot.set_origined(True)
            self.coord = [0, 0]
            if self.robot.is_running():
                self._cancel_sequence()
            else:
                self.parent.status_bar.showMessage(
                    self.init_data.get_window('position_status_message').format(x=int(self.robot.get_coord()[0]),
                                                                                y=int(self.robot.get_coord()[1]),
                                                                                angle=self.robot.get_angle()))
                self.sequence_origin_lbl.setText(self.init_data.get_main_robot('sequence_origin_lbl_text_start'))
                self.parent.board.setVisible(True)
                self.parent.vinyl.setVisible(True)
                self.time = time()
