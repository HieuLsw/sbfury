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

import ConfigParser
import pygame
from pygame.time import get_ticks
import common

class Control:
    """Gestiona el dispositivo de entrada para el juego.

    Se ofrece una vista simplificada del teclado, ocultando algunos detalles
    como la repetición de teclas o las combinaciones especiales.

    Para consultar el estado del control puede leer directamente los
    atributos: left, right, up, down, attack o jump.
    
    Las combinaciones especiales también se consultan como atributos: run,
    special.

    La configuración de controles se lee directamente desde un archivo de
    configuración .ini (ver método '_read_config').
    """
    
    def __init__(self):
        #self.keys = self._read_config(common.CONFIGDIR)
        self.last_pressed = [(None, get_ticks())] * 3
        self._create_keymap()

    def _create_keymap(self):
        "Relaciona todos los indices de teclas con los atributos de acción."
        # Format: 
        #   key -> symkey code
        #   value -> tuple('attribute', allow_repeat)
        self.map = {
            273: ('up', True),
            274: ('down', True),
            276: ('left', True),
            275: ('right', True),
            # alternative or customized
            107: ('up', True),
            106: ('down', True),
            104: ('left', True),
            108: ('right', True),
            # buttons
            115: ('attack', False),
            13: ('attack', False),
            32: ('attack', False),
            97: ('jump', False),
            }

        # Create attributes with initial value
        for attribute, _ in self.map.values():
            setattr(self, attribute, False)

        self.run = False
        self.special = False

    def update(self, event, status):
        "Actualiza los atributos del gestor de control."
        try:
            key = self.map[event.key]
        except KeyError:
            return

        attribute, allow_repeat = key
        setattr(self, attribute, status)
        self.push(attribute)

        if not status:
            self.run = False
            self.push(None)

    def post_update(self):
        "Deshabilita la repetición de teclas en algunos movimientos."
        lastkey, _ = self.last_pressed[2]

        for key, allow_repeat in self.map.values():
            if lastkey == key and not allow_repeat:
                setattr(self, key, False)
                time = pygame.time.get_ticks()
        self.special = False
        self.check_combo()

    def check_combo(self):
        "Verifica si las combinaciones de teclas permiten 'run' o 'special'."
        combo = self.get_last_movements()

        if combo:
            self.special = combo == ('down', 'up', 'attack')
            self.run = \
                    combo == ('left', None, 'left') or \
                    combo == ('right', None, 'right')

    def push(self, key):
        "Agrega el movimiento a la pila de verificación de combos."
        time = get_ticks()
        self.last_pressed.append((key, time))
        self.last_pressed.pop(0)

    def get_last_movements(self):
        "Retorna los últimos 3 movimientos para analizar combos."
        combo = self.last_pressed[:]
        k1, t1 = combo[0]
        k2, _ = combo[1]
        k3, _ = combo[2]
        speed = get_ticks() - t1

        if speed < 300:
            return (k1, k2, k3)

    def _read_config(self, configdir):
        cfg = ConfigParser.ConfigParser()
        cfg.read(configdir + '/config.ini')
        section = 'player_control'
        reference = ['left', 'right', 'up', 'down', 'jump', 'attack',
                'a_left', 'a_right', 'a_up', 'a_down']
        return [cfg.getint(section, x) for x in reference]
