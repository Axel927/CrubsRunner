# !/usr/bin/env python3
# -*- coding: utf-8 -*-
# Created by Axel Tremaudant on 07/06/2022

import pyqtgraph.opengl as gl
from math import cos, sin, radians
from time import time
import data
from modifiedClasses import ListWidget, GlViewWidget
from PySide6 import QtWidgets, QtGui, QtCore


class CoordSys(gl.GLMeshItem):
    def __init__(self, save_data: data.SaveData):
        super(CoordSys, self).__init__(smooth=True, drawFaces=True, drawEdges=True)
        self.save_data = save_data
        self.init_data = data.InitData()
        self.file = self.init_data.get_view('file')
        self.name = self.init_data.get_view('coord_sys_name')
        self.element_type = ""

    def set_file(self, file: str):
        self.file = file

    def get_file(self) -> str:
        return self.file

    def set_name(self, name: str):
        self.name = name

    def get_name(self) -> str:
        return self.name

    def set_edge_color(self, color):
        self.opts['edgeColor'] = color
        self.update()

    def get_element_type(self) -> str:
        return self.element_type

    def set_element_type(self, element_type: str):
        self.element_type = element_type

    def update_(self):
        self.setVisible(self.save_data.get_grid('coord_sys_visible'))


class Board(CoordSys):
    def __init__(self, save_data: data.SaveData, parent):
        super(Board, self).__init__(save_data)

        self.parent = parent
        self.file = self.init_data.get_board('file')
        self.name = self.init_data.get_board('name')
        self.time = 0.

        self.window = QtWidgets.QDialog(self.parent)
        self.color_btn = QtWidgets.QPushButton(self.init_data.get_board('color_name'), self.window)
        self.color_dialog = QtWidgets.QColorDialog(self.window)
        self.edge_color_btn = QtWidgets.QPushButton(self.init_data.get_board('edge_color_name'), self.window)
        self.close_btn = QtWidgets.QPushButton(self.init_data.get_board('close_btn_name'), self.window)
        self.reset_btn = QtWidgets.QPushButton(self.init_data.get_board('reset_btn_name'), self.window)
        self.layout = QtWidgets.QGridLayout(self.window)
        self.remove_btn = QtWidgets.QPushButton(self.init_data.get_board('remove_btn_name'), self.window)

    def properties_window(self):
        self.parent.properties_dock.setWidget(self.window)
        self.parent.properties_dock.setWindowTitle(self.init_data.get_board('window_title'))

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

        self.layout.addWidget(self.color_btn, 0, 0)
        self.layout.addWidget(self.edge_color_btn, 1, 0)
        self.layout.addWidget(self.close_btn, 2, 0)
        self.layout.addWidget(self.reset_btn, 3, 0)
        self.layout.addWidget(self.remove_btn, 4, 0)

        self._connections()
        self.window.show()

    def _connections(self):
        self.color_btn.clicked.connect(self._color_board)
        self.edge_color_btn.clicked.connect(self._edge_color_board)
        self.close_btn.clicked.connect(self._close)
        self.reset_btn.clicked.connect(self.reset)
        self.remove_btn.clicked.connect(self.remove)

    def _color_board(self):
        if time() - self.time < 0.2:
            return
        self.color_dialog.open()
        self.color_dialog.setWindowTitle(self.init_data.get_board('color_dialog_title'))

        color = self.save_data.get_board('color')
        self.color_dialog.setCurrentColor(QtGui.QColor.fromRgb(color[0], color[1], color[2], color[3]))
        self.color_dialog.setVisible(True)

        color = self.color_dialog.getColor()

        if 0 != color.green() and 0 != color.blue() and color.red() != 0:
            self.save_data.set_board('color', (
                color.red() / 255, color.green() / 255, color.blue() / 255, 1.))
            self.setColor(self.save_data.get_board('color'))
            self.parent.status_bar.showMessage(self.init_data.get_window('color_status_message').format(r=color.red(),
                                                                                                        v=color.green(),
                                                                                                        b=color.blue()))

        self.color_dialog.setVisible(False)
        self.color_dialog.close()
        self.time = time()

    def _edge_color_board(self):
        if time() - self.time < 0.2:
            return
        self.color_dialog.open()
        self.color_dialog.setWindowTitle(self.init_data.get_board('edge_color_dialog_title'))

        color = self.save_data.get_board('edge_color')
        self.color_dialog.setCurrentColor(QtGui.QColor.fromRgb(color[0], color[1], color[2], color[3]))
        self.color_dialog.setVisible(True)

        color = self.color_dialog.getColor()

        if 0 != color.green() and 0 != color.blue() and color.red() != 0:
            self.save_data.set_board('edge_color', (
                color.red() / 255, color.green() / 255, color.blue() / 255, 1.))
            self.set_edge_color(self.save_data.get_board('edge_color'))
            self.parent.status_bar.showMessage(self.init_data.get_window('color_status_message').format(r=color.red(),
                                                                                                        v=color.green(),
                                                                                                        b=color.blue()))

        self.color_dialog.setVisible(False)
        self.color_dialog.close()
        self.time = time()

    def _close(self):
        self.window.close()

    def reset(self):
        self.setColor(self.init_data.get_board('color'))
        self.set_edge_color(self.init_data.get_board('edge_color'))
        self.window.close()

    def remove(self, message=True):
        if self.parent.list_widget.get_len() < 2:
            return

        if message:
            ans = QtWidgets.QMessageBox(self.init_data.get_board('remove_message_box_type'),
                                        self.init_data.get_board('remove_message_box_title'),
                                        self.init_data.get_board('remove_message_box_message'),
                                        self.init_data.get_board('remove_message_box_buttons')).exec()

            if ans == QtWidgets.QMessageBox.No:
                return
        for i in range(self.parent.list_widget.get_len()):
            if self.get_name() == self.parent.list_widget.get_contents()[i].get_name():
                self.parent.list_widget.remove_content(i)
                break
        self.file = ""
        self.save_data.set_board('file', '')
        self.reset()
        self.setVisible(False)
        del self

    def update_(self):
        if self.file == '':
            self.file = self.save_data.get_board('file')
            self.parent.show_stl(self)

        self.setColor(self.save_data.get_board('color'))
        self.set_edge_color(self.save_data.get_board('edge_color'))


class Robot(Board):
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
        self.time = 0.
        self.invisible = False
        self.running = False
        self.gcrubs_file = ""
        self.is_updated = False
        self.ready_sequence = False

        if self.main_robot:
            self.speed = self.save_data.get_main_robot('speed')
            self.speed_rotation = self.save_data.get_main_robot('speed_rotation')
            self.name = self.init_data.get_main_robot('name')
        else:
            self.speed = self.save_data.get_second_robot('speed')
            self.speed_rotation = self.save_data.get_second_robot('speed_rotation')
            self.name = self.init_data.get_second_robot('name')

        self.window = QtWidgets.QDialog(self.parent)
        self.color_btn = QtWidgets.QPushButton(self.init_data.get_main_robot('color_name'), self.window)
        self.color_dialog = QtWidgets.QColorDialog(self.window)
        self.edge_color_btn = QtWidgets.QPushButton(self.init_data.get_main_robot('edge_color_name'), self.window)
        self.close_btn = QtWidgets.QPushButton(self.init_data.get_board('close_btn_name'), self.window)
        self.reset_btn = QtWidgets.QPushButton(self.init_data.get_board('reset_btn_name'), self.window)
        self.layout = QtWidgets.QGridLayout(self.window)
        self.remove_btn = QtWidgets.QPushButton(self.init_data.get_board('remove_btn_name'), self.window)
        self.angle_rotation_sb = QtWidgets.QSpinBox(self.window)
        self.axis_angle = 0
        self.axis_rotation_rb_x = QtWidgets.QRadioButton(self.init_data.get_main_robot('axis_rotation_x_name'),
                                                         self.window)
        self.axis_rotation_rb_y = QtWidgets.QRadioButton(self.init_data.get_main_robot('axis_rotation_y_name'),
                                                         self.window)
        self.axis_rotation_rb_z = QtWidgets.QRadioButton(self.init_data.get_main_robot('axis_rotation_z_name'),
                                                         self.window)
        self.offset_sb = QtWidgets.QSpinBox(self.window)
        self.offset = 0
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
        self.sequence_list = ListWidget()
        self.sequence_origin_lbl = QtWidgets.QLabel(self.init_data.get_main_robot('sequence_origin_lbl_text'))
        self.sequence_origin_btn = QtWidgets.QPushButton(self.init_data.get_main_robot('sequence_origin_btn_name'))

    def properties_window(self):
        if self.main_robot:
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
        self.speed_sb.setValue(self.speed)

        self.speed_rotation_sb.setMaximum(self.init_data.get_main_robot('rotation_max'))
        self.speed_rotation_sb.setMinimum(self.init_data.get_main_robot('rotation_min'))
        self.speed_rotation_sb.setValue(self.speed_rotation)

        self.angle_rotation_sb.setMinimum(self.init_data.get_main_robot('angle_rotation_min'))
        self.angle_rotation_sb.setMaximum(self.init_data.get_main_robot('angle_rotation_max'))

        self.offset_sb.setMinimum(self.init_data.get_main_robot('offset_sb_min'))
        self.offset_sb.setMaximum(self.init_data.get_main_robot('offset_sb_max'))

        if self.main_robot:
            self.angle_rotation_sb.setValue(self.save_data.get_main_robot('angle_rotation'))
            self.offset_sb.setValue(self.save_data.get_main_robot('offset'))
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
            self.offset_sb.setValue(self.save_data.get_second_robot('offset'))
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
        self.color_btn.clicked.connect(self._color_robot)
        self.edge_color_btn.clicked.connect(self._edge_color_robot)
        self.close_btn.clicked.connect(self._close)
        self.reset_btn.clicked.connect(self.reset)
        self.remove_btn.clicked.connect(self.remove)
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

    def is_ready_sequence(self) -> bool:
        return self.ready_sequence

    def _color_robot(self):
        if time() - self.time < 0.2:
            return
        self.color_dialog.open()
        self.color_dialog.setWindowTitle(self.init_data.get_main_robot('color_dialog_title'))

        if self.main_robot:
            color = self.save_data.get_main_robot('color')

        else:
            color = self.save_data.get_second_robot('color')
        self.color_dialog.setCurrentColor(QtGui.QColor.fromRgb(color[0], color[1], color[2], color[3]))
        self.color_dialog.setVisible(True)

        color = self.color_dialog.getColor()

        if 0 != color.green() and 0 != color.blue() and color.red() != 0:
            if self.main_robot:
                self.save_data.set_main_robot('color', (
                    color.red() / 255, color.green() / 255, color.blue() / 255, 1.))
                self.setColor(self.save_data.get_main_robot('color'))
            else:
                self.save_data.set_second_robot('color', (
                    color.red() / 255, color.green() / 255, color.blue() / 255, 1.))
                self.setColor(self.save_data.get_second_robot('color'))

            self.parent.status_bar.showMessage(self.init_data.get_window('color_status_message').format(r=color.red(),
                                                                                                        v=color.green(),
                                                                                                        b=color.blue()))

        self.color_dialog.setVisible(False)
        self.color_dialog.close()
        self.time = time()

    def _edge_color_robot(self):
        if time() - self.time < 0.2:
            return
        self.color_dialog.open()
        self.color_dialog.setWindowTitle(self.init_data.get_main_robot('edge_color_dialog_title'))

        if self.main_robot:
            color = self.save_data.get_main_robot('edge_color')

        else:
            color = self.save_data.get_second_robot('edge_color')
        self.color_dialog.setCurrentColor(QtGui.QColor.fromRgb(color[0], color[1], color[2], color[3]))
        self.color_dialog.setVisible(True)

        color = self.color_dialog.getColor()

        if 0 != color.green() and 0 != color.blue() and color.red() != 0:
            if self.main_robot:
                self.save_data.set_main_robot('edge_color', (
                    color.red() / 255, color.green() / 255, color.blue() / 255, 1.))
                self.set_edge_color(self.save_data.get_main_robot('edge_color'))
            else:
                self.save_data.set_second_robot('edge_color', (
                    color.red() / 255, color.green() / 255, color.blue() / 255, 1.))
                self.set_edge_color(self.save_data.get_second_robot('edge_color'))

            self.parent.status_bar.showMessage(self.init_data.get_window('color_status_message').format(r=color.red(),
                                                                                                        v=color.green(),
                                                                                                        b=color.blue()))

        self.color_dialog.setVisible(False)
        self.color_dialog.close()
        self.time = time()

    def _close(self):
        self.window.close()

    def reset(self):
        if self.main_robot:
            self.setColor(self.init_data.get_main_robot('color'))
            self.set_edge_color(self.init_data.get_main_robot('edge_color'))

        else:
            self.setColor(self.init_data.get_second_robot('color'))
            self.set_edge_color(self.init_data.get_second_robot('edge_color'))

        self.window.close()

    def import_gcrubs(self):
        file = QtWidgets.QFileDialog.getOpenFileName(self.window,
                                                     self.init_data.get_main_robot('import_gcrubs_title'),
                                                     self.save_data.get_window('directory'),
                                                     self.init_data.get_main_robot('import_gcrubs_extension'))[0]
        self.gcrubs_file = file
        if self.main_robot:
            self.save_data.set_main_robot('gcrubs_file', file)
        else:
            self.save_data.set_second_robot('gcrubs_file', file)

    def remove(self, message=True):
        if message:
            if self.main_robot:
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
            if self.get_name() == self.parent.list_widget.get_contents()[i].get_name():
                self.parent.list_widget.remove_content(i)
                break
        self.file = ""
        if self.main_robot:
            self.save_data.set_main_robot('file', '')
        else:
            self.save_data.set_second_robot('file', "")
        self.reset()
        self.setVisible(False)
        del self

    def _speed(self):
        self.speed = self.speed_sb.value()
        if self.main_robot:
            self.save_data.set_main_robot('speed', self.speed_sb.value())
        else:
            self.save_data.set_second_robot('speed', self.speed_sb.value())

    def _speed_rotation(self):
        self.speed_rotation = self.speed_rotation_sb.value()
        if self.main_robot:
            self.save_data.set_main_robot('speed_rotation', self.speed_rotation_sb.value())
        else:
            self.save_data.set_second_robot('speed_rotation', self.speed_rotation_sb.value())

    def _rotate(self):
        self.rotate(self.angle_rotation_sb.value() - self.axis_angle, int(self.axis_rotation_rb_x.isChecked()),
                    int(self.axis_rotation_rb_y.isChecked()), int(self.axis_rotation_rb_z.isChecked()), local=True)
        self.axis_angle = self.angle_rotation_sb.value()
        if self.main_robot:
            if self.axis_rotation_rb_x.isChecked():
                self.save_data.set_main_robot('axis_rotation', 'x')
                self.save_data.set_main_robot('angle_rotation', self.angle_rotation_sb.value())
            elif self.axis_rotation_rb_y.isChecked():
                self.save_data.set_main_robot('axis_rotation', 'y')
                self.save_data.set_main_robot('angle_rotation', self.angle_rotation_sb.value())
            else:
                self.save_data.set_main_robot('axis_rotation', 'z')
                self.save_data.set_main_robot('angle_rotation', self.angle_rotation_sb.value())
        else:
            if self.axis_rotation_rb_x.isChecked():
                self.save_data.set_second_robot('axis_rotation', 'x')
                self.save_data.set_second_robot('angle_rotation', self.angle_rotation_sb.value())
            elif self.axis_rotation_rb_y.isChecked():
                self.save_data.set_second_robot('axis_rotation', 'y')
                self.save_data.set_second_robot('angle_rotation', self.angle_rotation_sb.value())
            else:
                self.save_data.set_second_robot('axis_rotation', 'z')
                self.save_data.set_second_robot('angle_rotation', self.angle_rotation_sb.value())

    def _axis_x(self):
        self.axis_angle = 0
        if self.main_robot:
            if self.save_data.get_main_robot('axis_rotation') == 'y':
                self.rotate(-self.angle_rotation_sb.value(), 0, 1, 0, local=True)
                self.save_data.set_main_robot('angle_rotation', 0)
            elif self.save_data.get_main_robot('axis_rotation') == 'z':
                self.rotate(-self.angle_rotation_sb.value(), 0, 0, 1, local=True)
                self.save_data.set_main_robot('angle_rotation', 0)
        else:
            if self.save_data.get_second_robot('axis_rotation') == 'y':
                self.rotate(-self.angle_rotation_sb.value(), 0, 1, 0, local=True)
                self.save_data.set_second_robot('angle_rotation', 0)
            elif self.save_data.get_second_robot('axis_rotation') == 'z':
                self.rotate(-self.angle_rotation_sb.value(), 0, 0, 1, local=True)
                self.save_data.set_second_robot('angle_rotation', 0)
        self.angle_rotation_sb.setValue(0)

    def _axis_y(self):
        self.axis_angle = 0
        if self.main_robot:
            if self.save_data.get_main_robot('axis_rotation') == 'x':
                self.rotate(-self.angle_rotation_sb.value(), 1, 0, 0, local=True)
                self.save_data.set_main_robot('angle_rotation', 0)
            elif self.save_data.get_main_robot('axis_rotation') == 'z':
                self.rotate(-self.angle_rotation_sb.value(), 0, 0, 1, local=True)
                self.save_data.set_main_robot('angle_rotation', 0)
        else:
            if self.save_data.get_second_robot('axis_rotation') == 'x':
                self.rotate(-self.angle_rotation_sb.value(), 1, 0, 0, local=True)
                self.save_data.set_second_robot('angle_rotation', 0)
            elif self.save_data.get_second_robot('axis_rotation') == 'z':
                self.rotate(-self.angle_rotation_sb.value(), 0, 0, 1, local=True)
                self.save_data.set_second_robot('angle_rotation', 0)
        self.angle_rotation_sb.setValue(0)

    def _axis_z(self):
        self.axis_angle = 0
        if self.main_robot:
            if self.save_data.get_main_robot('axis_rotation') == 'y':
                self.rotate(-self.angle_rotation_sb.value(), 0, 1, 0, local=True)
                self.save_data.set_main_robot('angle_rotation', 0)
            elif self.save_data.get_main_robot('axis_rotation') == 'x':
                self.rotate(-self.angle_rotation_sb.value(), 1, 0, 0, local=True)
                self.save_data.set_main_robot('angle_rotation', 0)
        else:
            if self.save_data.get_second_robot('axis_rotation') == 'y':
                self.rotate(-self.angle_rotation_sb.value(), 0, 1, 0, local=True)
                self.save_data.set_second_robot('angle_rotation', 0)
            elif self.save_data.get_second_robot('axis_rotation') == 'x':
                self.rotate(-self.angle_rotation_sb.value(), 1, 0, 0, local=True)
                self.save_data.set_second_robot('angle_rotation', 0)
        self.angle_rotation_sb.setValue(0)

    def _offset(self):
        self.translate(0, 0, self.offset_sb.value() - self.offset)
        self.offset = self.offset_sb.value()
        if self.main_robot:
            self.save_data.set_main_robot('offset', self.offset)
        else:
            self.save_data.set_second_robot('offset', self.offset)

    def create_sequence(self):
        self._close()
        self.origined = False

        if self.main_robot:
            self.parent.sequence_dock.setWindowTitle(self.init_data.get_main_robot('sequence_dialog_title'))
        else:
            self.parent.sequence_dock.setWindowTitle(self.init_data.get_second_robot('sequence_dialog_title'))

        self.parent.sequence_dock.setWidget(self.sequence_dialog)

        for key in self.save_data.get_gcrubs('cmd_name').keys():
            self.sequence_list.addItem(key)
            self.sequence_list.add_content(key)
        self.sequence_list.sortItems(self.init_data.get_main_robot('list_sorting_order'))

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

        self.sequence_origin_btn.setVisible(True)
        self.sequence_origin_lbl.setVisible(True)

        if not self.save_data.get_grid('coord_sys_visible'):
            self.parent.x_coord_sys.setVisible(True)
            self.parent.y_coord_sys.setVisible(True)
            self.parent.z_coord_sys.setVisible(True)

    def sequence_list_update(self):
        for _ in range(self.sequence_list.get_len()):
            self.sequence_list.remove_content(0)
        for key in self.save_data.get_gcrubs('cmd_name').keys():
            self.sequence_list.addItem(key)
            self.sequence_list.add_content(key)

        self.sequence_list.sortItems(self.init_data.get_main_robot('list_sorting_order'))

    def _cancel_sequence(self):
        self.sequence_text.clear()
        self.sequence_dialog.close()
        self.sequence_list.setVisible(False)
        self.ready_sequence = False

    def save_sequence(self):
        if self.main_robot:
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

            if self.main_robot:
                self.save_data.set_main_robot('sequence', self.sequence_text.document().toPlainText())
            else:
                self.save_data.set_second_robot('sequence', self.sequence_text.document().toPlainText())

            self.gcrubs_file = filename

        else:
            print("file not opened")

    def _set_sequence(self):
        self.sequence_text.append(self.save_data.get_gcrubs("cmd_name").get(
            self.sequence_list.get_contents()[self.sequence_list.currentRow()]))

        self.key = None

    def _set_origin(self):
        if self.origined:
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

            if self.main_robot:
                if self.save_data.get_main_robot('sequence') == '':
                    self.sequence_text.setText(self.init_data.get_main_robot('sequence_text').format(
                        comment=self.save_data.get_gcrubs('cmd_name').get("Commentaire"),
                        date=QtCore.QDate.currentDate().toString(self.init_data.get_main_robot('date_format'))))
                else:
                    self.sequence_text.setText(self.save_data.get_main_robot('sequence'))
            else:
                if self.save_data.get_second_robot('sequence') == '':
                    self.sequence_text.setText(self.init_data.get_second_robot('sequence_text').format(
                        comment=self.save_data.get_gcrubs('cmd_name').get("Commentaire"),
                        date=QtCore.QDate.currentDate().toString(self.init_data.get_main_robot('date_format'))))
                else:
                    self.sequence_text.setText(self.save_data.get_second_robot('sequence'))

            self.sequence_text.append(self.init_data.get_main_robot('start_sequence_text').format(
                comment=self.save_data.get_gcrubs('cmd_name').get("Commentaire"),
                x=int(self.get_coord()[0]),
                y=int(self.get_coord()[1]),
                angle=self.get_angle()))
            self.ready_sequence = True

        else:
            self.origined = True
            self.coord = [0, 0]
            if self.running:
                self._cancel_sequence()
            else:
                self.parent.status_bar.showMessage(
                    self.init_data.get_window('position_status_message').format(x=int(self.get_coord()[0]),
                                                                                y=int(self.get_coord()[1]),
                                                                                angle=self.get_angle()))
                self.sequence_origin_lbl.setText(self.init_data.get_main_robot('sequence_origin_lbl_text_start'))
                self.parent.board.setVisible(True)
                self.time = time()

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

    def is_origined(self) -> bool:
        return self.origined

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
            mvt = GlViewWidget.robot_movement(self.save_data.get_main_robot('axis_rotation'),
                                              self.save_data.get_main_robot('angle_rotation'))
        else:
            mvt = GlViewWidget.robot_movement(self.save_data.get_second_robot('axis_rotation'),
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

    def get_speed_rotation(self) -> int:
        return self.speed_rotation
