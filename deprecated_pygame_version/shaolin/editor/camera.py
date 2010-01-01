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
import config

CAMERA_SPEED = 10

class Camera:

    def __init__(self, bound_left, bound_right):
        self.x = 320
        self.y = 0
        self.bound_left = bound_left
        self.bound_right = bound_right
        config.STAGE_CAMERA_MIN = 0
        config.STAGE_CAMERA_STEPS = 2

    def update(self):
        k = pygame.key.get_pressed()

        if k[pygame.K_RIGHT] or k[pygame.K_l] or k[pygame.K_d]:
            self.move(1)
        elif k[pygame.K_LEFT] or k[pygame.K_h] or k[pygame.K_a]:
            self.move(-1)

    def get_relative_position(self, x, y):
        return self.x - 320 + x, y

    def move(self, dx):
        self.x += CAMERA_SPEED * dx

        if self.x < self.bound_left:
            self.x = self.bound_left
        elif self.x > self.bound_right:
            self.x = self.bound_right
