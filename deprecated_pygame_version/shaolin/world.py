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

from font import Font
from fps import FPS
from common import *
from scenes.transition import Transition

class World:
    """Representa el objeto principal del juego.
    
    Contiene el bucle principal para mantener actualizados todos los eventos
    de aplicación y gestionar una referencia a la escena actual."""
    
    
    def __init__(self, argv, fps=60):
        self.display = pygame.display
        self.state = None

        options.parse_args(argv)
        self._create_screen()
        pygame.display.set_caption("Shaolin's Blind Fury - %s" %VERSION)
        pygame.mouse.set_visible(options.show_mouse)
        pygame.display.set_icon(load_image('icon.png', DATADIR))
        self.quit = False
        self.fps = FPS(fps)
        self.font = Font()

    def _create_screen(self):
        """Genera la ventana principal del videojuego"""

        if options.fullscreen:
            flags = pygame.FULLSCREEN
        else:
            flags = 0

        center_window()
        size = (640, 480)
        self.screen = pygame.display.set_mode(size, flags)

    def change_state(self, new_state, do_animate=True):
        "Altera la escena actual"

        if self.state:
            if do_animate:
                self.state = Transition(self, self.state, new_state)
            else:
                self.state = new_state
        else:
            self.state = new_state

    def loop(self):
        "Mantiene en actualización constante al juego"
        
        while not self.quit:
            n = self.fps.update()

            for t in xrange(n):

                for e in pygame.event.get():
                    self.state.handle_event(e)

                    # TODO: remover toda sentencia de depuración
                    if e.type == pygame.QUIT:
                        self.quit = True
                    else:
                        if e.type == pygame.KEYDOWN:
                            
                            if e.key == pygame.K_F3:
                                pygame.display.toggle_fullscreen()
                            elif e.key == pygame.K_q:
                                self.quit = True
                            elif e.key == pygame.K_1:
                                self.fps.set_fps(1)
                            elif e.key == pygame.K_2:
                                self.fps.set_fps(3)
                            elif e.key == pygame.K_3:
                                self.fps.set_fps(10)
                        elif e.type == pygame.KEYUP:
                            if e.key in [pygame.K_1, pygame.K_2, pygame.K_3]:
                                self.fps.set_fps(60)

                self.state.update()

            if n > 0:
                self.state.draw(self.screen)
