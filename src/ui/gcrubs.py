# !/usr/bin/env python3
# -*- coding: utf-8 -*-
# Created by Axel Tremaudant on 20/06/22

from PySide6 import QtWidgets, QtCore
from data.initData import InitData
from data.saveData import SaveData
from widget.button import Button
from widget.lineEdit import LineEdit
from widget.label import Label
from widget.keyDialog import KeyDialog


class GCrubs:
    def __init__(self, save_data: SaveData, parent):
        self.save_data = save_data
        self.init_data = InitData()
        self.parent = parent
        self.cmd = list()
        self.cmd_size = 0

        self.window = QtWidgets.QDialog(self.parent)
        self.layout = QtWidgets.QVBoxLayout(self.window)
        self.scroll_area = QtWidgets.QScrollArea()
        self.gb = QtWidgets.QGroupBox()
        self.description_lbl = QtWidgets.QLabel(self.init_data.get_gcrubs('description_lbl_text'), self.window)
        self.apply_btn = QtWidgets.QPushButton(self.init_data.get_gcrubs('apply_btn_name'), self.window)
        self.cancel_btn = QtWidgets.QPushButton(self.init_data.get_gcrubs('cancel_btn_name'), self.window)
        self.add_btn = QtWidgets.QPushButton(self.init_data.get_gcrubs('add_btn_name'))
        self.grid_layout = QtWidgets.QGridLayout()

        self.key_dialog = QtWidgets.QDialog(self.parent)
        self.key_lbl = QtWidgets.QLabel("", self.key_dialog)
        self.key_layout = QtWidgets.QVBoxLayout(self.key_dialog)
        self.key_close = QtWidgets.QPushButton(self.init_data.get_gcrubs('key_close_name'), self.key_dialog)

    def edit(self):
        self.gb = QtWidgets.QGroupBox()
        self.window.setWindowTitle(self.init_data.get_gcrubs('edit_window_title'))
        self.window.setFixedSize(self.init_data.get_gcrubs('sa_width'), self.init_data.get_gcrubs('sa_height'))
        self.window.setModal(self.init_data.get_gcrubs('window_modal'))

        self.scroll_area.setWidgetResizable(True)

        self.grid_layout = QtWidgets.QGridLayout()

        self.cmd = list()
        self.cmd_size = 0

        for key, value in zip(self.save_data.get_gcrubs('cmd_name').keys(),
                              self.save_data.get_gcrubs('cmd_name').values()):
            self._cmd_append(key, value)

        for i in range(6):
            self.cmd[i][0].setEnabled(False)
            self.cmd[i][1].setEnabled(False)

        self.apply_btn.setCursor(self.init_data.get_gcrubs('apply_btn_cursor'))
        self.apply_btn.setDefault(self.init_data.get_gcrubs('apply_btn_default'))
        self.cancel_btn.setCursor(self.init_data.get_gcrubs('cancel_btn_cursor'))
        self.cancel_btn.setDefault(self.init_data.get_gcrubs('cancel_btn_default'))

        self.add_btn = QtWidgets.QPushButton(self.init_data.get_gcrubs('add_btn_name'))
        self.add_btn.setDefault(self.init_data.get_gcrubs('add_btn_default'))
        self.add_btn.setCursor(self.init_data.get_gcrubs('add_btn_cursor'))

        btn_layout = QtWidgets.QHBoxLayout()
        btn_layout.addWidget(self.cancel_btn)
        btn_layout.addWidget(self.apply_btn)

        v_layout = QtWidgets.QVBoxLayout()
        v_layout.addWidget(self.description_lbl)
        v_layout.addLayout(self.grid_layout)
        v_layout.addWidget(self.add_btn)
        self.gb.setLayout(v_layout)
        self.scroll_area.setWidget(self.gb)

        self.layout.addWidget(self.scroll_area)
        self.layout.addLayout(btn_layout)
        self.window.setLayout(self.layout)

        self._connections()
        self.window.show()

    def _connections(self):
        self.cancel_btn.clicked.connect(self._cancel)
        self.apply_btn.clicked.connect(self._apply)
        self.add_btn.clicked.connect(self._add)
        for i in range(self.cmd_size):
            self.cmd[i][0].clicked.connect(self.cmd[i][0].set_clicked)
            self.cmd[i][0].clicked.connect(self._del)
            self.cmd[i][3].clicked.connect(self.cmd[i][3].set_clicked)
            self.cmd[i][3].clicked.connect(self._key)

        self.key_close.clicked.connect(self._key_close)

    def _cancel(self):
        self.window.close()

    def _apply(self):
        cmd_name = dict()
        cmd_key = dict()
        for i in range(self.cmd_size):
            if self.cmd[i][0].isVisible():
                cmd_name[self.cmd[i][1].text().capitalize()] = self.cmd[i][2].text()
                if self.cmd[i][2].get_key() == QtCore.Qt.Key(0):
                    cmd_key[self.cmd[i][1].text().capitalize()] = None
                else:
                    cmd_key[self.cmd[i][1].text().capitalize()] = self.cmd[i][2].get_key()

        self.save_data.set_gcrubs('cmd_name', cmd_name)
        self.save_data.set_gcrubs('cmd_key', cmd_key)
        self.parent.main_robot.sequence_list_update()
        self.window.close()

    def _del(self):
        for i in range(self.cmd_size):
            if self.cmd[i][0].is_clicked():
                for j in range(4):
                    self.cmd[i][j].setVisible(False)
                self.cmd[i][0].set_unclicked()

    def _add(self):
        self._cmd_append()
        self.cmd[self.cmd_size - 1][0].clicked.connect(self.cmd[self.cmd_size - 1][0].set_clicked)
        self.cmd[self.cmd_size - 1][0].clicked.connect(self._del)
        self.cmd[self.cmd_size - 1][3].clicked.connect(self.cmd[self.cmd_size - 1][3].set_clicked)
        self.cmd[self.cmd_size - 1][3].clicked.connect(self._key)

    def _cmd_append(self, key="", value=""):
        self.cmd.append([Button(self.scroll_area, self.cmd_size),
                         QtWidgets.QLineEdit(self.scroll_area),
                         LineEdit(self.scroll_area),
                         Button(self.scroll_area, self.cmd_size),
                         Label(KeyDialog.ret_key(self.save_data.get_gcrubs('cmd_key').get(key)))
                         ])
        self.cmd[self.cmd_size][0].setCursor(self.init_data.get_gcrubs('btn_cursor'))
        self.cmd[self.cmd_size][3].setCursor(self.init_data.get_gcrubs('btn_cursor'))
        self.cmd[self.cmd_size][0].setToolTip(self.init_data.get_gcrubs('del_btn_tip'))
        self.cmd[self.cmd_size][3].setToolTip(self.init_data.get_gcrubs('key_btn_tip'))
        self.cmd[self.cmd_size][0].setIcon(self.init_data.get_gcrubs('del_btn_icon'))
        self.cmd[self.cmd_size][3].setIcon(self.init_data.get_gcrubs('key_btn_icon'))

        self.cmd[self.cmd_size][1].setText(key)
        self.cmd[self.cmd_size][2].setText(value)
        self.cmd[self.cmd_size][2].set_key(self.save_data.get_gcrubs('cmd_key').get(key))

        for i in range(5):
            self.grid_layout.addWidget(self.cmd[self.cmd_size][i], self.cmd_size, i)

        self.cmd_size += 1

    def _key(self):
        self.window.hide()
        self.parent.properties_dock.setWindowTitle(self.init_data.get_gcrubs('key_dialog_title'))
        self.parent.properties_dock.setWidget(self.key_dialog)

        for i in range(self.cmd_size):
            if self.cmd[i][3].is_clicked():
                self.cmd[i][3].set_unclicked()
                self.key_lbl.setText(self.init_data.get_gcrubs('key_lbl_text').format(
                    instruction=self.cmd[i][1].text()))

                self.parent.viewer.get_key(self.key_lbl, self.cmd[i][2])
                self.key_layout.addWidget(self.key_lbl)
                break

        self.key_close.setCursor(self.init_data.get_gcrubs('key_close_cursor'))
        self.key_close.setDefault(self.init_data.get_gcrubs('key_close_default'))
        self.key_layout.addWidget(self.key_close)

        self.key_dialog.setLayout(self.key_layout)
        self.key_dialog.show()

    def _key_close(self):
        self.parent.viewer.stop_get_key()
        self.key_dialog.close()
        for i in range(self.cmd_size):
            self.cmd[i][4].setText(KeyDialog.ret_key(self.cmd[i][2].get_key()))

        self.window.show()

    def get_cmd(self):
        return self.cmd
