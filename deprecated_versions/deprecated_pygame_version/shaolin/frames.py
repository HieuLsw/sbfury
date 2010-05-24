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
import pygame

from common import load_image

class Frames:
    """Administra una collección de imagenes de un estado.

    Cada imagen debe contener en su nombre la cantidad de cuadros que contiene
    la grilla completa, por ejemplo 'run_5.png' indica que la animación está
    compuesta por una grilla de 5 cuadros (de igual tamaño) separados por una
    linea horizontal a la izquierda"""
    
    def __init__(self, path, filename, delay=0, control_point=None):
        max = self._get_frames_number_from_filename(filename)
        self.delay = delay
        image = load_image(filename, path)

        # separa los cuadros de animación de la grilla
        self.frames = [self._sub_frame(image, n, max) for n in xrange(max)]
        self.fliped_frames = [self._revert(f) for f in self.frames]
        self.control_point = control_point

    def _sub_frame(self, image, index, max):
        "Extrae un cuadro de animación de la grilla como superficie"

        rect = image.get_rect()
        rect.w /= max
        rect.x += 1 + index * rect.w
        rect.w -= 1
        return image.subsurface(rect)

    
    def _revert(self, image):
        "Invierte horizontalmente una superficie"

        return pygame.transform.flip(image, -1, 0)


    def _get_frames_number_from_filename(self, filename):
        """Obtiene la cantidad de cuadros que tiene una grilla.

        La cantidad de cuadros en una grilla se especifica en el mismo nombre de
        archivo, por ejemplo 'run_5.png' indica que la imagen del estado 'run'
        tiene 5 cuadros de animación."""

        l = filename.rfind('_') + 1
        r = filename.rfind('.')
        return int(filename[l:r])
