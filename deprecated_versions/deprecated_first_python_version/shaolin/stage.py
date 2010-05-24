# -* coding: utf-8 -*-
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
from common import *

from enemies.enemy import Enemy
from shadow import Shadow
from stageobject import StageObject

class Stage:
    
    def __init__(self, game):
        self.game = game
        path = DATADIR + '/stages/01.png'
        self.background = pygame.image.load(path).convert()
        self.area = pygame.Rect(0, 30, 640, 480)
        self.w = self.background.get_width()
        self.h = self.background.get_height()
        self.set_position(0, 30)

    def load_level(self, level):
        self._create_enemies_and_objects(level)

    def update(self):
        x = self.player.x
        y = self.player.y
        self.set_position(x, 0)

    def draw(self, screen):
        screen.blit(self.background, (0, 0), self.area)

    def set_position(self, x, y):
        """Change camera position with a smooth motion."""

        self.final_x = x - 320
        self.final_y = y - 240
        speed = 23.0

        x_dist = self.final_x - self.area.x
        y_dist = self.final_y - self.area.y

        # interpolación para realizar movimientos 'suaves'.
        if abs(x_dist) > 60:
            self.area.x += (self.final_x - self.area.x) / speed
        if abs(y_dist) > 60:
            self.area.y += (self.final_y - self.area.y) / speed

        # limite izquiedo y derecho
        if self.area.x < 0:
            self.area.x = 0
        elif self.area.x > self.w - 640:
            self.area.x = self.w - 640

        # limite superior e inferior
        if self.area.y > self.h - 240:
            self.area.y = self.h - 240
        elif self.area.y < 0:
            self.area.y = 0

    def do_camera_effect(self, power=3):
        self.area.y += power
        self.final_y -= power

    def _create_enemies_and_objects(self, level):
        enemies = [
            ['darkfat', (80, 300)],
            ['darkfat', (280, 250)],
            ['darkfat', (400, 250)],
            ['darkfat', (350, 400)]]
        objects = [
            ['stone', (100, 350)],
            ['misc', (340, 420)],
            ['misc', (260, 460)],
            ['misc', (280, 400)],
            ]

        for name, pos in enemies:
            self._create_enemy(name, pos)

        for name, pos in objects:
            self._create_object(name, pos)

    def _create_enemy(self, name, (x, y)):
        enemy = Enemy(self.game, name, self.game.sprites, DATADIR, x, y)
        shadow = Shadow(enemy, DATADIR)
        self.game.enemies.append(enemy)
        self.game.sprites.add([enemy, shadow])

    def _create_object(self, name, (x, y)):
        image = load_image(DATADIR + '/stages/objects/%s.png' % name)
        object = StageObject(image, x, y)
        self.game.sprites.add(object)
