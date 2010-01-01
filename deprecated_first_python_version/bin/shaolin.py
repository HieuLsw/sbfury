#! /usr/bin/env python
import sys
import os

game = 'shaolin'
os.chdir('..')

try:
    path = os.path.join(os.path.dirname(__file__), game)
    gamedir = os.path.abspath(path)
    sys.path.insert(0, gamedir)
except:
    pass

os.chdir(game)
from world import World

w = World()
w.loop()
