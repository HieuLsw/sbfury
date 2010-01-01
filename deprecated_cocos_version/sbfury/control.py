# -*- encoding: utf-8 -*-
# Shaolin's Blind Fury
#
# Copyright 2008 - Hugo Ruscitti
# License: GPLv3 (see http://www.gnu.org/licenses/gpl.html)

import time

import pyglet
import cocos
from pyglet.window import key


global_last_tick = time.time()

def get_ticks():
    global global_last_tick

    actual = time.time()
    dt = actual - global_last_tick
    global_last_tick = actual

    return dt


class Map:
    """Show the control state:

        `left`: left button are pressed.
        `right`: right button are pressed.
        `up`: up button are pressed.
        `down`: down button are pressed.

        `motion`: any motion button are pressed (like: up, left...).
        `run`: if user hit "left, left" or "right, right".
    """

    def __init__(self):
        self.up = False
        self.down = False
        self.left = False
        self.right = False
        self.attack = False
        self.jump = False
        self.run = False

    def _get_motion(self):
        """Show if any player motion button are pressed"""
        return self.up or self.down or self.right or self.left

    motion = property(_get_motion)

    def __str__(self):
        return str(vars(self))


class Control(cocos.layer.Layer):
    """Handles user events."""

    is_event_handler = True

    def __init__(self, player):
        super(Control, self).__init__()
        self._player = player

        self._create_map()
        self._map = Map()
        self._last_motion_history = [(None, get_ticks())] * 3

    def _create_map(self):
        self._dict = {
                key.UP: 'up',
                key.DOWN: 'down',
                key.LEFT: 'left',
                key.RIGHT: 'right',
                key.A: 'jump',
                key.D: 'jump',
                key.S: 'attack',
                # Alternative keys
                key.L: 'right',
                key.H: 'left',
                key.J: 'down',
                key.K: 'up',
                }
        self._do_not_repeat = ['jump', 'attack']
    
    def on_key_press(self, symbol, modifiers):
        try:
            key_name = self._dict[symbol]
            self._register_motion_in_history(key_name)
            self._check_motion_combo_in_history()
            setattr(self._map, key_name, True)

            # Notify event to player
            self._player.on_control_press(self._map)

            # Disable key repeat in some keys
            if key_name in self._do_not_repeat:
                setattr(self._map, key_name, False)
        except KeyError:
            pass

    def _register_motion_in_history(self, key_name):
        """Updates the motion history buffer for combos."""

        self._last_motion_history.pop(0)
        self._last_motion_history.append((key_name, get_ticks()))

    def _check_motion_combo_in_history(self):
        motions = [m[0] for m in self._last_motion_history]
        last_tick = self._last_motion_history[2][1]

        if motions in [['right', None, 'right'], ['left', None, 'left']]:
            if last_tick < 0.2:
                self._map.run = True
                # TODO: fijarse que `self._map.run` debería regresar a False en
                #       algún momento...
    
    def on_key_release(self, symbol, modifiers):
        try:
            key_name = self._dict[symbol]
            self._register_motion_in_history(None)
            setattr(self._map, key_name, False)

            # Disable notify if not a repeat key
            if key_name not in self._do_not_repeat:
                self._player.on_control_release(self._map)

            # restore `run` combo state.
            self._map.run = False

        except KeyError:
            pass



if __name__ == '__main__':
    import common

    common.director.init()

    class Player:

        def on_control_press(self, control):
            #print control
            pass

        def on_control_release(self, control):
            #print control
            pass

    scene = cocos.scene.Scene()
    player = Player()
    control = Control(player)
    scene.add(control)
    common.director.run(scene)
