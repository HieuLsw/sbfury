# -*- encoding: utf-8 -*-
# Shaolin's Blind Fury
#
# Copyright 2008 - Hugo Ruscitti
# License: GPLv3 (see http://www.gnu.org/licenses/gpl.html)

import pyglet
import cocos

import scene
import common
import transition

class Background(cocos.layer.Layer):

    is_event_handler = True

    def __init__(self):
        super(Background, self).__init__()
        self.image = common.load_image('scene/credits/background.png')

    def draw(self):
        self.image.blit(0, 0)

    def on_key_press(self, symbol, modifiers):
        if symbol:
            new_scene = scene.menu.Menu()
            effect = transition.MoveUp
            common.change_scene(new_scene, transition=effect)
            return True

class Credits(cocos.scene.Scene):

    def __init__(self):
        super(Credits, self).__init__()
        self.add(Background())
