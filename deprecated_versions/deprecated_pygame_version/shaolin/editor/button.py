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
from pygame.sprite import Sprite

import common
import stage
import group

class Button(Sprite):

    def __init__(self, name, column, row, callback, status):
        Sprite.__init__(self)
        self.on_click = callback
        self.name = name
        self._create_surfaces()
        self.set_focus(False)
        self.rect = self.image.get_rect()
        self.to_x = column * 50 + 10
        self.to_y = row * 50 + 10
        self.x = self.to_x
        self.y = -500
        self.status = status

    def set_focus(self, state):
        if state:
            self.image = self.hover
        else:
            self.image = self.normal

    def update(self):
        self.y += (self.to_y - self.y) / 5.0
        self.x += (self.to_x - self.x) / 5.0
        self.rect.x = self.x
        self.rect.y = self.y

    def _create_surfaces(self):
        icon = common.load_image("%s.png" %(self.name), "buttons")
        pos = icon.get_rect()
        pos.center = (20, 20)

        self.normal = common.load_image("button_normal.png", "buttons")
        self.normal.blit(icon, pos)

        self.hover = common.load_image("button_hover.png", "buttons")
        self.hover.blit(icon, pos)

    def do_click(self):
        self.x += 10
        self.y += 10
        self.on_click(self)
