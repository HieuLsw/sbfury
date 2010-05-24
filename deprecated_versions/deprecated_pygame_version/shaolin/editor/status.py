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

from pygame.sprite import Sprite

TIME_TO_HIDE = 300

class Status(Sprite):

    def __init__(self, font):
        Sprite.__init__(self)
        self.font = font
        self.set_text("Welcome to Shaolin's Level Editor")

    def set_text(self, text):
        self.image = self.font.render(text)
        self.rect = self.image.get_rect()
        self._show()

    def update(self):
        self.rect.top += (self.to_y - self.rect.top) / 10.0

        if self.visible:
            self.tick += 1

            if self.tick > TIME_TO_HIDE:
                self._hide()

    def _show(self):
        self.tick = 0
        self.visible = True
        self.to_y = 480 - self.rect.h
        self.rect.top = 480

    def _hide(self):
        self.visible = False
        self.to_y = 500
