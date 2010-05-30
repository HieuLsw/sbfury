# -*- encoding: utf-8 -*-
# Shaolin's Blind Fury
#
# Copyright 2008 - Hugo Ruscitti
# License: GPLv3 (see http://www.gnu.org/licenses/gpl.html)

import cocos

import common
import scene

class Loading(cocos.scene.Scene):
    """Show a loading animation while load Game scene in a thread."""

    def __init__(self, level):
        super(Loading, self).__init__()
        self.add(LoadingLayer(self))
        self.level = level
        self.schedule_interval(self.change_to_next_scene, 1)

    def change_to_next_scene(self, dt):
        self.unschedule(self.change_to_next_scene)
        new_scene = scene.game.Game(self.level)
        common.change_scene(new_scene, 
                transition=cocos.scenes.transitions.FadeTransition)


class LoadingLayer(cocos.layer.Layer):
    """Show a loading animation."""

    def __init__(self, father):
        super(LoadingLayer, self).__init__()
        self.father = father
        self._create_sprite()

    def _create_sprite(self):
        animation = common.load_image('wait.png')
        self.sprite = cocos.sprite.Sprite(animation)
        self.sprite.position = 320, 240

    def draw(self):
        self.sprite.draw()
