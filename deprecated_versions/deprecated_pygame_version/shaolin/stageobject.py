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

from object import Object
from common import *
from random import randint

class StageObject(Object):
    "Un objeto estático en el escenario."

    def __init__(self, image, x, y):
        Object.__init__(self)
        self.image = image
        self.x, self.y = x, y
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y
        self.dy = 0
        self.z = -y

class DestroyableStageObject(StageObject):
    """An object that you could break in two parts.

    This object can create new sprites too, ie to show two breaked parts
    of it."""

    def __init__(self, name, x, y, can_be_flip=True):
        self.can_be_flip = can_be_flip
        path = DATADIR + '/stages/objects/'
        self.normal = load_image("%s_1.png" %name, path, True)
        self.break_1 = load_image("%s_2.png" %name, path, True)
        self.break_2 = load_image("%s_3.png" %name, path, True)
        self.bump_image = load_image("%s_4.png" %name, path, True)
        StageObject.__init__(self, self.normal, x, y)
        self.sensitive = True
        self.step = 0
        w = self.normal.get_width()
        self.collision_rect = pygame.Rect(x - w/2, y - 20, w, 20)
        self.z = -y +20

    def update(self):
        self.check_collision()

    def check_collision(self):
        e = self.player

        if self.sensitive and e.collision_rect and same_z_dist(e, self):
            if e.collision_rect.colliderect(self.get_screen_rect()):
                if e.collision_power < 2:
                    self.bump()
                else:
                    self.destroy(e.collision_power)
        else:
            for e in self.enemies:
                if self.sensitive and e.collision_fly:
                    if e.collision_fly.colliderect(self.get_screen_rect()):
                        self.destroy(5, False)

    def bump(self):

        if self.step > 3:
            self.destroy(3)
        else:
            self.step += 1

        if self.step < 2:
            self.player.create_hit()
            self.image = self.bump_image

            if self.can_be_flip and self.player.x > self.rect.x:
                self.image = pygame.transform.flip(self.image, True, False)

    def get_screen_rect(self):
        image_rect = self.image.get_rect()
        return (self.rect.x, self.rect.y, image_rect.w, image_rect.h)

    def destroy(self, power, create_hit=True):
        if create_hit:
            self.player.create_hit()
        self.sensitive = False
        self.kill()
        x, y = self.rect.x, self.rect.y
        base = self.rect.bottom

        if self.player.x < self.rect.x:
            delta = 1 * power
            flip = False
        else:
            delta = -1 * power
            flip = True

        self.sprites.add(ObjectPart(self.break_1, x, y - 90, base, delta * 1,
            flip))
        self.sprites.add(ObjectPart(self.break_2, x, y, base, delta * 1.3,
            flip))


class ObjectPart(Object):
    "Un fragmento de un objeto que se destruye."

    def __init__(self, image, x, y, base_y, dx, flip=False):
        Object.__init__(self)
        self.dx = dx
        self.dy = randint(-7, -4)
        self.image = image
        self.rect = image.get_rect()
        self.rect.x, self.rect.y = x, y
        self.alpha = 255
        self.z = - base_y
        self.base_y = base_y

        if flip:
            self.image = pygame.transform.flip(self.image, True, False)

    def update(self):
        self.alpha -= 4

        if self.alpha < 0:
            self.kill()
            return

        self.rect.move_ip(self.dx, self.dy)
        self.image.set_alpha(self.alpha)
        self.dy += 0.5

        if self.rect.bottom > self.base_y:
            self.rect.bottom = self.base_y - 1
            self.dy *= -1
            self.dy /= 4
            self.dx /= 2
