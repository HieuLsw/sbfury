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
from object import Object
from common import DATADIR, load_image
import config

class Shadow(Object):
    "Muestra una sombra debajo de algún personaje."
    
    def __init__(self, player):
        Object.__init__(self)
        self.player = player
        self.image = load_image('shadow.png', DATADIR)
        self.rect = pygame.Rect(player.x, player.y, 0, 0)
        self.xoffset = self.image.get_width() / 2

    def update(self):
        pass

    def update_from_parent(self):
        self.rect.x = self.player.x - self.xoffset
        self.rect.y = self.player.y - 20

        # desaparece junto al personaje del juego
        if not self.player.live:
            self.image = load_image('shadow_to_disolve.png', DATADIR, True)
            self.i = 20
            self.update = self.update_fadeout
            self.update()

    def update_fadeout(self):
        self.image.set_alpha(self.i)

        self.i -= 1

        if self.i < 1:
            self.kill()

