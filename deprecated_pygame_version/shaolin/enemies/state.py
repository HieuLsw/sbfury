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

import math
import pygame
from pygame.time import get_ticks
import common 
import config
import random

class NotImplemented(Exception):
    pass


class State:
    
    def __init__(self, enemy):
        #print "The new state is:", self.__class__
        self.enemy = enemy
        self.enemy.unset_collision()

    def update(self):
        raise NotImplemented('you must redefine "update" method')


class Stand(State):
    
    def __init__(self, enemy):
        State.__init__(self, enemy)
        enemy.animation.set_state('stand')
        self.delay_to_change_state = random.randint(30, 50)

    def update(self):
        self.enemy.update_animation()
        self.enemy.see_to_player()
        self.enemy.do_collision_check(None)

        if self.delay_to_change_state < 0:
            if self.enemy.is_close_to_player():
                self.enemy.change_state(Attack(self.enemy))
            else:
                self.enemy.change_state(WalkToPlayer(self.enemy))
        else:
            self.delay_to_change_state -= 1


class WalkToPlayer(State):
    
    def __init__(self, enemy):
        State.__init__(self, enemy)
        enemy.animation.set_state('walk')
        self._set_destiny(self.enemy.player.x, self.enemy.player.y)
        self.t = 0.0
        self.delay_to_stand = 100

        if self.enemy.player.y < enemy.y:
            self.dt = -0.01
        else:
            self.dt = +0.01

    def update(self):
        self.enemy.update_animation()
        velocity = 5
        self.enemy.see_to_player()
        self.dy = math.sin(self.t) * 1
        self.t += self.dt
        self.enemy.move(self.dx * 2, self.dy * 2)
        self.enemy.do_collision_check(None)

        if self.enemy.is_close_to_player():
            self.enemy.change_state(Stand(self.enemy))
        else:
            self.delay_to_stand -= 1
            if self.delay_to_stand < 0:
                self.enemy.change_state(Stand(self.enemy))

    def _set_destiny(self, x, y):
        mx, my = self.enemy.x, self.enemy.y
        angle_to_player = common.get_angle_between_points(mx, my, x, y)
        self.dx = math.cos(angle_to_player)
        self.dy = - math.sin(angle_to_player)


class Attack(State):

    def __init__(self, enemy):
        State.__init__(self, enemy)
        enemy.animation.set_state('attack1')

    def update(self):
        self.enemy.do_collision_check(None)
        if self.enemy.update_animation():
            self.enemy.change_state(Stand(self.enemy))


class HitStand(State):
    
    def __init__(self, enemy, number=1):
        State.__init__(self, enemy)
        enemy.animation.set_state('hitstand' + str(number))

        if self.enemy.flip:
            self.enemy.move(+2, 0)
        else:
            self.enemy.move(-2, 0)

        self.enemy.sensitive = False
        self.enemy.energy.change_energy(-10)
        common.audio.play('punch1')

    def update(self):

        if self.enemy.update_animation():
            self.enemy.change_state(Stand(self.enemy))
            self.enemy.sensitive = True


class HardHit(State):
    
    def __init__(self, enemy, dy=-6, initial_dx=4):
        State.__init__(self, enemy)
        enemy.animation.set_state('hardhit')
        self.dy = dy
        self.initial_dy = dy
        self.enemy.sensitive = False
        self.enemy.energy.change_energy(-15)
        common.audio.play('punch2')
        self.in_air = True
        #self.enemy.game.world.fps.slow()

        if enemy.flip:
            self.dx = abs(initial_dx)
        else:
            self.dx = - abs(initial_dx)

    def update(self):

        self.dy += 0.5
        self.enemy.dy += self.dy
        
        self.enemy.move(self.dx, 0)

        # si toca el suelo
        if self.enemy.dy > - self.initial_dy -1:
            self.in_air = False
            self.initial_dy += 1.9
            self.dy = self.initial_dy
            self.reduce_dx()

            if self.dx > 3 or self.dx < -3:
                common.audio.play('touch_flood')
                self.enemy.game.stage.do_camera_effect()

            if self.initial_dy > 1:
                common.audio.play('touch_flood')
                self.enemy.change_state(Ground(self.enemy))
                self.enemy.dy = 0
                return

        if self.in_air:
            self.enemy.update_animation()
        else:
            if self.dy < 0.0:
                frame = 3
            else:
                frame = 2

            flip = self.enemy.flip
            self.enemy.animation.step = frame
            self.enemy.image = self.enemy.animation.get_image(flip)


    def reduce_dx(self):
        try:
            self.dx -= (self.dx / abs(self.dx)) 
        except:
            self.dx = 0
        pass


class Ground(State):
    
    def __init__(self, enemy):
        State.__init__(self, enemy)
        self.delay = 50
        enemy.animation.set_state('ground')
        enemy.update_animation()
        self.enemy.sensitive = False

    def update(self):
        self.delay -= 1
        
        if self.delay < 1:

            if self.enemy.energy.must_die():
                self.enemy.change_state(Die(self.enemy))
            else:
                self.enemy.change_state(GroundToStand(self.enemy))

class Die(State):

    def __init__(self, enemy):
        State.__init__(self, enemy)
        enemy.animation.set_state('die')
        enemy.update_animation()

        # necesario para el hacer transparente de manera gradual
        self.enemy.image = self.enemy.image.convert()
        colorkey = self.enemy.image.get_at((1, 0))
        self.enemy.image.set_colorkey(colorkey)
        self.i = 240
        self.update()
        self.enemy.live = False

    def update(self):
        self.enemy.image.set_alpha(self.i)

        self.i -= config.FADEOUT_SPEED

        if self.i < 1:
            self.enemy.kill()


class GroundToStand(State):
    
    def __init__(self, enemy):
        State.__init__(self, enemy)
        enemy.animation.set_state('groundtostand')


    def update(self):
        if self.enemy.update_animation():
            self.enemy.change_state(Stand(self.enemy))
            self.enemy.sensitive = True

class Attack(State):
    
    def __init__(self, enemy):
        State.__init__(self, enemy)
        (last_tick, last_number) = enemy.last_attack

        if get_ticks() - last_tick < 300:
            number = last_number + 1
            if number > 4:
                number = 1
        else:
            number = 1

        self.collision_power = number
        enemy.animation.set_state('attack' + str(number))
        self.number = number

        # Abandona el estado si no puede golpear al protagonista
        if not enemy.is_close_to_player():
            pass

    def update(self):
        if self.enemy.update_animation():
            self.enemy.change_state(Stand(self.enemy))
        else:
            # si es el cuadro de animacion indicado genera una colision
            if self.enemy.animation.step == 1:
                self.enemy.set_collision(self.collision_power)
                if self.enemy.get_collision_send():
                    self.enemy.last_attack = (get_ticks(), self.number)
        

class Taked(State):
    
    def __init__(self, player):
        State.__init__(self, player)
        player.animation.set_state('taked')
        player.update_animation()

    def update(self):
        self.player.update_animation()


class HitTaked(State):
    
    def __init__(self, enemy, continue_taked=True):
        State.__init__(self, enemy)
        enemy.animation.set_state('hittaked')
        self.continue_taked = continue_taked

    def update(self):

        if self.enemy.update_animation():

            if self.continue_taked:
                self.enemy.change_state(Taked(self.enemy))
            else:
                self.enemy.change_state(Stand(self.enemy))


class AttackTake(State):
    
    def __init__(self, player, enemy_taked, attack_counter, continue_taked=True):

        State.__init__(self, player)
        player.animation.set_state('attacktake')
        common.audio.play('punch1')
        self.player.create_hit()
        self.continue_taked = continue_taked
        self.enemy_taked = enemy_taked
        self.attack_counter = attack_counter

    def update(self):

        if self.player.update_animation():

            if self.continue_taked:
                self.player.change_state(Take(self.player, self.enemy_taked,
                    self.attack_counter))
            else:
                self.player.change_state(Stand(self.player))


class Throwed(State):
    
    def __init__(self, enemy, dy=-8):
        State.__init__(self, enemy)
        enemy.animation.set_state('throwed')
        self.dy = dy
        self.initial_dy = dy
        self.enemy.sensitive = False
        self.enemy.energy.change_energy(-15)
        self.in_air = True

        if enemy.flip:
            self.dx = 6
        else:
            self.dx = -6

    def update(self):

        self.dy += 0.5
        self.enemy.dy += self.dy
        
        self.enemy.move(self.dx, 0)

        # si toca el suelo
        if self.enemy.dy > - self.initial_dy -1:
            self.in_air = False
            self.initial_dy += 1.9
            self.dy = self.initial_dy
            self.reduce_dx()

            if self.dx > 3 or self.dx < -3:
                common.audio.play('touch_flood')
                self.enemy.game.stage.do_camera_effect()

            if self.initial_dy > 1:
                common.audio.play('touch_flood')
                self.enemy.collision_fly = None
                self.enemy.change_state(Ground(self.enemy))
                self.enemy.dy = 0
                return

        # update collision rect with other objects
        self.enemy.collision_fly = pygame.Rect(self.enemy.rect)
        self.enemy.collision_fly.x = self.enemy.x
        self.enemy.collision_fly.y += 50
        self.enemy.collision_fly.h = 20
        self.enemy.collision_fly.w = 40

        if self.in_air:
            self.enemy.update_animation()
        else:
            if self.dy < 0.0:
                frame = 3
            else:
                frame = 2

            flip = self.enemy.flip
            self.enemy.animation.step = frame
            self.enemy.image = self.enemy.animation.get_image(flip)

    def reduce_dx(self):
        try:
            self.dx -= (self.dx / abs(self.dx)) 
        except:
            self.dx = 0
        pass
