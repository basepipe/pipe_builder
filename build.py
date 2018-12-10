

from PyInstaller.__main__ import run
from resources import build_rc


import shutil
import os

if os.path.isdir('dist'):
    shutil.rmtree('dist')
if os.path.isdir('build'):
    shutil.rmtree('build')

cur_dir = os.getcwd()
os.chdir("resources")
build_rc.main()
os.chdir(cur_dir)
run(['--clean', 'build.spec'])