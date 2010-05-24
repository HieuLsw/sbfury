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

from pygame.sprite import RenderPlain
from common import VISIBLE_DEBUG


class Group(RenderPlain):
    
    def __init__(self, camera):
        RenderPlain.__init__(self)
        self.camera = camera

    def draw(self, screen):
        sprites = self.sprites()
        sprites.sort(cmp=self.sort)

        for s in sprites:
            # Realiza el desplazamiento de escenario (Scroll)
            rect = s.rect.move(-self.camera.area.x, -self.camera.area.y)
            screen.blit(s.image, rect)
            
            if VISIBLE_DEBUG:
                try:
                    if s.collision_rect:
                        dx, dy = -self.camera.area.x, -self.camera.area.y
                        rect = s.collision_rect.move(dx, dy)                
                        screen.fill((255, 255, 100), rect)
                except:
                    pass

    def sort(self, s1, s2):
        if s1.z > s2.z:
            return -1
        else:
            return +1
