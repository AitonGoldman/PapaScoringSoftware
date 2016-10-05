"""Set up your virtual environment for development"""
import os, subprocess
from distutils import spawn

VENV_PATH = spawn.find_executable('virtualenv')
if not VENV_PATH:
    raise Exception("Install virtualenv")
subprocess.call([VENV_PATH, 'venv'])
subprocess.call([
    os.path.join('venv', 'bin', 'pip'),
    'install',
    '-r',
    'requirements.txt'
])
subprocess.call([
    os.path.join('venv', 'bin', 'pip'),
    'install',
    '-e',
    'pip install -e git+http://github.com/russ-/pychallonge#egg=pychallonge'
])
