# -*- coding: utf-8 -*-

from gui import MainWindow
import sys
from cx_Freeze import setup, Executable

base = None
if sys.platform == 'win32':
    base = 'Win32GUI'
    
include_files=['favicon.ico']
options = {
    'build_exe': {
        'compressed': True,
        'include_files':include_files
    }
}
executables = [
    Executable('main.py', base=base, icon="favicon.ico", compress=True)
]

setup(name='Blur Tool',
      version=MainWindow.VERSION,
      description='Blur Tool',
      author="RogueShadow",
      options=options,
      executables=executables
      )
