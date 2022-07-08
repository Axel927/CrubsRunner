# !/usr/bin/env python3
# -*- coding: utf-8 -*-
# Created by Axel Tremaudant on 07/07/2022

import element
import data
import ui


class Board(element.CoordSys):
    def __init__(self, save_data: data.SaveData, parent):
        super(Board, self).__init__(save_data)

        self.parent = parent
        self.file = self.init_data.get_board('file')
        self.name = self.init_data.get_board('name')
        self.window = ui.Board(self.parent, self.save_data, self)

    def properties(self):
        self.window.properties_window()

    def update_(self):
        if self.file == '':
            self.file = self.save_data.get_board('file')
            self.parent.show_stl(self)

        self.setColor(self.save_data.get_board('color'))
        self.set_edge_color(self.save_data.get_board('edge_color'))

    def set_file(self, file: str):
        self.file = file
