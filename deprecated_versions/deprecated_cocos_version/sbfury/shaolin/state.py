# -*- encoding: utf-8 -*-
# Shaolin's Blind Fury
#
# Copyright 2008 - Hugo Ruscitti
# License: GPLv3 (see http://www.gnu.org/licenses/gpl.html)

import time

import config
from sprite import State

COLLISION_RECT_ATTACK = (0, 80, 90, 20)
COLLISION_RECT_AIR_ATTACK = (0, 30, 110, 20)

class Stand(State):

    def __init__(self, target, map=None):
        State.__init__(self, target)
        target.set_animation('stand')

        if map:
            self.on_control_press(map)

    def on_control_press(self, map):
        if map.run:
            self.target.set_state(Run(self.target, map))
        elif map.motion:
            self.target.set_state(Walk(self.target, map))

        if map.attack:
            self.target.set_state(Attack(self.target))
        elif map.jump:
            self.target.set_state(JumpStand(self.target))

    def update(self, dt):
        self.target.update_animation(dt)


class Walk(State):

    def __init__(self, target, map):
        State.__init__(self, target)
        target.set_animation('walk')
        self._set_direction(map)

    def _set_direction(self, map):
        self.dx, self.dy = 0, 0

        if map.left:
            self.dx = -1
            self.target.flip = True
        elif map.right:
            self.dx = 1
            self.target.flip = False

        if map.up:
            self.dy = 1
        elif map.down:
            self.dy = -1

    def update(self, dt):
        self.target.move(dt * self.dx, dt * self.dy)
        self.target.update_animation(dt)

    def on_control_press(self, map):
        self._set_direction(map)

        if map.attack:
            self.target.set_state(Attack(self.target))
        elif map.jump:
            self.target.set_state(JumpWalk(self.target, self.dx))

    def on_control_release(self, map):
        self._set_direction(map)
        if not map.motion:
            self.target.set_state(Stand(self.target))

class Run(Walk):

    def __init__(self, target, map):
        Walk.__init__(self, target, map)
        target.set_animation('run')
        self._set_direction(map)
        target.rotation = 30

    def update(self, dt):
        dx = dt * self.dx * 2
        dy = dt * self.dy * 2

        self.target.move(dx, dy)
        self.target.update_animation(dt)

    def on_control_press(self, map):
        self._set_direction(map)

        if map.attack:
            self.target.set_state(AttackWhenRun(self.target, self.dx * 2))
        elif map.jump:
            self.target.set_state(JumpWalk(self.target, self.dx * 2))

class AttackWhenRun(State):

    def __init__(self, target, dx):
        State.__init__(self, target)
        target.set_animation('attackrun')
        target.set_collision(COLLISION_RECT_ATTACK, 4)
        self.dx = dx

    def update(self, dt):
        self.target.move(dt * self.dx, 0)
        self.target.update_animation(dt)

        reduce_speed = 3 * dt

        # Change state when speed are close to 0.
        if abs(self.dx) < reduce_speed:
            self.target.set_collision(None)
            self.target.set_state(Stand(self.target))
        else:
            # Reduce motion speed.

            if self.dx > 0:
                self.dx -= reduce_speed
            else:
                self.dx += reduce_speed


class Attack(State):
    
    # remember the last attack to create combo attacks.
    last_attack_tick = 0
    attack_counter = 1

    def __init__(self, target):
        State.__init__(self, target)

        # Determine what attack animation to use
        now = time.time()

        # get time elapsed from last attack
        dt = now - Attack.last_attack_tick

        if dt < 0.5:
            Attack.attack_counter += 1

            if Attack.attack_counter > 4:
                Attack.attack_counter = 1
        else:
            Attack.attack_counter = 1

        Attack.last_attack_tick = now
        target.set_animation('attack' + str(Attack.attack_counter))
        target.set_collision(COLLISION_RECT_ATTACK, Attack.attack_counter)

    def update(self, dt):
        if self.target.update_animation(dt):
            self.target.set_collision(None)
            self.target.set_state(Stand(self.target))


class AbstractJump(State):

    def __init__(self, target, dx=0, vy=None):
        State.__init__(self, target)

        if not vy:
            self.vy = config.SHAOLIN_INITIAL_JUMP_SPEED
        else:
            self.vy = vy

        self.dx = dx
        self.dy = 0

    def update_jump(self, dt):
        """Return True if jump are done."""
        self.target.distance_to_floor += self.vy * dt * 50
        self.vy -= dt * 30
        self.target.move(self.dx * dt, self.dy * dt)

        if self.target.distance_to_floor < 0:
            self.target.distance_to_floor = 0
            return True

    def _set_animation_frame(self, vy):
        if vy > 3:
            self.target.set_frame(0)
        elif vy < -1:
            self.target.set_frame(2)
        else:
            self.target.set_frame(1)

class JumpStand(AbstractJump):

    def __init__(self, target, vy=None):
        AbstractJump.__init__(self, target, vy=vy)
        target.set_animation('jumpstand')

    def update(self, dt):
        self._set_animation_frame(self.vy)

        if self.update_jump(dt):
            self.target.set_state(Stand(self.target))

    def on_control_press(self, map):
        if map.left:
            self.dx = -0.5
            self.target.flip = True
        elif map.right:
            self.dx = 0.5
            self.target.flip = False
        elif map.attack:
            self.target.set_state(AttackJumpStand(self.target, self.vy))

    def on_control_release(self, map):
        if self.dx > 0:
            if not map.right:
                self.dx = 0
        elif self.dx < 0:
            if not map.left:
                self.dx = 0


class JumpWalk(AbstractJump):

    def __init__(self, target, dx, vy=None):
        AbstractJump.__init__(self, target, dx, vy)
        target.set_animation('jumpstand')

    def update(self, dt):
        self._set_animation_frame(self.vy)

        if self.update_jump(dt):
            self.target.set_state(Stand(self.target))

    def on_control_press(self, map):
        if map.left:
            self.target.flip = True
        elif map.right:
            self.target.flip = False

        if map.attack:
            self.target.set_state(AttackJumpWalk(self.target, self.dx, self.vy))


class AttackJumpStand(AbstractJump):

    def __init__(self, target, vy):
        AbstractJump.__init__(self, target, vy=vy)
        target.set_animation('attackjumpstand')
        self.dt = 0
        target.set_collision(COLLISION_RECT_AIR_ATTACK, 4)

    def update(self, dt):
        self.dt += dt
        self.target.update_animation(dt, repeat=False)

        if self.update_jump(dt) or self.dt > 0.5:
            self.target.set_state(JumpStand(self.target, vy=self.vy))
            self.target.set_collision(None)

class AttackJumpWalk(AbstractJump):

    def __init__(self, target, dx, vy):
        AbstractJump.__init__(self, target, dx, vy=vy)
        target.set_animation('attackjumpstand')
        self.dt = 0
        target.set_collision(COLLISION_RECT_AIR_ATTACK, 4)

    def update(self, dt):
        self.dt += dt
        self.target.update_animation(dt, repeat=False)

        if self.update_jump(dt) or self.dt > 0.5:
            self.target.set_state(JumpWalk(self.target, self.dx, vy=self.vy))
            self.target.set_collision(None)


