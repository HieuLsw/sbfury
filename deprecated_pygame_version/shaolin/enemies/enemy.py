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

import random
import pygame

from object import Object
from animation import Animation
from common import same_z_dist
from hit import Hit
from enemy import *
from state import *
import shadow
import energy


class Enemy(Object):
    "Representa un enemigo del videojuego."
    
    def __init__(self, game, name, sprites, x, y, player):
        Object.__init__(self, game.stage)
        self.game = game
        self.name = name
        self.init_animations()
        self.image = self.animation.get_image()
        self.x = x
        self.y = y
        self.rect = pygame.Rect(self.x, self.y, 10, 10)
        self.flip = True
        self.change_state(Stand(self))
        self.dy = 0
        self.sprites = sprites
        self.last_attack = (0, 0)
        self.player = player
        self.shadow = shadow.Shadow(self)

        # Collision when is trowed
        self.collision_fly = None
        self.update_animation()

        if player:
            self.update()
            self.energy = energy.EnergyModel(name, 100, game.on_enemy_energy_model_change)
        else:
            Object.update(self)
            self.z = -self.y

    def init_animations(self):
        self.animation = Animation('enemies/' + self.name)

    def update(self):
        if self.are_in_camera_area():
            self.state.update()
            Object.update(self)
            self.z = -self.y
            self.shadow.update_from_parent()

    def kill(self):
        Object.kill(self)
        self.shadow.kill()

    def update_animation(self):
        self.image = self.animation.get_image(self.flip)
        return self.animation.advance()

    def change_state(self, state):
        self.state = state

    def set_collision(self, power=1):
        """Define una zona como 'colisionable' para golpear a otros"""

        (_, _, w, h) = self.image.get_rect()
        cw, ch = 50, 10

        if self.flip:
            x = self.x - cw - w/2 + cw + 15
        else:
            x = self.x + w/2 - cw - 15

        y = self.y + self.dy - h / 2
        
        Object.set_collision(self, (x, y), cw, ch)
        self.collision_power = power

    def do_collision_check(self, new_state_if_occur):
        "Evalúa si recibe un golpe, si es así altera su estado."

        collision = self._get_collision_receive()

        if collision:
            power, self.flip = collision

            if self.energy.must_die():
                self.change_state(HardHit(self))
            else:
                if power == 1 or power == 3:
                    self.change_state(HitStand(self))
                elif power == 2:
                    self.change_state(HitStand(self, 2))
                elif power == 5: # special
                    self.change_state(HardHit(self, -16, 8))
                else:
                    self.change_state(HardHit(self))

            self.create_hit()

    def _get_collision_receive(self):
        """Determina si en ese momento es golpeado por otro personaje."""

        e = self.game.player

        if self.sensitive and e.collision_rect and same_z_dist(e, self):
            if e.collision_rect.colliderect(self.get_screen_rect()):
                try:
                    new_flip = (self.x - e.x) / abs(self.x - e.x)
                except:
                    new_flip = 1
                return e.collision_power, new_flip == 1

    def get_collision_send(self):
        "Retorna True si detecta que ha golpeado a un personaje"

        e = self.player

        if e.sensitive and self.collision_rect and same_z_dist(e, self):
            if self.collision_rect.colliderect(e.get_screen_rect()):
                return True

    def create_hit(self, dy=0):
        """Genera un explosión que indica la existencia de un golpe."""
        dx = -40 if self.flip else 0

        x = self.x + dx
        y = self.y - 100 + dy
        self.sprites.add(Hit(x, y))

    def can_take_by_player(self):
        "Informa al jugador si este enemigo se puede sujetar."
        return isinstance(self.state, (Stand, WalkToPlayer))

    def see_to_player(self):
        self.flip = True if self.rect.x > self.player.rect.x else False

    def is_close_to_player(self):
        "Informa si el enemigo está muy cerca del protagonista."
        a, b = self, self.player
        return same_z_dist(a, b) and common.get_dist(a, b) < 100
