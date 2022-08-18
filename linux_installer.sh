#!/bin/bash

# Script bash pour installer CrubsRunner sur Linux

directory=$(dirname "$PWD/$0") # Recuperation du dossier actuel

echo "Copie des fichiers vers /home/$USER/.CrubsRunner"
mkdir /home/"$USER"/.CrubsRunner
mv "$directory"/icon/ /home/"$USER"/.CrubsRunner
mv "$directory"/3d_files/ /home/"$USER"/.CrubsRunner

mv "$directory"/CrubsRunner "$directory"/..

echo "Suppression du dossier CrubsRunner_Linux"
rm -r "$directory"
echo "Installation terminee"
