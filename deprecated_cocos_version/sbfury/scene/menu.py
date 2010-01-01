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
        self.image = common.load_image('scene/menu/background.png')

    def draw(self):
        self.image.blit(0, 0)

class Items(cocos.menu.Menu):
    
    def __init__(self):
        super(Items, self).__init__()
        self.menu_valign = cocos.menu.BOTTOM
        self.menu_halign = cocos.menu.RIGHT
        self.title = ""

        items = [
                (cocos.menu.MenuItem('New Game', self.on_new_game)),
                (cocos.menu.MenuItem('Options ', self.on_options)),
                (cocos.menu.MenuItem('Credits ', self.on_credits)),
                (cocos.menu.MenuItem('Quit ',    self.on_quit)),
                ]

        speed = 0.2

        self.create_menu(items, 
                selected_effect=cocos.actions.ScaleTo(1, speed),
                unselected_effect=cocos.menu.ScaleTo(1, speed),
                activated_effect=cocos.menu.shake())

    def on_new_game(self):
        new_scene = scene.game.Game() 
        #new_scene = scene.loading.Loading()
        common.change_scene(new_scene, 
                transition=cocos.scenes.transitions.FadeTransition)

    def on_options(self):
        new_scene = scene.options.Options() 
        common.change_scene(new_scene, transition=transition.MoveLeft)

    def on_credits(self):
        new_scene = scene.credits.Credits() 
        common.change_scene(new_scene, transition=transition.MoveDown)

    def on_quit(self):
        pyglet.app.exit()


class Menu(cocos.scene.Scene):

    def __init__(self):
        super(Menu, self).__init__()
        self.add(Background())
        self.add(Items())
