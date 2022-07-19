# !/usr/bin/env python3
# -*- coding: utf-8 -*-
# Created by Axel Tremaudant on 11/07/2022

"""
Fichier contenant des fonctions concernant les objets 3D.
"""

from stl import mesh
from PySide6 import QtWidgets
import numpy as np
import pyqtgraph.opengl as gl
from PIL import Image

import element
import data

# stl plus rapide que obj


def make_mesh(elem: gl.GLMeshItem, points: np.array, faces: np.array):
    """
    Fonction qui cree un maillage a partir des points et des faces et l'enregistre dans elem.
    :param elem: gl.GLMeshItem: Element dans lequel enregistrer le maillage
    :param points: np.array: Tableau des points
    :param faces: np.array: Tableau des faces
    :return: None
    """
    init_data = data.Init()
    meshdata = gl.MeshData(vertexes=points, faces=faces)

    elem.setMeshData(meshdata=meshdata)

    # Obtention des dimensions
    min_coord = np.amin(points, 0)
    max_coord = np.amax(points, 0)
    dim = max_coord - min_coord
    min_max = np.ravel([min_coord, max_coord])

    if np.amax(dim, 0) < 1.:  # Si les dimensions sont inferieures a 1 mm
        try:
            elem.set_invisible(True)
            dim *= init_data.get_main_robot('invisible_coef')  # On augmente les dimensions
            min_max *= init_data.get_main_robot('invisible_coef')
        except AttributeError:
            pass
    try:
        elem.set_dimensions(dim)
        elem.set_min_max(np.reshape(min_max, (3, 2), order='F'))
    except AttributeError:
        pass


def show_obj(elem: gl.GLMeshItem):
    """
    Fonction pour charger un fichier .obj.
    :param elem: gl.GLMeshItem: Element
    :return: None
    """
    if elem.get_file() == "":
        return

    init_data = data.Init()
    try:
        with open(elem.get_file(), 'r') as file:
            facets = list()
            points = list()
            for line in file:
                if line[:2] == 'v ':
                    facets.append([float(point) for point in line[2:].split()])
                elif line[:2] == 'f ':
                    point = list()
                    for i in line[2:].split():
                        point.append(facets[int(i.split("/")[0]) - 1])
                    points.append(point)
    except FileNotFoundError:
        QtWidgets.QMessageBox(init_data.get_window('error_open_file_type'),
                              init_data.get_window('error_open_file_title'),
                              init_data.get_window('error_open_file_message').format(
                                  filename=elem.get_file())).exec()
        return

    points = np.array(points).reshape(-1, 3)
    faces = np.arange(points.shape[0]).reshape(-1, 3)  # Creation des faces
    make_mesh(elem, points, faces)


def show_stl(elem: gl.GLMeshItem):
    """
    Fonction pour ouvrir un fichier stl. elem est modifie durant la fonction.
    :param elem: gl.GLMeshItem: Element a afficher.
    :return: None
    """
    if elem.get_file() == "":
        return

    init_data = data.Init()

    try:
        points = mesh.Mesh.from_file(elem.get_file()).points.reshape(-1, 3)  # Recuperation des points
    except FileNotFoundError:
        QtWidgets.QMessageBox(init_data.get_window('error_open_file_type'),
                              init_data.get_window('error_open_file_title'),
                              init_data.get_window('error_open_file_message').format(
                                  filename=elem.get_file())).exec()
        return

    faces = np.arange(points.shape[0]).reshape(-1, 3)  # Creation des faces
    make_mesh(elem, points, faces)


def show_vinyl(vinyl: element.Vinyl):
    """
    Fonction pour ouvrir un tapis. vinyl est modifie durant la fonction.
    :param vinyl: widget.ImageItem: Tapis
    :return: None
    """
    if vinyl.get_file() == "":
        return

    init_data = data.Init()
    width = init_data.get_grid('width')  # Longueur du plateau

    try:
        vinyl.set_array(np.array(Image.open(vinyl.get_file())))
    except FileNotFoundError:
        QtWidgets.QMessageBox(init_data.get_window('error_open_file_type'),
                              init_data.get_window('error_open_file_title'),
                              init_data.get_window('error_open_file_message').format(
                                  filename=vinyl.get_file())).exec()
        return

    # Met a la bonne taille
    vinyl.scale(width / vinyl.get_pixel_width(), width / vinyl.get_pixel_width(), width / vinyl.get_pixel_width())

    # Et le place correctement
    vinyl.rotate(90, 0, 0, 1)
    vinyl.rotate(180, 1, 0, 0)
    vinyl.translate(width / 2, init_data.get_grid('height') / 2, 0)
