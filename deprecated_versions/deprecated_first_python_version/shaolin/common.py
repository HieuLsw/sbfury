# -*- coding: utf-8 -*-
# Copyright 2007 Hugo Ruscitti <hugoruscitti@gmail.com>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Scribes; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301
# USA
import pygame
from audio import Audio
from math import sqrt


# Global stuff...
DATADIR = '../data'
CONFIGDIR = '../config'
DEBUG = True
VISIBLE_DEBUG = False

audio = Audio(DATADIR)


def load_image(filename, datadir='./', convert=False):
    """Carga una imagen y le asigna un color de transparencia

    El color de transparencia se obtiene del segundo pixel de la primer linea,
    el pixel (1, 0)."""

    image = pygame.image.load(filename)
    colorkey = image.get_at((1, 0))
    image.set_colorkey(colorkey)

    if convert:
        return image.convert()
    else:
        return image

def same_z_dist(s1, s2):
    return abs(s1.z - s2.z) < 14

def get_dist(s1, s2):
    """Retorna la distancia entre los Sprites s1 y s2."""
    ca = s1.x - s2.x
    co = s1.y - s2.y
    return sqrt(ca*ca + co*co)

def get_dist_x(s1, s2):
    return s1.x - s2.x

def get_dist_y(s1, s2):
    return s1.y - s2.y
