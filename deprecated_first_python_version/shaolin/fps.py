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
from pygame.time import get_ticks, wait

class FPS:
    
    def __init__(self, fps, maxframeskip=2):
        
        self.tick = self.last_tick = self.last_fps_tick = get_ticks()
        self.frecuency = int(1000 / fps)
        self.normal_frecuency = int(1000 / fps)
        self.maxframeskip = maxframeskip
        self.status = 0
        self.fps_count = 0
        self.slow_motion_delay = 0


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
        if self.slow_motion_delay <= 0:
            self.frecuency = self.normal_frecuency * 4
            self.slow_motion_delay = 30
