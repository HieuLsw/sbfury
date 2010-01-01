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

import os
import pygame
from ConfigParser import ConfigParser

from frames import Frames


class Animation:
    
    def __init__(self, path, do_flip=True, sequence=[0,1], delay=0):
        files = [x for x in os.listdir(path) if x.endswith('.png')]
        self.frames = {}
        self.data = ConfigParser()
        self.data.read(os.path.join(path, 'info.ini'))

        for x in files:
            name = self._get_state_name_from_filename(x)
            delay = self.data.getint(name, 'delay')
            frames = Frames(path, x, delay)
            self.frames[name] = frames
            #print "Set up '%s' state" % name

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

    def get_first_frame(self, fliped=False):
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


if __name__ == '__main__':
    a = Animation('')
