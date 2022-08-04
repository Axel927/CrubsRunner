# !/usr/bin/env python3
# -*- coding: utf-8 -*-
# Created by Axel Tremaudant on 07/07/2022

"""
Fichier contenant toutes les valeurs utiles pendant le programme et qui peuvent etre modifiees durant l'utilisation.
Ces valeurs sont celles qui sont ecrites dans les fichiers de sauvegarde.
"""

from PySide6 import QtCore
import numpy as np

from src import data


class Save:
    def __init__(self):
        self.init_data = data.Init()
        self.settings = QtCore.QSettings('Crubs', 'CrubsRunner')

        self.window = {  # Donnees du projet
            'directory': self.settings.value('directory', ''),
            'project_file': ""
        }

        self.grid = {  # Donnees de la grille
            'height': self.init_data.get_grid('spacing_height'),
            'width': self.init_data.get_grid('spacing_width'),
            'transparency': self.init_data.get_grid('transparency'),
            'color': self.init_data.get_grid('color'),
            'visible': self.init_data.get_grid('visible'),

            'coord_sys_visible': self.init_data.get_grid('coord_sys_visible'),
            'moving_speed': 10
        }

        self.board = {  # Donnees du plateau
            'file': "",
            'color': self.init_data.get_board('color'),
            'edge_color': self.init_data.get_board('edge_color'),
            'angle_rotation': 0,
            'axis_rotation': 'x',
            'offset': 0
        }

        self.vinyl = {
            'file': "",
            'pixel_height': 0,
            'pixel_width': 0
        }

        self.main_robot = {  # Donnees du robot principal
            'file': "",
            'color': self.init_data.get_main_robot('color'),
            'edge_color': self.init_data.get_main_robot('edge_color'),
            'angle_rotation': 0,
            'axis_rotation': 'x',
            'offset': 0,
            'speed': 200,
            'speed_rotation': 45,
            'gcrubs_file': "",
            'sequence': "",
            'start_position': np.zeros(shape=3, dtype='float')  # x, y, angle
        }

        self.second_robot = {  # Donnees du robot secondaire
            'file': "",
            'color': self.init_data.get_second_robot('color'),
            'edge_color': self.init_data.get_second_robot('edge_color'),
            'angle_rotation': 0,
            'axis_rotation': 'x',
            'offset': 0,
            'speed': 200,
            'speed_rotation': 45,
            'gcrubs_file': "",
            'sequence': "",
            'start_position': np.zeros(shape=3, dtype='float')  # x, y, angle
        }

        self.gcrubs = {  # Donnees concernant la sequence
            'cmd_name': {  # Associe le nom de la commande avec la commande
                'Commentaire': ";;",
                'Pause': "ts;;{temps};;",
                "Se deplacer en avant": "cm;;8;;{dist};;",
                "Se deplacer en arriere": "cm;;2;;{dist};;",
                "Tourner a droite": "cm;;5;;{angle};;",
                "Tourner a gauche": "cm;;0;;{angle};;",
            },

            'cmd_key': {  # Associe le nom de la commande avec son raccourcis clavier
                'Commentaire': None,
                'Pause': None,
                "Se deplacer en avant": QtCore.Qt.Key_Up,
                "Se deplacer en arriere": QtCore.Qt.Key_Down,
                "Tourner a droite": QtCore.Qt.Key_D,
                "Tourner a gauche": QtCore.Qt.Key_Q,
            },

            'keys': {  # Associe la direction dans laquelle doit se deplacer le robot avec sa touche du clavier
                'go_right': QtCore.Qt.Key_Right,
                'go_left': QtCore.Qt.Key_Left,
                'go_up': QtCore.Qt.Key_Up,
                'go_down': QtCore.Qt.Key_Down,
                'turn_right': QtCore.Qt.Key_D,
                'turn_left': QtCore.Qt.Key_Q
            }
        }

    def get_window(self, key: str):
        """
        Renvoie la donnee de la fenetre principale qui correspond a la cle.
        :param key: str: Cle pour obtenir la valeur correspondante
        :return: any: Valeur correspondant a la cle
        """
        return self.window.get(key)

    def set_window(self, key: str, value):
        """
        Definit la valeur value a la cle key pour ce qui concerne le projet en general.
        :param key: str: Cle a laquelle definir la valeur
        :param value: any: Definit la valeur correspondant a la cle
        :return: None
        """
        self.window[key] = value

    def get_board(self, key: str):
        """
        Renvoie la donnee du plateau qui correspond a la cle.
        :param key: str: Cle pour obtenir la valeur correspondante
        :return: any: Valeur correspondant a la cle
        """
        return self.board.get(key)

    def set_board(self, key: str, value):
        """
        Definit la valeur value a la cle key pour ce qui concerne le plateau.
        :param key: str: Cle a laquelle definir la valeur
        :param value: any: Definit la valeur correspondant a la cle
        :return: None
        """
        self.board[key] = value

    def get_vinyl(self, key: str):
        """
        Renvoie la donnee du tapis qui correspond a la cle.
        :param key: Cle pour obtenir la valeur correspondante
        :return: Valeur correspondant a la cle
        """
        return self.vinyl.get(key)

    def set_vinyl(self, key: str, value):
        """
        Definit la valeur value a la cle key pour ce qui concerne le tapis.
        :param key: str: Cle a laquelle definir la valeur
        :param value: any: Definit la valeur correspondant a la cle
        :return: None
        """
        self.vinyl[key] = value

    def get_main_robot(self, key: str):
        """
        Renvoie la donnee du robot principal qui correspond a la cle.
        :param key: str: Cle pour obtenir la valeur correspondante
        :return: any: Valeur correspondant a la cle
        """
        return self.main_robot.get(key)

    def set_main_robot(self, key: str, value):
        """
        Definit la valeur value a la cle key pour ce qui concerne le robot principal.
        :param key: str: Cle a laquelle definir la valeur
        :param value: any: Definit la valeur correspondant a la cle
        :return: None
        """
        self.main_robot[key] = value

    def get_second_robot(self, key: str):
        """
        Renvoie la donnee du robot secondaire qui correspond a la cle.
        :param key: str: Cle pour obtenir la valeur correspondante
        :return: any: Valeur correspondant a la cle
        """
        return self.second_robot.get(key)

    def set_second_robot(self, key: str, value):
        """
        Definit la valeur value a la cle key pour ce qui concerne le robot secondaire.
        :param key: str: Cle a laquelle definir la valeur
        :param value: any: Definit la valeur correspondant a la cle
        :return: None
        """
        self.second_robot[key] = value

    def get_grid(self, key: str):
        """
        Renvoie la donnee de la grille qui correspond a la cle.
        :param key: str: Cle pour obtenir la valeur correspondante
        :return: any: Valeur correspondant a la cle
        """
        return self.grid.get(key)

    def set_grid(self, key: str, value):
        """
        Definit la valeur value a la cle key pour ce qui concerne la grille.
        :param key: str: Cle a laquelle definir la valeur
        :param value: any: Definit la valeur correspondant a la cle
        :return: None
        """
        if key == 'transparency':
            self.grid['color'] = (*self.grid.get('color')[:3], value)

        self.grid[key] = value

    def get_gcrubs(self, key: str):
        """
        Renvoie la donnee de la partie sequentielle qui correspond a la cle.
        :param key: str: Cle pour obtenir la valeur correspondante
        :return: any: Valeur correspondant a la cle
        """
        return self.gcrubs.get(key)

    def set_gcrubs(self, key: str, value):
        """
        Definit la valeur value a la cle key pour ce qui concerne la partie sequentielle.
        :param key: str: Cle a laquelle definir la valeur
        :param value: any: Definit la valeur correspondant a la cle
        :return: None
        """
        if value != dict():  # Si c'est pas un dico vide
            self.gcrubs[key] = value

    def save(self, to_save: str):
        """
        Renvoie sous forme de string le dictionnaire to_save.
        Si to_save n'est pas dans la liste des dictionnaires, renvoie "".

        Liste des dictionnaires :
            window, board, main_robot, second_robot, grid, gcrubs, vinyl

        :param to_save: str: Dictionnaire que l'on veut sous format str
        :return: str: Dictionnaire sous format str
        """
        ans = ""
        if to_save == 'window':
            ans = self.init_data.get_window('window_first_line')
            for key, value in zip(self.window.keys(), self.window.values()):
                ans += str(key) + " = '" + str(value) + "'\n"

        elif to_save == 'board':
            ans = self.init_data.get_window('board_first_line')
            for key, value in zip(self.board.keys(), self.board.values()):
                ans += str(key) + " = '" + str(value) + "'\n"

        elif to_save == 'main_robot':
            ans = self.init_data.get_window('main_robot_first_line')
            for key, value in zip(self.main_robot.keys(), self.main_robot.values()):
                if key == 'sequence':
                    continue
                else:
                    ans += str(key) + " = '" + str(value) + "'\n"

        elif to_save == 'second_robot':
            ans = self.init_data.get_window('second_robot_first_line')
            for key, value in zip(self.second_robot.keys(), self.second_robot.values()):
                if key == 'sequence':
                    continue
                else:
                    ans += str(key) + " = '" + str(value) + "'\n"

        elif to_save == 'grid':
            ans = self.init_data.get_window('grid_first_line')
            for key, value in zip(self.grid.keys(), self.grid.values()):
                ans += str(key) + " = '" + str(value) + "'\n"

        elif to_save == 'gcrubs':
            ans = self.init_data.get_window('gcrubs_first_line')
            for key, value in zip(self.gcrubs.keys(), self.gcrubs.values()):
                ans += str(key) + " = " + str(value) + "\n"

        elif to_save == 'vinyl':
            ans = self.init_data.get_window('vinyl_first_line')
            for key, value in zip(self.vinyl.keys(), self.vinyl.values()):
                ans += str(key) + " = '" + str(value) + "'\n"

        return ans

    def get_len_cmd(self) -> int:
        """
        Renvoie le nombre de commandes.
        :return: int: Nombre de commandes
        """
        return len(self.gcrubs.get('cmd_name'))

    def get_len(self, dictionary: str) -> int:
        """
        Renvoie le nombre d'elements pour chaque dictionnaire.
        Renvoie 0 si ce n'est pas un des dictionnaires.

        Liste des dictionnaires :
            window, board, main_robot, second_robot, grid, gcrubs, vinyl

        :param dictionary: str: Dictionnaire dont on veut le nombre d'elements
        :return: int : Nombre d'element du dictionnaire
        """
        if dictionary == 'window':
            return len(self.window)
        elif dictionary == 'board':
            return len(self.board)
        elif dictionary == 'main_robot':
            return len(self.main_robot) - 1  # -1 car la sequence n'est pas enregistree
        elif dictionary == 'second_robot':
            return len(self.second_robot) - 1
        elif dictionary == 'grid':
            return len(self.grid)
        elif dictionary == 'gcrubs':
            return len(self.gcrubs)
        elif dictionary == 'vinyl':
            return len(self.vinyl)
        else:
            return 0

    def set_settings(self, key: str, value):
        """
        Enregistre value a key
        :param key: str: Cle de la sauvegarde
        :param value: any: Objet a enregistrer
        :return: None
        """
        self.settings.setValue(key, value)

    def get_init_data(self) -> data.Init:
        """
        Renvoie un pointeur vers les donnees initiales.
        :return: data.Init: donnees
        """
        return self.init_data
