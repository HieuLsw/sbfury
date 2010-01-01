# -*- encoding: utf-8 -*-
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
from common import *
import common
from pygame.sprite import Group
import menu

class Options:
    "Permite conocer y alterar las opciones del juego."

    def __init__(self, world):
        self.world = world
        self.sprites = Group()
        self.background = load_image("options.png", "scenes")
        options = [
                ("Actual mode: window", "Actual mode: fullscreen", 
                    self.on_change_fs, common.options.fullscreen),
                ("Audio: disable", "Audio: enable", 
                    self.on_change_audio, common.audio.enabled),
                ("Sound Volume:", common.options.sound_volume, 
                    self.on_change_sound_volume),
                ("Music Volume:", common.options.music_volume, 
                    self.on_change_music_volume),
                ("Exit", self.on_return_to_main_menu),
                ]
        self.menu = menu.Menu(230, 250, self.sprites, world.font, options)

    def update(self):
        self.menu.update()

    def draw(self, screen):
        screen.blit(self.background, (0, 0))
        self.sprites.draw(screen)
        pygame.display.flip()

    def on_return_to_main_menu(self):
        import scenes
        self.world.change_state(scenes.mainmenu.MainMenu(self.world))

    def on_change_fs(self):
        result = pygame.display.toggle_fullscreen()
        return result

    def on_change_audio(self):
        new_state = not common.audio.enabled
        common.audio.set_enabled(new_state)
        return 1

    def on_change_sound_volume(self):
        common.audio.set_sound_volume(0.5)

    def on_change_music_volume(self):
        common.audio.set_music_volume(0.5)

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.on_return_to_main_menu()

        self.menu.update_control(event)
