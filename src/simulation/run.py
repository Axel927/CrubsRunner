# !/usr/bin/env python3
# -*- coding: utf-8 -*-
# Created by Axel Tremaudant on 01/07/2022

from PySide6 import QtCore, QtWidgets

import ui
import data
import element


# Note : mr mean main robot and sr mean second robot


class Run:
    def __init__(self, save_data: data.SaveData, main_robot: element.Robot, second_robot: element.Robot, parent=None):
        self.save_data = save_data
        self.init_data = data.InitData()
        self.main_robot = main_robot
        self.second_robot = second_robot
        self.ongoing = False
        self.window = None
        self.parent = parent
        self.stop_robot = 0
        self.nb_robot = 0
        self.running = False
        self.mr_active = ""
        self.sr_active = ""

        self.time_move_mr = QtCore.QTimer()
        self.time_move_mr.timeout.connect(self._time_move_mr)
        self.start_time_move_mr = QtCore.QTimer()
        self.start_time_move_mr.timeout.connect(self._start_time_mr)
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self._timer)
        self.time = -2.
        self.time_move_sr = QtCore.QTimer()
        self.time_move_sr.timeout.connect(self._time_move_sr)
        self.start_time_move_sr = QtCore.QTimer()
        self.start_time_move_sr.timeout.connect(self._start_time_sr)
        self.sleep_mr = QtCore.QTimer()
        self.sleep_mr.timeout.connect(self._stop_sleep_mr)
        self.sleep_sr = QtCore.QTimer()
        self.sleep_sr.timeout.connect(self._stop_sleep_sr)

        self.nb_time_mr = 0
        self.dist_per_time_mr = 0
        self.rest_mr = 0
        self.number_command_mr = 0
        self.nb_time_sr = 0
        self.dist_per_time_sr = 0
        self.rest_sr = 0
        self.number_command_sr = 0
        self.main_robot_file = list()
        self.second_robot_file = list()
        self.move_cmd_mr = None
        self.last_move_mr = None
        self.move_cmd_sr = None
        self.last_move_sr = None
        self.mr_end = True
        self.sr_end = True
        self.timing_mr = False
        self.timing_sr = False

    def set_main_robot(self, rbt: element.Robot):
        self.main_robot = rbt

    def set_second_robot(self, rbt: element.Robot):
        self.second_robot = rbt

    def is_ongoing(self) -> bool:
        return self.ongoing

    def is_running(self) -> bool:
        return self.running

    def stop(self):
        self.timer.stop()
        if self.time_move_mr.isActive():
            self.time_move_mr.stop()
            self.mr_active = "move"
        elif self.sleep_mr.isActive():
            self.sleep_mr.stop()
            self.mr_active = "sleep"

        if self.time_move_sr.isActive():
            self.time_move_sr.stop()
            self.sr_active = "move"
        elif self.sleep_sr.isActive():
            self.sleep_sr.stop()
            self.sr_active = "sleep"
        self.running = False

    def resume(self):
        self.running = True
        self.timer.start()
        if self.mr_active == "move":
            self.time_move_mr.start(self.init_data.get_gcrubs('period'))
        elif self.mr_active == "sleep":
            self.sleep_mr.start()

        if self.sr_active == "move":
            self.time_move_sr.start(self.init_data.get_gcrubs('period'))
        elif self.sr_active == "sleep":
            self.sleep_sr.start()

    def finish(self):
        self.stop()
        self._stop()

    def run(self):
        self.window = ui.Run(self.save_data, self.parent)
        self.time = -2
        self.stop_robot = 0
        self.nb_robot = 0
        self.ongoing = True
        if self.main_robot.is_running():
            self.go_to_start(self.main_robot)
            self.mr_end = False
            self.nb_robot += 1
            try:
                with open(self.main_robot.get_gcrubs_file(), 'r') as file:
                    self.main_robot_file = file.readlines()
            except FileNotFoundError:
                QtWidgets.QMessageBox(self.init_data.get_window('error_open_file_type'),
                                      self.init_data.get_window('error_open_file_title'),
                                      self.init_data.get_window('error_open_file_message').format(
                                          filename=file)).exec()
                self.finish()
                return
            self.start_time_move_mr.start(self.init_data.get_run('time_before_start'))
        if self.second_robot.is_running():
            self.go_to_start(self.second_robot)
            self.sr_end = False
            self.nb_robot += 1
            try:
                with open(self.second_robot.get_gcrubs_file(), 'r') as file:
                    self.second_robot_file = file.readlines()
            except FileNotFoundError:
                QtWidgets.QMessageBox(self.init_data.get_window('error_open_file_type'),
                                      self.init_data.get_window('error_open_file_title'),
                                      self.init_data.get_window('error_open_file_message').format(
                                          filename=file)).exec()
                self.finish()
                return
        self.start_time_move_sr.start(self.init_data.get_run('time_before_start'))

        self.running = True
        self.timer.start(self.init_data.get_run('timer_refresh'))

    def _timer(self):
        self.time += self.init_data.get_run('timer_refresh') / 1000
        self.window.set_time(self.time)

    def _start_time_mr(self):
        self.start_time_move_mr.stop()
        self.next_command_mr()

    def _time_move_mr(self):
        self.timing_mr = True
        if self.nb_time_mr > 0:
            eval(self.move_cmd_mr)
            self.nb_time_mr -= 1
        elif self.nb_time_mr == 0:
            self.nb_time_mr -= 1
            eval(self.last_move_mr)
        else:
            self.time_move_mr.stop()
            self.next_command_mr()

    def next_command_mr(self):
        self.timing_mr = False
        if self.number_command_mr < len(self.main_robot_file):
            if not self.mr_end:
                if self.number_command_mr == len(self.main_robot_file) - 1:
                    self.mr_end = True
                cmd = self.main_robot_file[self.number_command_mr]
                self.window.set_mr_command(cmd)
                self.moving(cmd, self.main_robot)
            self.number_command_mr += 1
        else:
            self.main_robot.set_running(False)
            self._stop()
            return

        if not self.timing_mr:
            self.next_command_mr()

    def _stop(self):
        self.stop_robot += 1
        if self.stop_robot == self.nb_robot:
            self.timer.stop()
            self.ongoing = False
            self.main_robot.set_running(False)
            self.second_robot.set_running(False)
            self.parent.run_action.setIcon(self.init_data.get_run('run_action_icon_stopped'))
            self.parent.stop_run_action.setEnabled(False)

    def _start_time_sr(self):
        self.start_time_move_sr.stop()
        self.next_command_sr()

    def _time_move_sr(self):
        self.timing_sr = True
        if self.nb_time_sr > 0:
            eval(self.move_cmd_sr)
            self.nb_time_sr -= 1
        elif self.nb_time_sr == 0:
            self.nb_time_sr -= 1
            eval(self.last_move_sr)
        else:
            self.time_move_sr.stop()
            self.next_command_sr()

    def next_command_sr(self):
        self.timing_sr = False
        if self.number_command_sr < len(self.second_robot_file):
            if not self.sr_end:
                if self.number_command_sr == len(self.second_robot_file) - 1:
                    self.sr_end = True
                cmd = self.second_robot_file[self.number_command_sr]
                self.window.set_sr_command(cmd)
                self.moving(cmd, self.second_robot)
            self.number_command_sr += 1
        else:
            self.second_robot.set_running(False)
            self._stop()
            return

        if not self.timing_sr:
            self.next_command_sr()

    def _sleep_mr(self, time: float):
        self.sleep_mr.start(time * 1000)

    def _stop_sleep_mr(self):
        self.sleep_mr.stop()
        self.next_command_mr()

    def _sleep_sr(self, time: float):
        self.sleep_sr.start(time * 1000)
        self.next_command_sr()

    def _stop_sleep_sr(self):
        self.sleep_sr.stop()

    def moving(self, cmd: str, rbt: element.Robot):
        name = self.save_data.get_gcrubs('cmd_name')  # On recupere les commandes
        if cmd == "\n":  # Si ligne vide
            return

        if name.get('Commentaire') == cmd[:len(name.get('Commentaire'))]:  # Si c'est un commentaire
            return

        sep = name.get('Pause').find('{')
        if cmd[:sep] == name.get('Pause')[:sep]:
            end_sep = sep
            for char in cmd[sep:]:
                if not char.isdigit() and char != '.':  # Si ce n'est pas un nombre
                    break
                end_sep += 1

            if rbt.is_main_robot():
                self._sleep_mr(float(cmd[sep:end_sep]))
                self.timing_mr = True
            else:
                self._sleep_sr(float(cmd[sep:end_sep]))
                self.timing_sr = True
            return

        sep = name.get('Se deplacer en avant').find('{')
        if cmd[:sep] == name.get('Se deplacer en avant')[:sep]:
            self.move(rbt, cmd, 'Se deplacer en avant', sep)
            return

        sep = name.get('Se deplacer en arriere').find('{')
        if cmd[:sep] == name.get('Se deplacer en arriere')[:sep]:
            self.move(rbt, cmd, 'Se deplacer en arriere', sep)
            return

        sep = name.get('Tourner a droite').find('{')
        if cmd[:sep] == name.get('Tourner a droite')[:sep]:
            self.move(rbt, cmd, 'Tourner a droite', sep)
            return

        sep = name.get('Tourner a gauche').find('{')
        if cmd[:sep] == name.get('Tourner a gauche')[:sep]:
            self.move(rbt, cmd, 'Tourner a gauche', sep)
            return

        for key, value in zip(self.save_data.get_gcrubs('cmd_key').keys(),
                              self.save_data.get_gcrubs('cmd_key').values()):
            if value == QtCore.Qt.Key_Up and (key != 'Se deplacer en avant' or key != 'Se deplacer en arriere'):
                sep = name.get(key).find('{')
                if cmd[:sep] == name.get(key)[:sep]:
                    self.move(rbt, cmd, key, sep)
                    return
            elif value == QtCore.Qt.Key_Down and (key != 'Se deplacer en avant' or key != 'Se deplacer en arriere'):
                sep = name.get(key).find('{')
                if cmd[:sep] == name.get(key)[:sep]:
                    self.move(rbt, cmd, key, sep)
                    return
            elif value == QtCore.Qt.Key_Right and (key != 'Se deplacer en avant' or key != 'Se deplacer en arriere'):
                sep = name.get(key).find('{')
                if cmd[:sep] == name.get(key)[:sep]:
                    self.move(rbt, cmd, key, sep)
                    return
            elif value == QtCore.Qt.Key_Left and (key != 'Se deplacer en avant' or key != 'Se deplacer en arriere'):
                sep = name.get(key).find('{')
                if cmd[:sep] == name.get(key)[:sep]:
                    self.move(rbt, cmd, key, sep)
                    return

    def move(self, rbt: element.Robot, cmd: str, key: str, sep: int):
        self.timing_mr = True
        self.timing_sr = True
        cmd_key = self.save_data.get_gcrubs('cmd_key')
        rotation = False

        if cmd_key.get(key) == self.save_data.get_gcrubs('keys').get('go_up'):
            move_cmd = ".move_robot(0, {dist_per_time}, 0)"
            last_move = ".move_robot(0, {rest}, 0)"
        elif cmd_key.get(key) == self.save_data.get_gcrubs('keys').get('go_down'):
            move_cmd = ".move_robot(0, -{dist_per_time}, 0)"
            last_move = ".move_robot(0, -{rest}, 0)"
        elif cmd_key.get(key) == self.save_data.get_gcrubs('keys').get('go_right'):
            move_cmd = ".move_robot({dist_per_time}, 0, 0)"
            last_move = ".move_robot({rest}, 0, 0)"
        elif cmd_key.get(key) == self.save_data.get_gcrubs('keys').get('go_left'):
            move_cmd = ".move_robot(-{dist_per_time}, 0, 0)"
            last_move = ".move_robot(-{rest}, 0, 0)"
        elif cmd_key.get(key) == self.save_data.get_gcrubs('keys').get('turn_right'):
            rotation = True
            move_cmd = ".move_robot(0, 0, -{dist_per_time})"
            last_move = ".move_robot(0, 0, -{rest})"
        elif cmd_key.get(key) == self.save_data.get_gcrubs('keys').get('turn_left'):
            rotation = True
            move_cmd = ".move_robot(0, 0, {dist_per_time})"
            last_move = ".move_robot(0, 0, {rest})"
        else:
            if rbt.is_main_robot():
                self.timing_mr = False
            else:
                self.timing_sr = False
            return

        if rbt.is_main_robot():
            if rotation:
                self.dist_per_time_mr = rbt.get_speed_rotation() * self.init_data.get_gcrubs('period') / 1000
            else:
                self.dist_per_time_mr = rbt.get_speed() * self.init_data.get_gcrubs('period') / 1000
            end_sep = sep
            for char in cmd[sep:]:
                if not char.isdigit():
                    break
                end_sep += 1
            if self.dist_per_time_mr != 0:
                self.nb_time_mr = int(cmd[sep:end_sep]) // self.dist_per_time_mr
            else:
                self.nb_time_mr = 0
            self.rest_mr = int(cmd[sep:end_sep]) - self.nb_time_mr * self.dist_per_time_mr
            self.time_move_mr.start(self.init_data.get_gcrubs('period'))
            self.move_cmd_mr = "self.main_robot" + move_cmd.format(dist_per_time="self.dist_per_time_mr")
            self.last_move_mr = "self.main_robot" + last_move.format(rest="self.rest_mr")
        else:
            if rotation:
                self.dist_per_time_sr = rbt.get_speed_rotation() * self.init_data.get_gcrubs('period') / 1000
            else:
                self.dist_per_time_sr = rbt.get_speed() * self.init_data.get_gcrubs('period') / 1000
            end_sep = sep
            for char in cmd[sep:]:
                if not char.isdigit():
                    break
                end_sep += 1
            if self.dist_per_time_sr != 0:
                self.nb_time_sr = int(cmd[sep:end_sep]) // self.dist_per_time_sr
            else:
                self.nb_time_sr = 0
            self.rest_sr = int(cmd[sep:end_sep]) - self.nb_time_sr * self.dist_per_time_sr
            self.time_move_sr.start(self.init_data.get_gcrubs('period'))
            self.move_cmd_sr = "self.second_robot" + move_cmd.format(dist_per_time="self.dist_per_time_sr")
            self.last_move_sr = "self.second_robot" + last_move.format(rest="self.rest_sr")

    @staticmethod
    def go_to_start(rbt: element.Robot):
        if rbt.get_gcrubs_file() == "":
            return

        with open(rbt.get_gcrubs_file(), 'r') as file:
            line = file.readline()
            while line.find(" Position de depart : ") == -1:
                line = file.readline()

        coord = [0., 0., 0]  # x, y, angle

        coord[0] = float(line[line.find("x = ") + 4:line.find(" mm")])  # Obtention de x
        line = line[line.find(" mm") + 4:]

        coord[1] = float(line[line.find("y = ") + 4:line.find(" mm")])  # Obtention de y
        line = line[line.find(" mm") + 4:]

        coord[2] = float(line[line.find("angle = ") + 8:line.find(" degres")])  # Obtention de l'angle

        rbt.move_robot(0, 0, -rbt.get_angle())
        rbt.move_robot(coord[0] - rbt.get_coord()[0], coord[1] - rbt.get_coord()[1], coord[2] - rbt.get_angle())
