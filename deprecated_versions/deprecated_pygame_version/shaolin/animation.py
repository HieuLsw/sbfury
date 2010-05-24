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
import ConfigParser
import config
from frames import Frames

class SimpleAnimation:
    "Una secuencia de cuadros de animación."

    def __init__(self, path, name, frames, delay=0):
        self.image_frames = Frames(path, name, delay)
        self.step = -1
        self.delay = delay
        self.delay_counter = -1
        self.frames = frames

    def advance(self, repeat=True):
        "Devuelve una a una las superficies de la animación."

        if self.delay_counter < 0:
            if len(self.frames) > 0:
                self.step = self.frames.pop(0)

            self.delay_counter = self.delay
        else:
            self.delay_counter -= 1

        return self.image_frames.frames[self.step]


class Animation:
    "Representa un conjunto de estados de animación."

    def __init__(self, path, do_flip=True, sequence=[0,1], delay=0):
        path = os.path.join(config.DATADIR, path)
        files = [x for x in os.listdir(path) if x.endswith('.png')]
        self.frames = {}
        self.data = ConfigParser.ConfigParser()
        self.data.read(os.path.join(path, 'info.ini'))

        for x in files:
            if '_' in x:
                name = self._get_state_name_from_filename(x)
                delay = self.data.getint(name, 'delay')
                try:
                    dx = self.data.getint(name, 'dx')
                    dy = self.data.getint(name, 'dy')
                    control_point = (dx, dy)
                    #print "%s state has control point" %name
                except ConfigParser.NoOptionError:
                    control_point = None

                frames = Frames(path, x, delay, control_point)
                self.frames[name] = frames

        self.set_state('stand')

    def _get_state_name_from_filename(self, filename):
        """Obtiene el nombre de estado asociado a un archivo de imagen, por
        ejemplo si se invoca a la función con el archivo 'run_5.png' se obtiene 
        'run'."""

        basename = os.path.basename(filename)
        return basename.split('_')[0]

    def set_state(self, state):
        "Define el estado de animación a mostrar como cadena."

        self.state = state
        self.step = 0
        self.delay_counter = 0
        self.actual_frame = self.frames[self.state]

    def get_image(self, fliped=False):
        if fliped:
            return self.actual_frame.fliped_frames[self.step]
        else:
            return self.actual_frame.frames[self.step]
    
    def get_control_point(self, fliped=False):
        dx, dy = self.actual_frame.control_point

        if fliped:
            dx = self.actual_frame.frames[0].get_width() - dx
        
        return (dx, dy)

    def get_first_frame(self, fliped=False):
        "Retorna el primer cuadro de una animación."
        if fliped:
            return self.actual_frame.fliped_frames[0]
        else:
            return self.actual_frame.frames[0]

    def advance(self, repeat=True):
        """Avanza un cuadro de animación. 
        
        Retorna True si la animación ha terminado. Dependiendo del parámetro
        repeat, la animación regresará al cuadro 0 o se detendrá mostrando
        el último cuadro."""

        self.delay_counter += 1

        if self.delay_counter > self.actual_frame.delay:
            self.step += 1
            self.delay_counter = 0

        if self.step >= len(self.actual_frame.frames):
            if repeat:
                self.step = 0
            else:
                self.step -= 1
            return True
