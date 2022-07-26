# !/usr/bin/env python3
# -*- coding: utf-8 -*-
# Created by Axel Tremaudant on 07/07/2022

"""
Fichier contenant la classe CoordSys.
"""

import pyqtgraph.opengl as gl
import numpy as np


class CoordSys(gl.GLMeshItem):
    """
    Classe qui gere la partie systeme de coordonnees
    """
    def __init__(self, save_data):
        """
        Constructeur de CoordSys.
        :param save_data: data.Save: Les donnees de sauvegarde y sont recuperees et ecrites
        """
        super(CoordSys, self).__init__(smooth=True, drawFaces=True, drawEdges=True)
        self.save_data = save_data
        self.init_data = self.save_data.get_init_data()
        self.file = ""
        self.name = ""
        self.element_type = ""
        self.dimensions = np.zeros(shape=3, dtype="float")
        self.min_max = np.zeros(shape=(3, 2), dtype="float")

    def set_file(self, file: str):
        """
        Definit le fichier 3D de l'element.
        :param file: str: Nouveau fichier
        :return: None
        """
        self.file = file

    def get_file(self) -> str:
        """
        Renvoie le fichier 3D de l'element.
        :return: str: Fichier
        """
        return self.file

    def get_dimensions(self) -> np.array:
        """
        Renvoie les dimensions de l'objet.
        :return: np.array: Dimensions [x, y, z] contient des flottants
        """
        return self.dimensions

    def set_dimensions(self, dimensions: np.array):
        """
        Definit les dimensions de l'objet.
        :param dimensions:  np.array: Dimensions [x, y, z] contient des flottants
        :return: None
        """
        self.dimensions = dimensions

    def get_min_max(self) -> np.array:
        """
        Renvoie les coordonnees minimales et maximales de l'objet selon chaque axe.
        :return: np.array: [[min x, max x], [min y, max y], [min z, max z]] contient des flottants
        """
        return self.min_max

    def set_min_max(self, min_max: np.array):
        """
        Definit les coordonnees minimales et maximales de l'objet selon chaque axe
        :param min_max: np.array: [[min x, max x], [min y, max y], [min z, max z]] contient des flottants
        :return: None
        """
        self.min_max = min_max

    def set_name(self, name: str):
        """
        Definit le nom de l'objet
        :param name: str: Nom
        :return: None
        """
        self.name = name

    def get_name(self) -> str:
        """
        Renvoie le nom de l'objet.
        :return: str: Nom
        """
        return self.name

    def set_edge_color(self, color: tuple):
        """
        Definit les couleurs des bords de l'objet.
        :param color: tuple: (r, v, b) entre 0 et 1
        :return: None
        """
        self.opts['edgeColor'] = color
        self.update()

    def get_element_type(self) -> str:
        """
        Renvoie le type de l'objet.
        :return: str: Type
        """
        return self.element_type

    def set_element_type(self, element_type: str):
        """
        Definit le type de l'objet
        :param element_type: str: Type
        :return: None
        """
        self.element_type = element_type

    def update_(self):
        """
        Met a jour l'objet.
        :return: None
        """
        self.setVisible(self.save_data.get_grid('coord_sys_visible'))
