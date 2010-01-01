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
from sprite import Sprite
import common

BACKGROUND = (100, 0, 0)
FOREGROUND = (255, 255, 0)

class EnergyView(Sprite):
    "Representa un indicador de energia en pantalla"
    
    def __init__(self, x, y, font):
        Sprite.__init__(self, x, y)
        self.background = common.load_image("energy_view.png")
        self.model = None
        self.font = font
        self.image = self.background.convert_alpha()
        self.rect = self.image.get_rect()
        self.to_y = y
        self.rect.move_ip(x, y)
        self.rect.y = -50

    def set_model(self, model):
        self.model = model
        self.image = self.background.convert_alpha()
        self.current_energy = model.energy
        self.name_image = self.font.render(model.name)
        self._update_view()
        self.rect.y = self.to_y

    def _update_view(self):
        self.image = self.background.convert_alpha()
        rect = self.image.get_rect()
        rect.x += 37
        rect.y += 1
        rect.h, rect.w = 13, 148
        self.image.fill(BACKGROUND, rect)
        rect.w = self.current_energy * 1.5 - 2
        self.image.fill(FOREGROUND, rect)
        self.image.blit(self.name_image, (40, 15))
        self.image.blit(self.model.image, (1, 1))
        
    def update(self):
        if self.model:
            if self.current_energy != self.model.energy:
                self.current_energy = self.model.energy
                self._update_view()

class EnergyModel:
    "Modelo de datos para EnergyView, cada personaje debe tener uno de estos"

    def __init__(self, name, energy, on_change_callback):
        self.name = name
        self.energy = energy
        self.on_change_callback = on_change_callback

        try:
            self.image = common.load_image("preview.png", name)
        except:
            self.image = common.load_image("preview.png", "enemies/" + name)

    def change_energy(self, value):
        self.energy += value
        self.on_change_callback(self)

    def must_die(self):
        return self.energy < 1
