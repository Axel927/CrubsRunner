# !/usr/bin/env python3
# -*- coding: utf-8 -*-
# Created by Axel Tremaudant on 07/07/2022

import pyqtgraph.opengl as gl
from data.saveData import SaveData
from data.initData import InitData


class CoordSys(gl.GLMeshItem):
    def __init__(self, save_data: SaveData):
        super(CoordSys, self).__init__(smooth=True, drawFaces=True, drawEdges=True)
        self.save_data = save_data
        self.init_data = InitData()
        self.file = self.init_data.get_view('file')
        self.name = self.init_data.get_view('coord_sys_name')
        self.element_type = ""
        self.dimensions = [0., 0., 0.]
        self.min_max = [[0., 0.], [0., 0.], [0., 0.]]

    def set_file(self, file: str):
        self.file = file

    def get_file(self) -> str:
        return self.file

    def get_dimensions(self) -> list:
        return self.dimensions

    def set_dimensions(self, dimensions: list):
        self.dimensions = dimensions

    def get_min_max(self) -> list:
        return self.min_max

    def set_min_max(self, min_max: list):
        self.min_max = min_max

    def set_name(self, name: str):
        self.name = name

    def get_name(self) -> str:
        return self.name

    def set_edge_color(self, color):
        self.opts['edgeColor'] = color
        self.update()

    def get_element_type(self) -> str:
        return self.element_type

    def set_element_type(self, element_type: str):
        self.element_type = element_type

    def update_(self):
        self.setVisible(self.save_data.get_grid('coord_sys_visible'))
