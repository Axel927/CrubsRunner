# !/usr/bin/env python3
# -*- coding: utf-8 -*-
# Created by Axel Tremaudant on 07/06/2022

"""
Fichier qui contient la classe GridItem.
"""

import pyqtgraph.opengl as gl
from PySide6 import QtGui, QtWidgets
from time import time
import data


class GridItem(gl.GLGridItem):
    """
    Classe qui s'occupe de la grille dans le widget central et de ses parametres.
    """
    def __init__(self, save_data: data.Save, parent):
        """
        Constructeur de GridItem.
        :param save_data: data.Save: Donnees de sauvegarde
        :param parent: ui.MainWindow: Fenetre principale
        """
        super(GridItem, self).__init__()
        self.save_data = save_data
        self.init_data = data.Init()
        self.parent = parent
        self.time = 0.

        self.window = QtWidgets.QDialog(self.parent)
        self.viewer = gl.GLViewWidget()
        self.cb_see_grid = QtWidgets.QCheckBox(self.init_data.get_grid('see_name'))
        self.width_grid_label = QtWidgets.QLabel(self.init_data.get_grid('width_name'))
        self.width_grid_sb = QtWidgets.QSpinBox()
        self.height_grid_label = QtWidgets.QLabel(self.init_data.get_grid('height_name'))
        self.height_grid_sb = QtWidgets.QSpinBox()
        self.color_grid_btn = QtWidgets.QPushButton(self.init_data.get_grid('color_name'))
        self.color_dialog = QtWidgets.QColorDialog()
        self.transparency_grid_label = QtWidgets.QLabel(self.init_data.get_grid('transparency_name'))
        self.transparency_grid_sb = QtWidgets.QSpinBox()
        self.coord_sys_cb = QtWidgets.QCheckBox(self.init_data.get_grid('coord_sys_name'))
        self.close_btn = QtWidgets.QPushButton(self.init_data.get_grid('close_name'))
        self.reset_btn = QtWidgets.QPushButton(self.init_data.get_grid('reset_name'))
        self.grid_layout = QtWidgets.QGridLayout()
        self.group_box = QtWidgets.QGroupBox(self.init_data.get_grid('element_name'), self.window)
        self.window_layout = QtWidgets.QGridLayout(self.window)

    def properties(self):
        """
        Cree la fenetre des proprietes
        :return: None
        """
        self.parent.properties_dock.setWidget(self.window)
        self.parent.properties_dock.setWindowTitle(self.init_data.get_grid('window_name'))

        self.cb_see_grid.setChecked(self.visible())

        self.width_grid_sb.setParent(self.window)
        self.width_grid_sb.setMinimum(self.init_data.get_grid('width_min'))
        self.width_grid_sb.setMaximum(self.init_data.get_grid('width_max'))
        self.width_grid_sb.setValue(self.save_data.get_grid('width'))

        self.height_grid_sb.setMinimum(self.init_data.get_grid('height_min'))
        self.height_grid_sb.setMaximum(self.init_data.get_grid('height_max'))
        self.height_grid_sb.setValue(self.save_data.get_grid('height'))

        self.color_grid_btn.setCursor(self.init_data.get_grid('color_cursor'))
        self.color_grid_btn.setDefault(self.init_data.get_grid('color_default'))
        self.color_dialog.setParent(self.window)
        self.color_dialog.setVisible(False)

        self.transparency_grid_sb.setMaximum(255)
        self.transparency_grid_sb.setMinimum(0)
        self.transparency_grid_sb.setValue(self.save_data.get_grid('transparency'))

        self.grid_layout.addWidget(self.cb_see_grid, 0, 0)
        self.grid_layout.addWidget(self.width_grid_label, 1, 1)
        self.grid_layout.addWidget(self.width_grid_sb, 1, 2)
        self.grid_layout.addWidget(self.height_grid_label, 2, 1)
        self.grid_layout.addWidget(self.height_grid_sb, 2, 2)
        self.grid_layout.addWidget(self.color_grid_btn, 3, 1)
        self.grid_layout.addWidget(self.transparency_grid_label, 4, 1)
        self.grid_layout.addWidget(self.transparency_grid_sb, 4, 2)

        self.group_box.setLayout(self.grid_layout)

        self.coord_sys_cb.setChecked(self.save_data.get_grid('coord_sys_visible'))

        self.close_btn.setParent(self.window)
        self.close_btn.setDefault(self.init_data.get_grid('close_default'))
        self.close_btn.setCursor(self.init_data.get_grid('close_cursor'))
        self.reset_btn.setParent(self.window)
        self.reset_btn.setCursor(self.init_data.get_grid('reset_cursor'))
        self.reset_btn.setDefault(self.init_data.get_grid('reset_default'))

        self.window_layout.addWidget(self.group_box, 0, 0)
        self.window_layout.addWidget(self.coord_sys_cb, 1, 0)
        self.window_layout.addWidget(self.close_btn, 2, 0)
        self.window_layout.addWidget(self.reset_btn, 3, 0)

        self._connections()
        self.window.show()

    def _connections(self):
        """
        Cree les connexions entre les widgets et les slots.
        :return: None
        """
        self.cb_see_grid.stateChanged.connect(self._see_grid)
        self.height_grid_sb.valueChanged.connect(self._height_grid)
        self.width_grid_sb.valueChanged.connect(self._width_grid)
        self.color_grid_btn.clicked.connect(self._color_grid)
        self.close_btn.clicked.connect(self._close_window)
        self.reset_btn.clicked.connect(self.reset)
        self.transparency_grid_sb.valueChanged.connect(self._transparency_grid)
        self.coord_sys_cb.stateChanged.connect(self._see_coord_sys)

    def _see_grid(self):
        """
        Slot pour afficher ou non la grille.
        :return: None
        """
        if self.cb_see_grid.isChecked():
            self.setVisible(True)
            self.height_grid_sb.setVisible(True)
            self.width_grid_sb.setVisible(True)
            self.height_grid_label.setVisible(True)
            self.width_grid_label.setVisible(True)
            self.color_grid_btn.setVisible(True)
            self.transparency_grid_label.setVisible(True)
            self.transparency_grid_sb.setVisible(True)
            self.save_data.set_grid('visible', True)
        else:
            self.setVisible(False)
            self.width_grid_sb.setVisible(False)
            self.height_grid_sb.setVisible(False)
            self.width_grid_label.setVisible(False)
            self.height_grid_label.setVisible(False)
            self.color_grid_btn.setVisible(False)
            self.transparency_grid_label.setVisible(False)
            self.transparency_grid_sb.setVisible(False)
            self.save_data.set_grid('visible', False)

    def _see_coord_sys(self):
        """
        Slot pour voir ou non le systeme de coordonnees.
        :return: None
        """
        if self.coord_sys_cb.isChecked():
            self.save_data.set_grid('coord_sys_visible', True)
            self.parent.x_coord_sys.setVisible(True)
            self.parent.y_coord_sys.setVisible(True)
            self.parent.z_coord_sys.setVisible(True)
        else:
            self.save_data.set_grid('coord_sys_visible', False)
            self.parent.x_coord_sys.setVisible(False)
            self.parent.y_coord_sys.setVisible(False)
            self.parent.z_coord_sys.setVisible(False)

    def _height_grid(self):
        """
        Slot pour mettre a jour la hauteur des carreaux.
        :return: None
        """
        self.save_data.set_grid('height', self.height_grid_sb.value())
        self.setSpacing(self.save_data.get_grid('width'), self.save_data.get_grid('height'))

    def _width_grid(self):
        """
        Slot pour mettre a jour la largeur des carreaux.
        :return: None
        """
        self.save_data.set_grid('width', self.width_grid_sb.value())
        self.setSpacing(self.save_data.get_grid('width'), self.save_data.get_grid('height'))

    def _color_grid(self):
        """
        slot pour modifier la couleur de la grille.
        :return: None
        """
        if time() - self.time < 0.2:  # Evite le bug de plusieurs apparitions
            return

        self.color_dialog.open()
        self.color_dialog.setWindowTitle(self.init_data.get_grid('color_dialog_name'))

        color = self.save_data.get_grid('color')
        self.color_dialog.setCurrentColor(QtGui.QColor.fromRgb(color[0], color[1], color[2], color[3]))

        color = self.color_dialog.getColor()

        self.setColor(color)
        self.save_data.set_grid('color', (self.color().red(),
                                          self.color().green(),
                                          self.color().blue(),
                                          self.transparency_grid_sb.value()
                                          ))
        self.parent.status_bar.showMessage(self.init_data.get_window('color_status_message').format(r=color.red(),
                                                                                                    v=color.green(),
                                                                                                    b=color.blue()))
        self.color_dialog.close()
        self.time = time()

    def _close_window(self):
        """
        Slot pour fermer la fenetre.
        :return: None
        """
        self.window.close()

    def reset(self):
        """
        Methode pour remettre la grille dans son etat initial.
        :return: None
        """
        self.setSpacing(self.init_data.get_grid('spacing_width'), self.init_data.get_grid('spacing_height'))
        self.setColor(self.init_data.get_grid('color'))
        self.setVisible(True)
        self.transparency_grid_sb.setValue(self.init_data.get_grid('transparency'))
        self.width_grid_sb.setValue(self.init_data.get_grid('spacing_width'))
        self.height_grid_sb.setValue(self.init_data.get_grid('spacing_height'))
        self.parent.status_bar.showMessage(
            self.init_data.get_window('color_status_message').format(r=self.init_data.get_grid('color')[0],
                                                                     v=self.init_data.get_grid('color')[1],
                                                                     b=self.init_data.get_grid('color')[2]))
        self.save_data.set_grid('color', self.init_data.get_grid('color'))
        self.save_data.set_grid('transparency', self.init_data.get_grid('transparency'))
        self.save_data.set_grid('height', self.init_data.get_grid('spacing_height'))
        self.save_data.set_grid('width', self.init_data.get_grid('spacing_width'))
        self.window.close()

        self.parent.x_coord_sys.setVisible(not self.init_data.get_view('color_sys_visible'))
        self.parent.y_coord_sys.setVisible(not self.init_data.get_view('color_sys_visible'))
        self.parent.z_coord_sys.setVisible(not self.init_data.get_view('color_sys_visible'))

    def _transparency_grid(self):
        """
        Slot pour changer la transparence de la grille.
        :return: None
        """
        self.save_data.set_grid('transparency', self.transparency_grid_sb.value())
        self.setColor(self.save_data.get_grid('color'))

    def update_(self):
        """
        Met la grille a jour.
        :return: None
        """
        self.setSpacing(self.save_data.get_grid('width'), self.save_data.get_grid('height'))
        self.setVisible(self.save_data.get_grid('visible'))
        self.setColor(self.save_data.get_grid('color'))

        self.parent.x_coord_sys.setVisible(self.save_data.get_grid('color_sys_visible'))
        self.parent.y_coord_sys.setVisible(self.save_data.get_grid('color_sys_visible'))
        self.parent.z_coord_sys.setVisible(self.save_data.get_grid('color_sys_visible'))

    def get_name(self) -> str:
        """
        Renvoie le nom de la grille.
        :return: str: Nom
        """
        return self.init_data.get_grid('element_name')
