# -*- encoding: utf-8 -*-
# Shaolin's Blind Fury
#
# Copyright 2008 - Hugo Ruscitti
# License: GPLv3 (see http://www.gnu.org/licenses/gpl.html)

import sys
sys.path.append('../')

import pyglet
import cocos

import enemies
import common
import sprite
import animation
import state
import shadow


class Hannia(enemies.Enemy):

    def __init__(self, shaolin, x=400, y=200):
        super(Hannia, self).__init__(shaolin, must_be_updated=True)
        self.position = x, y
        self._load_animations()
        self.set_ai_states(
                [state.Wait(self, 1), state.PunchToPlayerIfCloser(self)]
                #state.WalkRandom(self, 1)])
                )
        self.go_to_next_ai_state()
        self.shadow = shadow.Shadow()
        self.move(0, 0)

    def _load_animations(self):
        Animation = animation.Animation

        self._animations = {
                'stand': Animation('enemies/hannia/stand.png', 1),
                'hitstand1': Animation('enemies/hannia/hitstand1.png', 1),
                'attack': Animation('enemies/hannia/hitstand1.png', 1),
                'hitstand2': Animation('enemies/hannia/hitstand2.png', 1),
                'hardhit': Animation('enemies/hannia/hardhit.png', 4),
                'ground': Animation('enemies/hannia/ground.png', 1),
                'ground_to_stand': Animation('enemies/hannia/ground_to_stand.png', 3),
                'walk': Animation('enemies/hannia/walk.png', 4),
                }

    def set_animation(self, id):
        self.animation = self._animations[id]
