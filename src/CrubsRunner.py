# !/usr/bin/env python3
# -*- coding: utf-8 -*-
# Created by Axel Tremaudant on 07/06/2022

"""
Fichier de lancement de l'application CrubsRunner.
"""

import sys
import os
from platform import system
from pathlib import Path
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QIcon

path = Path(__file__).parent.resolve()
os.chdir(path)
if os.getcwd() not in sys.path:  # /.../CrubsRunner/src
    sys.path.append(os.getcwd())

os.chdir('../')
if os.getcwd() not in sys.path:  # /.../CrubsRunner
    sys.path.append(os.getcwd())

if system() == "Linux":
    sys.path.append("/home/{user}/.CrubsRunner/".format(user=str(path).split('/')[1]))

from src import data
from src import ui


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
    app = QApplication(sys.argv)
    init_data = data.Init()
    set_app(app)

    init_data.get_window('window_title')
    window = ui.MainWindow()  # Cree la fenetre
    window.resize(init_data.get_window('window_start_width'), init_data.get_window('window_start_height'))
    window.show()

    sys.exit(app.exec())


if __name__ == '__main__':
    main()
