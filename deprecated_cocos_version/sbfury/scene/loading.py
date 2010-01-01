# -*- encoding: utf-8 -*-
# Shaolin's Blind Fury
#
# Copyright 2008 - Hugo Ruscitti
# License: GPLv3 (see http://www.gnu.org/licenses/gpl.html)

from threading import Thread

import cocos

import common
import scene


class CreateGameThread(Thread):
    """Load the Game scene in background to not freeze the game."""

    def __init__(self, scene):
        super(CreateGameThread, self).__init__()
        self.scene = scene

    def run(self):
        import os
        os.system('sleep 1s')
        game_scene = scene.game.Game()
        self.scene.change_to_scene(game_scene)


class Loading(cocos.scene.Scene):
    """Show a loading animation while load Game scene in a thread."""

    def __init__(self):
        super(Loading, self).__init__()
        self.add(LoadingLayer(self))
        self.thread = CreateGameThread(self)
        self.thread.start()

    def change_to_scene(self, new_scene):
        common.change_scene(new_scene, 
                transition=cocos.scenes.transitions.FadeTransition)


class LoadingLayer(cocos.layer.Layer):
    """Show a loading animation."""

    def __init__(self, father):
        super(LoadingLayer, self).__init__()
        self.father = father
        self._create_sprite()

    def _create_sprite(self):
        animation = common.load_animation('loading.gif')
        self.sprite = cocos.sprite.Sprite(animation)
        self.sprite.position = 320, 240

    def draw(self):
        self.sprite.draw()
