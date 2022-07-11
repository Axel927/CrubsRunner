# !/usr/bin/env python3
# -*- coding: utf-8 -*-
# Created by Axel Tremaudant on 08/07/2022

"""
Fichier contenant la class Board, partie interface graphique.
"""

from PySide6 import QtWidgets, QtGui
from time import time
import data


class Board:
    """
    Classe qui gere la partie graphique du plateau.
    """
    def __init__(self, parent, save_data: data.Save, board):
        """
        Constructeur de Board.
        :param parent: ui.MainWindow: Fenetre principale
        :param save_data: data.Save: Donnees de sauvegarde
        :param board: element.Board: Plateau
        """
        self.parent = parent
        self.init_data = data.Init()
        self.save_data = save_data
        self.board = board
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
        """
        Cree la fenetre des proprietes du plateau.
        :return: None
        """
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
        """
        Cree les connexions entre les widget et les slots.
        :return: None
        """
        self.color_btn.clicked.connect(self._color_board)
        self.edge_color_btn.clicked.connect(self._edge_color_board)
        self.close_btn.clicked.connect(self._close)
        self.reset_btn.clicked.connect(self.reset)
        self.remove_btn.clicked.connect(self._remove)

    def _color_board(self):
        """
        Slot qui gere la couleur du plateau.
        :return: None
        """
        if time() - self.time < 0.2:  # Evite de multiple apparitions de la fenetre
            return

        self.color_dialog.open()
        self.color_dialog.setWindowTitle(self.init_data.get_board('color_dialog_title'))

        color = self.save_data.get_board('color')
        self.color_dialog.setCurrentColor(QtGui.QColor.fromRgb(color[0], color[1], color[2], color[3]))

        color = self.color_dialog.getColor()

        self.save_data.set_board('color', (
            color.red() / 255, color.green() / 255, color.blue() / 255, 1.))
        self.board.setColor(self.save_data.get_board('color'))
        self.parent.status_bar.showMessage(self.init_data.get_window('color_status_message').format(r=color.red(),
                                                                                                    v=color.green(),
                                                                                                    b=color.blue()))
        self.color_dialog.close()
        self.time = time()

    def _edge_color_board(self):
        """
        Slot qui gere la couleur des arretes du plateau.
        :return: None
        """
        if time() - self.time < 0.2:  # Evite de multiple apparitions de la fenetre
            return

        self.color_dialog.open()
        self.color_dialog.setWindowTitle(self.init_data.get_board('edge_color_dialog_title'))

        color = self.save_data.get_board('edge_color')
        self.color_dialog.setCurrentColor(QtGui.QColor.fromRgb(color[0], color[1], color[2], color[3]))
        self.color_dialog.setVisible(True)

        color = self.color_dialog.getColor()

        self.save_data.set_board('edge_color', (
            color.red() / 255, color.green() / 255, color.blue() / 255, 1.))
        self.board.set_edge_color(self.save_data.get_board('edge_color'))
        self.parent.status_bar.showMessage(self.init_data.get_window('color_status_message').format(r=color.red(),
                                                                                                    v=color.green(),
                                                                                                    b=color.blue()))
        self.color_dialog.setVisible(False)
        self.color_dialog.close()
        self.time = time()

    def _close(self):
        """
        Slot qui ferme la fenetre.
        :return: None
        """
        self.window.close()

    def reset(self):
        """
        Remet le plateau selon la configuration initiale.
        :return: None
        """
        self.board.setColor(self.init_data.get_board('color'))
        self.board.set_edge_color(self.init_data.get_board('edge_color'))
        self.window.close()

    def remove(self, message=True):
        """
        Retire le plateau de la fenetre.
        :param message: bool: Si True, affiche un message pour confirmer la suppression.
        :return: None
        """
        if self.parent.list_widget.get_len() < 2:  # Evite un bug qui fait que ca retire trop d'elements
            return

        if message:
            ans = QtWidgets.QMessageBox(self.init_data.get_board('remove_message_box_type'),
                                        self.init_data.get_board('remove_message_box_title'),
                                        self.init_data.get_board('remove_message_box_message'),
                                        self.init_data.get_board('remove_message_box_buttons')).exec()

            if ans == QtWidgets.QMessageBox.No:
                return
        for i in range(self.parent.list_widget.get_len()):
            # Si c'est l'element dans le list widget
            if self.board.get_name() == self.parent.list_widget.get_contents()[i].get_name():
                self.parent.list_widget.remove_content(i)
                break

        self.board.set_file("")
        self.save_data.set_board('file', '')
        self.reset()
        self.board.setVisible(False)
        del self

    def _remove(self):
        """
        Slot pour supprimer le plateau.
        :return: None
        """
        self.remove(True)
