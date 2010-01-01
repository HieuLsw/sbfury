# -*- encoding: utf-8 -*-
# Shaolin's Blind Fury
#
# Copyright 2008 - Hugo Ruscitti
# License: GPLv3 (see http://www.gnu.org/licenses/gpl.html)

import sys
sys.path.append('./')

import pyglet
import cocos

import config
import common
import sprite
from animation import Animation
import state
import shadow

class Shaolin(sprite.Sprite):
    """Game Hero."""

    def __init__(self):
        super(Shaolin, self).__init__(must_be_updated=True)
        self.flip = False
        self._load_animations()
        self.position = 80, 100
        self.set_state(state.Stand(self))
        self.shadow = shadow.Shadow()
        self.move(0, 0)

    def set_animation(self, id):
        self.animation = self._animations[id]

    def _load_animations(self):
        self._animations = {
                'attack1': Animation('shaolin/attack1.png', 2, 0.05),
                'attack2': Animation('shaolin/attack2.png', 2, 0.05),
                'attack3': Animation('shaolin/attack3.png', 2, 0.05),
                'attack4': Animation('shaolin/attack4.png', 2, 0.1),
                'attackjumprun':    Animation('shaolin/attackjumprun.png', 2),
                'attackjumpstand':  Animation('shaolin/attackjumpstand.png', 2),
                'attackjumpwalk':   Animation('shaolin/attackjumpwalk.png', 2),
                'attackrun':        Animation('shaolin/attackrun.png', 1),
                'attacktake':       Animation('shaolin/attacktake.png', 1),
                'ground':           Animation('shaolin/ground.png', 1),
                'groundtostand':    Animation('shaolin/groundtostand.png', 1),
                'hardhit':      Animation('shaolin/hardhit.png', 2),
                'hitstand1':    Animation('shaolin/hitstand1.png', 2),
                'hitstand2':    Animation('shaolin/hitstand2.png', 2),
                'jumpstand':    Animation('shaolin/jumpstand.png', 3),
                'jumpwalk': Animation('shaolin/jumpwalk.png', 3),
                'run':      Animation('shaolin/run.png', 4, 0.03),
                'special':  Animation('shaolin/special.png', 5),
                'stand':    Animation('shaolin/stand.png', 4),
                'starting': Animation('shaolin/starting.png', 3),
                'take':     Animation('shaolin/take.png', 1),
                'throw':    Animation('shaolin/throw.png', 3),
                'walk':     Animation('shaolin/walk.png', 4),
                }
    

    def on_control_press(self, map):
        self._state.on_control_press(map)

    def on_control_release(self, map):
        self._state.on_control_release(map)


if __name__ == '__main__':
    import control
    common.director.init(resizable=True)

    shaolin = Shaolin()
    control = control.Control(shaolin)
    layer = cocos.layer.ColorLayer(100, 100, 100, 255)
    scene = cocos.scene.Scene(layer)
    layer.add(shaolin)
    layer.add(control)
    layer.add(shaolin.shadow)

    common.director.run(scene)
