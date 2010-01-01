# -*- encoding: utf-8 -*-
# Shaolin's Blind Fury
#
# Copyright 2008 - Hugo Ruscitti
# License: GPLv3 (see http://www.gnu.org/licenses/gpl.html)

import pyglet
import common

import cocos
from cocos.actions import *

import stage
import control
import shaolin
import enemies

FINAL_LEVEL = 6


class UIControl(cocos.layer.Layer):
    """Front layer with tip for developers and beta testers."""

    is_event_handler = True

    def __init__(self, game):
        super(UIControl, self).__init__()
        self.game = game

        if game.level < FINAL_LEVEL:
            self._create_text()

    def _create_text(self):
        msg = "Use: <F7> next level"
        text = cocos.text.Label(msg, x=5, y=5)
        self.add(text)

    def on_key_press(self, symbol, modifiers):
        if self.game.level < FINAL_LEVEL and symbol == pyglet.window.key.F7:
            self.game.advance_level()

class Messages(cocos.layer.Layer):
    """Show text messages on screen."""

    def __init__(self, game):
        super(Messages, self).__init__()
        self.game = game

    def show_message(self, msg):
        message = cocos.text.Label(msg, font_name='arial',
                font_size=52, 
                color=(0, 0, 0, 255),
                position=(320, 300),
                anchor_x='center', anchor_y='center')

        speed = 0.25
        message.scale = 0
        message.do(Delay(0.5) + ScaleTo(1, speed) + 
                Delay(1) + MoveBy((0, 600), speed))
        self.add(message)


class Game(cocos.scene.Scene):

    def __init__(self):
        super(Game, self).__init__()
        self.level = 1
        self.ui = None
        self.messages = Messages(self)
        self.add(self.messages, z=1)

        self._create_player_and_stage()
        self._create_enemies()
        self._create_uicontrol()
        self._show_stage_message()

    def _create_uicontrol(self):
        if self.ui:
            self.remove(self.ui)

        self.ui = UIControl(self)
        self.add(self.ui)

    def _create_enemies(self):
        self._create_enemy('fat', 300, 300)
        self._create_enemy('hannia', 250, 100)

    def _create_enemy(self, name, x, y):
        name_class = {
                'fat': enemies.fat.Fat,
                'hannia': enemies.hannia.Hannia,
                }

        class_of_enemy = name_class[name]
        enemy = class_of_enemy(x, y)
        self.stage.add_element(enemy)
        self.stage.add_element(enemy.shadow)
        self.stage.collision_manager.add_enemy(enemy)

    def _create_player_and_stage(self):
        shaolin_sprite = shaolin.shaolin.Shaolin()
        control_layer = control.Control(shaolin_sprite)

        # Create Stage
        self.stage = stage.Stage(self.level, object_to_follow=shaolin_sprite)
        self.add(self.stage)

        # Add player to stage
        self.stage.add_element(control_layer)
        self.stage.add_element(shaolin_sprite)
        self.stage.add_element(shaolin_sprite.shadow)

        # Add player to collision manager
        self.stage.collision_manager.add_player(shaolin_sprite)

    def advance_level(self):
        self.level += 1
        self.remove(self.stage)
        #self._create_player_and_stage()
        #self._create_uicontrol()
        #self._show_stage_message()
        import scene
        import cocos

        new_scene = scene.loading.Loading()
        common.change_scene(new_scene, 
                transition=cocos.scenes.transitions.FadeTransition)

    def _show_stage_message(self):
        if self.level == FINAL_LEVEL:
            self.messages.show_message("Final stage")
        else:
            self.messages.show_message("Stage %d" %(self.level))
