# -*- coding: utf-8 -*-

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
      version='1.0.1.0',
      description='Blur Tool',
      author="RogueShadow",
      options=options,
      executables=executables
      )
