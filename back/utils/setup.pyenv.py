"""Set up your virtual environment for development"""
import os, subprocess
from distutils import spawn

subprocess.call([
   'pip',
   'install',
   '-r',
   'requirements.txt'
])
subprocess.call([
   'pip',
   'install',
   '-e',
   'git+http://github.com/russ-/pychallonge#egg=pychallonge'
])
