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
from pygame.sprite import RenderPlain
from common import VISIBLE_DEBUG, options


class Group(RenderPlain):
    "Agrupa sprites dentro de escenas con cámara y profundidad."
    
    def __init__(self, camera=None):
        RenderPlain.__init__(self)
        self.camera = camera

    def draw(self, screen):
        "Dibuja los sprites en un area de pantalla de 640x480 pixeles."
        sprites = self.sprites()
        sprites.sort(cmp=self.sort)

        for s in sprites:
            # Realiza el desplazamiento de escenario (Scroll)
            rect = s.rect.move(-self.camera.area.x, -self.camera.area.y)
            screen.blit(s.image, rect)
            
            if VISIBLE_DEBUG:
                self._draw_box_lines(s, screen)

    def _draw_box_lines(self, s, screen):
        try:
            if s.collision_rect:
                dx, dy = -self.camera.area.x, -self.camera.area.y
                rect = s.collision_rect.move(dx, dy)                
                border = (255, 0, 0)
                pygame.draw.rect(screen, border, rect, 1)
        except:
            pass

        dx, dy = -self.camera.area.x, -self.camera.area.y
        rect = s.rect.move(dx, dy)                
        color_rect = (0, 180, 0)
        pygame.draw.rect(screen, color_rect, rect, 1)

        try:
            if s.collision_fly:
                dx, dy = -self.camera.area.x, -self.camera.area.y
                rect = s.collision_fly.move(dx, dy)                
                screen.fill((255, 255, 100), rect)
        except:
            pass

    def sort(self, s1, s2):
        if s1.z > s2.z:
            return -1
        else:
            return +1
