# -*- encoding: utf-8 -*-
# Shaolin's Blind Fury
#
# Copyright 2008 - Hugo Ruscitti
# License: GPLv3 (see http://www.gnu.org/licenses/gpl.html)

import os

from pyglet.window import key
import cocos
from cocos.sprite import Sprite
from cocos.actions import *

import common
import scene


class Background(cocos.layer.Layer):

    is_event_handler = True

    def __init__(self, logo):
        super(Background, self).__init__()
        self.image = common.load_image('scene/intro/background.png')
        self.logo = logo

    def draw(self):
        common.fix_alpha()
        self.image.blit(0, 0)
        common.fix_alpha()

    def on_key_press(self, symbol, modifiers):
        if symbol in [key.ENTER, key.SPACE]:
            self.logo.skip_scene()


class Logo(cocos.scene.Scene):

    def __init__(self):
        super(Logo, self).__init__()
        self.add(Background(self))
        self._create_sprites()

    def _create_sprites(self):
        SPEED = 0.4

        logo_image = common.load_image('scene/intro/ceferino.png')
        logo = Sprite(logo_image)
        logo.scale = 4
        logo.rotation = 180
        logo.opacity = 0
        logo.do(Place((100, 230)))
        logo.do(Delay(SPEED / 2) + 
                (FadeIn(SPEED * 2) | RotateBy(180, SPEED) | ScaleTo(1, SPEED)))

        losers_image = common.load_image('scene/intro/losers.png')
        losers = Sprite(losers_image)
        losers.position = 300, 500
        losers.rotation = 180
        losers.opacity = 0
        losers.do(Delay(SPEED) + 
                (MoveTo((300, 250), SPEED) | FadeIn(SPEED) | RotateBy(180, SPEED)))

        juegos_image = common.load_image('scene/intro/juegos.png')
        juegos = Sprite(juegos_image)
        juegos.position = 500, 0
        juegos.rotation = -180
        juegos.opacity = 0
        juegos.do(Delay(SPEED/2 * 3) +
                (MoveTo((520, 250), SPEED) | FadeIn(SPEED) | RotateBy(180, SPEED))
                + Delay(2) + CallFunc(self.skip_scene))

        self.add(logo)
        self.add(losers)
        self.add(juegos)
        self.juegos = juegos

    def skip_scene(self):
        self.juegos.stop()
        common.change_scene(scene.menu.Menu())
