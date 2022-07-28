# !/usr/bin/env python3
# -*- coding: utf-8 -*-
# Created by Axel Tremaudant on 07/06/2022

"""
Fichier de lancement de l'application CrubsRunner.
"""

import sys
import os
from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QIcon

import data
import ui

if os.getcwd().split('/')[-1] == 'src':
    os.chdir('../')  # Set the directory CrubsRunner as the current working directory
    if os.getcwd() not in sys.path:
        sys.path.append(os.getcwd())


def set_app(application: QApplication):
    """
    Definit des parametres de l'application.
    :param application: QApplication: Application
    :return: None
    """
    init = data.Init()

    application.setWindowIcon(QIcon(init.get_window('app_icon')))
    application.setApplicationName(init.get_window('app_title'))
    application.setDesktopFileName(init.get_window('app_title'))
    application.setObjectName(init.get_window('app_title'))
    application.setOrganizationName(init.get_window('organisation_name'))


def main():
    """
    Fonction principale qui lance l'application.
    :return: None
    """
    app = QApplication()
    init_data = data.Init()
    set_app(app)

    init_data.get_window('window_title')
    window = ui.MainWindow()  # Cree la fenetre
    window.resize(init_data.get_window('window_start_width'), init_data.get_window('window_start_height'))
    window.show()

    sys.exit(app.exec())


if __name__ == '__main__':
    main()
