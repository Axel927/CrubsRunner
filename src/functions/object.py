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
Fichier contenant des fonctions concernant les objets 3D.
"""

from PyQt5 import QtWidgets
import numpy as np
import pyqtgraph.opengl as gl
from PIL import Image
import fitz  # PyMuPDF
import trimesh
from sys import path

from src import element
from src import data


def make_mesh(elem: gl.GLMeshItem, points: np.array, faces: np.array):
    """
    Fonction qui cree un maillage a partir des points et des faces et l'enregistre dans elem.
    :param elem: gl.GLMeshItem: Element dans lequel enregistrer le maillage
    :param points: np.array: Tableau des points
    :param faces: np.array: Tableau des faces
    :return: None
    """
    # Obtention des dimensions
    min_coord = np.amin(points, 0)  # Minimum selon chaque axe
    max_coord = np.amax(points, 0)  # Maximum selon chaque axe
    dim = max_coord - min_coord  # Calcul des dimensions dans tous les axes
    min_max = np.ravel([min_coord, max_coord])  # Aligne les coordonnees

    if np.amax(dim, 0) < 1.:  # Si les dimensions sont inferieures a 1 mm
        try:
            init_data = data.Init()
            dim *= init_data.get_main_robot('invisible_coef')  # On augmente les dimensions
            min_max *= init_data.get_main_robot('invisible_coef')
            points *= init_data.get_main_robot('invisible_coef')
        except AttributeError:
            pass
    try:
        elem.set_dimensions(dim)
        elem.set_min_max(min_max.reshape((3, 2), order='F'))
    except AttributeError:
        pass

    elem.setMeshData(meshdata=gl.MeshData(vertexes=points, faces=faces))


def show_mesh(elem: gl.GLMeshItem) -> bool:
    """
    Fonction pour ouvrir un fichier 3D. elem est modifie durant la fonction.
    Temps d'execution : stl < obj < 3mf
    :param elem: gl.GLMeshItem: Element a afficher.
    :return: bool: True si tout s'est bien passe, False sinon
    """
    if elem.get_file() == "":
        return False

    init_data = data.Init()
    try:
        if '.' + elem.get_file().split('.')[-1] in init_data.get_extension('3d_file'):
            if elem.get_element_type() == 'coord_sys':
                mesh = None
                for p in path:
                    # noinspection PyBroadException
                    try:
                        mesh = trimesh.load(p + '/' + elem.get_file(), force='mesh')
                        break
                    except:  # C'est un peu sale mais erreur inconnue en executable
                        continue

                if not mesh:
                    return False
            else:
                mesh = trimesh.load(elem.get_file(), force='mesh')

        else:
            QtWidgets.QMessageBox(init_data.get_window('error_format_file_type'),
                                  init_data.get_window('error_format_file_title'),
                                  init_data.get_window('error_format_file_message').format(
                                      filename=elem.get_file())).exec()
            return False
    except (FileNotFoundError, ValueError):
        QtWidgets.QMessageBox(init_data.get_window('error_open_file_type'),
                              init_data.get_window('error_open_file_title'),
                              init_data.get_window('error_open_file_message').format(
                                  filename=elem.get_file())).exec()
        return False

    make_mesh(elem, mesh.vertices, mesh.faces)
    return True


def show_vinyl(vinyl: element.Vinyl) -> bool:
    """
    Fonction pour ouvrir un tapis. vinyl est modifie durant la fonction.
    :param vinyl: widget.ImageItem: Tapis
    :return: bool: Renvoie True si tout s'est bien passe, False sinon
    """
    if vinyl.get_file() == "":
        return False

    init_data = data.Init()

    try:
        if '.' + vinyl.get_file().split('.')[-1] in init_data.get_extension('vinyl'):
            if vinyl.get_file().split('.')[-1] == 'pdf':
                vinyl.set_array(load_pdf(vinyl.get_file()))
            else:
                vinyl.set_array(np.array(Image.open(vinyl.get_file())))
        else:
            QtWidgets.QMessageBox(init_data.get_window('error_format_file_type'),
                                  init_data.get_window('error_format_file_title'),
                                  init_data.get_window('error_format_file_message').format(
                                      filename=vinyl.get_file())).exec()
            return False
    except FileNotFoundError:
        QtWidgets.QMessageBox(init_data.get_window('error_open_file_type'),
                              init_data.get_window('error_open_file_title'),
                              init_data.get_window('error_open_file_message').format(
                                  filename=vinyl.get_file())).exec()
        return False

    width = init_data.get_grid('width')  # Longueur du plateau
    # Met a la bonne taille
    vinyl.scale(width / vinyl.get_pixel_width(), width / vinyl.get_pixel_width(), width / vinyl.get_pixel_width())

    # Et le place correctement
    vinyl.rotate(90, 0, 0, 1)
    vinyl.rotate(180, 1, 0, 0)
    vinyl.translate(width / 2, init_data.get_grid('height') / 2, 0)
    return True


def load_pdf(file: str) -> np.array:
    """
    Charge une image pdf et renvoie un tableau numpy 3D.
    :param file: str: Chemin du fichier
    :return: np.array: Tableau 3D
    """
    pdf = fitz.open(file)
    pix = pdf.get_page_pixmap(0)  # Conversion en pixmap
    if pix.alpha:  # S'il y a un canal alpha
        return np.array(Image.frombytes("RGBA", (pix.width, pix.height), bytes(pix.samples_mv)))
    else:
        return np.array(Image.frombytes("RGB", (pix.width, pix.height), bytes(pix.samples_mv)))
