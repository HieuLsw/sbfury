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

from pygame.sprite import Group
from sprite import SpriteAnimated
from sprite import LEFT, RIGHT
from common import *
from animation import SimpleAnimation
import scenes.mainmenu


class Logo:
    "Escena que muestra el logotipo del grupo losersjuegos."

    def __init__(self, world):
        self.world = world
        self.sprites = Group()
        self._create_sprites()
        self._reset_timer()

    def _reset_timer(self):
        self.time_out = 50

    def update(self):
        key = pygame.key.get_pressed()

        if key[pygame.K_ESCAPE]:
            self.world.state = Logo(self.world)
            self._reset_timer()
            return
        else:
            self.sprites.update()

        if self.time_out < 1 or key[pygame.K_RETURN]:
            self.world.change_state(scenes.mainmenu.MainMenu(self.world))

        self.time_out -= 1

    def draw(self, screen):
        screen.fill((92, 123, 94))
        self.sprites.draw(screen)
        pygame.display.flip()

    def _create_sprites(self):
        steps = [0, 0, 0, 1, 2, 3, 4]
        losers = SimpleAnimation('logo', 'losers_5.png', steps, 2)
        sprite_losers = LogoSpriteAnimated(losers, LEFT, 190, 190)

        steps2 = [0, 0, 0, 1, 2, 3, 4]
        juegos = SimpleAnimation('logo', 'juegos_5.png', steps2, 2)
        sprite_juegos = LogoSpriteAnimated(juegos, RIGHT, 390, 190)

        steps3 = [0, 0, 0, 1, 1, 2, 3]
        ceferino = SimpleAnimation('logo', 'ceferino_4.png', steps3, 2)
        sprite_ceferino = LogoSpriteAnimated(ceferino, RIGHT, 40, 160)

        self.sprites.add([sprite_juegos, sprite_losers, sprite_ceferino])

    def handle_event(self, event):
        pass


class LogoSpriteAnimated(SpriteAnimated):
    "Sprite de objeto en movimiento para la escena Logo."

    def __init__(self, animation, pos, to_x, to_y):
        self.animation = animation
        first_frame = self.animation.advance()
        SpriteAnimated.__init__(self, first_frame, pos, to_x, to_y)

    def update(self):
        SpriteAnimated.update(self)
        self.image = self.animation.advance(True)
