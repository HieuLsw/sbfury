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

from stage import Stage
from player.player import Player
from control import Control
from text import Text
from common import VISIBLE_DEBUG, DEBUG, DATADIR
import energy
import group
import scenes.mainmenu


class Game:
    "Representa la escena de pelea, donde el shaolin camina por el escenario."
    
    def __init__(self, world):
        self.world = world
        self.enemies = []

        self.sprites = group.Group()
        self.stage = Stage(self, self.sprites)
        self.sprites.camera = self.stage

        self.sprites_in_front = pygame.sprite.RenderPlain()
        self._create_player()
        self.stage.object_to_follow = self.player
        self.stage.load_level(1)

        if VISIBLE_DEBUG:
            # Visor de rendimiento
            self.text = Text(world.font, world.fps, "FPS: %d")
            self.sprites_in_front.add(self.text)

    def _create_player(self):
        self.control = Control()
        self.player = Player(self, self.control, self.sprites, DATADIR)
        self.sprites.add(self.player)
        self.sprites.add(self.player.shadow)
        self.sprites.add(self.player.bandage)

        self.energy = energy.EnergyView(10, 10, self.world.font)
        self.energy.set_model(self.player.energy_model)
        self.sprites_in_front.add(self.energy)

        self.enemy_energy = energy.EnergyView(440, 10, self.world.font)
        self.sprites_in_front.add(self.enemy_energy)

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            self.control.update(event, True)
            if event.key == pygame.K_ESCAPE:
                new_scene = scenes.mainmenu.MainMenu(self.world)
                self.world.change_state(new_scene)
        elif event.type == pygame.KEYUP:
            self.control.update(event, False)
        
    def update(self):
        self.stage.update()
        self.sprites.update()
        self.sprites_in_front.update()

        if DEBUG:
            b1, b2, b3 = pygame.mouse.get_pressed()

            if b1:
                self.stage.do_camera_effect()
            elif b2:
                self.stage.do_camera_effect(10)
            elif b3:
                self.world.fps.slow()

        self.control.post_update()

    def draw(self, screen):
        self.stage.draw(screen)
        self.sprites.draw(screen)
        self.sprites_in_front.draw(screen)
        self.stage.last_draw(screen)
        pygame.display.flip()

    def on_player_energy_model_change(self, model):
        pass

    def on_enemy_energy_model_change(self, model):
        self.enemy_energy.set_model(model)


class GameTestLevel(Game):
    """Escena de juego para probar un nivel desde el editor.

    A diferencia de la escena Game, GameTestLevel permite regresar
    fácilmente al editor de niveles."""

    def __init__(self, world, level, editor, dx):
        Game.__init__(self, world)
        self.editor = editor
        # Adapta la posición de cámara acorde a la posición actual
        self.player.x = dx
        self.stage.final_x = dx - 320
        self.stage.area.x = dx - 320
        self.stage.update()

    def update(self):
        Game.update(self)

    def handle_event(self, event):

        # Do return to editor
        if event.type == pygame.KEYDOWN:
            self.control.update(event, True)

            if event.key == pygame.K_ESCAPE:
                dx = self.stage.object_to_follow.x

                self.editor.camera.x = dx
                self.editor.stage.final_x = dx -320
                self.editor.stage.area.x = dx -320
                self.world.change_state(self.editor, do_animate=False)
                self.editor.stage.update()

        elif event.type == pygame.KEYUP:
            self.control.update(event, False)
