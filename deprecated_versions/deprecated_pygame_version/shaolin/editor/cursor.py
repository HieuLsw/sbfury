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

import common
from object import Object

class Cursor(Object):

    def __init__(self, x=100, y=400):
        Object.__init__(self)
        self.normal = common.load_image("cursor.png")
        self.invisible = common.load_image("invisible.png")
        self.set_visible(False)
        self.x, self.y = x, y
        self.rect = self.normal.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y
        self.dy = 0
        self.z = -y

    def update(self):
        pass

    def set_position(self, x, y):
        self.x, self.y = x, y
        self.rect.center = x, y
        self.z = -y + 30

    def set_visible(self, state):
        if state:
            self.image = self.normal
        else:
            self.image = self.invisible
