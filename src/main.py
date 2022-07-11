# !/usr/bin/env python3
# -*- coding: utf-8 -*-
# Created by Axel Tremaudant on 07/06/2022

"""
Fichier de lancement de l'application CrubsRunner.
"""

import sys
import os
from PySide6.QtWidgets import QApplication

import ui
import data

if os.getcwd().split('/')[-1] == 'src':
    os.chdir('../')  # Set the directory CrubsRunner as the current working directory
    if os.getcwd() not in sys.path:
        sys.path.append(os.getcwd())

if __name__ == '__main__':
    app = QApplication()
    init_data = data.Init()

    window = ui.MainWindow()  # Cree la fenetre
    window.resize(init_data.get_window('window_start_width'), init_data.get_window('window_start_height'))
    window.show()

    sys.exit(app.exec())
