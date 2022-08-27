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
Utilisation :
 * MacOS : python3 setup.py py2app
 * Windows : python setup.py py2exe
"""

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

from sys import setrecursionlimit
from pathlib import Path
from platform import system

setrecursionlimit(1500)
path = Path(__file__).parent.resolve()

VERSION = '1.1.0'

AUTHOR = "Membres du CRUBS : \n" \
          "* Axel Tremaudant \n"

AUTHOR_EMAIL = "axel.tremaudant@gmail.com"

MAINTAINER = "CRUBS"

MAINTAINER_EMAIL = "club.robotique.ubs@gmail.com"

# Tous les paquets utilises dans l'application
INCLUDES = ['src', 'PyQt5', 'PyQt5.QtWidgets', 'PyQt5.QtCore', 'PyQt5.QtGui',
            'numpy', 'trimesh', 'fitz', 'pyqtgraph', 'OpenGL', 'os', 'sys', 'pathlib', 'time', 'PIL', 'platform']

# Packets installes mais inutiles pour l'application,
# cela peut permettre de reduire grandement la taille de l'application
# Normalement inutile de la remplir si vous avez créé un environnement virtuel
# et que vous n'avez pas ajoute de packets inutiles
EXCLUDES = []

if system() == 'Linux':
    print("Pour compiler l'application sur Linux, executez : bash linux_builder.sh")

elif system() == 'Darwin':
    APP = ['src/CrubsRunner.py']
    
    DATA_FILES = ['icon', '3d_files', 'LICENSE']

    OPTIONS = {'iconfile': str(path) + '/icon/icon_app.icns',
               'includes': INCLUDES,
               'excludes': EXCLUDES
               }

    setup(
        app=APP,
        data_files=DATA_FILES,
        options={'py2app': OPTIONS},
        setup_requires=['py2app'],
        version=VERSION,
        author=AUTHOR,
        author_email=AUTHOR_EMAIL,
        maintainer=MAINTAINER,
        maintainer_email=MAINTAINER_EMAIL
    )

elif system() == 'Windows':
    import py2exe
    
    APP = [{'script': str(path) + "\\src\\CrubsRunner.py",
            'icon_resources': [(1, str(path) + "\\icon\\icon_app.ico")]
            }]
            
    DATA_FILES = [('3d_files', str(path) + '\\3d_files'), ('LICENSE', str(path) + '\\LICENSE'),
                  ('icon', str(path) + '\\icon')]

    OPTIONS = {'includes': INCLUDES,
               'excludes': EXCLUDES,
               'bundle_files': 1, 
               'compressed': True
               }

    setup(
        windows=APP,
        data_files=DATA_FILES,
        options={'py2exe': OPTIONS},
        version=VERSION,
        author=AUTHOR,
        author_email=AUTHOR_EMAIL,
        maintainer=MAINTAINER,
        maintainer_email=MAINTAINER_EMAIL
    )

else:
    print("L'OS {os} n'est pas supporte pour la compilation.".format(os=system()))
