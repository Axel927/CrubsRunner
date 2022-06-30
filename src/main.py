# !/usr/bin/env python3
# -*- coding: utf-8 -*-
# Created by Axel Tremaudant on 07/06/2022

import sys
import os
from PySide6.QtWidgets import QApplication

import mainWindow
from data import InitData

if os.getcwd().split('/')[-1] == 'src':
    os.chdir('../')  # Set the directory CrubsRunner as the current working directory
    if os.getcwd() not in sys.path:
        sys.path.append(os.getcwd())

if __name__ == '__main__':
    app = QApplication()
    init_data = InitData()

    window = mainWindow.MainWindow()
    window.resize(init_data.get_window('window_start_width'), init_data.get_window('window_start_height'))
    window.show()

    sys.exit(app.exec())
