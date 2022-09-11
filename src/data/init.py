#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Created by Axel Tremaudant on 10/06/2022

"""
Fichier contenant toutes les valeurs utiles a l'application dans la classe InitData.
Ces valeurs ne changent pas pendant que l'application tourne.
"""

from PyQt5 import QtCore, QtWidgets, QtGui
from platform import system

if system() == 'Windows':
    COEF = -1
else:
    COEF = 1


class Init:
    """
    Classe contenant toutes les valeurs utiles a CrubsRunner.
    """
    def __init__(self):
        self.window = {  # Donnees pour la fenetre principale
            'app_title': "CrubsRunner",
            'app_icon': "icon/icon_app.png",
            'organisation_name': "Crubs",

            'name_tool_bar': "Projet",
            'tool_bar_movable': False,
            'speed_tip': "Vitesse de déplacement du robot",
            'cursor_while_opening': QtCore.Qt.WaitCursor,
            'normal_cursor': QtCore.Qt.ArrowCursor,

            'new_project_name': "Nouveau",
            'new_project_status_tip': "Créer un nouveau projet",
            'new_project_shortcut': QtGui.QKeySequence.New,  # Ctrl + N
            'new_project_icon': "icon/icon_new.png",

            'open_project_name': "Ouvrir",
            'open_project_shortcut': QtGui.QKeySequence.Open,  # Ctrl + O
            'open_project_status_tip': "Ouvrir un projet",
            'open_project_icon': "icon/icon_open.png",
            'open_project_dialog_title': "Ouvrir un projet",

            'save_project_name': "Enregistrer",
            'save_project_shortcut': QtGui.QKeySequence.Save,  # Ctrl + S
            'save_project_status_tip': "Enregistrer le projet",
            'save_project_icon': "icon/icon_save.png",

            'save_as_project_name': "Enregistrer sous",
            'save_as_project_shortcut': QtGui.QKeySequence.SaveAs,  # Ctrl + Shift + S
            'save_as_project_status_tip': "Enregistrer sous le projet",
            'save_as_project_icon': "icon/icon_save_as.png",
            'save_as_project_dialog_title': "Enregistrer le projet",
            'project_extension': "CrubsRunner project (*.crp)",
            'project_default_name': "SansNom",

            'saving_file_first_line': "## Fichier de sauvegarde de projet CrubsRunner du {date}\n",
            'window_first_line': "\n## Window\n",
            'grid_first_line': "\n## Grid\n",
            'board_first_line': "\n## Board\n",
            'main_robot_first_line': "\n## Main robot\n",
            'second_robot_first_line': "\n## Second robot\n",
            'gcrubs_first_line': "\n## gcrubs\n",
            'vinyl_first_line': "\n## vinyl\n",

            'import_name': "Importer",
            'import_shortcut': QtGui.QKeySequence.Italic,  # Ctrl + I
            'import_status_tip': "Importer un composant",
            'import_icon': "icon/icon_import.png",
            'import_dialog_title': "Choisir le composant à importer",
            'import_dialog_modal': True,
            'import_radio_board_name': "Plateau",
            'import_radio_vinyl_name': "Tapis",
            'import_radio_main_robot_name': "Robot principal",
            'import_radio_second_robot_name': "Robot secondaire",
            'import_radio_main_robot_checked': False,
            'import_radio_board_checked': True,
            'import_radio_vinyl_checked': False,
            'import_radio_second_robot_checked': False,
            'import_cancel_btn_name': "Annuler",
            'import_ok_btn_name': "Valider",
            'import_cancel_btn_checked': True,
            'import_ok_btn_checked': False,
            'import_height': 150,
            'import_width': 280,

            'export_name': "Exporter",
            'export_shortcut': QtGui.QKeySequence(QtCore.Qt.CTRL | QtCore.Qt.Key_E),
            'export_status_tip': "Exporter un composant",
            'export_icon': "icon/icon_export.png",
            "export_dialog_title": "Exporter un composant",  # Other parameters : same as import
            'export_component_dialog_min_size': (280, 150),

            'top_view_action_name': "Vue de dessus",
            'top_view_action_shortcut': QtGui.QKeySequence.AddTab,  # Ctrl + T
            'top_view_action_status_tip': "Vue de dessus",
            'top_view_action_icon': "icon/icon_top_view.png",

            'start_view_action_name': "Vue de départ",
            'start_view_action_shortcut': QtGui.QKeySequence.Underline,  # Ctrl + U
            'start_view_action_status_tip': "Vue de départ",
            'start_view_action_icon': "icon/icon_start_view.png",

            'bottom_view_action_name': "Vue de dessous",
            'bottom_view_action_shortcut': QtGui.QKeySequence.Bold,  # Ctrl + B
            'bottom_view_action_status_tip': "Vue de dessous",
            'bottom_view_action_icon': "icon/icon_bottom_view.png",

            'undo_name': "Annuler le déplacement",
            'undo_shortcut': QtGui.QKeySequence.Undo,  # Ctrl + Z
            'undo_status_tip': "Annuler le déplacement",
            'undo_icon': "icon/icon_undo.png",
            'max_len_doing': 50,

            'redo_name': "Remettre le déplacement",
            'redo_shortcut': QtGui.QKeySequence.Redo,  # Ctrl + Shift + Z ou Ctrl + Y
            'redo_status_tip': "Remettre le déplacement",
            'redo_icon': "icon/icon_redo.png",

            'key_action_name': "Choisir les touches",
            'key_action_status_tip': "Choisir les touches",
            'key_action_icon': "icon/icon_key.png",

            'edit_action_icon': "icon/icon_edit_gcrubs.png",
            'del_btn_icon': "icon/icon_del.png",
            'key_btn_icon': 'icon/icon_key.png',
            'run_action_icon_stopped': "icon/icon_run_stopped.png",
            'run_action_icon_running': "icon/icon_run_running.png",
            'stop_run_action_icon': "icon/icon_stop_run.png",

            'speed_simulation_btn_name': "x {multi}",
            'speed_simulation_btn_tip': "Vitesse de la simulation",
            'speed_simulation_btn_values': (0.25, 0.5, 1, 2, 4),

            'window_title': "CrubsRunner",
            'accept_drops': True,
            'window_start_width': 1200,
            'window_start_height': 800,

            'add_component_dock_area': QtCore.Qt.RightDockWidgetArea,  # Place le dockWidget a droite
            'name_component_dock': "Composants",
            'component_dock_allowed_areas': QtCore.Qt.RightDockWidgetArea | QtCore.Qt.LeftDockWidgetArea,
            'component_dock_features': QtWidgets.QDockWidget.DockWidgetFeature.DockWidgetMovable,  # Ne peut etre ferme
            'properties_dock_allowed_areas': QtCore.Qt.RightDockWidgetArea | QtCore.Qt.LeftDockWidgetArea,
            'add_properties_dock_area': QtCore.Qt.RightDockWidgetArea,
            'properties_dock_features': QtWidgets.QDockWidget.DockWidgetFeature.DockWidgetMovable,
            'sequence_dock_allowed_areas': QtCore.Qt.RightDockWidgetArea | QtCore.Qt.LeftDockWidgetArea,
            'add_sequence_dock_area': QtCore.Qt.LeftDockWidgetArea,
            'sequence_dock_features': QtWidgets.QDockWidget.DockWidgetFeature.DockWidgetMovable,

            'import_message_box_type': QtWidgets.QMessageBox.Warning,
            'import_message_box_title': "Erreur d'importation",
            'import_message_box_message': "Vous devez supprimer le composant avant d'en importer un autre.",
            "drop_message_box_message": "Les deux robots sont déjà attribués, veuillez en supprimer un avant "
                                        "d'en ajouter un autre.",

            'status_bar_message': "Position du {element} : ({x}, {y}) mm",
            'color_status_message': "Couleur : r = {r}, v = {v}, b = {b} ",
            'position_status_message': "Position : x = {x} mm, y = {y} mm, angle = {angle} degres ",

            'menu_bar_menu1': "&Fichier",
            'menu_bar_menu2': "&Édition",
            'menu_bar_menu3': "&Run",

            'error_open_file_type': QtWidgets.QMessageBox.Critical,
            'error_open_file_title': "Erreur à l'ouverture ou à la lecture",
            'error_open_file_message': "Le fichier '{filename}' n'a pas été trouvé ou n'a pas pu être lu.'",

            'error_format_file_type': QtWidgets.QMessageBox.Critical,
            'error_format_file_title': "Format non supporté",
            'error_format_file_message': "Le format du fichier '{filename}' n'est pas supporté.'",

            'keys_modal': True,
            'keys_title': "Choix des touches",
            'keys_lbl_0': "Aller à droite : ",
            'keys_lbl_1': "Aller à gauche : ",
            'keys_lbl_2': "Aller en haut : ",
            'keys_lbl_3': "Aller en bas : ",
            'keys_lbl_4': "Tourner à droite : ",
            'keys_lbl_5': "Tourner à gauche : ",
            'keys_lbl_key': "Touche : {key}",
            'keys_apply_btn_name': "Appliquer",
            'keys_apply_default': True,
            'keys_apply_cursor': QtCore.Qt.PointingHandCursor,
            'keys_close_btn_name': "Annuler",
            'keys_close_default': False,
            'keys_close_cursor': QtCore.Qt.PointingHandCursor,
        }  # end self.window

        self.board = {  # Contient toutes les donnees pour le plateau
            'type': "board",
            'name': "Plateau",

            'new_message_box_type': QtWidgets.QMessageBox.Information,
            'new_message_box_title': "Information",
            'new_message_box_message': "Choisir le plateau",
            'file_dialog_open_title': "Choisir le plateau",
            'file_dialog_open_extensions': "All files (*.stl *.obj *.3mf *.crb) ;; STL (*.stl) ;; OBJ (*.obj)"
                                           ";; 3MF (*.3mf) ;; CrubsRunner board (*.crb)",

            'save_extension': "CrubsRunner board (*.crb)",
            'color': (255 / 255, 211 / 255, 133 / 255, 1),  # de 0 a 1
            'edge_color': (105 / 255, 105 / 255, 105 / 255, 1),  # de 0 a 1

            'element_name': "Plateau",
            'appearance_translation_x': -1500,
            'appearance_translation_y': 1000,
            'appearance_translation_z': -1,

            'window_title': "Propriétés du plateau",

            'color_name': "Choisir la couleur du plateau",
            'color_cursor': QtCore.Qt.PointingHandCursor,
            'color_default': False,
            'color_dialog_title': "Couleur du plateau",
            'edge_color_name': "Choisir la couleur des arêtes",
            'edge_color_default': False,
            'edge_color_dialog_title': "Couleur des arêtes du plateau",

            'axis_rotation_x_name': "x",
            'axis_rotation_y_name': "y",
            'axis_rotation_z_name': "z",
            'angle_rotation_min': -180,
            'angle_rotation_max': 180,
            'gb_name': "Mise en place du plateau",
            'angle_lbl_name': "Angle : ",
            'axis_lbl_name': "Axe de rotation : ",

            'offset_lbl_name': "Hauteur : ",
            'offset_sb_min': -3000,
            'offset_sb_max': 3000,

            'close_btn_name': "Fermer",
            'close_cursor': QtCore.Qt.PointingHandCursor,
            'close_default': True,
            'reset_btn_name': "Reset",
            'reset_cursor': QtCore.Qt.PointingHandCursor,
            'reset_default': False,
            'remove_btn_name': "Supprimer",
            'remove_default': False,
            'remove_cursor': QtCore.Qt.PointingHandCursor,

            'remove_message_box_type': QtWidgets.QMessageBox.Question,
            'remove_message_box_title': "Suppression d'élément",
            'remove_message_box_message': "Etes-vous sûr de vouloir supprimer le plateau ?\n"
                                          "Cette action est irréversible.",
            'remove_message_box_buttons': QtWidgets.QMessageBox.No | QtWidgets.QMessageBox.Yes,
        }  # end self.board

        self.vinyl = {  # Contient toutes les donnees pour le vinyl
            'vinyl_message_box_type': QtWidgets.QMessageBox.Information,
            'vinyl_message_box_title': "Information",
            'vinyl_message_box_message': "Choisir le tapis du plateau",
            'vinyl_dialog_open_title': "Choisir le tapis du plateau",
            'vinyl_dialog_open_extensions': "All files (*.png *.pdf *.jpg *.jpeg) ;; PNG (*.png) ;; PDF (*.pdf)"
                                            ";; JPEG (*.jpg *.jpeg)",
            'remove_message_box_type': QtWidgets.QMessageBox.Question,
            'remove_message_box_title': "Suppression d'élément",
            'remove_message_box_message': "Etes-vous sûr de vouloir supprimer le tapis ?\n"
                                          "Cette action est irréversible.",
            'remove_message_box_buttons': QtWidgets.QMessageBox.No | QtWidgets.QMessageBox.Yes,
        }  # end self.vinyl

        # Contient toutes les donnees pour le robot principal et les donnees communes aux deux robots
        self.main_robot = {
            'type': "robot",
            'name': "Robot principal",

            'new_message_box_type': QtWidgets.QMessageBox.Information,
            'new_message_box_title': "Information",
            'new_message_box_message': "Choisir le robot principal",
            'file_dialog_open_title': "Choisir le robot principal",
            'file_dialog_open_extensions': "All files (*.stl *.obj *.3mf *.crr) ;; STL (*.stl) ;; OBJ (*.obj) ;; "
                                           "3MF (*.3mf) ;; CrubsRunner robot (*.crr)",
            'color': (29 / 255, 144 / 255, 18 / 255, 1),  # de 0 a 1
            'edge_color': (12 / 255, 73 / 255, 10 / 255, 1),  # de 0 a 1
            'save_extension': "CrubsRunner robot (*.crr)",

            'element_name': "Robot principal",
            'appearance_translation_x': 0,
            'appearance_translation_y': 0,
            'appearance_translation_z': 0,

            'window_title': "Propriétés du robot principal",
            'color_name': "Choisir la couleur du robot",
            'edge_color_name': "Choisir la couleur des arêtes",
            'color_dialog_title': "Couleur du robot",
            'edge_color_dialog_title': "Couleur des arêtes",
            'remove_message_box_message': "Êtes-vous sûr de vouloir supprimer le robot principal ?\n"
                                          "Cette action est irréversible.",
            'axis_rotation_x_name': "x",
            'axis_rotation_y_name': "y",
            'axis_rotation_z_name': "z",
            'angle_rotation_min': -180,
            'angle_rotation_max': 180,

            'gb_name': "Mise en place du robot sur le plateau",
            'angle_lbl_name': "Angle : ",
            'axis_lbl_name': "Axe de rotation : ",
            'offset_lbl_name': "Hauteur : ",
            'offset_sb_min': -3000,
            'offset_sb_max': 3000,
            'invisible_coef': 1000,

            'speed_lbl': "Vitesse (mm/s) : ",
            'speed_min': 1,
            'speed_max': 1000,
            'speed_rotation_lbl': "Vitesse de rotation (degrés/s) : ",
            'rotation_min':  1,
            'rotation_max': 360,
            'gb_speed_name': "Vitesses",
            'track_visible_cb_name': "Voir la trace",
            'track_visible_cb_checked': True,

            'sequence_btn_name': "Créer la séquence du robot",
            'sequence_btn_default': False,
            'sequence_btn_cursor': QtCore.Qt.PointingHandCursor,

            'import_gcrubs_btn_name': "Importer le fichier séquentiel",
            'import_gcrubs_btn_default': False,
            'import_gcrubs_btn_cursor': QtCore.Qt.PointingHandCursor,
            'import_gcrubs_title': "Choisir le fichier séquentiel",
            'import_gcrubs_extension': "Fichier séquentiel (*.gcrubs)",

            'sequence_dialog_title': "Séquence du robot principal",
            'sequence_text': "{comment} Sequence gcrubs generee par CrubsRunner le {date} pour le robot principal.\n",
            'sequence_save_btn_name': "Enregistrer",
            'sequence_save_btn_default': True,
            'sequence_save_btn_cursor': QtCore.Qt.PointingHandCursor,
            'sequence_cancel_btn_name': "Fermer",
            'sequence_cancel_btn_default': False,
            'sequence_cancel_btn_cursor': QtCore.Qt.PointingHandCursor,
            'sequence_new_btn_name': "Nouveau fichier",
            'sequence_new_btn_default': False,
            'sequence_new_btn_cursor': QtCore.Qt.PointingHandCursor,
            'save_sequence_title': "Sauvegarder le fichier généré",
            'date_format': "dd/MM/yy",

            'list_sorting_order': QtCore.Qt.AscendingOrder,
            'sequence_speed_lbl_text': "Vitesse du robot : ",

            'sequence_origin_lbl_text': "Placer le robot sur l'origine\n"
                                        "(axe z (en bleu) au niveau de\n"
                                        "l'axe de rotation).",
            'sequence_origin_lbl_text_start': "Placer le robot en position de départ.",
            'start_sequence_text': "{comment} Position de depart : x = {x} mm, y = {y} mm, angle = {angle} degres\n",
            'position_text': "Position de depart :",
            'sequence_origin_btn_name': "Fait",
            'sequence_origin_btn_default': True,
            'sequence_origin_btn_cursor': QtCore.Qt.PointingHandCursor,

            'track_width': 20,  # mm
            'out_limits': (2000, 1500)  # mm avant de considerer hors du plateau
        }   # End self.main_robot

        self.second_robot = {  # Contient les donnees pour le robot secondaire
            'type': "robot",
            'name': "Robot secondaire",

            'new_message_box_type': QtWidgets.QMessageBox.Question,
            'new_message_box_title': "Question",
            'new_message_box_message': "Y a-t-il un second robot ?",
            'new_message_box_buttons': QtWidgets.QMessageBox.No | QtWidgets.QMessageBox.Yes,
            'file_dialog_open_title': "Choisir le robot secondaire",
            'color': (40 / 255, 49 / 255, 255 / 255, 1),  # de 0 a 1
            'edge_color': (11 / 255, 33 / 255, 180 / 255, 1),  # de 0 a 1
            'save_extension': "CrubsRunner robot (*.crr)",

            'element_name': "Robot secondaire",
            'appearance_translation_x': 0,
            'appearance_translation_y': 0,
            'appearance_translation_z': 0,

            'window_title': "Propriétés du robot secondaire",
            'remove_message_box_message': "Êtes-vous sûr de vouloir supprimer le robot secondaire ?\n"
                                          "Cette action est irréversible.",

            'sequence_dialog_title': "Séquence du robot secondaire",
            'sequence_text': "{comment} Sequence gcrubs generee par CrubsRunner le {date} pour le robot secondaire.\n\n"
        }  # End self.second_robot

        self.view = {  # Contient les donnees pour la gestion de la vue du widget central
            'start_view_position_rotation': QtGui.QQuaternion.fromEulerAngles(QtGui.QVector3D(-45, 0, 0)),
            'start_view_position_distance': 4000,
            'start_view_position_pos': QtGui.QVector3D(0, 0, 0),

            'top_view_position_elevation': 90 * COEF,
            'bottom_view_position_elevation': -90 * COEF,

            'moving_cursor': QtCore.Qt.ClosedHandCursor,
            'orbit_cursor': QtCore.Qt.DragMoveCursor,
            'rotation_view_key': QtCore.Qt.MouseButton.LeftButton,
            'moving_view1': QtCore.Qt.KeyboardModifier.ControlModifier,  # & ev.modifiers()
            'moving_view_middle_button': QtCore.Qt.MouseButton.MiddleButton,
            'moving_view_middle_button1': QtCore.Qt.KeyboardModifier.ControlModifier,  # & ev.modifiers()
            'moving_view2': QtCore.Qt.MouseButton.RightButton,

            'coord_sys_name': "Repere",
            'coord_sys_file': "3d_files/coord_sys.stl",
            'coord_sys_visible': True,
            'coord_sys_x_color': (1., 0., 0., 1.),
            'coord_sys_y_color': (0., 1., 0., 1.),
            'coord_sys_z_color': (0., 0., 1., 1.),

            'min_zoom': 3000,
            'max_zoom': 10000
        }  # End self.view

        self.grid = {  # Contient les donnees de la grille dans le widget central
            'element_name': "Grille",
            'height': 2000,
            'width': 3000,
            'spacing_height': 100,
            'spacing_width': 100,
            'color': (255, 255, 255, 75),  # de 0 a 255
            'transparency': 75,
            'visible': True,

            'coord_sys_name': "Voir le repère",
            'coord_sys_visible': True,

            'see_name': "Voir la grille",
            'width_name': "Largeur du carreau (mm) :",
            'width_min': 1,
            'width_max': 2000,

            'height_name': "Hauteur du carreau (mm) :",
            'height_min': 1,
            'height_max': 3000,

            'color_name': "Choisir la couleur",
            'color_default': False,
            'color_cursor': QtCore.Qt.PointingHandCursor,

            'transparency_name': "Transparence : ",

            'close_name': "Fermer",
            'close_default': True,
            'close_cursor': QtCore.Qt.PointingHandCursor,

            'reset_name': "Reset",
            'reset_default': False,
            'reset_cursor': QtCore.Qt.PointingHandCursor,

            'window_name': "Propriétés de la grille",
            'window_modal': True,

            'color_dialog_name': "Choisir la couleur de la grille",

            'group_box_name': "Grille"
        }  # End self.grid

        self.gcrubs = {  # Contient les donnees pour toute la partie fichier sequentiel
            'extension': "Sequence CrubsRunner (*.gcrubs)",
            'edit_action_name': "Éditer les commandes gcrubs",
            'edit_action_status_tip': "Éditer les commandes gcrubs",

            'edit_window_title': "Éditer les commandes gcrubs",
            'description_lbl_text': "Remplir à gauche la description de ce que fait l'action et à droite "
                                    "la séquence correspondante.\n"
                                    "Mettre entre crochets ce qui peut varier. Les variables 'dist', 'angle' et 'temps'"
                                    " sont connues et sont à utiliser\n"
                                    "(les unités sont respectivement 'millimètre', 'degré' et 'seconde').",
            'apply_btn_name': "Appliquer",
            'apply_btn_default': True,
            'apply_btn_cursor': QtCore.Qt.PointingHandCursor,
            'cancel_btn_name': "Annuler",
            'cancel_btn_default': False,
            'cancel_btn_cursor': QtCore.Qt.PointingHandCursor,
            'add_btn_name': "Ajouter une commande",
            'add_btn_default': False,
            'add_btn_cursor': QtCore.Qt.PointingHandCursor,

            'key_btn_tip': "Choisir la touche associée",
            'del_btn_tip': "Supprimer la commande",
            'btn_cursor': QtCore.Qt.PointingHandCursor,

            'sa_height': 430,
            'sa_width': 730,
            'window_modal': True,

            'key_dialog_title': "Définir le mouvement associé",
            'key_lbl_text': "Appuyer sur la touche correspondant à l'instruction\n"
                            "'{instruction}'\n"
                            "Touche : ",
            'key_close_name': "Fermer",
            'key_close_cursor': QtCore.Qt.PointingHandCursor,
            'key_close_default': True,
        }  # End self.gcrubs

        self.run = {  # Contient les donnees pour la simulation
            'run_action_name': "Lancer une simulation",
            'run_action_shortcut': QtGui.QKeySequence(QtCore.Qt.CTRL | QtCore.Qt.Key_R),
            'run_action_tip': "Lancer une simulation",

            'stop_run_action_name': "Arrêter la simulation",
            'stop_run_action_shortcut': QtGui.QKeySequence(QtCore.Qt.CTRL | QtCore.Qt.Key_R | QtCore.Qt.SHIFT),
            'stop_run_action_tip': "Arrêter la simulation",

            'dialog_title': "Choix du robot à simuler",
            'dialog_modal': True,
            'main_robot_cb_name': "Robot principal",
            'main_robot_cb_checked': False,
            'second_robot_cb_name': "Robot secondaire",
            'second_robot_cb_checked': False,
            'cancel_btn_name': "Annuler",
            'cancel_btn_default': False,
            'ok_btn_name': "Valider",
            'ok_btn_default': True,

            'window_title': "Simulation",
            'cmd_lbl_main': "Commande robot principal : {cmd}",
            'cmd_lbl_second': "Commande robot secondaire : {cmd}",
            'time_lbl': "Chrono : {time} s",
            'theoretical_time_lbl': "Temps théorique : {time} s",
            'theoretical_time_accuracy': 2,  # Nombre de chiffres apres la virgule
            'accuracy_timer': None,  # None pour ne pas voir les chiffres apres la virgule
            'time_before_start': 2000,  # ms
            'timer_refresh': 1000,  # ms
            'time_for_refresh_estimation': 2,  # s
            # 15 parce que c'est ce qu'il fallait apres plusieurs tests, peut varier selon le pc
            # mais aucun lien direct trouve avec le reste donc bon...
            'added_time_refresh_time': 15  # ms
        }  # End self.run

        self.extensions = {  # Contient toutes les extensions ouvrables par l'application
            'project': ".crp",
            'board': ".crb",
            'robot': ".crr",
            'sequence': ".gcrubs",
            '3d_file': (".stl", ".obj", ".3mf"),
            'vinyl': (".png", ".pdf", ".jpg", ".jpeg")
        }  # End self.extensions

    def get_window(self, key: str):
        """
        Renvoie la donnee de la fenetre principale qui correspond a la cle.
        :param key: Cle pour obtenir la valeur correspondante
        :return: Valeur correspondant a la cle
        """
        return self.window.get(key)

    def get_board(self, key: str):
        """
        Renvoie la donnee du plateau qui correspond a la cle.
        :param key: Cle pour obtenir la valeur correspondante
        :return: Valeur correspondant a la cle
        """
        return self.board.get(key)

    def get_vinyl(self, key: str):
        """
        Renvoie la donnee du tapis qui correspond a la cle.
        :param key: Cle pour obtenir la valeur correspondante
        :return: Valeur correspondant a la cle
        """
        return self.vinyl.get(key)

    def get_main_robot(self, key: str):
        """
        Renvoie la donnee du robot principal qui correspond a la cle.
        :param key: Cle pour obtenir la valeur correspondante
        :return: Valeur correspondant a la cle
        """
        return self.main_robot.get(key)

    def get_second_robot(self, key: str):
        """
        Renvoie la donnee du robot secondaire qui correspond a la cle.
        :param key: Cle pour obtenir la valeur correspondante
        :return: Valeur correspondant a la cle
        """
        return self.second_robot.get(key)

    def get_view(self, key: str):
        """
        Renvoie la donnee de la gestion de la vue qui correspond a la cle.
        :param key: Cle pour obtenir la valeur correspondante
        :return: Valeur correspondant a la cle
        """
        return self.view.get(key)

    def get_grid(self, key: str):
        """
        Renvoie la donnee de la grille qui correspond a la cle.
        :param key: Cle pour obtenir la valeur correspondante
        :return: Valeur correspondant a la cle
        """
        return self.grid.get(key)

    def get_extension(self, key: str):
        """
        Renvoie l'extension qui correspond a la cle.
        Si key == 'value': renvoie toutes les valeurs
        :param key: Cle pour obtenir la valeur correspondante
        :return: Valeur correspondant a la cle
        """
        if key == 'value':
            return self.extensions.values()  # Renvoie toutes les extensions
        else:
            return self.extensions.get(key)

    def get_gcrubs(self, key: str):
        """
        Renvoie la donnee de la partie sequentielle qui correspond a la cle.
        :param key: Cle pour obtenir la valeur correspondante
        :return: Valeur correspondant a la cle
        """
        return self.gcrubs.get(key)

    def get_run(self, key: str):
        """
        Renvoie la donnee de la partie simulation qui correspond a la cle.
        :param key: Cle pour obtenir la valeur correspondante
        :return: Valeur correspondant a la cle
        """
        return self.run.get(key)
