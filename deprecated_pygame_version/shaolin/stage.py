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
from common import *
import common
import config

from enemies.enemy import Enemy
from enemies import state as enemy_state
from stageobject import StageObject, DestroyableStageObject

# Tipos de objetos de escenario
ENEMY, DESTROYABLE, SIMPLE, SPECIAL_CAMERA_STOP = range(4)

class Stage:
    "Representa un escenario con objetos y personajes."
    
    def __init__(self, game, sprites):
        self.game = game
        self.sprites = sprites
        self.set_object_references()

        self.area = pygame.Rect(0, 30, 640, 480)
        self._set_position_without_intepolation(320, 240)
        self.ant_objects = pygame.sprite.Group()
        self.objects = []
        self.destroyable_objects = pygame.sprite.Group()
        self.level = 1
        self.last_x = 0
        self.up_bound = 470
        self.down_bound = 230

    def set_object_references(self):
        self.object_types = {
                "box": DESTROYABLE,
                "fatninja": ENEMY,
                "red": ENEMY,
                "lamp": SIMPLE,
                "light": SIMPLE,
                "dark": SIMPLE,
                "stonea": DESTROYABLE,
                "stoneb": SIMPLE,
                "miscstonea": SIMPLE,
                "miscstoneb": SIMPLE,
                "miscstonec": SIMPLE,
                "border_front": SIMPLE,
                "border_back": SIMPLE,
                "camera_stop": SPECIAL_CAMERA_STOP,
                }
        self.object_handlers = {
                DESTROYABLE: self._create_destroyable_object,
                SIMPLE: self._create_object,
                ENEMY: self._create_enemy,
                SPECIAL_CAMERA_STOP: self._create_camera_stop,
                }

    def load_level(self, level):
        self.level = level
        self._create_enemies_and_objects(level)
        self.layers = self._create_layers()
        self.background = self.layers[0]
        self.w = self.background.get_width()
        self.h = self.background.get_height()

    def next(self):
        self.level += 1
        self.load_level(self.level)

    def previous(self):
        "Retrocede un nivel, informa False en caso de error."
        if self.level == 0:
            return False

        self.level += 1
        return True

    def update(self):
        to_x = self.object_to_follow.x

        if to_x > self.last_x:
            self.set_position(self.object_to_follow.x, 0)
            self.last_x = to_x

    def draw(self, screen):
        layer_3 = pygame.Rect(self.area)
        layer_3.x /= 5
        layer_2 = pygame.Rect(self.area)
        layer_2.x /= 1.3
        screen.blit(self.layers[3], (0, 0), layer_3)
        screen.blit(self.layers[2], (0, 0), layer_2)
        screen.blit(self.layers[1], (0, 0), self.area)
        screen.blit(self.background, (0, 0), self.area)

    def last_draw(self, screen):
        layer_2 = pygame.Rect(self.area)
        layer_2.x /= 0.8
        y = screen.get_height() - self.layers[4].get_height()
        screen.blit(self.layers[4], (0, y), layer_2)

    def set_position(self, x, y):
        """Change camera position with a smooth motion."""

        self.final_x = x - 320
        self.final_y = y - 240

        x_dist = self.final_x - self.area.x
        y_dist = self.final_y - self.area.y

        # interpolación para realizar movimientos 'suaves'.
        if abs(x_dist) > config.STAGE_CAMERA_MIN:
            self.area.x += (x_dist) / config.STAGE_CAMERA_STEPS
        if abs(y_dist) > config.STAGE_CAMERA_MIN:
            self.area.y += (y_dist) / config.STAGE_CAMERA_STEPS

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

        self.set_bounds(self.area.x, self.area.x + 640)

    def do_camera_effect(self, power=3):
        #self.area.y -= power
        self.final_y -= power * 5

    def try_movement(self, x, y, dx, dy, jump_height=0):
        "Move point (x, y) to (x + dx, y + dy), but apply a stage boundary."

        if self._exist_an_object_in(x + dx, y, jump_height):
            object = self.get_destroyable_object_at(x + dx, y)
            foots_y = y + jump_height
            object_top_border = object.y - object.height

            if foots_y > object_top_border:
                dx = 0
                jump_height = - object.height

        if self._exist_an_object_in(x, y + dy, jump_height):
            object = self.get_destroyable_object_at(x, y + dy)
            foots_y = y + jump_height
            object_top_border = object.y - object.height

            if foots_y > object_top_border:
                dy = 0
                jump_height = - object.height

        x += dx
        y += dy

        y = common.set_limit(y, self.down_bound, self.up_bound)
        x = common.set_limit(x, self.left_bound, self.right_bound)

        return x, y, jump_height

    def set_bounds(self, left, right):
        self.left_bound = left
        self.right_bound = right
        #print "New bounds at [%d, %d]" %(left, right)

    def get_dist_to_flood(self, x, y, dy):
        object = self.get_destroyable_object_at(x, y)

        if object:
            return dy + object.height
        else:
            return dy

    def _create_layers(self):
        dir = "stages/%d" %self.level
        layers = []
        layers.append(load_image('layer_0.png', dir, True).convert())
        layers.append(load_image('layer_1.png', dir, True))
        layers.append(load_image('layer_2.png', dir, True))
        layers.append(load_image('layer_3.png', dir))
        layers.append(load_image('layer_4.png', dir))
        return layers

    def _exist_an_object_in(self, x, y, jump_height):
        object = self.get_destroyable_object_at(x, y)

        if object:
            return True

    def get_object_at(self, x, y):
        for obj in self.objects:
            name, pos, instance = obj
            rect = pygame.Rect(0, 0, 80, 30)
            rect.center = pos

            if rect.collidepoint(x, y):
                return instance

    def erase_object(self, object):
        for obj in self.objects:
            _, _, instance = obj

            if instance == object:
                self.objects.remove(obj)
                instance.kill()
                return

    def get_destroyable_object_at(self, x, y):
        for obj in self.destroyable_objects:

            if obj.collision_rect.collidepoint(x, y):
                return obj

    def get_flood_dy(self, x, y):
        object = self.get_destroyable_object_at(x, y)

        if object:
            return -object.height
        else:
            return 0

    def _set_position_without_intepolation(self, x, y):
        self.final_x = self.area.x = x - 320
        self.final_y = self.area.y = y - 240
        self.set_bounds(x - 320, x + 320)

    def _create_enemies_and_objects(self, level_number):
        path = os.path.join(config.STAGEDIR, "stage_%d.txt" %level_number)
        stage_file = open(path, "rt")
        self.objects = []
        objects = []

        for line in stage_file.readlines():
            name, x, y = line.split()
            self.create_object(name, (int(x), int(y)))

        stage_file.close()

    def save(self):
        level_number = self.level
        path = os.path.join(config.STAGEDIR, "stage_%d.txt" %level_number)
        stage_file = open(path, "wt")

        for object in self.objects:
            name, (x, y), _ = object
            stage_file.write("%s %d %d\n" %(name, x, y))

        stage_file.close()

    def create_object(self, name, pos):
        type = self.object_types[name]
        handler = self.object_handlers[type]
        instance = handler(name, pos)
        self.objects.append([name, pos, instance])

    def _create_enemy(self, name, (x, y)):
        try:
            player = self.game.player
        except:
            player = None

        enemy = Enemy(self.game, name, self.sprites, x, y, player)
        enemy.shadow.update_from_parent()

        try:
            self.game.enemies.append(enemy)
        except:
            pass

        self.sprites.add(enemy)
        self.sprites.add(enemy.shadow)
        return enemy

    def _create_camera_stop(self, name, (x, y)):
        image = load_image(DATADIR + '/stages/objects/%s.png' % name)
        object = StageObject(image, x, y)
        self.sprites.add(object)
        return object

    def _create_object(self, name, (x, y)):
        image = load_image(DATADIR + '/stages/objects/%s.png' % name)
        object = StageObject(image, x, y)
        self.sprites.add(object)
        return object

    def _create_destroyable_object(self, name, (x, y)):
        sprites = self.sprites
        # TODO: object_to_follow no necesariamente es el jugador...
        p = self.object_to_follow

        object = DestroyableStageObject(name, x, y)
        object.player = p
        # FIX: esto hace fallar al editor
        try:
            object.enemies = self.game.enemies
        except:
            pass
        
        object.sprites = sprites
        object.height = 70

        sprites.add(object)
        self.destroyable_objects.add(object)
        return object
