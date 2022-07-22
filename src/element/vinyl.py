# !/usr/bin/env python3
# -*- coding: utf-8 -*-
# Created by Axel Tremaudant on 13/07/2022

"""
Fichier contenant la classe ImageItem.
"""
import numpy as np
import pyqtgraph.opengl as gl
from PySide6 import QtWidgets

import data
import functions.object


class Vinyl(gl.GLImageItem):
    """
    Classe concernant le tapis du plateau.
    """

    def __init__(self, parent, save_data: data.Save, array=None, file=""):
        """
        Constructeur de ImageItem.
        :param parent: ui.MainWindow: Fenetre principale
        :param save_data: data.Save: Donnees de sauvegarde
        :param array: numpy.array: Tableau 3D
        :param file: str: Nom du fichier
        """
        super(Vinyl, self).__init__(array)

        self.pixel_height = len(array) if array is not None else 0
        self.pixel_width = len(array[0]) if array is not None else 0
        self.file = file
        self.save_data = save_data
        self.parent = parent
        self.name = "Tapis"
        self.save_data.set_vinyl('file', self.file)
        self.save_data.set_vinyl('pixel_height', self.pixel_height)
        self.save_data.set_vinyl('pixel_width', self.pixel_width)

    def get_pixel_height(self) -> int:
        """
        Renvoie le nombre de pixels en hauteur.
        :return: int: nombre de pixels
        """
        return self.pixel_height

    def get_pixel_width(self) -> int:
        """
        Renvoie le nombre de pixels en largeur.
        :return: int: nombre de pixels
        """
        return self.pixel_width

    def set_file(self, file: str):
        """
        Definit le fichier du tapis.
        :param file: str: Nom du fichier.
        :return: None
        """
        self.file = file
        self.save_data.set_vinyl('file', self.file)

    def get_file(self) -> str:
        """
        Renvoie le fichier du tapis.
        :return: str: Fichier
        """
        return self.file

    def set_array(self, array: np.array):
        """
        Definit le tableau de donnees s'il n'a pas ete definit auparavant. Sinon ne fait rien.
        :param array: numpy.array: Tableau 3D
        :return: None
        """
        if array.shape[2] == 3:  # Si pas de canal alpha, on l'ajoute et l'initialise a 255
            array = np.concatenate((array, np.full((array.shape[0], array.shape[1], 1), 255)), axis=2)

        self.setData(array)
        self.pixel_height = len(array)
        self.pixel_width = len(array[0])
        self.save_data.set_vinyl('pixel_height', self.pixel_height)
        self.save_data.set_vinyl('pixel_width', self.pixel_width)

    def get_name(self) -> str:
        """
        Renvoie le nom a afficher.
        :return: str: Nom
        """
        return self.name

    def update_(self):
        """
        Met le tapis a jour.
        :return: None
        """
        if self.file == '':
            self.file = self.save_data.get_vinyl('file')
            functions.object.show_vinyl(self)
        if self.file == "":
            for i in range(self.parent.list_widget.get_len()):
                # Si c'est l'element dans le list widget
                if self.get_name() == self.parent.list_widget.get_contents()[i].get_name():
                    self.parent.list_widget.remove_content(i)
                    break

    def properties(self):
        """
        Retire le tapis de la fenetre.
        :return: None
        """
        if self.parent.list_widget.get_len() < 2:  # Evite un bug qui fait que ca retire trop d'elements
            return

        init_data = data.Init()
        ans = QtWidgets.QMessageBox(init_data.get_vinyl('remove_message_box_type'),
                                    init_data.get_vinyl('remove_message_box_title'),
                                    init_data.get_vinyl('remove_message_box_message'),
                                    init_data.get_vinyl('remove_message_box_buttons')).exec()

        if ans == QtWidgets.QMessageBox.No:
            return

        for i in range(self.parent.list_widget.get_len()):
            # Si c'est l'element dans le list widget
            if self.get_name() == self.parent.list_widget.get_contents()[i].get_name():
                self.parent.list_widget.remove_content(i)
                break

        self.set_file("")
        self.save_data.set_vinyl('file', '')
        self.setVisible(False)
