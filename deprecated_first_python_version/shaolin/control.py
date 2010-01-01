# -*- coding: utf-8 -*-
# Copyright 2007 Hugo Ruscitti <hugoruscitti@gmail.com>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Scribes; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301
# USA
import ConfigParser
from pygame.key import get_pressed
from pygame.time import get_ticks

LEFT, RIGHT, UP, DOWN, JUMP, ATTACK, NONE = range(7)

class Control:
    
    def __init__(self, player, configdir):
        self.keys = self._read_config(player, configdir)
        self.last_pressed = [(NONE, get_ticks())] * 4

    def update(self):
        pressed = get_pressed()
        last, t = self.last_pressed[3]

        self.up = pressed[self.keys[UP]]
        self.down = pressed[self.keys[DOWN]]
        self.left = pressed[self.keys[LEFT]]
        self.right = pressed[self.keys[RIGHT]]
        self.jump = pressed[self.keys[JUMP]] and last != JUMP
        self.attack = pressed[self.keys[ATTACK]] and last != ATTACK
        
        # aplica combos
        combo = self.combo()
        self.run = combo == (LEFT, NONE, LEFT) or combo == (RIGHT, NONE, RIGHT)
        self.special = combo == (DOWN, UP, ATTACK)

        # gestiona la pila de combos
        if self.attack and last != ATTACK:
            self.push(ATTACK)
            return
        if self.up and last != UP:
            self.push(UP)
            return
        elif self.down and last != DOWN:
            self.push(DOWN)
            return
        elif self.left and last != LEFT:
            self.push(LEFT)
            return
        elif self.right and last != RIGHT:
            self.push(RIGHT)
            return
        elif self.jump and last != JUMP:
            self.push(JUMP)
            return

        if last != NONE:
            # deja se pulsar una tecla
            if not pressed[self.keys[last]]:
                self.push(NONE)
            
    def push(self, key):
        time = get_ticks()
        self.last_pressed.append((key, time))
        self.last_pressed.pop(0)

    def combo(self):
        combo = self.last_pressed[1:]
        k1, t1 = combo[0]
        k2, _ = combo[1]
        k3, _ = combo[2]
        speed = get_ticks() - t1

        if speed < 300:
            return (k1, k2, k3)

        

    def _read_config(self, player, configdir):
        cfg = ConfigParser.ConfigParser()
        cfg.read(configdir + '/config.ini')
        section = 'control_player_%d' % player
        reference = ['left', 'right', 'up', 'down', 'jump', 'attack']
        return [cfg.getint(section, x) for x in reference]


if __name__ == '__main__':
    c = Control(0)
