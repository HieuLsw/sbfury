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
from object import Object
from common import DATADIR, load_image
import config
import animation

class Bandage(Object):
    
    def __init__(self, player):
        Object.__init__(self)
        self.player = player
        self.animation = animation.Animation('bandage')
        self.rect = pygame.Rect(player.x, player.y, 0, 0)
        self.step = 0
        self.set_state('starting')

    def update(self):
        pass

    def update_from_parent(self):
        self.dy = self.player.dy - 70
        self.z = self.player.z + 1

        if self.player.flip:
            self.x = self.player.x + 10
        else:
            self.x = self.player.x - 10

        self.y = self.player.y - 50

        dx, dy = self.animation.get_control_point(self.player.flip)

        self.rect.x = self.x - dx
        self.rect.y = self.y - dy + self.dy
        self.state()

    def update_animation(self):
        self.image = self.animation.get_image(self.player.flip)
        return self.animation.advance()

    def set_state(self, state):
        self.state = getattr(self, '_handler_update_state_%s' %state)
        self.animation.set_state(state)

    def _handler_update_state_starting(self):
        self.update_animation()

    def _handler_update_state_run(self):
        self.update_animation()

    def _handler_update_state_tostand(self):
        # cambia al estado 'stand' cuando concluye la animación
        if self.update_animation():
            self.set_state('stand')

    def _handler_update_state_towalk(self):
        # cambia al estado 'walk' cuando concluye la animación
        if self.update_animation():
            self.set_state('walk')

    def _handler_update_state_stand(self):
        self.update_animation()

    def _handler_update_state_walk(self):
        self.update_animation()

    def _handler_update_state_jumpstand(self):
        pass

    def _handler_update_state_attackrun(self):
        self.update_animation()

    def _handler_update_state_throw(self):
        self.update_animation()

    def _handler_update_state_take(self):
        self.update_animation()

    def _handler_update_state_attacktake(self):
        self.update_animation()

    def _handler_update_state_ground(self):
        self.update_animation()

    def _handler_update_state_hardhit(self):
        pass
