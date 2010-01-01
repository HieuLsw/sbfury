# -*- coding: utf-8 -*-
#
# Shaolin's Blind Fury
# Copyright 2007 2008 Hugo Ruscitti <hugoruscitti@gmail.com>
# http://www.losersjuegos.com.ar
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, see http://www.gnu.org/licenses

import pygame

class Audio:
    "Adminstra todos los recursos de sonido y músicas."
    
    def __init__(self, datadir):
        import common
        self.set_enabled(not common.options.disabled_sound)
        self.datadir = datadir

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

    def set_sound_volume(self, vol):
        "Define el nivel de volumen para todos los sonidos del juego."
        for sound in self.sounds:
            print "new sound volume:", vol

    def set_music_volume(self, vol):
        "Define el nivel de volumen para la música del juego."
        print "new music volume:", vol

    def set_enabled(self, state):
        if state:
            print "Habilita sonidos"
            self.enabled = True
            pygame.mixer.init()
            self._load_sounds()
        else:
            print "No habilita sonidos"
            self.enabled = False

