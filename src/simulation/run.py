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
Fichier contenant la classe Run.
"""

from PyQt5 import QtCore, QtWidgets, QtGui
import numpy as np
from sys import path

from src import ui
from src import element


# Note : mr mean main robot and sr mean second robot


class Run:
    """
    Classe pour la simulation des deplacements des robots.
    """

    def __init__(self, save_data, main_robot: element.Robot, second_robot: element.Robot, parent=None):
        """
        Constructeur de Run.
        :param save_data: data.Save: Les donnees de sauvegarde y sont recuperees et ecrites
        :param main_robot: element.Robot: Robot principal
        :param second_robot: element.Robot: Robot secondaire
        :param parent: ui.MainWindow: Fenetre principale
        """

        self.save_data = save_data
        self.init_data = self.save_data.get_init_data()
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
        self.time = -self.init_data.get_run("time_before_start") / 1000  # Conversion en secondes
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
        self.timing_mr = False
        self.timing_sr = False
        self.refresh_time = 100

    def set_main_robot(self, rbt: element.Robot):
        """
        Definit le robot principal.
        :param rbt: element.Robot: main_robot
        :return: None
        """
        self.main_robot = rbt

    def set_second_robot(self, rbt: element.Robot):
        """
        Definit le robot secondaire.
        :param rbt: element.Robot: second_robot
        :return: None
        """
        self.second_robot = rbt

    def is_ongoing(self) -> bool:
        """
        Indique si une simulation est en cours.
        :return: bool: ongoing
        """
        return self.ongoing

    def is_running(self) -> bool:
        """
        Indique si la simulation est en pause ou non.
        :return: bool: running
        """
        return self.running

    def stop(self):
        """
        Met la simulation en pause.
        :return: None
        """
        self.timer.stop()  # Arret du chrono
        if self.time_move_mr.isActive():  # Pour le robot principal
            self.time_move_mr.stop()  # Arret du deplacement
            self.mr_active = "move"  # Enregistre l'action en tant que mouvement
        elif self.sleep_mr.isActive():
            self.sleep_mr.stop()  # Arret du sleep
            self.mr_active = "sleep"  # Enregistre l'action en tant que sleep

        if self.time_move_sr.isActive():  # Pour le robot secondaire
            self.time_move_sr.stop()
            self.sr_active = "move"
        elif self.sleep_sr.isActive():
            self.sleep_sr.stop()
            self.sr_active = "sleep"
        self.running = False

    def set_refresh_time(self):
        """
        Calcule le temps de rafraichissement entre chaque action pour une simulation optimale. Affecte la valeur a
        self.refresh_time
        :return: None
        """
        from time import time

        display_time = np.zeros(50)
        begin = time()
        i = 0

        if self.main_robot.is_running():
            # Tant que display_time n'est pas rempli ou que la condition de temps n'est pas passee
            while time() - begin < self.init_data.get_run('time_for_refresh_estimation') and i < len(display_time):
                start = time()
                self.main_robot.move_robot(0, 0, -1)  # On fait tourner le robot de 1 degre sur la droite
                self.parent.viewer.paintGL()  # On affiche la position
                display_time[i] = time() - start

                start = time()
                self.main_robot.move_robot(0, 0, 1)
                self.parent.viewer.paintGL()
                display_time[i + 1] = time() - start
                i += 2

        elif self.second_robot.is_running():
            while time() - begin < self.init_data.get_run('time_for_refresh_estimation') and i < len(display_time):
                start = time()
                self.second_robot.move_robot(0, 0, -1)
                self.parent.viewer.paintGL()
                display_time[i] = time() - start

                start = time()
                self.second_robot.move_robot(0, 0, 1)
                self.parent.viewer.paintGL()
                display_time[i + 1] = time() - start
                i += 2

        # Convertit la duree en ms et en ajoute encore un peu
        self.refresh_time = np.ceil(display_time.max() * 1000 + self.init_data.get_run('added_time_refresh_time'))

    def resume(self):
        """
        Reprend la simulation ou elle en etait.
        :return: None
        """
        self.running = True
        self.timer.start()  # Relance le chrono
        if self.mr_active == "move":
            self.time_move_mr.start(self.refresh_time)
        elif self.mr_active == "sleep":
            self.sleep_mr.start()

        if self.sr_active == "move":
            self.time_move_sr.start(self.refresh_time)
        elif self.sr_active == "sleep":
            self.sleep_sr.start()

    def finish(self):
        """
        Arrete completement la simulation.
        :return: None
        """
        self.stop()
        self._stop()

    def run(self):
        """
        Demarre la simulation.
        :return: None
        """
        self.window = ui.Run(self.parent)
        self.time = -2
        self.stop_robot = 0
        self.nb_robot = 0
        self.ongoing = True
        mr_theoretical_time = 0.
        sr_theoretical_time = 0.

        if self.main_robot.is_running():  # Si le robot principal fait la simulation
            self.nb_robot += 1
            try:
                with open(self.main_robot.get_gcrubs_file(), 'r') as file:  # Lit les instructions
                    self.main_robot_file = file.readlines()
                    for line in self.main_robot_file:
                        if self.init_data.get_main_robot('position_text') in line:
                            self.go_to_start(self.main_robot, line)  # Place le robot au point de depart
                            break

            except FileNotFoundError:
                QtWidgets.QMessageBox(self.init_data.get_window('error_open_file_type'),
                                      self.init_data.get_window('error_open_file_title'),
                                      self.init_data.get_window('error_open_file_message').format(
                                          filename=file)).exec()
                self.finish()
                return
            mr_theoretical_time = self.calculate_theoretical_time(self.main_robot, self.main_robot_file, self.save_data)

        if self.second_robot.is_running():  # Si le robot secondaire fait la simulation
            self.nb_robot += 1
            try:
                with open(self.second_robot.get_gcrubs_file(), 'r') as file:  # Lit les instructions
                    self.second_robot_file = file.readlines()
                    for line in self.second_robot_file:
                        if self.init_data.get_main_robot('position_text') in line:
                            self.go_to_start(self.second_robot, line)  # Place le robot au point de depart
                            break

            except FileNotFoundError:
                QtWidgets.QMessageBox(self.init_data.get_window('error_open_file_type'),
                                      self.init_data.get_window('error_open_file_title'),
                                      self.init_data.get_window('error_open_file_message').format(
                                          filename=file)).exec()
                self.finish()
                return
            sr_theoretical_time = self.calculate_theoretical_time(self.second_robot, self.second_robot_file,
                                                                  self.save_data)

        self.running = True
        self.window.set_theoretical_time(max(mr_theoretical_time, sr_theoretical_time))
        self.set_refresh_time()
        self.start_time_move_mr.start(self.init_data.get_run('time_before_start') /
                                      self.init_data.get_window('speed_simulation_btn_values')[
                                          self.parent.speed_simulation_btn_nb])
        self.start_time_move_sr.start(self.init_data.get_run('time_before_start') /
                                      self.init_data.get_window('speed_simulation_btn_values')[
                                          self.parent.speed_simulation_btn_nb])
        self.timer.start(
            self.init_data.get_run('timer_refresh') / self.init_data.get_window('speed_simulation_btn_values')[
                self.parent.speed_simulation_btn_nb])  # Demarre le chrono

    def _timer(self):
        """
        Affiche le temps qui s'ecoule.
        :return: None
        """
        self.time += self.init_data.get_run('timer_refresh') / 1000
        self.window.set_time(self.time)

    def _start_time_mr(self):
        """
        Demarre la simulation du robot principal.
        :return: None
        """
        self.start_time_move_mr.stop()
        self.next_command_mr()

    def _time_move_mr(self):
        """
        Fait bouger le robot principal.
        :return: None
        """
        self.timing_mr = True
        if self.nb_time_mr > 0:
            self.main_robot.move_robot(*self.move_cmd_mr)
            self.nb_time_mr -= 1
        elif self.nb_time_mr == 0:
            self.nb_time_mr -= 1
            self.main_robot.move_robot(*self.last_move_mr)
        else:
            self.time_move_mr.stop()
            self.next_command_mr()

    def next_command_mr(self):
        """
        Lit la commande suivante pour le robot principal.
        :return: None
        """
        self.timing_mr = False
        if self.number_command_mr < len(self.main_robot_file):  # S'il reste des commandes
            cmd = self.main_robot_file[self.number_command_mr]  # Recupere la commande
            self.window.set_mr_command(cmd)  # Affiche la commande
            self.moving(cmd, self.main_robot)  # Agit
            self.number_command_mr += 1
        else:  # Sinon arret
            self.main_robot.set_running(False)
            self._stop()
            return

        if not self.timing_mr:  # Si une commande qui prend du temps n'est pas en cours
            self.next_command_mr()

    def _stop(self):
        """
        Fin de la simulation.
        :return: None
        """
        self.stop_robot += 1
        if self.stop_robot == 2:  # Si tous les robots ont fini
            self.timer.stop()  # Arret du chrono
            self.ongoing = False
            self.main_robot.set_running(False)
            self.second_robot.set_running(False)

            for p in path:
                # noinspection PyBroadException
                try:
                    f = open(p + '/' + self.init_data.get_window("run_action_icon_stopped"), 'r')
                    f.close()
                    self.parent.run_action.setIcon(QtGui.QIcon(p + '/' +
                                                               self.init_data.get_window("run_action_icon_stopped")))
                    break
                except:  # C'est un peu sale mais erreur inconnue en executable
                    continue

            self.parent.stop_run_action.setEnabled(False)

    def _start_time_sr(self):
        """
        Demarre la simulation du robot secondaire.
        :return: None
        """
        self.start_time_move_sr.stop()
        self.next_command_sr()

    def _time_move_sr(self):
        """
        Fait bouger le robot secondaire.
        :return: None
        """
        self.timing_sr = True
        if self.nb_time_sr > 0:
            self.second_robot.move_robot(*self.move_cmd_sr)
            self.nb_time_sr -= 1
        elif self.nb_time_sr == 0:
            self.nb_time_sr -= 1
            self.second_robot.move_robot(*self.last_move_sr)
        else:
            self.time_move_sr.stop()
            self.next_command_sr()

    def next_command_sr(self):
        """
        Lit la commande suivante pour le robot principal.
        :return: None
        """
        self.timing_sr = False
        if self.number_command_sr < len(self.second_robot_file):  # S'il reste des commandes
            cmd = self.second_robot_file[self.number_command_sr]  # Recuperation de la commande
            self.window.set_sr_command(cmd)  # Affichage de la commande
            self.moving(cmd, self.second_robot)  # Agit
            self.number_command_sr += 1
        else:
            self.second_robot.set_running(False)
            self._stop()
            return

        if not self.timing_sr:
            self.next_command_sr()

    def _sleep_mr(self, time: float):
        """
        Le robot principal ne fait plus rien pendant time secondes.
        :param time: float: Duree en secondes
        :return: None
        """
        self.sleep_mr.start(
            time * 1000 / self.init_data.get_window('speed_simulation_btn_values')[self.parent.speed_simulation_btn_nb])

    def _stop_sleep_mr(self):
        """
        Reprise des action du robot principal.
        :return: None
        """
        self.sleep_mr.stop()
        self.next_command_mr()

    def _sleep_sr(self, time: float):
        """
        Le robot secondaire ne fait plus rien pendant time secondes.
        :param time: float: Duree en secondes
        :return: None
        """
        self.sleep_sr.start(time * 1000 / self.init_data.get_window('speed_simulation_btn_values')[
            self.parent.speed_simulation_btn_nb])

    def _stop_sleep_sr(self):
        """
        Reprise des action du robot secondaire.
        :return: None
        """
        self.sleep_sr.stop()
        self.next_command_sr()

    def moving(self, cmd: str, rbt: element.Robot):
        """
        Decide ce que le robot doit faire selon la commande.
        :param cmd: str: Commande
        :param rbt: Robot auquel correspond la commande
        :return: None
        """
        # Si la vitesse de simulation a ete modifiee on change la vitesse d'affichage du temps
        if self.timer.interval() != self.init_data.get_run('timer_refresh') / \
                self.init_data.get_window('speed_simulation_btn_values')[self.parent.speed_simulation_btn_nb]:
            self.timer.stop()
            self.timer.start(self.init_data.get_run('timer_refresh') /
                             self.init_data.get_window('speed_simulation_btn_values')[
                                 self.parent.speed_simulation_btn_nb])

        name = self.save_data.get_gcrubs('cmd_name')  # On recupere les commandes

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

        # Pour toutes les autres commandes, on verifie que la touche correspondante n'est pas la meme
        # qu'une touche definie par un mouvement
        for key, value in zip(self.save_data.get_gcrubs('cmd_key').keys(),
                              self.save_data.get_gcrubs('cmd_key').values()):
            if value == self.save_data.get_gcrubs('keys').get('go_up') and \
                    (key != 'Se deplacer en avant' and key != 'Se deplacer en arriere' and
                     key != 'Tourner a gauche' and key != 'Tourner a droite'):
                sep = name.get(key).find('{')
                if cmd[:sep] == name.get(key)[:sep]:
                    self.move(rbt, cmd, key, sep)
                    return
            elif value == self.save_data.get_gcrubs('keys').get('go_down') and \
                    (key != 'Se deplacer en avant' and key != 'Se deplacer en arriere' and
                     key != 'Tourner a gauche' and key != 'Tourner a droite'):
                sep = name.get(key).find('{')
                if cmd[:sep] == name.get(key)[:sep]:
                    self.move(rbt, cmd, key, sep)
                    return
            elif value == self.save_data.get_gcrubs('keys').get('go_right') and \
                    (key != 'Se deplacer en avant' and key != 'Se deplacer en arriere' and
                     key != 'Tourner a gauche' and key != 'Tourner a droite'):
                sep = name.get(key).find('{')
                if cmd[:sep] == name.get(key)[:sep]:
                    self.move(rbt, cmd, key, sep)
                    return
            elif value == self.save_data.get_gcrubs('keys').get('go_left') and \
                    (key != 'Se deplacer en avant' and key != 'Se deplacer en arriere' and
                     key != 'Tourner a gauche' and key != 'Tourner a droite'):
                sep = name.get(key).find('{')
                if cmd[:sep] == name.get(key)[:sep]:
                    self.move(rbt, cmd, key, sep)
                    return

        sep = name.get('Pause').find('{')
        if cmd[:sep] == name.get('Pause')[:sep]:  # si c'est une pause
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

    def move(self, rbt: element.Robot, cmd: str, key: str, sep: int):
        """
        Deplace le robot.
        :param rbt: element.Robot: Robot qui doit se deplacer
        :param cmd: str: Commande
        :param key: str: Touche correspondant a la commande
        :param sep: int: Position du debut de la distance a lire
        :return: None
        """
        self.timing_mr = True
        self.timing_sr = True
        cmd_key = self.save_data.get_gcrubs('cmd_key')
        rotation = False

        if cmd_key.get(key) == self.save_data.get_gcrubs('keys').get('go_up'):
            move = np.array([0, 1, 0])
        elif cmd_key.get(key) == self.save_data.get_gcrubs('keys').get('go_down'):
            move = np.array([0, -1, 0])
        elif cmd_key.get(key) == self.save_data.get_gcrubs('keys').get('go_right'):
            move = np.array([1, 0, 0])
        elif cmd_key.get(key) == self.save_data.get_gcrubs('keys').get('go_left'):
            move = np.array([-1, 0, 0])
        elif cmd_key.get(key) == self.save_data.get_gcrubs('keys').get('turn_right'):
            rotation = True
            move = np.array([0, 0, -1])
        elif cmd_key.get(key) == self.save_data.get_gcrubs('keys').get('turn_left'):
            rotation = True
            move = np.array([0, 0, 1])
        else:
            if rbt.is_main_robot():
                self.timing_mr = False
            else:
                self.timing_sr = False
            return

        end_sep = sep
        for char in cmd[sep:]:
            if not char.isdigit():
                break  # Obtention de la position de la fin de la valeur
            end_sep += 1

        if rbt.is_main_robot():
            # Calcul de la distance a parcourir a chaque appel de _time_move_mr
            if rotation:
                self.dist_per_time_mr = rbt.get_speed_rotation() * self.refresh_time / 1000 * \
                                        self.init_data.get_window('speed_simulation_btn_values')[
                                            self.parent.speed_simulation_btn_nb]
            else:
                self.dist_per_time_mr = rbt.get_speed() * self.refresh_time / 1000 * \
                                        self.init_data.get_window('speed_simulation_btn_values')[
                                            self.parent.speed_simulation_btn_nb]

            # Calcul du nombre d'appel a _time_move_mr
            self.nb_time_mr = int(cmd[sep:end_sep]) // self.dist_per_time_mr

            # Calcul du reste a parcourir
            self.rest_mr = int(cmd[sep:end_sep]) - self.nb_time_mr * self.dist_per_time_mr

            self.time_move_mr.start(self.refresh_time)
            self.move_cmd_mr = move * self.dist_per_time_mr
            self.last_move_mr = move * self.rest_mr
        else:
            # Calcul de la distance a parcourir a chaque appel de _time_move_sr
            if rotation:
                self.dist_per_time_sr = rbt.get_speed_rotation() * self.refresh_time / 1000 * \
                                        self.init_data.get_window('speed_simulation_btn_values')[
                                            self.parent.speed_simulation_btn_nb]
            else:
                self.dist_per_time_sr = rbt.get_speed() * self.refresh_time / 1000 * \
                                        self.init_data.get_window('speed_simulation_btn_values')[
                                            self.parent.speed_simulation_btn_nb]

            # Calcul du nombre d'appel a _time_move_sr
            self.nb_time_sr = int(cmd[sep:end_sep]) // self.dist_per_time_sr

            # Calcul du reste a parcourir
            self.rest_sr = int(cmd[sep:end_sep]) - self.nb_time_sr * self.dist_per_time_sr

            self.time_move_sr.start(self.refresh_time)
            self.move_cmd_sr = move * self.dist_per_time_sr
            self.last_move_sr = move * self.rest_sr

    @staticmethod
    def go_to_start(rbt: element.Robot, line: str) -> np.array:
        """
        Place le robot au point de depart
        :param rbt: element.Robot: Robot concerne
        :param line: str: Ligne du fichier sequentiel contenant la position de depart
        :return: np.array: Coordonnees du point depart [x, y, angle]
        """
        coord = np.zeros(3, float)  # [x, y, angle]

        coord[0] = float(line[line.find("x = ") + len("x = "):line.find(" mm")])  # Obtention de x
        line = line[line.find(" mm") + len("x = "):]

        coord[1] = float(line[line.find("y = ") + len("y = "):line.find(" mm")])  # Obtention de y
        line = line[line.find(" mm") + len("y = "):]

        coord[2] = float(line[line.find("angle = ") + len("angle = "):line.find(" degres")])  # Obtention de l'angle

        # Place le robot dans l'orientation de depart car move_robot deplace en coordonnees locales
        rbt.move_robot(0, 0, -rbt.get_angle())
        rbt.move_robot(coord[0] - rbt.get_coord()[0], coord[1] - rbt.get_coord()[1], coord[2] - rbt.get_angle())

        return coord

    @staticmethod
    def calculate_theoretical_time(robot: element.Robot, sequence: list, save_data) -> float:
        """
        Calcule le temps theorique que doit passer le robot a executer une sequence.
        Ne gere que les rotations et les deplacements en avant et en arriere.
        Aucun deplacement ajoute n'est pris en compte.
        :param robot: element.Robot: Robot auquel correspond la sequence.
        :param sequence: list: Liste des commandes
        :param save_data: data.Save: Donnees de sauvegardes
        :return: float: Temps en secondes
        """
        time = 0.
        name = save_data.get_gcrubs('cmd_name')  # On recupere les commandes

        for line in sequence:
            sep = name.get('Se deplacer en avant').find('{')
            if line[:sep] == name.get('Se deplacer en avant')[:sep]:
                time += Run.time_from_command(robot, line, sep, 'Se deplacer en avant', save_data)
                continue

            sep = name.get('Se deplacer en arriere').find('{')
            if line[:sep] == name.get('Se deplacer en arriere')[:sep]:
                time += Run.time_from_command(robot, line, sep, 'Se deplacer en arriere', save_data)
                continue

            sep = name.get('Tourner a droite').find('{')
            if line[:sep] == name.get('Tourner a droite')[:sep]:
                time += Run.time_from_command(robot, line, sep, 'Tourner a droite', save_data)
                continue

            sep = name.get('Tourner a gauche').find('{')
            if line[:sep] == name.get('Tourner a gauche')[:sep]:
                time += Run.time_from_command(robot, line, sep, 'Tourner a gauche', save_data)
                continue

            sep = name.get('Pause').find('{')
            if line[:sep] == name.get('Pause')[:sep]:  # si c'est une pause
                end_sep = sep
                for char in line[sep:]:
                    if not char.isdigit() and char != '.':  # Si ce n'est pas un chiffre
                        break
                    end_sep += 1

                time += float(line[sep:end_sep])
                continue

        return time

    @staticmethod
    def time_from_command(robot: element.Robot, cmd: str, sep: int, key: str, save_data) -> float:
        """
        Renvoie le temps necessaire au deplacement du robot selon la distance a parcourir.
        :param robot: element.Robot: Robot dont on veut connaitre le temps de deplacement
        :param cmd: str: Commande sequentielle
        :param sep: int: Position du debut de la distance
        :param key: str: Touche correspondante au deplacement
        :param save_data: data.Save: Donnees de sauvegarde
        :return: float: Temps du deplacement en secondes
        """
        cmd_key = save_data.get_gcrubs('cmd_key')
        if cmd_key.get(key) == save_data.get_gcrubs('keys').get('turn_right') or \
                cmd_key.get(key) == save_data.get_gcrubs('keys').get('turn_left'):
            rotation = True
        elif cmd_key.get(key) == save_data.get_gcrubs('keys').get('go_up') or \
                cmd_key.get(key) == save_data.get_gcrubs('keys').get('go_down') or \
                cmd_key.get(key) == save_data.get_gcrubs('keys').get('go_left') or \
                cmd_key.get(key) == save_data.get_gcrubs('keys').get('go_right'):
            rotation = False
        else:
            return 0.

        end_sep = sep
        for char in cmd[sep:]:
            if not char.isdigit():
                break  # Obtention de la position de la fin de la valeur
            end_sep += 1

        if rotation:
            return int(cmd[sep:end_sep]) / robot.get_speed_rotation()
        else:
            return int(cmd[sep:end_sep]) / robot.get_speed()
