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
from sprite import Sprite

class Energy(Sprite):
    
    def __init__(self, x, y, w, h):
        Sprite.__init__(self, x, y)
        self.model = None
        self.w = w
        self.image = pygame.Surface((w + 2, h))
        self.rect = self.image.get_rect().move(x, y)
        self.z = -1000
        self.collision_rect = None

    def set_model(self, id_model):
        self.model = id_model
        self.current_energy = id_model.energy
        self._update_view()

    def _update_view(self):
        rect = pygame.Rect(0, 0, self.rect.w, self.rect.h).inflate(-2, -2)
        self.image.fill((220, 0, 0), rect)
        rect.w = self.current_energy
        self.image.fill((255, 255, 0), rect)

    def update(self):
        if self.current_energy != self.model.energy:
            self.current_energy = self.model.energy
            self._update_view()
