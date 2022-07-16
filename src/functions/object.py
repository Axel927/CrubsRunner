# !/usr/bin/env python3
# -*- coding: utf-8 -*-
# Created by Axel Tremaudant on 11/07/2022

"""
Fichier contenant des fonctions concernant les objets 3D.
"""

from stl import mesh
from PySide6 import QtWidgets
from sys import float_info
import numpy as np
import pyqtgraph.opengl as gl
from PIL import Image

import element
import data


def show_stl(elem: element.CoordSys):
    """
    Fonction pour ouvrir un fichier stl. elem est modifie durant la fonction.
    :param elem: element.CoordSys: Element a afficher.
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
    meshdata = gl.MeshData(vertexes=points, faces=faces)

    elem.setMeshData(meshdata=meshdata)

    # Obtention des dimensions
    min_coord = [float_info.max] * 3  # 1.7976931348623157e+308
    max_coord = [float_info.min] * 3  # 2.2250738585072014e-308
    for point in points:
        for i in range(len(point)):
            min_coord[i] = min(min_coord[i], point[i])
            max_coord[i] = max(max_coord[i], point[i])

    dim = list()
    min_max = list()
    for i in range(len(min_coord)):
        dim.append(max_coord[i] - min_coord[i])
        min_max.append([min_coord[i], max_coord[i]])

    if max(dim) < 1.:  # Si les dimensions sont inferieures a 1 mm
        try:
            elem.set_invisible(True)
            for i in range(len(dim)):
                dim[i] *= init_data.get_main_robot('invisible_coef')  # On augmente les dimensions
                for j in range(len(min_max[i])):
                    min_max[i][j] *= init_data.get_main_robot('invisible_coef')
        except AttributeError:
            pass

    elem.set_dimensions(dim)
    elem.set_min_max(min_max)


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
