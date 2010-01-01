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
from sprite import Sprite
from pygame import Rect

class Object(Sprite):
    
    def __init__(self):
        Sprite.__init__(self)
        self.z = 0
        self.unset_collision()
        self.sensitive = True       # indica si es sensible a las colisiones

    def set_collision(self, point, w, h):
        x, y = point
        self.collision_rect = Rect(x, y, w, h)

    def unset_collision(self):
        self.collision_rect = None

    def update(self):
        hotspot_x = self.image.get_width() / 2
        hotspot_y = self.image.get_height() - 13
        self.rect.x = self.x - hotspot_x
        self.rect.y = self.y - hotspot_y + self.dy

    def on_collision_send(self):
        pass
