# !/usr/bin/env python3
# -*- coding: utf-8 -*-
# Created by Axel Tremaudant on 07/07/2022


from PySide6 import QtWidgets
import data

# Note : mr mean main robot and sr mean second robot


class Run:
    def __init__(self, save_data: data.SaveData, parent=None):
        self.init_data = data.InitData()
        self.save_data = save_data
        self.parent = parent

        self.window = QtWidgets.QDialog(self.parent)
        self.cmd_mr_lbl = QtWidgets.QLabel(self.init_data.get_run('cmd_lbl_main').format(cmd=""))
        self.cmd_sr_lbl = QtWidgets.QLabel(self.init_data.get_run('cmd_lbl_second').format(cmd=""))
        self.time_lbl = QtWidgets.QLabel(self.init_data.get_run('time_lbl').format(time=-2.))
        self.layout = QtWidgets.QVBoxLayout()

        self.init_window()

    def init_window(self):
        self.parent.properties_dock.setWidget(self.window)
        self.parent.properties_dock.setWindowTitle(self.init_data.get_run('window_title'))

        self.layout.addWidget(self.time_lbl)
        self.layout.addWidget(self.cmd_mr_lbl)
        self.layout.addWidget(self.cmd_sr_lbl)

        self.window.setLayout(self.layout)
        self.window.show()

    def set_time(self, set_time: float):
        self.time_lbl.setText(self.init_data.get_run('time_lbl').format(
            time=round(set_time, self.init_data.get_run('accuracy_timer'))))

    def set_mr_command(self, command: str):
        self.cmd_mr_lbl.setText(self.init_data.get_run('cmd_lbl_main').format(cmd=command))

    def set_sr_command(self, command: str):
        self.cmd_sr_lbl.setText(self.init_data.get_run('cmd_lbl_second').format(cmd=command))
