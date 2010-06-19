# -*- encoding: utf-8 -*-
# Shaolin's Blind Fury
#
# Copyright 2008 - Hugo Ruscitti
# License: GPLv3 (see http://www.gnu.org/licenses/gpl.html)

import os
import pyglet
from pyglet.gl import  *

import cocos
from cocos.director import director
from cocos.scenes import *
from sound import Sound



def load_image(filename):
    """Creates a texture of the graphic file.

    :Parameters:
        `filename`: str
            path, relative to data directory, to the request file.
    """

    dirname = os.path.abspath(os.path.dirname(__file__))
    path = os.path.join(dirname, '..', 'data', filename)

    return pyglet.image.load(path).get_texture(rectangle=True)


def load_sound(filename):
    "Carga un sonido desde el directorio data"
    dirname = os.path.abspath(os.path.dirname(__file__))
    path = os.path.join(dirname, '..', 'data', filename)
    return pyglet.media.load(path, streaming=False)

def load_animation(filename):
    """Creates a animation from file

    :Parameters:
        `filename`: str
            path, relative to data directory, to the request file.
    """

    dirname = os.path.abspath(os.path.dirname(__file__))
    path = os.path.join(dirname, '..', 'data', filename)

    return pyglet.image.load_animation(path)

def draw_collision(x, y, w, h):
    glColor4f(1, 1, 1, 0.5)
    pyglet.graphics.draw(4, pyglet.gl.GL_POLYGON,
        ('v2f', (x, y, 
                 x + w, y, 
                 x + w, y - h,
                 x, y - h)))
    glColor4f(1, 1, 1, 1)

def draw_point(x, y):
    pyglet.graphics.draw(1, pyglet.gl.GL_POINTS, ('v2f', (x, y)))

def change_scene(new_scene, transition=None):
    if not transition:
        transition = FadeTransition

    director.replace(transition(new_scene, duration=0.6))

def fix_alpha():
    """Restore alpha value for old nvidia cards driver."""
    glColor4f(1, 1, 1, 1)

def in_range(value, min, max):
    """Evaluate if value are in (min, max)"""
    return min < value < max



sound = Sound()
