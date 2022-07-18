# !/usr/bin/env python3
# -*- coding: utf-8 -*-
# Created by Axel Tremaudant on 07/06/2022

"""
Fichier qui contient la classe MainWindow.
"""

from PySide6 import QtWidgets, QtGui, QtCore
from time import time
from platform import system
import warnings

import functions
import ui
import element
import data
import widget
import simulation


class MainWindow(QtWidgets.QMainWindow):
    """
    Classe de la fenetre principale de CrubsRunner.
    """

    def __init__(self):
        """
        Constructeur de MainWindow.
        """
        super(MainWindow, self).__init__()

        # Definition des attributs
        self.save_data = data.Save()
        self.init_data = data.Init()

        self.doing = list()
        self.undoing = list()
        self.dropped_filename = ""
        self.time = 0.

        self.board = element.Board(self.save_data, self)
        self.main_robot = element.Robot(self.save_data, self, True)
        self.second_robot = element.Robot(self.save_data, self, False)
        self.vinyl = element.Vinyl(self, self.save_data)
        self.gcrubs = ui.GCrubs(self.save_data, self)

        self.layout = QtWidgets.QVBoxLayout()
        self.center_widget = QtWidgets.QWidget()

        self.component_dock = QtWidgets.QDockWidget(self.init_data.get_window('name_component_dock'), self)
        self.properties_dock = QtWidgets.QDockWidget(self)
        self.sequence_dock = QtWidgets.QDockWidget(self)
        self.list_widget = widget.ListWidget()

        self.viewer = widget.ViewWidget(self, self.save_data)
        self.grid = ui.GridItem(self.save_data, self)
        self.x_coord_sys = element.CoordSys(self.save_data)
        self.y_coord_sys = element.CoordSys(self.save_data)
        self.z_coord_sys = element.CoordSys(self.save_data)

        self.menuBar = QtWidgets.QMenuBar(self)
        self.toolBar = self.addToolBar(self.init_data.get_window('name_tool_bar'))
        self.status_bar = QtWidgets.QStatusBar(self)

        self.running = simulation.Run(self.save_data, self.main_robot, self.second_robot, self)

        self.new_project_action = QtGui.QAction(self.init_data.get_window('new_project_name'), self)
        self.open_project_action = QtGui.QAction(self.init_data.get_window('open_project_name'), self)
        self.save_action = QtGui.QAction(self.init_data.get_window('save_project_name'), self)
        self.save_as_action = QtGui.QAction(self.init_data.get_window('save_as_project_name'), self)
        self.import_action = QtGui.QAction(self.init_data.get_window('import_name'), self)
        self.export_action = QtGui.QAction(self.init_data.get_window('export_name'), self)
        self.edit_gcrubs_action = QtGui.QAction(self.init_data.get_gcrubs('edit_action_name'))
        self.undo_action = QtGui.QAction(self.init_data.get_window('undo_name'), self)
        self.redo_action = QtGui.QAction(self.init_data.get_window('redo_name'), self)
        self.run_action = QtGui.QAction(self.init_data.get_run('run_action_name'), self)
        self.stop_run_action = QtGui.QAction(self.init_data.get_run('stop_run_action_name'), self)
        self.key_action = QtGui.QAction(self.init_data.get_window('key_action_name'), self)

        self.top_view_action = QtGui.QAction(self.init_data.get_window('top_view_action_name'), self)
        self.start_view_action = QtGui.QAction(self.init_data.get_window('start_view_action_name'), self)
        self.bottom_view_action = QtGui.QAction(self.init_data.get_window('bottom_view_action_name'), self)

        self.speed_sb = QtWidgets.QSpinBox(self)
        self.speed_simulation_btn_nb = 2
        self.speed_simulation_btn = QtWidgets.QPushButton(self.init_data.get_window('speed_simulation_btn_name').format(
            multi=self.init_data.get_window('speed_simulation_btn_values')[self.speed_simulation_btn_nb]), self)

        # Initialisation de la fenetre
        self.init_window()

    def init_window(self):
        """
        Initialise la fenetre.
        :return: None
        """
        self.setWindowTitle(self.init_data.get_window('window_title'))

        self.create_actions()
        self.create_menubar()
        self.create_toolbar()
        self.create_dock_widget()
        self.setStatusBar(self.status_bar)
        self.status_bar.show()

        self.setCentralWidget(self.center_widget)
        self.center_widget.setLayout(self.layout)

        self.init_3d()
        self.create_connections()

        self.setAcceptDrops(self.init_data.get_window('accept_drops'))
        if system() == 'Darwin':
            self.showFullScreen()

    def create_dock_widget(self):
        """
        Cree le dock widget.
        :return: None
        """
        self.component_dock.setAllowedAreas(self.init_data.get_window('component_dock_allowed_areas'))
        self.component_dock.setFeatures(self.init_data.get_window('component_dock_features'))

        self.component_dock.setWidget(self.list_widget)
        self.addDockWidget(self.init_data.get_window('add_component_dock_area'), self.component_dock)

        self.list_widget.add_content(self.grid)

        self.properties_dock.setAllowedAreas(self.init_data.get_window('properties_dock_allowed_areas'))
        self.properties_dock.setFeatures(self.init_data.get_window('properties_dock_features'))
        self.addDockWidget(self.init_data.get_window('add_properties_dock_area'), self.properties_dock)

        self.sequence_dock.setAllowedAreas(self.init_data.get_window('sequence_dock_allowed_areas'))
        self.sequence_dock.setFeatures(self.init_data.get_window('sequence_dock_features'))
        self.addDockWidget(self.init_data.get_window('add_sequence_dock_area'), self.sequence_dock)

    def create_toolbar(self):
        """
        Cree la barre d'outils.
        :return: None
        """
        self.toolBar.addAction(self.new_project_action)
        self.toolBar.addAction(self.open_project_action)
        self.toolBar.addAction(self.save_action)
        self.toolBar.addAction(self.save_as_action)
        self.toolBar.addAction(self.import_action)
        self.toolBar.addAction(self.export_action)

        self.toolBar.addSeparator()
        self.toolBar.addAction(self.undo_action)
        self.toolBar.addAction(self.redo_action)
        self.toolBar.addAction(self.top_view_action)
        self.toolBar.addAction(self.bottom_view_action)
        self.toolBar.addAction(self.start_view_action)
        self.toolBar.addAction(self.key_action)

        self.toolBar.addSeparator()
        self.toolBar.addAction(self.edit_gcrubs_action)
        self.toolBar.addWidget(self.speed_sb)
        self.toolBar.addAction(self.run_action)
        self.toolBar.addAction(self.stop_run_action)
        self.toolBar.addWidget(self.speed_simulation_btn)

        self.speed_sb.setValue(self.save_data.get_grid('moving_speed'))
        self.speed_sb.setStatusTip(self.init_data.get_window('speed_tip'))

        self.speed_simulation_btn.setToolTip(self.init_data.get_window('speed_simulation_btn_tip'))

        self.toolBar.setMovable(self.init_data.get_window('tool_bar_movable'))

    def create_actions(self):
        """
        Cree les actions.
        :return: None
        """
        self.new_project_action.setShortcuts(self.init_data.get_window('new_project_shortcut'))
        self.new_project_action.setStatusTip(self.init_data.get_window('new_project_status_tip'))
        self.new_project_action.setIcon(self.init_data.get_window('new_project_icon'))

        self.open_project_action.setShortcuts(self.init_data.get_window('open_project_shortcut'))
        self.open_project_action.setStatusTip(self.init_data.get_window('open_project_status_tip'))
        self.open_project_action.setIcon(self.init_data.get_window('open_project_icon'))

        self.save_action.setShortcuts(self.init_data.get_window('save_project_shortcut'))
        self.save_action.setStatusTip(self.init_data.get_window('save_project_status_tip'))
        self.save_action.setIcon(self.init_data.get_window('save_project_icon'))

        self.save_as_action.setShortcuts(self.init_data.get_window('save_as_project_shortcut'))
        self.save_as_action.setStatusTip(self.init_data.get_window('save_as_project_status_tip'))
        self.save_as_action.setIcon(self.init_data.get_window('save_as_project_icon'))

        self.import_action.setShortcuts(self.init_data.get_window('import_shortcut'))
        self.import_action.setStatusTip(self.init_data.get_window('import_status_tip'))
        self.import_action.setIcon(self.init_data.get_window('import_icon'))

        with warnings.catch_warnings():  # Ignore le RuntimeWarning du a la sequence
            warnings.simplefilter('ignore')
            self.export_action.setShortcuts(self.init_data.get_window('export_shortcut'))
        self.export_action.setStatusTip(self.init_data.get_window('export_status_tip'))
        self.export_action.setIcon(self.init_data.get_window('export_icon'))

        self.undo_action.setShortcuts(self.init_data.get_window('undo_shortcut'))
        self.undo_action.setStatusTip(self.init_data.get_window('undo_status_tip'))
        self.undo_action.setIcon(self.init_data.get_window('undo_icon'))

        self.redo_action.setShortcuts(self.init_data.get_window('redo_shortcut'))
        self.redo_action.setStatusTip(self.init_data.get_window('redo_status_tip'))
        self.redo_action.setIcon(self.init_data.get_window('redo_icon'))

        self.top_view_action.setShortcuts(self.init_data.get_window('top_view_action_shortcut'))
        self.top_view_action.setStatusTip(self.init_data.get_window('top_view_action_status_tip'))
        self.top_view_action.setIcon(self.init_data.get_window('top_view_action_icon'))

        self.bottom_view_action.setShortcuts(self.init_data.get_window('bottom_view_action_shortcut'))
        self.bottom_view_action.setStatusTip(self.init_data.get_window('bottom_view_action_status_tip'))
        self.bottom_view_action.setIcon(self.init_data.get_window('bottom_view_action_icon'))

        self.start_view_action.setShortcuts(self.init_data.get_window('start_view_action_shortcut'))
        self.start_view_action.setStatusTip(self.init_data.get_window('start_view_action_status_tip'))
        self.start_view_action.setIcon(self.init_data.get_window('start_view_action_icon'))

        self.edit_gcrubs_action.setStatusTip(self.init_data.get_gcrubs('edit_action_status_tip'))
        self.edit_gcrubs_action.setIcon(self.init_data.get_gcrubs('edit_action_icon'))

        with warnings.catch_warnings():  # Ignore le RuntimeWarning du a la sequence
            warnings.simplefilter('ignore')
            self.run_action.setShortcuts(self.init_data.get_run('run_action_shortcut'))
        self.run_action.setStatusTip(self.init_data.get_run('run_action_tip'))
        self.run_action.setIcon(self.init_data.get_run('run_action_icon_stopped'))

        with warnings.catch_warnings():  # Ignore le RuntimeWarning du a la sequence
            warnings.simplefilter('ignore')
            self.stop_run_action.setShortcuts(self.init_data.get_run('stop_run_action_shortcut'))
        self.stop_run_action.setStatusTip(self.init_data.get_run('stop_run_action_tip'))
        self.stop_run_action.setIcon(self.init_data.get_run('stop_run_action_icon'))
        self.stop_run_action.setEnabled(False)

        self.key_action.setStatusTip(self.init_data.get_window('key_action_status_tip'))
        self.key_action.setIcon(self.init_data.get_window('key_action_icon'))

    def create_menubar(self):
        """
        Cree la barre de menus.
        :return: None
        """
        file_menu = self.menuBar.addMenu(self.init_data.get_window('menu_bar_menu1'))
        file_menu.addAction(self.new_project_action)
        file_menu.addAction(self.open_project_action)
        file_menu.addAction(self.save_action)
        file_menu.addAction(self.save_as_action)
        file_menu.addAction(self.import_action)
        file_menu.addAction(self.export_action)

        edit_menu = self.menuBar.addMenu(self.init_data.get_window('menu_bar_menu2'))
        edit_menu.addAction(self.undo_action)
        edit_menu.addAction(self.redo_action)
        edit_menu.addAction(self.top_view_action)
        edit_menu.addAction(self.bottom_view_action)
        edit_menu.addAction(self.start_view_action)
        edit_menu.addAction(self.edit_gcrubs_action)
        edit_menu.addAction(self.key_action)

        run_menu = self.menuBar.addMenu(self.init_data.get_window('menu_bar_menu3'))
        run_menu.addAction(self.run_action)
        run_menu.addAction(self.stop_run_action)
        self.setMenuBar(self.menuBar)

    def init_3d(self):
        """
        Initialise la partie 3D.
        :return: None
        """
        self.layout.addWidget(self.viewer, 1)

        self.start_view()

        self.grid.setSize(self.init_data.get_grid('width'), self.init_data.get_grid('height'))
        self.grid.setSpacing(self.init_data.get_grid('spacing_width'), self.init_data.get_grid('spacing_height'))
        self.viewer.addItem(self.grid)

        self.create_coord_sys()

    def create_connections(self):
        """
        Cree les connexions.
        :return: None
        """
        self.new_project_action.connect(QtCore.SIGNAL('triggered()'), self.new_project)
        self.open_project_action.connect(QtCore.SIGNAL('triggered()'), self.open_project)
        self.save_action.connect(QtCore.SIGNAL('triggered()'), self.save_project)
        self.save_as_action.connect(QtCore.SIGNAL('triggered()'), self.save_as_project)
        self.import_action.connect(QtCore.SIGNAL('triggered()'), self.import_component)
        self.export_action.connect(QtCore.SIGNAL('triggered()'), self.export_component)
        self.undo_action.connect(QtCore.SIGNAL('triggered()'), self.undo)
        self.redo_action.connect(QtCore.SIGNAL('triggered()'), self.redo)
        self.list_widget.itemDoubleClicked.connect(self.element_properties)
        self.list_widget.currentRowChanged.connect(self.select_element)
        self.start_view_action.connect(QtCore.SIGNAL('triggered()'), self.start_view)
        self.top_view_action.connect(QtCore.SIGNAL('triggered()'), self.top_view)
        self.bottom_view_action.connect(QtCore.SIGNAL('triggered()'), self.bottom_view)
        self.edit_gcrubs_action.connect(QtCore.SIGNAL('triggered()'), self.edit_gcrubs)
        self.speed_sb.valueChanged.connect(self.speed)
        self.run_action.connect(QtCore.SIGNAL('triggered()'), self.run)
        self.stop_run_action.connect(QtCore.SIGNAL('triggered()'), self.stop_run)
        self.key_action.connect(QtCore.SIGNAL('triggered()'), self.keys)
        self.speed_simulation_btn.clicked.connect(self.speed_simulation)

    def speed_simulation(self):
        if time() - self.time < 0.2:
            return

        self.speed_simulation_btn_nb += 1
        if self.speed_simulation_btn_nb == len(self.init_data.get_window('speed_simulation_btn_values')):
            self.speed_simulation_btn_nb = 0
        self.speed_simulation_btn.setText(self.init_data.get_window('speed_simulation_btn_name').format(
            multi=self.init_data.get_window('speed_simulation_btn_values')[self.speed_simulation_btn_nb]))

        self.time = time()

    def create_coord_sys(self):
        """
        Cree le systeme de coordonnees.
        :return: None
        """
        self.x_coord_sys.set_file(self.init_data.get_view('coord_sys_file'))
        self.y_coord_sys.set_file(self.init_data.get_view('coord_sys_file'))
        self.z_coord_sys.set_file(self.init_data.get_view('coord_sys_file'))

        self.x_coord_sys.setColor(self.init_data.get_view('coord_sys_x_color'))
        self.y_coord_sys.setColor(self.init_data.get_view('coord_sys_y_color'))
        self.z_coord_sys.setColor(self.init_data.get_view('coord_sys_z_color'))

        self.x_coord_sys.set_edge_color(self.init_data.get_view('coord_sys_x_color'))
        self.y_coord_sys.set_edge_color(self.init_data.get_view('coord_sys_y_color'))
        self.z_coord_sys.set_edge_color(self.init_data.get_view('coord_sys_z_color'))

        self.x_coord_sys.set_name("x")
        self.y_coord_sys.set_name("y")
        self.z_coord_sys.set_name("z")

        self.x_coord_sys.set_element_type("coord_sys")
        self.y_coord_sys.set_element_type("coord_sys")
        self.z_coord_sys.set_element_type("coord_sys")

        functions.object.show_stl(self.x_coord_sys)
        self.viewer.addItem(self.x_coord_sys)
        functions.object.show_stl(self.y_coord_sys)
        self.viewer.addItem(self.y_coord_sys)
        functions.object.show_stl(self.z_coord_sys)
        self.viewer.addItem(self.z_coord_sys)

        self.y_coord_sys.rotate(90, 0, 0, 1)
        self.z_coord_sys.rotate(-90, 0, 1, 0)

    def new_project(self):
        """
        Slot pour creer un nouveau projet.
        :return: None
        """
        if time() - self.time < 0.2:  # Evite une multiple apparition de la fenetre
            return

        self.grid.reset()
        self.board.remove(False)
        self.board = element.Board(self.save_data, self)
        self.main_robot.remove(False)
        self.main_robot = element.Robot(self.save_data, self, True)
        self.second_robot.remove(False)
        self.second_robot = element.Robot(self.save_data, self, False)
        del self.vinyl
        self.vinyl = element.Vinyl(self, self.save_data)
        del self.list_widget
        self.list_widget = widget.ListWidget()
        self.list_widget.add_content(self.grid)
        self.component_dock.setWidget(self.list_widget)
        self.create_connections()

        self.new_board()
        self.new_vinyl()
        self.new_main_robot()
        self.new_second_robot()
        self.time = time()

    def new_board(self, message=True, file=""):
        """
        Slot pour creer un nouveau plateau.
        :param message: bool: Si True, affiche un message
        :param file: str: Nom du fichier
        :return: None
        """
        if message:
            QtWidgets.QMessageBox(self.init_data.get_board('new_message_box_type'),
                                  self.init_data.get_board('new_message_box_title'),
                                  self.init_data.get_board('new_message_box_message')).exec()

        if file == "":
            file = QtWidgets.QFileDialog.getOpenFileName(self,
                                                         self.init_data.get_board('new_message_box_title'),
                                                         self.save_data.get_window('directory'),
                                                         self.init_data.get_board('file_dialog_open_extensions'))[0]
        extension = file.split('.')[-1]

        if file:
            del self.board
            self.board = element.Board(self.save_data, self)
            if '.' + extension in self.init_data.get_extension('3d_file'):
                self.board.set_file(file)
                self.save_data.set_board('file', file)
                self.board.setColor(self.init_data.get_board('color'))
                self.board.set_edge_color(self.init_data.get_board('edge_color'))
                self.board.set_name(self.init_data.get_board('name'))
                if extension == 'stl':
                    functions.object.show_stl(self.board)
                elif extension == 'obj':
                    functions.object.show_obj(self.board)
                self.viewer.addItem(self.board)
                self.board.translate(self.init_data.get_board('appearance_translation_x'),
                                     self.init_data.get_board('appearance_translation_y'),
                                     self.init_data.get_board('appearance_translation_z'))
                self.list_widget.add_content(self.board)

            elif extension == self.init_data.get_extension('board')[1:] or \
                    extension == self.init_data.get_extension('board')[1:]:
                self.board.set_name(self.init_data.get_board('name'))
                self.x_coord_sys.setVisible(True)
                self.y_coord_sys.setVisible(True)
                self.z_coord_sys.setVisible(True)

    def new_vinyl(self, message=True, file=""):
        """
        Slot pour creer un nouveau tapis.
        :param message: bool: Si True, affiche un message
        :param file: str: Nom du fichier
        :return: None
        """
        if message:
            QtWidgets.QMessageBox(self.init_data.get_vinyl('vinyl_message_box_type'),
                                  self.init_data.get_vinyl('vinyl_message_box_title'),
                                  self.init_data.get_vinyl('vinyl_message_box_message')).exec()

        if file == "":
            file = QtWidgets.QFileDialog.getOpenFileName(self,
                                                         self.init_data.get_vinyl('vinyl_dialog_open_title'),
                                                         self.save_data.get_window('directory'),
                                                         self.init_data.get_vinyl('vinyl_dialog_open_extensions'))[0]
        if file and '.' + file.split('.')[-1] in self.init_data.get_extension('vinyl'):
            del self.vinyl
            self.vinyl = element.Vinyl(self, self.save_data)
            self.vinyl.set_file(file)
            functions.object.show_vinyl(self.vinyl)
            self.viewer.addItem(self.vinyl)
            self.list_widget.add_content(self.vinyl)

    def new_main_robot(self, message=True, file=""):
        """
        Slot pour creer un nouveau robot principal.
        :param message: bool: Si True, affiche un message
        :param file: str: Nom du fichier
        :return: None
        """
        if message:
            QtWidgets.QMessageBox(self.init_data.get_main_robot('new_message_box_type'),
                                  self.init_data.get_main_robot('new_message_box_title'),
                                  self.init_data.get_main_robot('new_message_box_message')).exec()

        if file == "":
            file = QtWidgets.QFileDialog.getOpenFileName(self,
                                                         self.init_data.get_main_robot('new_message_box_title'),
                                                         self.save_data.get_window('directory'),
                                                         self.init_data.get_main_robot('file_dialog_open_extensions'))[
                0]
        extension = file.split('.')[-1]

        if file:
            del self.main_robot
            self.main_robot = element.Robot(self.save_data, self, True)
            self.running.set_main_robot(self.main_robot)
            if '.' + extension[:3] in self.init_data.get_extension('3d_file'):
                self.main_robot.set_file(file)
                self.save_data.set_main_robot('file', file)
                self.main_robot.setColor(self.init_data.get_main_robot('color'))
                self.main_robot.set_edge_color(self.init_data.get_main_robot('edge_color'))
                self.main_robot.set_name(self.init_data.get_main_robot('name'))
                if extension == 'stl':
                    functions.object.show_stl(self.main_robot)
                elif extension == 'obj':
                    functions.object.show_obj(self.main_robot)
                self.viewer.addItem(self.main_robot)
                self.list_widget.add_content(self.main_robot)
                self.main_robot.set_offset(-self.main_robot.get_min_max()[2][0])
                self.main_robot.translate(0, 0, self.main_robot.get_offset())
                self.save_data.set_main_robot('offset', self.main_robot.get_offset())

            elif extension[-4:-1] == self.init_data.get_extension('robot')[1:] or \
                    extension == self.init_data.get_extension('robot')[1:]:
                self.open_project(file)
                self.main_robot.set_name(self.init_data.get_main_robot('name'))
                self.x_coord_sys.setVisible(True)
                self.y_coord_sys.setVisible(True)
                self.z_coord_sys.setVisible(True)

            if self.main_robot.is_invisible():
                coef = self.init_data.get_main_robot('invisible_coef')
                self.main_robot.scale(coef, coef, coef)

    def new_second_robot(self, message=True, file=""):
        """
        Slot pour creer le robot secondaire.
        :param message: bool: Si True, affiche un message
        :param file: str: Nom du fichier
        :return: None
        """
        if message:
            ans = QtWidgets.QMessageBox(self.init_data.get_second_robot('new_message_box_type'),
                                        self.init_data.get_second_robot('new_message_box_title'),
                                        self.init_data.get_second_robot('new_message_box_message'),
                                        self.init_data.get_second_robot('new_message_box_buttons')).exec()

            if ans == QtWidgets.QMessageBox.No:
                return

        if file == "":
            file = QtWidgets.QFileDialog.getOpenFileName(self,
                                                         self.init_data.get_second_robot(
                                                             'new_message_box_title'),
                                                         self.save_data.get_window('directory'),
                                                         self.init_data.get_main_robot(
                                                             'file_dialog_open_extensions'))[0]
        extension = file.split('.')[-1]

        if file:
            del self.second_robot
            self.second_robot = element.Robot(self.save_data, self, False)
            self.running.set_second_robot(self.second_robot)
            if '.' + extension[:3] in self.init_data.get_extension('3d_file'):
                self.save_data.set_second_robot('file', file)
                self.second_robot.set_file(file)
                self.second_robot.setColor(self.init_data.get_second_robot('color'))
                self.second_robot.set_edge_color(self.init_data.get_second_robot('edge_color'))
                self.second_robot.set_name(self.init_data.get_second_robot('name'))
                if extension == 'stl':
                    functions.object.show_stl(self.second_robot)
                elif extension == 'obj':
                    functions.object.show_obj(self.second_robot)
                self.viewer.addItem(self.second_robot)
                self.list_widget.add_content(self.second_robot)
                self.second_robot.set_offset(-self.second_robot.get_min_max()[2][0])
                self.second_robot.translate(0, 0, self.second_robot.get_offset())
                self.save_data.set_second_robot('offset', self.second_robot.get_offset())
            elif extension[-4:-1] == self.init_data.get_extension('robot')[1:] or \
                    extension == self.init_data.get_extension('robot')[1:]:
                self.open_project(file)
                self.second_robot.set_name(self.init_data.get_second_robot('name'))
                self.x_coord_sys.setVisible(True)
                self.y_coord_sys.setVisible(True)
                self.z_coord_sys.setVisible(True)

            if self.second_robot.is_invisible():
                coef = self.init_data.get_main_robot('invisible_coef')
                self.second_robot.scale(coef, coef, coef)

    def open_project(self, file=""):
        """
        Slot pour ouvrir un projet.
        :param file: str: Nom du fichier
        :return: None
        """
        if time() - self.time < 0.2:
            return

        if file == "":
            file = QtWidgets.QFileDialog.getOpenFileName(self, self.init_data.get_window('open_project_dialog_title'),
                                                         self.save_data.get_window('directory'),
                                                         self.init_data.get_window('project_extension'))[0]
            if file:  # On retire tout
                self.grid.reset()
                del self.board
                self.board = element.Board(self.save_data, self)
                del self.vinyl
                self.vinyl = element.Vinyl(self, self.save_data)
                del self.main_robot
                self.main_robot = element.Robot(self.save_data, self, True)
                del self.second_robot
                self.second_robot = element.Robot(self.save_data, self, False)
                del self.list_widget
                self.list_widget = widget.ListWidget()
                self.list_widget.add_content(self.grid)
                self.component_dock.setWidget(self.list_widget)
                self.create_connections()

        if file:
            try:
                with open(file, 'r') as file:
                    file.readline()
                    param = file.readline()
                    while param != "":
                        if param.find(self.init_data.get_window('window_first_line')[1:-1]) != -1:
                            for _ in range(self.save_data.get_len('window')):
                                param = file.readline()
                                try:
                                    self.save_data.set_window(param.split(' = ')[0], eval(param.split(' = ')[1][1:-2]))
                                except (IndexError, SyntaxError, NameError):
                                    self.save_data.set_window(param.split(' = ')[0], eval(param.split(' = ')[1][:-1]))

                        elif param.find(self.init_data.get_window('grid_first_line')[1:-1]) != -1:
                            for _ in range(self.save_data.get_len('grid')):
                                param = file.readline()
                                try:
                                    self.save_data.set_grid(param.split(' = ')[0], eval(param.split(' = ')[1][1:-2]))
                                except (IndexError, SyntaxError, NameError):
                                    self.save_data.set_grid(param.split(' = ')[0], eval(param.split(' = ')[1][:-1]))

                        elif param.find(self.init_data.get_window('board_first_line')[1:-1]) != -1:
                            for _ in range(self.save_data.get_len('board')):
                                param = file.readline()
                                try:
                                    self.save_data.set_board(param.split(' = ')[0], eval(param.split(' = ')[1][1:-2]))
                                except (IndexError, SyntaxError, NameError):
                                    self.save_data.set_board(param.split(' = ')[0], eval(param.split(' = ')[1][:-1]))
                            self.list_widget.add_content(self.board)
                            self.board.translate(self.init_data.get_board('appearance_translation_x'),
                                                 self.init_data.get_board('appearance_translation_y'),
                                                 self.init_data.get_board('appearance_translation_z'))

                        elif param.find(self.init_data.get_window('main_robot_first_line')[1:-1]) != -1:
                            for _ in range(self.save_data.get_len('main_robot')):
                                param = file.readline()
                                try:
                                    self.save_data.set_main_robot(param.split(' = ')[0],
                                                                  eval(param.split(' = ')[1][1:-2]))
                                except (IndexError, SyntaxError, NameError):
                                    self.save_data.set_main_robot(param.split(' = ')[0],
                                                                  eval(param.split(' = ')[1][:-1]))
                            self.list_widget.add_content(self.main_robot)

                        elif param.find(self.init_data.get_window('second_robot_first_line')[1:-1]) != -1:
                            for _ in range(self.save_data.get_len('second_robot')):
                                param = file.readline()
                                try:
                                    self.save_data.set_second_robot(param.split(' = ')[0],
                                                                    eval(param.split(' = ')[1][1:-2]))
                                except (IndexError, SyntaxError, NameError):
                                    self.save_data.set_second_robot(param.split(' = ')[0],
                                                                    eval(param.split(' = ')[1][:-1]))
                            self.list_widget.add_content(self.second_robot)

                        elif param.find(self.init_data.get_window('gcrubs_first_line')[1:-1]) != -1:
                            for _ in range(self.save_data.get_len('gcrubs')):
                                param = file.readline()
                                try:
                                    self.save_data.set_gcrubs(param.split(' = ')[0],
                                                              eval(param.split(' = ')[1][1:-2].replace("PySide6.", "")))
                                except (IndexError, SyntaxError, NameError):
                                    self.save_data.set_gcrubs(param.split(' = ')[0],
                                                              eval(param.split(' = ')[1][:-1].replace("PySide6.", "")))
                        elif param.find(self.init_data.get_window('vinyl_first_line')[1:-1]) != -1:
                            for _ in range(self.save_data.get_len('vinyl')):
                                param = file.readline()
                                try:
                                    self.save_data.set_vinyl(param.split(' = ')[0],
                                                             eval(param.split(' = ')[1][1:-2]))
                                except (IndexError, SyntaxError, NameError):
                                    self.save_data.set_vinyl(param.split(' = ')[0],
                                                             eval(param.split(' = ')[1][:-1]))
                            self.list_widget.add_content(self.vinyl)
                        param = file.readline()
            except FileNotFoundError:
                QtWidgets.QMessageBox(self.init_data.get_window('error_open_file_type'),
                                      self.init_data.get_window('error_open_file_title'),
                                      self.init_data.get_window('error_open_file_message').format(
                                          filename=file)).exec()
            self.update_()
        self.time = time()

    def save_project(self):
        """
        Slot pour sauvegarder le projet.
        :return: None
        """
        if self.save_data.get_window('project_file') == "":
            self.save_as_project()
        else:
            self.write_file(self.save_data.get_window('project_file'))

        if self.save_data.get_main_robot('gcrubs_file') != "":
            self.main_robot.save_sequence()

        if self.save_data.get_second_robot('gcrubs_file') != "":
            self.second_robot.save_sequence()

    def save_as_project(self):
        """
        Slot pour enregistrer sous le projet.
        :return: None
        """
        file = \
            QtWidgets.QFileDialog.getSaveFileName(self, self.init_data.get_window('save_as_project_dialog_title'),
                                                  self.save_data.get_window(
                                                      'directory') + '/' + self.init_data.get_window(
                                                      'project_default_name') + self.init_data.get_extension('project'),
                                                  self.save_data.get_window('project_extension'))[0]

        if file:
            if file.split('.')[-1] != self.init_data.get_extension('project')[1:]:
                file = file.split('.')[0] + self.init_data.get_extension('project')

            self.save_data.set_window('project_file', file)
            self.save_data.set_window('directory', file.rpartition('/')[0])
            self.write_file(file)

    def write_file(self, file_name: str):
        """
        Fonction pour ecrire toutes les donnees du projet dans un fichier.
        :param file_name: str: Nom du fichier dans lequel ecrire.
        :return: None
        """
        try:
            with open(file_name, 'w') as file:
                file.write(self.init_data.get_window('saving_file_first_line').format(
                    date=QtCore.QDate.currentDate().toString(self.init_data.get_main_robot('date_format'))))
                file.write(self.save_data.save('window'))
                file.write(self.save_data.save('grid'))
                file.write(self.save_data.save('board'))
                file.write(self.save_data.save('main_robot'))
                file.write(self.save_data.save('second_robot'))
                file.write(self.save_data.save('gcrubs'))
                file.write(self.save_data.save('vinyl'))
        except FileNotFoundError:
            QtWidgets.QMessageBox(self.init_data.get_window('error_open_file_type'),
                                  self.init_data.get_window('error_open_file_title'),
                                  self.init_data.get_window('error_open_file_message').format(
                                      filename=file_name)).exec()

    def import_component(self, file=""):
        """
        Slot pour importer un composant.
        :param file: str: Nom du ficher a importer
        :return: None
        """
        if time() - self.time < 0.2:
            return
        dialog = QtWidgets.QDialog(self)
        dialog.setWindowTitle(self.init_data.get_window('import_dialog_title'))
        dialog.setModal(self.init_data.get_window('import_dialog_modal'))
        dialog.setMinimumSize(self.init_data.get_window('import_width'), self.init_data.get_window('import_height'))

        radio_board = QtWidgets.QRadioButton(self.init_data.get_window('import_radio_board_name'), dialog)
        radio_vinyl = QtWidgets.QRadioButton(self.init_data.get_window('import_radio_vinyl_name'), dialog)
        radio_main_robot = QtWidgets.QRadioButton(self.init_data.get_window('import_radio_main_robot_name'), dialog)
        radio_second_robot = QtWidgets.QRadioButton(self.init_data.get_window('import_radio_second_robot_name'), dialog)

        radio_board.setChecked(self.init_data.get_window('import_radio_board_checked'))
        radio_vinyl.setChecked(self.init_data.get_window('import_radio_vinyl_checked'))
        radio_main_robot.setChecked(self.init_data.get_window('import_radio_main_robot_checked'))
        radio_second_robot.setChecked(self.init_data.get_window('import_radio_second_robot_checked'))

        cancel_btn = QtWidgets.QPushButton(self.init_data.get_window('import_cancel_btn_name'), dialog)
        ok_btn = QtWidgets.QPushButton(self.init_data.get_window('import_ok_btn_name'), dialog)
        cancel_btn.setChecked(self.init_data.get_window('import_cancel_btn_checked'))
        ok_btn.setChecked(self.init_data.get_window('import_ok_btn_checked'))

        layout = QtWidgets.QGridLayout(dialog)
        layout.addWidget(radio_board, 0, 0)
        layout.addWidget(radio_vinyl, 1, 0)
        layout.addWidget(radio_main_robot, 2, 0)
        layout.addWidget(radio_second_robot, 3, 0)
        layout.addWidget(cancel_btn, 4, 0)
        layout.addWidget(ok_btn, 4, 1)
        dialog.setLayout(layout)

        def cancel_btn_clicked():
            dialog.close()

        def ok_btn_clicked():
            if radio_board.isChecked() and self.save_data.get_board('file') == '':
                self.new_board(False, file)
            elif radio_main_robot.isChecked() and self.save_data.get_main_robot('file') == '':
                self.new_main_robot(False, file)
            elif radio_second_robot.isChecked() and self.save_data.get_second_robot('file') == '':
                self.new_second_robot(False, file)
            elif radio_vinyl.isChecked() and self.save_data.get_vinyl('file') == '':
                self.new_vinyl(False, file)
            else:
                QtWidgets.QMessageBox(self.init_data.get_window('import_message_box_type'),
                                      self.init_data.get_window('import_message_box_title'),
                                      self.init_data.get_window('import_message_box_message')).exec()
            dialog.close()

        cancel_btn.clicked.connect(cancel_btn_clicked)
        ok_btn.clicked.connect(ok_btn_clicked)

        dialog.show()
        self.time = time()

    def export_component(self):
        """
        Slot pour exporter un composant.
        :return: None
        """
        dialog = QtWidgets.QDialog(self)
        dialog.setWindowTitle(self.init_data.get_window('export_dialog_title'))
        dialog.setModal(self.init_data.get_window('import_dialog_modal'))
        dialog.setMinimumSize(280, 150)

        radio_board = QtWidgets.QRadioButton(self.init_data.get_window('import_radio_board_name'), dialog)
        radio_main_robot = QtWidgets.QRadioButton(self.init_data.get_window('import_radio_main_robot_name'), dialog)
        radio_second_robot = QtWidgets.QRadioButton(self.init_data.get_window('import_radio_second_robot_name'), dialog)

        radio_board.setChecked(self.init_data.get_window('import_radio_board_checked'))
        radio_main_robot.setChecked(self.init_data.get_window('import_radio_main_robot_checked'))
        radio_second_robot.setChecked(self.init_data.get_window('import_radio_second_robot_checked'))

        cancel_btn = QtWidgets.QPushButton(self.init_data.get_window('import_cancel_btn_name'), dialog)
        ok_btn = QtWidgets.QPushButton(self.init_data.get_window('import_ok_btn_name'), dialog)
        cancel_btn.setChecked(self.init_data.get_window('import_cancel_btn_checked'))
        ok_btn.setChecked(self.init_data.get_window('import_ok_btn_checked'))

        if self.board.get_file() == "":
            radio_board.setEnabled(False)

        if self.main_robot.get_file() == "":
            radio_main_robot.setEnabled(False)

        if self.second_robot.get_file() == "":
            radio_second_robot.setEnabled(False)

        layout = QtWidgets.QGridLayout(dialog)
        layout.addWidget(radio_board, 0, 0)
        layout.addWidget(radio_main_robot, 1, 0)
        layout.addWidget(radio_second_robot, 2, 0)
        layout.addWidget(cancel_btn, 3, 0)
        layout.addWidget(ok_btn, 3, 1)
        dialog.setLayout(layout)

        def cancel_btn_clicked():
            dialog.close()

        def ok_btn_clicked():
            if radio_board.isChecked() and radio_board.isVisible():  # Si on veut exporter le plateau
                file = QtWidgets.QFileDialog.getSaveFileName(self,
                                                             "Enregistrer " + self.init_data.get_window(
                                                                 'import_radio_board_name'),
                                                             self.save_data.get_window('directory') + '/' +
                                                             self.init_data.get_window('project_default_name') +
                                                             self.init_data.get_extension('board'),
                                                             self.save_data.get_board('save_extension'))[0]
                if file:
                    if file.split('.')[-1] != self.init_data.get_extension('board')[1:]:
                        file = file.split('.')[0] + self.init_data.get_extension('board')

                    self.save_data.set_window('directory', file.rpartition('/')[0])
                    try:
                        with open(file, 'w') as file_name:
                            file_name.write(self.save_data.save('board'))
                    except FileNotFoundError:
                        QtWidgets.QMessageBox(self.init_data.get_window('error_open_file_type'),
                                              self.init_data.get_window('error_open_file_title'),
                                              self.init_data.get_window('error_open_file_message').format(
                                                  filename=file_name)).exec()
                        return

            # Si on veut exporter le robot principal
            elif radio_main_robot.isChecked() and radio_main_robot.isVisible():
                file = QtWidgets.QFileDialog.getSaveFileName(self,
                                                             "Enregistrer " + self.init_data.get_window(
                                                                 'import_radio_main_robot_name'),
                                                             self.save_data.get_window('directory') + '/' +
                                                             self.init_data.get_window('project_default_name') +
                                                             self.init_data.get_extension('robot'),
                                                             self.save_data.get_main_robot('save_extension'))[0]

                if file:
                    if file.split('.')[-1] != self.init_data.get_extension('robot')[1:]:
                        file = file.split('.')[0] + self.init_data.get_extension('robot')

                    self.save_data.set_window('directory', file.rpartition('/')[0])
                    try:
                        with open(file, 'w') as file_name:
                            file_name.write(self.save_data.save('main_robot'))
                    except FileNotFoundError:
                        QtWidgets.QMessageBox(self.init_data.get_window('error_open_file_type'),
                                              self.init_data.get_window('error_open_file_title'),
                                              self.init_data.get_window('error_open_file_message').format(
                                                  filename=file_name)).exec()
                        return

            # Si on veut exporter le robot secondaire
            elif radio_second_robot.isChecked() and radio_second_robot.isVisible():
                file = QtWidgets.QFileDialog.getSaveFileName(self,
                                                             "Enregistrer " + self.init_data.get_window(
                                                                 'import_radio_second_robot_name'),
                                                             self.save_data.get_window('directory') + '/' +
                                                             self.init_data.get_window('project_default_name') +
                                                             self.init_data.get_extension('robot'),
                                                             self.save_data.get_second_robot('save_extension'))[0]

                if file:
                    if file.split('.')[-1] != self.init_data.get_extension('robot')[1:]:
                        file = file.split('.')[0] + self.init_data.get_extension('robot')

                    self.save_data.set_window('directory', file.rpartition('/')[0])
                    try:
                        with open(file, 'w') as file_name:
                            file_name.write(self.save_data.save('second_robot'))
                    except FileNotFoundError:
                        QtWidgets.QMessageBox(self.init_data.get_window('error_open_file_type'),
                                              self.init_data.get_window('error_open_file_title'),
                                              self.init_data.get_window('error_open_file_message').format(
                                                  filename=file_name)).exec()
                        return

            dialog.close()

        cancel_btn.clicked.connect(cancel_btn_clicked)
        ok_btn.clicked.connect(ok_btn_clicked)

        dialog.show()

    def undo(self):
        """
        Slot pour defaire.
        :return: None
        """
        if len(self.doing) > 0:
            for _ in range(len(self.undoing) - self.init_data.get_window('max_len_doing')):
                self.undoing.pop(0)
            self.undoing.append(self.doing.pop(-1))
            self.undoing[-1][0].move_robot(self.undoing[-1][1], self.undoing[-1][2], self.undoing[-1][3])
            self.status_bar.showMessage(
                self.init_data.get_window('position_status_message').format(x=int(self.undoing[-1][0].get_coord()[0]),
                                                                            y=int(self.undoing[-1][0].get_coord()[1]),
                                                                            angle=self.undoing[-1][0].get_angle()))

    def redo(self):
        """
        Slot pour refaire.
        :return: None
        """
        if len(self.undoing) > 0:
            for _ in range(len(self.doing) - self.init_data.get_window('max_len_doing')):
                self.doing.pop(0)
            self.doing.append(self.undoing.pop(-1))
            self.doing[-1][0].move_robot(-self.doing[-1][1], -self.doing[-1][2], -self.doing[-1][3])
            self.status_bar.showMessage(
                self.init_data.get_window('position_status_message').format(x=int(self.doing[-1][0].get_coord()[0]),
                                                                            y=int(self.doing[-1][0].get_coord()[1]),
                                                                            angle=self.doing[-1][0].get_angle()))

    def do(self, action):
        """
        Fonction pour faire.
        :param action: any: Action a ajouter.
        :return: None
        """
        for _ in range(len(self.doing) - self.init_data.get_window('max_len_doing')):
            self.doing.pop(0)
        self.doing.append(action)

    def updo(self, action):
        """
        Fonction pour modifier ce qui a ete fait precedemment sans ajouter en plus.
        :param action: any: Action a ajouter
        :return: None
        """
        self.doing[-1] = action

    def top_view(self):
        """
        Slot pour passer en vue de dessus.
        :return: None
        """
        self.viewer.setCameraPosition(elevation=self.init_data.get_view('top_view_position_elevation'))

    def bottom_view(self):
        """
        Slot pour passer en vue de dessous.
        :return: None
        """
        self.viewer.setCameraPosition(elevation=self.init_data.get_view('bottom_view_position_elevation'))

    def start_view(self):
        """
        Slot pour passer en vue initiale.
        :return: None
        """
        self.viewer.setCameraPosition(rotation=self.init_data.get_view('start_view_position_rotation'),
                                      distance=self.init_data.get_view('start_view_position_distance'),
                                      pos=self.init_data.get_view('start_view_position_pos'))

    def edit_gcrubs(self):
        """
        Slot pour editer les commandes gcrubs.
        :return: None
        """
        self.gcrubs.edit()

    def speed(self):
        """
        Slot pour mettre a jour la vitesse de deplacement des robots.
        :return:
        """
        self.save_data.set_grid('moving_speed', self.speed_sb.value())

    def run(self):
        """
        Slot pour lancer la simulation.
        :return: None
        """
        if self.running.is_ongoing():  # Si la simulation est deja en cours
            if self.running.is_running():  # Si la simulation est en pause ou non
                self.run_action.setIcon(self.init_data.get_run('run_action_icon_stopped'))
                self.running.stop()
            else:
                self.run_action.setIcon(self.init_data.get_run('run_action_icon_running'))
                self.running.resume()
        else:
            dialog = QtWidgets.QDialog(self)
            main_robot_cb = QtWidgets.QCheckBox(self.init_data.get_run('main_robot_cb_name'))
            second_robot_cb = QtWidgets.QCheckBox(self.init_data.get_run('second_robot_cb_name'))
            cancel_btn = QtWidgets.QPushButton(self.init_data.get_run('cancel_btn_name'))
            ok_btn = QtWidgets.QPushButton(self.init_data.get_run('ok_btn_name'))
            layout = QtWidgets.QGridLayout()

            dialog.setWindowTitle(self.init_data.get_run('dialog_title'))
            dialog.setModal(self.init_data.get_run('dialog_modal'))

            main_robot_cb.setChecked(self.init_data.get_run('main_robot_cb_checked'))
            second_robot_cb.setChecked(self.init_data.get_run('second_robot_cb_checked'))

            ok_btn.setDefault(self.init_data.get_run('ok_btn_default'))
            cancel_btn.setDefault(self.init_data.get_run('cancel_btn_default'))

            layout.addWidget(main_robot_cb, 0, 0)
            layout.addWidget(second_robot_cb, 1, 0)
            layout.addWidget(cancel_btn, 2, 0)
            layout.addWidget(ok_btn, 2, 1)
            dialog.setLayout(layout)

            if self.main_robot.get_gcrubs_file() == "" or not self.main_robot.visible():
                main_robot_cb.setEnabled(False)
            if self.second_robot.get_gcrubs_file() == "" or not self.second_robot.visible():
                second_robot_cb.setEnabled(False)

            if not main_robot_cb.isEnabled() and not second_robot_cb.isEnabled():
                ok_btn.setEnabled(False)

            def ok():
                if main_robot_cb.isChecked():
                    self.main_robot.set_running(True)
                    if not self.main_robot.is_origined():
                        self.main_robot.create_sequence()
                        dialog.close()
                        return
                if second_robot_cb.isChecked():
                    self.second_robot.set_running(True)
                    if not self.second_robot.is_origined():
                        self.second_robot.create_sequence()
                        dialog.close()
                        return

                dialog.close()
                self.stop_run_action.setEnabled(True)
                self.run_action.setIcon(self.init_data.get_run('run_action_icon_running'))
                self.running = simulation.Run(self.save_data, self.main_robot, self.second_robot, self)
                self.running.run()

            def cancel():
                dialog.close()

            ok_btn.clicked.connect(ok)
            cancel_btn.clicked.connect(cancel)

            dialog.show()

    def stop_run(self):
        """
        Slot pour arreter la simulation.
        :return: None
        """
        self.running.finish()
        self.stop_run_action.setEnabled(False)

    def element_properties(self):
        """
        Slot pour acceder aux proprietes des elements.
        :return: None
        """
        self.list_widget.get_contents()[self.list_widget.currentRow()].properties()

    def select_element(self):
        """
        Slot pour choisir l'element selectionne.
        :return: None
        """
        for i in range(self.list_widget.get_len()):
            try:
                if i == self.list_widget.currentRow():
                    self.list_widget.get_contents()[self.list_widget.currentRow()].set_selected(True)
                else:
                    self.list_widget.get_contents()[i].set_selected(False)
            except AttributeError:
                continue

    def keys(self):
        """
        Slot pour gerer les touches qui permettent de deplacer le robot.
        :return: None
        """
        window = widget.KeyDialog(self.save_data, self)
        window.setModal(self.init_data.get_window('keys_modal'))
        window.setWindowTitle(self.init_data.get_window('keys_title'))

        def get_key():
            k = 0
            for k in range(6):
                if keys[k][1].is_clicked():
                    break
            window.set_movement(list(self.save_data.get_gcrubs('keys').keys())[k])
            window.get_key(keys[k][2])
            keys[k][1].set_unclicked()

        def close_():
            window.close()

        def apply():
            key_ = dict()
            for k, val in zip(self.save_data.get_gcrubs('keys').keys(), keys):
                key_[k] = val[2].get_key()

            self.save_data.set_gcrubs('keys', key_)
            close_()

        keys = list()
        layout = QtWidgets.QGridLayout(window)
        for i, key in zip(range(6), self.save_data.get_gcrubs('keys').values()):
            keys.append(list())
            keys[i].append(QtWidgets.QLabel(self.init_data.get_window('keys_lbl_{num}'.format(num=i))))
            keys[i].append(widget.Button(self, i))
            keys[i].append(widget.Label(self.init_data.get_window('keys_lbl_key').format(
                key=window.ret_key(key))))
            keys[i][2].set_key(key)
            for j in range(len(keys[i])):
                layout.addWidget(keys[i][j], i, j)

            keys[i][1].clicked.connect(keys[i][1].set_clicked)
            keys[i][1].clicked.connect(get_key)

        close_btn = QtWidgets.QPushButton(self.init_data.get_window('keys_close_btn_name'))
        close_btn.setCursor(self.init_data.get_window('keys_close_cursor'))
        close_btn.setDefault(self.init_data.get_window('keys_close_default'))
        close_btn.clicked.connect(close_)
        apply_btn = QtWidgets.QPushButton(self.init_data.get_window('keys_apply_btn_name'))
        apply_btn.setCursor(self.init_data.get_window('keys_apply_cursor'))
        apply_btn.setDefault(self.init_data.get_window('keys_apply_default'))
        apply_btn.clicked.connect(apply)

        layout.addWidget(close_btn, 6, 0)
        layout.addWidget(apply_btn, 6, 2)
        window.setLayout(layout)
        window.show()

    def update_(self):
        """
        Fonction pour tout mettre a jour.
        :return: None
        """
        self.grid.update_()
        self.board.update_()
        self.vinyl.update_()
        self.main_robot.update_()
        self.second_robot.update_()
        self.z_coord_sys.update_()
        self.y_coord_sys.update_()
        self.x_coord_sys.update_()

        if self.board.get_file() != "":
            self.viewer.addItem(self.board)
        if self.vinyl.get_file() != "":
            self.viewer.addItem(self.vinyl)
        if self.main_robot.get_file() != "":
            self.viewer.addItem(self.main_robot)
        if self.second_robot.get_file() != "":
            self.viewer.addItem(self.second_robot)

    def closeEvent(self, event: QtGui.QCloseEvent) -> None:
        """
        Fonction appelee a la fermeture.
        :param event: QtGui.QCloseEvent: Evenement
        :return: None
        """
        self.save_data.set_settings('directory', self.save_data.get_window('directory'))
        event.accept()

    def dragEnterEvent(self, event: QtGui.QDragEnterEvent) -> None:
        """
        Fonction qui gere les entrees de glisser.
        :param event: QtGui.QDragEnterEvent: Evenement
        :return: None
        """
        mime_data = event.mimeData()
        mime_list = mime_data.formats()
        filename = ""

        if "text/uri-list" in mime_list:
            filename = mime_data.data("text/uri-list")
            filename = str(filename, encoding="utf-8")

            filename = filename.replace("file:///", "/").replace("\r\n", "").replace("%20", " ")

        # Si l'extension est utilisable
        if filename != "" and ('.' + filename.split('.')[-1] in self.init_data.get_extension('value') or
                               '.' + filename.split('.')[-1] in self.init_data.get_extension('vinyl') or
                               '.' + filename.split('.')[-1] in self.init_data.get_extension('3d_file')):
            event.accept()
            self.dropped_filename = filename
        else:
            event.ignore()
            self.dropped_filename = ""

    def dropEvent(self, event: QtGui.QDropEvent) -> None:
        """
        Fonction qui gere les evenements de depot.
        :param event: QtGui.QDropEvent: Evenement
        :return: None
        """
        extension = '.' + self.dropped_filename.split('.')[-1]
        if extension in self.init_data.get_extension('3d_file'):  # Si c'est un fichier 3D
            self.import_component(self.dropped_filename)

        elif extension == self.init_data.get_extension('project'):  # Si c'est un fichier de projet
            # On supprime tout
            self.grid.reset()
            self.board.remove(False)
            self.board = element.Board(self.save_data, self)
            self.main_robot.remove(False)
            self.main_robot = element.Robot(self.save_data, self, True)
            self.second_robot.remove(False)
            self.second_robot = element.Robot(self.save_data, self, False)
            del self.list_widget

            # On cree tout
            self.list_widget = widget.ListWidget()
            self.list_widget.add_content(self.grid)
            self.component_dock.setWidget(self.list_widget)
            self.create_connections()
            self.open_project(self.dropped_filename)

        elif extension == self.init_data.get_extension('board'):  # Si c'est un fichier de plateau
            if self.save_data.get_board('file') == '':
                del self.board
                self.board = element.Board(self.save_data, self)
                self.new_board(False, self.dropped_filename)
            else:
                QtWidgets.QMessageBox(self.init_data.get_window('import_message_box_type'),
                                      self.init_data.get_window('import_message_box_title'),
                                      self.init_data.get_window('import_message_box_message')).exec()

        elif extension == self.init_data.get_extension('robot'):  # Si c'est un fichier de robot
            try:
                with open(self.dropped_filename, 'r') as file:
                    file.readline()
                    param = file.readline()
                    while param[:3] != '## ':
                        param = file.readline()
            except FileNotFoundError:
                QtWidgets.QMessageBox(self.init_data.get_window('error_open_file_type'),
                                      self.init_data.get_window('error_open_file_title'),
                                      self.init_data.get_window('error_open_file_message').format(
                                          filename=self.dropped_filename)).exec()
                return

            if self.save_data.get_main_robot('file') == "" and \
                    param.find(self.init_data.get_window('main_robot_first_line')[1:-1]) != -1:
                del self.main_robot
                self.main_robot = element.Robot(self.save_data, self, True)
                self.new_main_robot(False, self.dropped_filename)

            elif self.save_data.get_second_robot('file') == "" and \
                    param.find(self.init_data.get_window('second_robot_first_line')[1:-1]) != -1:
                del self.second_robot
                self.second_robot = element.Robot(self.save_data, self, False)
                self.new_second_robot(False, self.dropped_filename)
            else:
                QtWidgets.QMessageBox(self.init_data.get_window('import_message_box_type'),
                                      self.init_data.get_window('import_message_box_title'),
                                      self.init_data.get_window('drop_message_box_message')).exec()

        elif extension in self.init_data.get_extension('vinyl'):
            if self.vinyl.get_file() == "":
                self.new_vinyl(False, self.dropped_filename)

        elif extension == self.init_data.get_extension('sequence'):  # Si c'est un fichier sequentiel
            pass

        self.dropped_filename = ""

    def contextMenuEvent(self, event: QtGui.QContextMenuEvent) -> None:
        """
        Fonction qui gere le menu clic droit de la souris.
        :param event: QtGui.QContextMenuEvent: Evenement
        :return: None
        """
        # Ne pas virer !!! Permet d'eviter de pouvoir virer la barre d'outils
        pass
