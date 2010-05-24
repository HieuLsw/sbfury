# -*- coding: utf-8 -*-
#
# Shaolin's Blind Fury
# Copyright 2007 2008 Hugo Ruscitti <hugoruscitti@gmail.com>
# http://www.losersjuegos.com.ar
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, see http://www.gnu.org/licenses

import os
import math
import pygame
from audio import Audio
from math import sqrt
from options import Options
from config import *

options = Options(VERSION)
audio = Audio(DATADIR)

def load_image(filename, datadir='./', convert=False):
    """Carga una imagen y le asigna un color de transparencia

    La transparencia de la imagen depende del parámetro "convert", si convert
    vale False se tomará el canal alpha de la imagen. Si "convert" vale True
    se asigna un color transparente, de idéntico color del  segundo pixel de
    la primer linea, el pixel (1, 0)."""

    path = os.path.join(DATADIR, datadir, filename)
    image = pygame.image.load(path)

    if convert:
        colorkey = image.get_at((1, 0))
        image.set_colorkey(colorkey)
        return image.convert()
    else:
        return image.convert_alpha()

def same_z_dist(s1, s2):
    return abs(s1.z - s2.z) < 20

def get_dist(s1, s2):
    """Retorna la distancia entre los Sprites s1 y s2."""
    ca = s1.x - s2.x
    co = s1.y - s2.y
    return sqrt(ca*ca + co*co)

def get_dist_x(s1, s2):
    return abs(s1.x - s2.x)

def get_dist_y(s1, s2):
    return abs(s1.y - s2.y)

def get_angle_between_sprites(s1, s2):
    return get_angle_between_points(s1.x, s1.y, s2.x, s2.y)

def get_angle_between_points(x0, y0, x1, y1):
    op = y0 - y1
    ad = x0 - x1
    return math.atan2(op, -ad)

def center_window():
    os.environ["SDL_VIDEO_CENTERED"] = "1"

def set_limit(value, min, max):
    if value > max:
        return max
    elif value < min:
        return min
    else:
        return value
