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

class Text(Sprite):

    def __init__(self, font, fps, string):
        Sprite.__init__(self)
        self.font = font
        self.fps = fps
        self.cache_status = fps.status
        self.string = string
        self._create_image()
        self.z = -90


    def update(self):
        if self.cache_status != self.fps.status:
            self._create_image()

    def _create_image(self):
        self.cache_status = self.fps.status
        self.image = self.font.render(self.string % (self.cache_status))
        self.rect = self.image.get_rect()
        self.rect.right = 630
        self.rect.top = 10
