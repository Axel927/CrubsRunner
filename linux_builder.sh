# !/bin/bash

# Script bash pour la distribution de CrubsRunner sur Linux

# Executer ce script depuis CrubsRunner

rm -rf build dist
echo python3 -m PyInstaller setup.spec
python3 -m PyInstaller setup.spec

echo "Copie des fichiers et dossier vers CrubsRunner_Linux"
mkdir CrubsRunner_Linux
cp dist/CrubsRunner CrubsRunner_Linux/CrubsRunner
cp -r icon/ CrubsRunner_Linux/icon/
cp -r 3d_files/ CrubsRunner_Linux/3d_files/
cp linux_installer.sh CrubsRunner_Linux/linux_installer.sh

echo "Compression du dossier"
tar -zcvf CrubsRunner_Linux_v1.1.0.tar.gz CrubsRunner_Linux
echo "Construction terminee"

