# -*- encoding: utf-8 -*-
# Shaolin's Blind Fury
#
# Copyright 2008 - Hugo Ruscitti
# License: GPLv3 (see http://www.gnu.org/licenses/gpl.html)

import config
import common

class Sound:

    def __init__(self):
        self.sounds = {}
        self.sounds['punch1'] = common.load_sound("sounds/punch1.wav")

    def play(self, code):
        self.sounds[code].play()
