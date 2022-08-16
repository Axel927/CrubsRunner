# !/usr/bin/env python3
# -*- coding: utf-8 -*-
# Created by Axel Tremaudant on 07/07/2022

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
