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
Fichier contenant la classe Run, partie graphique.
"""

from PyQt5 import QtWidgets
from src import data


# Note : mr mean main robot and sr mean second robot


class Run:
    """
    Classe qui gere la partie graphique de la simulation.
    """

    def __init__(self, parent=None):
        """
        Constructeur de Run.
        :param parent: ui.MainWindow: Fenetre principale
        """
        self.init_data = data.Init()
        self.parent = parent

        self.window = QtWidgets.QDialog(self.parent)
        self.cmd_mr_lbl = QtWidgets.QLabel(self.init_data.get_run('cmd_lbl_main').format(cmd=""))
        self.cmd_sr_lbl = QtWidgets.QLabel(self.init_data.get_run('cmd_lbl_second').format(cmd=""))
        self.time_lbl = QtWidgets.QLabel(self.init_data.get_run('time_lbl').format(time=-2.))
        self.theoretical_time = QtWidgets.QLabel(self.init_data.get_run('theoretical_time_lbl').format(time=0.))
        self.layout = QtWidgets.QVBoxLayout()

        self.init_window()

    def init_window(self):
        """
        Cree la fenetre.
        :return: None
        """
        self.parent.properties_dock.setWidget(self.window)
        self.parent.properties_dock.setWindowTitle(self.init_data.get_run('window_title'))

        self.layout.addWidget(self.time_lbl)
        self.layout.addWidget(self.theoretical_time)
        self.layout.addWidget(self.cmd_mr_lbl)
        self.layout.addWidget(self.cmd_sr_lbl)

        self.window.setLayout(self.layout)
        self.window.show()

    def set_time(self, set_time: float):
        """
        Affiche la valeur du chrono.
        :param set_time: float: Valeur a afficher
        :return: None
        """
        self.time_lbl.setText(self.init_data.get_run('time_lbl').format(
            time=round(set_time, self.init_data.get_run('accuracy_timer'))))

    def set_theoretical_time(self, time: float):
        """
        Affiche le temps theorique de la simulation.
        :param time: float: Temps a afficher
        :return: None
        """
        self.theoretical_time.setText(self.init_data.get_run('theoretical_time_lbl').format(
            time=round(time, self.init_data.get_run('theoretical_time_accuracy'))))

    def set_mr_command(self, command: str):
        """
        Definit la commande du robot principal a afficher.
        :param command: str: Commande a afficher
        :return: None
        """
        self.cmd_mr_lbl.setText(self.init_data.get_run('cmd_lbl_main').format(cmd=command))

    def set_sr_command(self, command: str):
        """
        Definit la commande du robot secondaire a afficher.
        :param command: str: Commande a afficher
        :return: None
        """
        self.cmd_sr_lbl.setText(self.init_data.get_run('cmd_lbl_second').format(cmd=command))
