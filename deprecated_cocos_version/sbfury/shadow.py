# -*- encoding: utf-8 -*-
# Shaolin's Blind Fury
#
# Copyright 2008 - Hugo Ruscitti
# License: GPLv3 (see http://www.gnu.org/licenses/gpl.html)

import cocos

import sprite
import common

from pyglet.gl import *

class Shadow(cocos.sprite.Sprite):
    """Follow the player position."""

    def __init__(self):
        image = common.load_image('shadow.png')
        super(Shadow, self).__init__(image)
        self.position = 400, 100
