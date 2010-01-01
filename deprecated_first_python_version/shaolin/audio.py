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

import pygame

class Audio:
    
    def __init__(self, datadir):
        self.enabled = True
        pygame.mixer.init()
        self.datadir = datadir
        self._load_sounds()

    def _load_sounds(self):
        names = ['punch1', 'punch2', 'throw', 'menu_change', 'menu_select', 
                'attack_run', 'touch_flood']
        self.sounds = dict()

        for n in names:
            filename = "%s/sounds/%s.wav" %(self.datadir, n)
            self.sounds[n] = pygame.mixer.Sound(filename)

    def play(self, name):
        """Play sound named 'name'"""

        if self.enabled:
            self.sounds[name].play()
        else:
            pass
