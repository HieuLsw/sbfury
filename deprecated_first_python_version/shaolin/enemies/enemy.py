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

from object import Object
from animation import Animation
from common import same_z_dist
from hit import Hit
from id import ID
from enemy_state import *



class Enemy(Object):
    
    def __init__(self, game, name, sprites, datadir, x=160, y=200):
        Object.__init__(self)
        self.game = game
        self.name = name
        self.datadir = datadir
        self.init_animations(datadir)
        self.image = self.animation.get_image()
        self.x = x
        self.y = y
        self.rect = pygame.Rect(self.x, self.y, 10, 10)
        self.flip = False
        self.change_state(Stand(self))
        self.dy = 0
        self.sprites = sprites
        self.last_attack = (0, 0)
        self.update()
        self.id = ID(name, 100)
        self.move(0,0)

    def init_animations(self, datadir):
        self.animation = Animation(datadir + '/enemies/' + self.name)

    def update(self):
        self.state.update()
        Object.update(self)
        self.z = -self.y

    def update_animation(self):
        self.image = self.animation.get_image(self.flip)
        return self.animation.advance()

    def change_state(self, state):
        self.state = state

    def move(self, dx, dy):
        "Intenta avanzar en la dirección indicada"

        self.x += dx
        self.y += dy

        up, down, left, right = 470, 230, 20, 1250

        if self.y > up:
            self.y = up
        elif self.y < down:
            self.y = down

        if self.x < left:
            self.x = left
        elif self.x > right:
            self.x = right

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

        # intenta golpear a sus enemigos (ESTO FUNCIONA)
        
        #for e in self.enemies:
        #    if same_z_dist(e, self):
        #        if self.collision_rect.colliderect(e.get_screen_rect()):
        #            print "He golpeado a otro personaje del juego"

    def get_collision_to_take_enemies(self, dy):
        """Verifica si puede sujetar a otros personajes del juego.

        Si están dadas las condiciones para sujetarlo (distancia y
        disponibilidad), retorna al enemigo. En caso contrario retorna None."""

        y_min = 10
        x_min = 30

        for e in self.game.enemies:
            if abs(common.get_dist_x(self, e)) < x_min:
                dist_y = common.get_dist_y(self, e)
                
                if dy >= 0:
                    if dist_y < 0 and dist_y > - y_min:
                        # intenta sujetar al enemigo mientras sube.
                        if e.can_take_by_player():
                            return e
                else:
                    if dist_y > 0 and dist_y < y_min:
                        # intenta sujetar al enemigo mientras baja.
                        if e.can_take_by_player():
                            return e

    def get_collision_receive(self):
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

    def get_screen_rect(self):
        image_rect = self.image.get_rect()
        return (self.rect.x, self.rect.y, image_rect.w, image_rect.h)

    def create_hit(self, dy=0):
        """Genera un explosión que indica la existencia de un golpe."""
        if self.flip:
            dx = - 40
        else:
            dx = 0

        x = self.x + dx
        y = self.y - 100 + dy
        self.sprites.add(Hit(x, y, self.datadir))

    def can_take_by_player(self):
        """Informa al jugador si este enemigo se puede sujetar."""

        return isinstance(self.state, (Stand, Walk, Run))
