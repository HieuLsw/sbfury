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

from pygame.time import get_ticks, wait

class FPS:
    "Gestiona la velocidad constante del juego y permite alterarla."
    
    def __init__(self, fps, maxframeskip=2):
        self.tick = self.last_tick = self.last_fps_tick = get_ticks()
        self.set_fps(fps)
        self.maxframeskip = maxframeskip
        self.status = 0
        self.fps_count = 0
        self.slow_motion_delay = 0

    def set_fps(self, fps):
        "Define el rendimiento esperado en cuadros por segundo."
        self.frecuency = int(1000 / fps)
        self.normal_frecuency = int(1000 / fps)

    def update(self):
        self.tick = get_ticks()
        delta = self.tick - self.last_tick

        if self.slow_motion_delay > 0:
            self.slow_motion_delay -= 1

            if self.slow_motion_delay <= 0:
                self.frecuency = self.normal_frecuency


        if delta > self.frecuency:
            skips = delta / self.frecuency

            if skips > self.maxframeskip:
                skips = self.maxframeskip
                self.last_tick = self.tick
            else:
                self.last_tick += skips * self.frecuency

            self._update_status()
            return skips
        else:
            wait(1)
            return 0

    def _update_status(self):
        if self.tick > self.last_fps_tick - 1000:
            self.last_fps_tick += 1000
            self.status = self.fps_count
            self.fps_count = 0
        else:
            self.fps_count += 1

    def slow(self):
        "Reduce la velocidad del juego durante unos instantes."
        if self.slow_motion_delay <= 0:
            self.frecuency = self.normal_frecuency * 4
            self.slow_motion_delay = 30
