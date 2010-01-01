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

class Font:
    "Representa una colección de fuentes tipográficas."

    def __init__(self):
        pygame.font.init()
        self.small = pygame.font.Font(None, 22)
        self.medium = pygame.font.Font(None, 35)
        self.big = pygame.font.Font(None, 50)
        self.sizes = {
                0: self.small,
                1: self.medium,
                2: self.big}

    def render(self, text, size=0, color=(255, 255, 255)):
        "Genera una nueva superficie conteniendo el texto indicado."
        return self.sizes[size].render(text, 1, color)


if __name__ == '__main__':
    f = Font()
