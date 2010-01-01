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

import pygame
from frames import Frames
from object import Object
from random import randint as rand

class Hit(Object):
    "Representa un golpe visual ante una colisión."
    
    def __init__(self, x, y):
        Object.__init__(self)
        x = int(x)
        y = int(y)
        self.x, self.y = rand(x - 20, x + 20), rand(y - 20, y + 20)
        color = rand(0, 2)
        self.frame = Frames("hits/", 'hit%d_6.png' %(color))
        self.step = -1
        self.delay = 0
        self.update_animation()
        self.rect = pygame.Rect(self.x, self.y, 0, 0)
        self.z = -2000

    def update_animation(self):
        if self.delay < 1:
            self.step += 1

            if self.step >= len(self.frame.frames):
                self.kill()
            else:
                self.image = self.frame.frames[self.step]

            self.delay = 1
        else:
            self.delay -= 1

    def update(self):
        self.update_animation()
