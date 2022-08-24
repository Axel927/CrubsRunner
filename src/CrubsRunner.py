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
Fichier de lancement de l'application CrubsRunner.
> python3 CrubsRunner.py
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
