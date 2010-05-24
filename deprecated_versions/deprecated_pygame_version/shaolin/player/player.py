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
from animation import Animation
from state import *
from common import same_z_dist
import energy
from hit import Hit
import shadow
import bandage


class Player(Object):
    
    def __init__(self, game, control, sprites, datadir):
        Object.__init__(self, game.stage)
        self.game = game
        self.name = 'shaolin'
        self.datadir = datadir
        self.init_animations(datadir)
        self.image = self.animation.get_image()
        self.x = 100
        self.y = 350
        self.rect = pygame.Rect(self.x, self.y, 10, 10)
        self.flip = False
        self.bandage = bandage.Bandage(self)
        self.change_state(Starting(self))
        self.dy = 0
        self.control = control
        self.sprites = sprites
        self.last_attack = (0, 0)
        self.energy_model = energy.EnergyModel(self.name, 100,
                game.on_player_energy_model_change)
        self.hit_receive_counter = 0
        self.shadow = shadow.Shadow(self)
        self.update()

    def init_animations(self, datadir):
        self.animation = Animation('shaolin')

    def update(self):
        self.state.update()
        Object.update(self)
        self.z = -self.y
        self.bandage.update_from_parent()
        self.shadow.update_from_parent()

    def update_animation(self):
        self.image = self.animation.get_image(self.flip)
        self.rect.size = self.image.get_width(), self.image.get_height()
        return self.animation.advance()

    def change_state(self, state):
        self.state = state

    def kill(self):
        Object.kill(self)
        self.shadow.kill()

    def set_collision(self, power=1, dy=0, cw=50):
        """Define una zona como 'colisionable' para golpear a otros"""

        (_, _, w, h) = self.image.get_rect()
        ch = 10

        if self.flip:
            x = self.x - cw - w/2 + cw + 15
        else:
            x = self.x + w/2 - cw - 15

        y = self.y + self.dy - h / 2 + dy
        
        Object.set_collision(self, (x, y), cw, ch)
        self.collision_power = power

        # intenta golpear a sus enemigos (ESTO FUNCIONA)
        
        #for e in self.enemies:
        #    if same_z_dist(e, self):
        #        if self.collision_rect.colliderect(e.get_screen_rect()):
        #            print "He golpeado a otro personaje del juego"

    def check_collision_receive(self):
        if self.get_collision_receive():
            power, self.flip = self.get_collision_receive()

            if power > 1:
                self.hit_receive_counter = 0
                self.change_state(HardHit(self))
            else:
                self.hit_receive_counter += 1

                if self.hit_receive_counter > 3:
                    self.change_state(HardHit(self))
                    self.hit_receive_counter = 0
                else:
                    self.change_state(HitStand(self))

            self.create_hit()


    def get_collision_to_take_enemies(self, dy):
        """Verifica si puede sujetar a otros personajes del juego.

        Si están dadas las condiciones para sujetarlo (distancia y
        disponibilidad), retorna al enemigo. En caso contrario retorna None"""

        y_min = 10
        x_min = 30

        for e in self.game.enemies:
            if abs(common.get_dist_x(self, e)) < x_min:
                dist_y = common.get_dist_y(self, e)

                
                if dy >= 0:
                    if dist_y > 0 and dist_y < y_min:
                        # intenta sujetar al enemigo mientras baja.
                        if e.can_take_by_player():
                            return e
                else:
                    if dist_y > 0 and dist_y < y_min:
                        # intenta sujetar al enemigo mientras sube.
                        if e.can_take_by_player():
                            return e

    def get_collision_receive(self):
        """Determina si en ese momento es golpeado por otro personaje."""

        for e in self.game.enemies:
            if self.sensitive and e.collision_rect and same_z_dist(e, self):
                if e.collision_rect.colliderect(self.get_screen_rect()):
                    try:
                        new_flip = (self.x - e.x) / abs(self.x - e.x)
                    except:
                        new_flip = 1
                    return e.collision_power, new_flip == 1

    def get_collision_send(self):
        "Retorna True si detecta que ha golpeado a un personaje"

        for e in self.game.enemies:
            if e.sensitive and self.collision_rect and same_z_dist(e, self):
                if self.collision_rect.colliderect(e.get_screen_rect()):
                    return True


    def create_hit(self):
        """Genera un explosión que indica la existencia de un golpe."""

        dx = - 60 if self.flip else 30
        x = self.x + dx
        y = self.y - 130
        common.audio.play('punch1')
        self.sprites.add(Hit(x, y))

    def can_take_by_player(self):
        """Informa al jugador si este enemigo se puede sujetar."""

        return isinstance(self.state, (Stand, Walk, Run))

    def do_fall_if_are_in_air(self):
        """Previene que el personaje no quede 'volando' cuando se quiere bajar
        de una caja"""

        x, y = self.get_pos()
        dist = self.stage.get_dist_to_flood(x, y, self.dy)

        if dist < 0:
            self.change_state(JumpStand(self, 0))
            return True

    def do_stand_if_are_in_flood(self):
        "Procura que el personaje 'pise' el suelo o los objetos del nivel"
        x, y = self.get_pos()
        dy = self.dy

        flood = self.stage.get_dist_to_flood(x, y, dy)

        if flood >= 0:
            self.change_state(Stand(self))
            self.dy = self.stage.get_flood_dy(x, y)
            return
