# !/usr/bin/env python3
# -*- coding: utf-8 -*-
# Created by Axel Tremaudant on 07/07/2022

from PySide6 import QtCore
from data.initData import InitData


class SaveData:
    def __init__(self):
        self.init_data = InitData()

        self.window = {
            'directory': "",
            'project_file': ""
        }

        self.grid = {
            'height': self.init_data.get_grid('spacing_height'),
            'width': self.init_data.get_grid('spacing_width'),
            'transparency': self.init_data.get_grid('transparency'),
            'color': self.init_data.get_grid('color'),
            'visible': self.init_data.get_grid('visible'),

            'coord_sys_visible': self.init_data.get_grid('coord_sys_visible'),
            'moving_speed': 10
        }

        self.board = {
            'file': "",
            'color': self.init_data.get_board('color'),
            'edge_color': self.init_data.get_board('edge_color')
        }

        self.main_robot = {
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
            'start_position': (0, 0, 0)  # x, y, angle
        }

        self.second_robot = {
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
            'start_position': (0, 0, 0)  # x, y, angle
        }

        self.gcrubs = {
            'cmd_name': {
                'Commentaire': ";;",
                'Pause': "ts;;{temps};;",
                "Se deplacer en avant": "cm;;8;;{dist};;",
                "Se deplacer en arriere": "cm;;2;;{dist};;",
                "Tourner a droite": "cm;;5;;{angle};;",
                "Tourner a gauche": "cm;;0;;{angle};;",
            },

            'cmd_key': {
                'Commentaire': None,
                'Pause': None,
                "Se deplacer en avant": QtCore.Qt.Key_Up,
                "Se deplacer en arriere": QtCore.Qt.Key_Down,
                "Tourner a droite": QtCore.Qt.Key_D,
                "Tourner a gauche": QtCore.Qt.Key_Q,
            }
        }

    def get_window(self, key: str):
        return self.window.get(key)

    def set_window(self, key: str, value):
        self.window[key] = value

    def get_board(self, key: str):
        return self.board.get(key)

    def set_board(self, key: str, value):
        self.board[key] = value

    def get_main_robot(self, key: str):
        return self.main_robot.get(key)

    def set_main_robot(self, key: str, value):
        self.main_robot[key] = value

    def get_second_robot(self, key: str):
        return self.second_robot.get(key)

    def set_second_robot(self, key: str, value):
        self.second_robot[key] = value

    def get_grid(self, key: str):
        return self.grid.get(key)

    def set_grid(self, key: str, value):
        if key == 'transparency':
            self.grid['color'] = (
                self.grid.get('color')[0], self.grid.get('color')[1], self.grid.get('color')[2], value)

        self.grid[key] = value

    def get_gcrubs(self, key: str):
        return self.gcrubs.get(key)

    def set_gcrubs(self, key: str, value):
        if value != dict():  # Si c'est pas un dico vide
            self.gcrubs[key] = value

    def save(self, to_save):
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
                ans += str(key) + " = '" + str(value) + "'\n"

        elif to_save == 'second_robot':
            ans = self.init_data.get_window('second_robot_first_line')
            for key, value in zip(self.second_robot.keys(), self.second_robot.values()):
                ans += str(key) + " = '" + str(value) + "'\n"

        elif to_save == 'grid':
            ans = self.init_data.get_window('grid_first_line')
            for key, value in zip(self.grid.keys(), self.grid.values()):
                ans += str(key) + " = '" + str(value) + "'\n"

        elif to_save == 'gcrubs':
            ans = self.init_data.get_window('gcrubs_first_line')
            for key, value in zip(self.gcrubs.keys(), self.gcrubs.values()):
                ans += str(key) + " = " + str(value) + "\n"

        return ans

    def get_len_cmd(self) -> int:
        return len(self.gcrubs.get('cmd_name'))

    def get_len(self, dictionary: str) -> int:
        if dictionary == 'window':
            return len(self.window)
        elif dictionary == 'board':
            return len(self.board)
        elif dictionary == 'main_robot':
            return len(self.main_robot)
        elif dictionary == 'second_robot':
            return len(self.second_robot)
        elif dictionary == 'grid':
            return len(self.grid)
        elif dictionary == 'gcrubs':
            return len(self.gcrubs)
        else:
            return 0
