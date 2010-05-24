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

import sys
from pygame.sprite import Group
from common import *

import menu


class MainMenu:
    "Escena del menú principal."

    def __init__(self, world):
        self.world = world
        self.sprites = Group()
        self.background = load_image("mainmenu.png", "scenes")
        options = [
                ("Start a new game", self.on_start_new_game),
                ("Options", self.on_options),
                ("About this game", self.on_about),
                ("Exit", self.on_exit),
                ]
        self.menu = menu.Menu(330, 300, self.sprites, world.font, options)

    def update(self):
        self.menu.update()

    def draw(self, screen):
        screen.blit(self.background, (0, 0))
        self.sprites.draw(screen)
        pygame.display.flip()

    def on_exit(self):
        sys.exit(0)

    def on_start_new_game(self):
        import game
        self.world.change_state(game.Game(self.world))

    def on_about(self):
        from scenes.about import About
        self.world.change_state(About(self.world))

    def on_options(self):
        from scenes.options import Options
        self.world.change_state(Options(self.world))

    def handle_event(self, event):
        self.menu.update_control(event)
