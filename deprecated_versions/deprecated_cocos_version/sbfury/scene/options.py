# -*- encoding: utf-8 -*-
# Shaolin's Blind Fury
#
# Copyright 2008 - Hugo Ruscitti
# License: GPLv3 (see http://www.gnu.org/licenses/gpl.html)

import pyglet
from pyglet.gl import *
import cocos

import scene
import common
import transition

class Background(cocos.layer.Layer):

    is_event_handler = True

    def __init__(self):
        super(Background, self).__init__()
        self.image = common.load_image('scene/options/background.png')

    def draw(self):
        self.image.blit(0, 0)


class Items(cocos.menu.Menu):
    
    def __init__(self):
        super(Items, self).__init__()
        self.menu_valign = cocos.menu.BOTTOM
        self.menu_halign = cocos.menu.RIGHT
        self.title = ""
        self._fullscreen = True

        items = [
                cocos.menu.ToggleMenuItem('Fullscreen:', self.on_fullscreen,
                    common.director.window.fullscreen), 
                cocos.menu.MenuItem('Return', self.on_return),

                ]

        speed = 0.2

        self.create_menu(items, 
                selected_effect=cocos.actions.ScaleTo(1, speed),
                unselected_effect=cocos.menu.ScaleTo(1, speed),
                activated_effect=cocos.menu.shake())

    def on_fullscreen(self, value):
        common.director.window.set_fullscreen(value)

    def on_return(self):
        new_scene = scene.menu.Menu() 
        common.change_scene(new_scene, transition=transition.MoveRight)

    def on_quit(self):
        self.on_return()


class Options(cocos.scene.Scene):

    def __init__(self):
        super(Options, self).__init__()
        self.add(Background())
        self.add(Items())
