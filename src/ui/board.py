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
Fichier contenant la class Board, partie interface graphique.
"""

from PyQt5 import QtWidgets, QtGui
from time import time
from platform import system


class Board:
    """
    Classe qui gere la partie graphique du plateau.
    """

    def __init__(self, parent, save_data, board):
        """
        Constructeur de Board.
        :param parent: ui.MainWindow: Fenetre principale
        :param save_data: data.Save: Donnees de sauvegarde
        :param board: element.Board: Plateau
        """
        self.parent = parent
        self.save_data = save_data
        self.init_data = self.save_data.get_init_data()
        self.board = board
        self.time = 0.
        self.window = QtWidgets.QDialog(self.parent)
        self.color_btn = QtWidgets.QPushButton(self.init_data.get_board('color_name'), self.window)
        self.color_dialog = QtWidgets.QColorDialog(self.window)
        self.edge_color_btn = QtWidgets.QPushButton(self.init_data.get_board('edge_color_name'), self.window)
        self.close_btn = QtWidgets.QPushButton(self.init_data.get_board('close_btn_name'), self.window)
        self.reset_btn = QtWidgets.QPushButton(self.init_data.get_board('reset_btn_name'), self.window)
        self.layout = QtWidgets.QVBoxLayout(self.window)
        self.remove_btn = QtWidgets.QPushButton(self.init_data.get_board('remove_btn_name'), self.window)
        self.angle_rotation_sb = QtWidgets.QSpinBox(self.window)

        self.axis_rotation_rb_x = QtWidgets.QRadioButton(self.init_data.get_board('axis_rotation_x_name'),
                                                         self.window)
        self.axis_rotation_rb_y = QtWidgets.QRadioButton(self.init_data.get_board('axis_rotation_y_name'),
                                                         self.window)
        self.axis_rotation_rb_z = QtWidgets.QRadioButton(self.init_data.get_board('axis_rotation_z_name'),
                                                         self.window)
        self.angle_lbl = QtWidgets.QLabel(self.init_data.get_board('angle_lbl_name'))
        self.axis_lbl = QtWidgets.QLabel(self.init_data.get_board('axis_lbl_name'))

        self.offset_sb = QtWidgets.QSpinBox(self.window)
        self.offset_lbl = QtWidgets.QLabel(self.init_data.get_board('offset_lbl_name'))

        self.axis_sb = {'x': QtWidgets.QSpinBox(self.window), 'y': QtWidgets.QSpinBox(self.window)}
        self.axis_sb_lbl = {'x': QtWidgets.QLabel('x'), 'y': QtWidgets.QLabel('y')}

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

        self.close_btn.setCursor(self.init_data.get_board('close_cursor'))
        self.close_btn.setDefault(self.init_data.get_board('close_default'))
        self.reset_btn.setCursor(self.init_data.get_board('reset_cursor'))
        self.reset_btn.setDefault(self.init_data.get_board('reset_default'))
        self.remove_btn.setCursor(self.init_data.get_board('remove_cursor'))
        self.remove_btn.setDefault(self.init_data.get_board('remove_default'))

        self.angle_rotation_sb.setMinimum(self.init_data.get_board('angle_rotation_min'))
        self.angle_rotation_sb.setMaximum(self.init_data.get_board('angle_rotation_max'))
        self.angle_rotation_sb.setValue(self.save_data.get_board('angle_rotation'))

        self.offset_sb.setMinimum(self.init_data.get_board('offset_sb_min'))
        self.offset_sb.setMaximum(self.init_data.get_board('offset_sb_max'))
        self.offset_sb.setValue(self.board.get_offset())

        for sb in self.axis_sb.keys():
            self.axis_sb.get(sb).setMinimum(self.init_data.get_board('offset_sb_min'))
            self.axis_sb.get(sb).setMaximum(self.init_data.get_board('offset_sb_max'))

        self.axis_sb.get('x').setValue(self.board.get_axis()[0])
        self.axis_sb.get('y').setValue(self.board.get_axis()[1])

        if self.save_data.get_board('axis_rotation') == 'x':
            self.axis_rotation_rb_x.setChecked(True)
            self.axis_rotation_rb_y.setChecked(False)
            self.axis_rotation_rb_z.setChecked(False)
        elif self.save_data.get_board('axis_rotation') == 'y':
            self.axis_rotation_rb_x.setChecked(False)
            self.axis_rotation_rb_y.setChecked(True)
            self.axis_rotation_rb_z.setChecked(False)
        elif self.save_data.get_board('axis_rotation') == 'z':
            self.axis_rotation_rb_x.setChecked(False)
            self.axis_rotation_rb_y.setChecked(False)
            self.axis_rotation_rb_z.setChecked(True)

        gb_layout = QtWidgets.QGridLayout()
        gb_layout.addWidget(self.angle_lbl, 0, 0)
        gb_layout.addWidget(self.angle_rotation_sb, 0, 1)
        gb_layout.addWidget(self.axis_lbl, 1, 0)
        gb_layout.addWidget(self.axis_rotation_rb_x, 1, 1)
        gb_layout.addWidget(self.axis_rotation_rb_y, 2, 1)
        gb_layout.addWidget(self.axis_rotation_rb_z, 3, 1)
        gb_layout.addWidget(self.offset_lbl, 4, 0)
        gb_layout.addWidget(self.offset_sb, 4, 1)
        gb_layout.addWidget(self.axis_sb_lbl.get('x'), 5, 0)
        gb_layout.addWidget(self.axis_sb.get('x'), 5, 1)
        gb_layout.addWidget(self.axis_sb_lbl.get('y'), 6, 0)
        gb_layout.addWidget(self.axis_sb.get('y'), 6, 1)
        group_box = QtWidgets.QGroupBox(self.init_data.get_board('gb_name'), self.window)
        group_box.setLayout(gb_layout)

        self.layout.addWidget(self.color_btn)
        self.layout.addWidget(self.edge_color_btn)
        self.layout.addWidget(group_box)
        self.layout.addWidget(self.close_btn)
        self.layout.addWidget(self.reset_btn)
        self.layout.addWidget(self.remove_btn)

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
        self.angle_rotation_sb.valueChanged.connect(self._rotate)
        self.axis_rotation_rb_x.clicked.connect(self._axis_x)
        self.axis_rotation_rb_y.clicked.connect(self._axis_y)
        self.axis_rotation_rb_z.clicked.connect(self._axis_z)
        self.offset_sb.valueChanged.connect(self._offset)
        self.axis_sb.get('x').valueChanged.connect(self._move_axis_x)
        self.axis_sb.get('y').valueChanged.connect(self._move_axis_y)

    def _move_axis_x(self):
        self.board.translate(self.axis_sb.get('x').value() - self.board.get_axis()[0], 0, 0)
        self.board.set_axis(self.axis_sb.get('x').value(), 'x')
        self.save_data.set_board('axis_x', self.board.get_axis()[0])

    def _move_axis_y(self):
        self.board.translate(0, self.axis_sb.get('y').value() - self.board.get_axis()[1], 0)
        self.board.set_axis(self.axis_sb.get('y').value(), 'y')
        self.save_data.set_board('axis_y', self.board.get_axis()[1])

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
        self.color_dialog.setCurrentColor(QtGui.QColor.fromRgb(*color))

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
        self.color_dialog.setCurrentColor(QtGui.QColor.fromRgb(*color))
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
        self.board.set_axis_angle(0)
        self.board.set_offset(0)
        self.board.setColor(self.init_data.get_board('color'))
        self.board.set_edge_color(self.init_data.get_board('edge_color'))
        self.window.close()

    def remove(self, message=True):
        """
        Retire le plateau de la fenetre.
        :param message: bool: Si True, affiche un message pour confirmer la suppression.
        :return: None
        """
        if time() - self.time < 0.2:
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
        self.time = time()

    def _remove(self):
        """
        Slot pour supprimer le plateau.
        :return: None
        """
        self.remove(True)

    def _rotate(self):
        """
        Slot pour faire tourner le plateau autour d'un axe.
        :return: None
        """
        self.board.rotate(self.angle_rotation_sb.value() - self.board.get_axis_angle(),
                          round(self.axis_rotation_rb_x.isChecked()),
                          round(self.axis_rotation_rb_y.isChecked()),
                          round(self.axis_rotation_rb_z.isChecked()),
                          local=True)

        self.board.set_axis_angle(self.angle_rotation_sb.value())
        if self.axis_rotation_rb_x.isChecked():
            self.save_data.set_board('axis_rotation', 'x')
            self.save_data.set_board('angle_rotation', self.angle_rotation_sb.value())
        elif self.axis_rotation_rb_y.isChecked():
            self.save_data.set_board('axis_rotation', 'y')
            self.save_data.set_board('angle_rotation', self.angle_rotation_sb.value())
        else:
            self.save_data.set_board('axis_rotation', 'z')
            self.save_data.set_board('angle_rotation', self.angle_rotation_sb.value())

    def _axis_x(self):
        """
        Slot si l'axe x est selectionne.
        :return: None
        """
        self.board.set_axis_angle(0)
        if self.save_data.get_board('axis_rotation') == 'y':
            self.board.rotate(0, 0, 1, 0, local=True)
        elif self.save_data.get_board('axis_rotation') == 'z':
            self.board.rotate(0, 0, 0, 1, local=True)
        elif self.save_data.get_board('axis_rotation') == 'x':
            self.board.rotate(0, 1, 0, 0, local=True)

        self.save_data.set_board('angle_rotation', 0)
        self.angle_rotation_sb.setValue(0)

    def _axis_y(self):
        """
        Slot si l'axe y est selectionne.
        :return: None
        """
        self.board.set_axis_angle(0)
        if self.save_data.get_board('axis_rotation') == 'x':
            self.board.rotate(0, 1, 0, 0, local=True)
        elif self.save_data.get_board('axis_rotation') == 'z':
            self.board.rotate(0, 0, 0, 1, local=True)
        elif self.save_data.get_board('axis_rotation') == 'y':
            self.board.rotate(0, 0, 1, 0, local=True)

        self.save_data.set_board('angle_rotation', 0)
        self.angle_rotation_sb.setValue(0)

    def _axis_z(self):
        """
        Slot si l'axe z est selectionne.
        :return: None
        """
        self.board.set_axis_angle(0)
        if self.save_data.get_board('axis_rotation') == 'y':
            self.board.rotate(0, 0, 1, 0, local=True)
        elif self.save_data.get_board('axis_rotation') == 'x':
            self.board.rotate(0, 1, 0, 0, local=True)
        elif self.save_data.get_board('axis_rotation') == 'z':
            self.board.rotate(0, 0, 0, 1, local=True)

        self.save_data.set_board('angle_rotation', 0)
        self.angle_rotation_sb.setValue(0)

    def _offset(self):
        """
        Slot pour deplacer le robot selon la valeur de l'offset
        :return: None
        """
        self.board.translate(0, 0, (self.offset_sb.value() - self.board.get_offset()))
        self.board.set_offset(self.offset_sb.value())
        self.save_data.set_board('offset', self.board.get_offset())
