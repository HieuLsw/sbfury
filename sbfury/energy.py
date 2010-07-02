# -*- encoding: utf-8 -*-
# Shaolin's Blind Fury
#
# Copyright 2008 - Hugo Ruscitti
# License: GPLv3 (see http://www.gnu.org/licenses/gpl.html)

import pyglet
import common

import cocos
from cocos.actions import *


# Parche para poder cambiar el texto de un nodo Label
def change_text(self, text):
    self.element.text= text

cocos.text.Label.change_text = change_text

class EnergyIndicator(cocos.text.Label):
    """Representa un indicador de enegia, que puede ser del protagonista o un enemigo.

    Este objeto toma a un personaje de referencia (target) y he intenta
    mostrar su atributo ``energy`` en pantalla."""

    def __init__(self, target, x, y):
        self.target = target
        cocos.text.Label.__init__(self,  x=x, y=y, font_size=16, 
                anchor_x='left', anchor_y='top', color=(0,0,0,255))
        self.schedule(self.update)
        self.change_text("HOLA")

    def update(self, dt):
        self.change_text(self.target.name + ": " + str(self.target.energy))
