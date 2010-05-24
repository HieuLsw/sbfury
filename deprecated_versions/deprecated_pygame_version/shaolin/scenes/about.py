# -*- encoding: utf-8 -*-
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
from common import *
from group import Group

class About:
    "Muestra información acerca los desarrolladores y losersjuegos."

    def __init__(self, world):
        self.world = world
        self.sprites = Group()
        self.background = load_image("about.png", "scenes")

    def update(self):
        pass

    def draw(self, screen):
        screen.blit(self.background, (0, 0))
        self.sprites.draw(screen)
        pygame.display.flip()

    def on_return_to_main_menu(self):
        import scenes
        self.world.change_state(scenes.mainmenu.MainMenu(self.world))

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.on_return_to_main_menu()
