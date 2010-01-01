# -*- encoding: utf-8 -*-
# Shaolin's Blind Fury
#
# Copyright 2008 - Hugo Ruscitti
# License: GPLv3 (see http://www.gnu.org/licenses/gpl.html)

import sys
sys.path.append('..')

import cocos
from cocos.director import director
from cocos.sprite import Sprite
from cocos.actions import *
import math

from test import *

import common


class Part(Sprite):
    """Some piece of the dragon's body"""

    def __init__(self):
        image = common.load_image('dragon/part.png')
        Sprite.__init__(self, image)


class Dragon(Sprite):
    """The dragon's head.
    
    It has a clock that updates every part of body."""

    def __init__(self):
        image = common.load_image('dragon/head.png')
        self.normal = image
        self.touch = common.load_image('dragon/head_touch.png')
        Sprite.__init__(self, image)
        self.anchor_x, self.anchor_y = 200, 200
        self.position = 300, 300
        self.schedule_interval(self.update, 1/60.0)
        self._create_body()

        rotate = Accelerate(RotateBy(20, 1), 2)
        #self.do(Repeat(rotate + Reverse(rotate)))

    def _create_body(self):
        self.body = []

        for part in range(10):
            self.body.append(Part())

    def update(self, dt):
        to = 700, 700
        initial = self.position

        dx = (to[0] - initial[0]) / (len(self.body) + 1)
        dy = (to[1] - initial[1]) / (len(self.body) + 1)

        last = self
        angle = math.atan2(initial[1] - to[1], initial[0] - to[0])
        angle = - (math.degrees(angle) - 180)

        for (index, part) in enumerate(self.body):
            x = initial[0] + dx * (index - 1) 
            y = initial[1] + dy * (index - 1)

            part.position = x, y
            part.rotation = angle + 20
            last = part


        if self.position[1] <= 240:
            self.rotation = 0
            self.image = self.touch
            self.anchor_x, self.anchor_y = 200, 200
        else:
            self.rotation = angle + 30
            self.image = self.normal


class EventLayer(cocos.layer.Layer):
    """Layer that handle mouse events to move the dragon."""

    is_event_handler = True

    def __init__(self):
        super(EventLayer, self).__init__()
        self.dragon = Dragon()


        for index, part in enumerate(self.dragon.body[::-1]):
            self.add(part, z=index / 10.0)

        self.add(self.dragon, z=1)
        image = common.load_image('dragon/body.png')
        sprite = cocos.sprite.Sprite(image)
        sprite.position = 500, 200
        self.add(sprite)

        image = common.load_image('shaolin/test.png')
        sprite = cocos.sprite.Sprite(image)
        sprite.position = 200, 150
        self.add(sprite)

        image = common.load_image('shaolin/test_2.png')
        sprite = cocos.sprite.Sprite(image)
        sprite.position = 50, 150
        self.add(sprite)

        image = common.load_image('enemies/hannia/stand.png')
        sprite = cocos.sprite.Sprite(image)
        sprite.position = 300, 150
        self.add(sprite)


    def on_mouse_motion(self, x, y, dx, dy):
        x, y = director.get_virtual_coordinates(x, y)
        self.dragon.position = x + 100, y + 100


if __name__ == '__main__':
    director.init(resizable=True)

    scene = cocos.scene.Scene(EventLayer())
    director.run(scene)
