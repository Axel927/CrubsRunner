# !/usr/bin/python3
# -*- coding: utf-8 -*-
# Created by Axel Tremaudant on 07/06/2022

import sys
import mainWindow
from PySide6.QtWidgets import QApplication
from data import InitData

if __name__ == '__main__':
    app = QApplication()

    init_data = InitData()

    window = mainWindow.MainWindow()
    window.resize(init_data.get_window('window_start_width'), init_data.get_window('window_start_height'))
    window.show()

    sys.exit(app.exec())
