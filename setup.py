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

DATA_FILES = ['icon', '3d_files']

# Tous les paquets utilises dans l'application
INCLUDES = ['src', 'PyQt5', 'PyQt5.QtWidgets', 'PyQt5.QtCore', 'PyQt5.QtGui',
            'numpy', 'trimesh', 'fitz', 'pyqtgraph', 'OpenGL', 'os', 'sys', 'pathlib', 'time', 'PIL']

# Packets installes mais inutiles pour l'application,
# cela peut permettre de reduire grandement la taille de l'application
EXCLUDES = []

if system() == 'Linux':
    print("Pour compiler l'application sur Linux, executez : bash linux_builder.sh")

elif system() == 'Darwin':
    APP = ['src/CrubsRunner.py']

    OPTIONS = {'iconfile': str(path) + '/icon/icon_app.icns',
               'includes': INCLUDES,
               'excludes': EXCLUDES
               }

    if not EXCLUDES:
        EXCLUDES = ['matplotlib', 'pygame', 'pytmx', 'sympy', 'pygments', 'Cython', 'scipy']

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
    APP = [{'script': str(path) + "src/CrubsRunner.py",
            'icon_resources': [(1, "icon/icon_app.ico")]
            }]

    OPTIONS = {'includes': INCLUDES,
               'excludes': EXCLUDES
               }

    if not EXCLUDES:
        EXCLUDES = []
    setup(
        windows=APP,
        data_files=DATA_FILES,
        options={'py2exe': OPTIONS},
        setup_requires=['py2exe'],
        version=VERSION,
        author=AUTHOR,
        author_email=AUTHOR_EMAIL,
        maintainer=MAINTAINER,
        maintainer_email=MAINTAINER_EMAIL
    )

else:
    print("L'OS {os} n'est pas supporte pour la compilation.".format(os=system()))
