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

import pygame

from font import Font
from fps import FPS
from game import Game
from common import *
from options import Options

class World:
    
    def __init__(self, fps):
        
        self.display = pygame.display
        self.options = Options()
        self._create_screen()
        pygame.display.set_caption("Shaolin Fury - beta version")
        pygame.mouse.set_visible(False)
        self.quit = False
        self.fps = FPS(fps)
        self.font = Font()
        self.change_state(Game(self, DATADIR, CONFIGDIR))

    def _create_screen(self):
        """Genera la ventana principal del videojuego"""

        if self.options.fullscreen:
            flags = pygame.FULLSCREEN
        else:
            flags = 0

        if self.options.reduce_mode:
            size = (320, 240)
        else:
            size = (640, 480)

        self.screen = pygame.display.set_mode(size, flags)

    def change_state(self, new_state):
        self.state = new_state

    def loop(self):
        
        while not self.quit:
            n = self.fps.update()

            for t in xrange(n):
                e = pygame.event.poll()

                if e:
                    if e.type == pygame.QUIT:
                        self.quit = True
                    else:
                        if e.type == pygame.KEYDOWN:
                            
                            if e.key == pygame.K_F3:
                                pygame.display.toggle_fullscreen()
                            elif e.key == pygame.K_q:
                                self.quit = True

                self.state.update()

            if n > 0:
                self.state.draw()
