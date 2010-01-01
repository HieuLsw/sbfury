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

from sprite import Sprite
from pygame import Rect

class Object(Sprite):
    "Representación abstracta de un objeto dentro del escenario."
    
    def __init__(self, stage=None):
        Sprite.__init__(self)
        self.z = 0
        self.unset_collision()
        self.sensitive = True       # indica si es sensible a las colisiones
        self.stage = stage
        self.live = True

        if stage:
            self.move = self.move_with_stage
        else:
            self.move = self.move_without_stage

    def set_collision(self, point, w, h):
        x, y = point
        self.collision_rect = Rect(x, y, w, h)

    def unset_collision(self):
        self.collision_rect = None

    def update(self):
        dx = self.image.get_width() / 2
        dy = self.image.get_height() - 5
        self.rect.x = self.x - dx
        self.rect.y = self.y - dy + self.dy

    def on_collision_send(self):
        pass

    def move_with_stage(self, dx, dy):
        "Intenta avanzar en la dirección indicada"
        self.x, self.y, f = self.stage.try_movement(self.x, self.y, 
                dx, dy, self.dy)

    def move_without_stage(self, dx, dy):
        self.x += dx
        self.y += dy

    def get_pos(self):
        return self.x, self.y

    def get_screen_rect(self):
        image_rect = self.image.get_rect()
        return (self.rect.x, self.rect.y, image_rect.w, image_rect.h)

    def are_in_camera_area(self):
        return self.x < self.game.stage.area.x + 640 + 50
