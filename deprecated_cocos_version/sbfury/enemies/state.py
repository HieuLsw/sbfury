# -*- encoding: utf-8 -*-
# Shaolin's Blind Fury
#
# Copyright 2008 - Hugo Ruscitti
# License: GPLv3 (see http://www.gnu.org/licenses/gpl.html)

from sprite import State


class Stand(State):

    def __init__(self, target):
        State.__init__(self, target)
        target.set_animation('stand')

    def update(self, dt):
        self.target.update_animation(dt)

    def on_collision_receive(self, other_sprite, collision_force):
        if other_sprite.x < self.target.x:
            self.target.flip = True
        else:
            self.target.flip = False

        if collision_force < 4:
            self.target.set_state(HitStand(self.target, collision_force))
        else:
            self.target.set_state(HardHit(self.target))

        return True


class Walk(Stand):

    def __init__(self, target):
        Stand.__init__(self, target)
        target.set_animation('walk')

    def update(self, dt):
        self.target.update_animation(dt)


class HitStand(State):

    def __init__(self, target, collision_force):
        State.__init__(self, target)

        if collision_force in [1, 3]:
            target.set_animation('hitstand1')
        else:
            target.set_animation('hitstand2')

    def update(self, dt):
        if self.target.update_animation(dt):
            self.target.set_state(Stand(self.target))


class HardHit(State):

    def __init__(self, target):
        State.__init__(self, target)
        target.set_animation('hardhit')
        self.vy = 7

        if self.target.flip:
            self.dx = 0.8
        else:
            self.dx = -0.8

    def update(self, dt):
        self.target.distance_to_floor += self.vy * dt * 50
        self.vy -= dt * 30
        self.target.move(self.dx * dt, 0)

        self._set_animation_frame()

        if self.target.distance_to_floor <= 0:
            self.target.distance_to_floor = 0
            self.target.set_state(Ground(self.target))

    def _set_animation_frame(self):
        if self.vy > 0:
            if self.vy > 5:
                self.target.set_frame(0)
            else:
                self.target.set_frame(1)
        else:
            if self.vy > -5:
                self.target.set_frame(2)
            else:
                self.target.set_frame(3)

class Ground(State):

    def __init__(self, target):
        State.__init__(self, target)
        target.set_animation('ground')
        self._step = 0

    def update(self, dt):
        self.target.update_animation(False)
        self._step += dt

        if self._step > 2:
            self.target.set_state(GroundToStand(self.target))


class GroundToStand(State):

    def __init__(self, target):
        State.__init__(self, target)
        target.set_animation('ground_to_stand')
    
    def update(self, dt):
        if self.target.update_animation(dt):
            self.target.set_state(Stand(self.target))
