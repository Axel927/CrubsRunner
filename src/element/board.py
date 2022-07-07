# !/usr/bin/env python3
# -*- coding: utf-8 -*-
# Created by Axel Tremaudant on 07/07/2022

from PySide6 import QtWidgets, QtGui
from time import time

from element.coordSys import CoordSys
from data.saveData import SaveData


class Board(CoordSys):
    def __init__(self, save_data: SaveData, parent):
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
