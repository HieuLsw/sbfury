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

from pygame.sprite import Sprite as Spr
TOP, LEFT, RIGHT, BOTTOM = range(4)

class Sprite(Spr):
    "Un sprite con coordenadas independientes del atributo rect."
    
    def __init__(self, x=0, y=0):
        Spr.__init__(self)
        self.x, self.y = x, y


class SpriteAnimated(Sprite):
    "Un sprite que se puede desplazar de un sitio a otro."

    def __init__(self, image, inicial_position=TOP, to_x=320, to_y=240):
        Sprite.__init__(self)
        self.to_x = to_x
        self.to_y = to_y
        self.image = image
        self.rect = image.get_rect()
        self._set_initial_position(inicial_position)

    def _set_initial_position(self, inicial_position):
        positions = {
                TOP: (self.to_x, -self.rect.h),
                LEFT: (-self.rect.w, self.to_y),
                RIGHT: (640, self.to_y),
                BOTTOM: (self.to_x, 480),
                }
        self.rect.topleft = positions[inicial_position]
        self.x, self.y = positions[inicial_position]

    def update(self):
        self.x += (self.to_x - self.x) / 4.0
        self.y += (self.to_y - self.y) / 4.0

        self.rect.topleft = int(self.x), int(self.y)

    def is_movement_done(self):
        "Informa si el movimiento de interpolación terminó."
        dx = self.to_x - self.x
        dy = self.to_y - self.y
        return abs(dx) < 3 and abs(dy) < 3

