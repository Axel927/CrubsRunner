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
Fichier contenant la classe ImageItem.
"""
import numpy as np
from time import time
import pyqtgraph.opengl as gl
from PyQt5 import QtWidgets

from src import functions


class Vinyl(gl.GLImageItem):
    """
    Classe concernant le tapis du plateau.
    """

    def __init__(self, parent, save_data, array=None, file=""):
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
        self.time = 0.
        self.setVisible(False)

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
        self.setVisible(True)

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
            if not functions.object.show_mesh(self):
                self.file = ''

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
        if time() - self.time < 0.2:
            return

        init_data = self.save_data.get_init_data()
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
        self.time = time()
