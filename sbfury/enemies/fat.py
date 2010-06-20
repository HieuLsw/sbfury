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


class Fat(enemies.Enemy):

    def __init__(self, shaolin, x=400, y=200):
        super(Fat, self).__init__(shaolin, must_be_updated=True)
        self.position = x, y
        self._load_animations()
        self.set_ai_states([state.Wait(self, 4), state.Wait(self, 4)])
        self.go_to_next_ai_state()
        self.shadow = shadow.Shadow()
        self.move(0, 0)

    def _load_animations(self):
        Animation = animation.Animation

        self._animations = {
                'stand': Animation('enemies/fat/stand.png', 1),
                'hitstand1': Animation('enemies/fat/hitstand1.png', 1),
                'hitstand2': Animation('enemies/fat/hitstand2.png', 1),
                'hardhit': Animation('enemies/fat/hardhit.png', 4),
                'ground': Animation('enemies/fat/ground.png', 1),
                'ground_to_stand': Animation('enemies/fat/ground_to_stand.png', 3),
                }

    def set_animation(self, id):
        self.animation = self._animations[id]
