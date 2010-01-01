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

import pygame

from energy import Energy
from stage import Stage
from group import Group
from player import Player
from shadow import Shadow
from control import Control
from text import Text
from common import VISIBLE_DEBUG, DEBUG

class Game:
    
    def __init__(self, world, datadir, configdir):
        self.world = world
        self.datadir = datadir
        self.configdir = configdir
        self.enemies = []

        self.stage = Stage(self)
        self.sprites = Group(self.stage)
        self.screen = world.screen

        # Visor de energia para el enemigo
        self._create_player()
        self.energy = Energy(10, 10, 100, 10)
        self.energy.set_model(self.player.id)

        self.stage.player = self.player
        self.stage.load_level(1)

        if VISIBLE_DEBUG:
            # Visor de rendimiento
            self.text = Text(world.font, world.fps, "FPS: %d")

    def _create_player(self):
        control = Control(0, self.configdir)
        self.player = Player(self, control, self.sprites, self.datadir)
        shadow_player = Shadow(self.player, self.datadir)
        self.sprites.add([self.player, shadow_player])
        
    def update(self):

        self.stage.update()
        self.sprites.update()
        self.energy.update()

        if VISIBLE_DEBUG:
            self.text.update()

        if DEBUG:
            b1, b2, b3 = pygame.mouse.get_pressed()

            if b1:
                self.stage.do_camera_effect()
            elif b2:
                self.stage.do_camera_effect(10)
            elif b3:
                self.world.fps.slow()

    def draw(self):
        self.stage.draw(self.screen)
        self.sprites.draw(self.screen)
        self.screen.blit(self.energy.image, self.energy.rect)

        if VISIBLE_DEBUG:
            self.screen.blit(self.text.image, self.text.rect)

        pygame.display.flip()

