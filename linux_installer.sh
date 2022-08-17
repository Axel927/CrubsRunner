# !/bin/bash

# Script bash pour installer CrubsRunner sur Linux

# Executer ce script depuis CrubsRunner_Linux

echo "Copie des fichiers vers /home/$USER/CrubsRunner"
mkdir /home/"$USER"/CrubsRunner
mv icon/ /home/"$USER"/CrubsRunner
mv 3d_files/ /home/"$USER"/CrubsRunner

mv CrubsRunner ..

echo "Suppression du dossier CrubsRunner_Linux"
cd ..
rm -r CrubsRunner_Linux
echo "Installation terminee"

