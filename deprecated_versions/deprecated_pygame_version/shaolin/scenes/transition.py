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
import common

class Transition:
    "Muestra una transición progresiva entre una escena y otra."

    def __init__(self, world, last, new):
        self.world = world
        self.last = last
        self.new = new
        self.delay = 0
        self.speed = 0.0
        self.draw = self.draw_opening

        # nueva escena
        self.new_screenshot = world.screen.convert()
        new.draw(self.new_screenshot)

        # anterior en dos partes
        self.last_1 = world.screen.convert()
        self.last_2 = world.screen.convert()
        last.draw(self.last_1)
        last.draw(self.last_2)

        # corte 1
        split_1 = common.load_image("split_1.png", "scenes")
        self.last_1.blit(split_1, (0, 0))
        self.last_1.set_colorkey((255, 0, 255))

        # corte 2
        split_2 = common.load_image("split_2.png", "scenes")
        self.last_2.blit(split_2, (0, 0))
        self.last_2.set_colorkey((255, 0, 255))

        # marca de corte
        self.split = common.load_image("split_3.png", "scenes")

    def update(self):
        self.speed += 0.2
        self.delay += self.speed / 12.0

        if self.delay > 24:
            self.world.state = self.new

        # sigue actualizando la nueva escena
        self.new.update()

    def draw_opening(self, screen):
        delta = 25 * self.delay

        self.new.draw(self.new_screenshot)
        screen.blit(self.new_screenshot, (0, 0))
        screen.blit(self.last_2, (delta, -delta))
        screen.blit(self.last_1, (-delta, delta))

        if self.delay == 0:
            screen.blit(self.split, (0, 0))
        elif self.delay < 0.2:
            screen.fill((255, 255, 255))

        pygame.display.flip()

    def handle_event(self, event):
        self.new.handle_event(event)
