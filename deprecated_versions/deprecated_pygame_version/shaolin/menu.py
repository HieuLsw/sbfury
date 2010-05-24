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
from sprite import SpriteAnimated, Sprite
import sprite
import common
import control

class Menu:
    "Representa un menú de opciones."

    def __init__(self, x, y, sprites, font, options):
        self.sprites = sprites
        self.items = []
        index = 0

        for value in options:
            # TODO: Hacer que el menú se posicione a la derecha de la 
            #       pantalla en lugar de recibir la coordenada de una
            #       esquina.

            if len(value) == 2:
                label, callback = value
                new_item = ItemMenu(x, y, index, font, label, callback)
            elif len(value) == 3:
                label, variable, callback = value
                new_item = ItemMenuWithVolume(x, y, index, font, label, variable, callback)
            else:
                l1, l2, callback, variable = value
                new_item = ItemMenuWithState(x, y, index, font, [l1, l2], callback)

            self.sprites.add(new_item)
            self.items.append(new_item)
            index += 1

        self.cursor = Cursor(self, x, y)
        self.sprites.add(self.cursor)

    def get_items_len(self):
        return len(self.items)

    def update_control(self, event):
        self.cursor.handle_event(event)

    def update(self):
        self.sprites.update()

    def select_by_index(self, index):
        item = self.items[index]
        item.select()

    def get_item_height(self):
        item = self.items[0]
        return item.image.get_height() + 8


class ItemMenu(SpriteAnimated):
    "Una entrada de texto para el menú."

    def __init__(self, x, y, index, font, label, callback):
        self.font = font
        self._set_text(label)
        to_y = y + (self.image.get_height() + 10) * index
        SpriteAnimated.__init__(self, self.image, sprite.RIGHT, x, to_y)
        self.callback = callback
        self.do_click = False
        self.delay_to_move = -1
        self.delay_to_activate_callback = -1

    def _set_text(self, label):
        self.image = self.font.render(label, size=2)

    def update(self):
        SpriteAnimated.update(self)

        if self.do_click:
            self.delay_to_move -= 1
            self.delay_to_activate_callback -= 1

            if self.delay_to_move < 0:
                self.x = self.to_x + 30
                self.delay_to_move = 40
            elif self.delay_to_activate_callback < 0:
                self.callback()
                self.do_click = False

    def select(self):
        "Activa una opción con demora."
        self.do_click = True
        self.delay_to_move = 3
        self.delay_to_activate_callback = 10

    def change_value(self, delta):
        pass


class ItemMenuWithState(ItemMenu):
    "Muestra una entrada con dos estados."

    def __init__(self, x, y, index, font, labels, callback):
        ItemMenu.__init__(self, x, y, index, font, labels[0], callback)
        self.labels = labels
        self.actual_index = 1
        self._alternate_text_label()

    def update(self):
        SpriteAnimated.update(self)

        if self.do_click:
            self.delay_to_move -= 1
            self.delay_to_activate_callback -= 1

            if self.delay_to_move < 0:
                self.x = self.to_x + 30
                self.delay_to_move = 40
                if self.callback():
                    self._alternate_text_label()
            elif self.delay_to_activate_callback < 0:
                self.do_click = False

    def _alternate_text_label(self):
        "Cambia el texto de la opción acorde a un nuevo estado."
        if self.actual_index == 0:
            self.actual_index = 1
            self._set_text(self.labels[self.actual_index])
        else:
            self.actual_index = 0
            self._set_text(self.labels[self.actual_index])


class ItemMenuWithVolume(ItemMenu):
    "Muestra una entrada con dos estados."

    def __init__(self, x, y, index, font, label, variable, callback):
        ItemMenu.__init__(self, x, y, index, font, label, callback)
        self.label = label
        self.volume = common.load_image('volume.png', 'menu')
        self.variable = variable
        self._update_text()

    def update(self):
        SpriteAnimated.update(self)

        if self.do_click:
            self.delay_to_move -= 1
            self.delay_to_activate_callback -= 1

            if self.delay_to_move < 0:
                self.x = self.to_x + 30
                self.delay_to_move = 40
            elif self.delay_to_activate_callback < 0:
                self.do_click = False

    def change_value(self, delta):
        self.variable += delta
        self.callback()

        if self.variable < 0:
            self.variable = 0
        elif self.variable > 8:
            self.variable = 8

        self._update_text()
        return True

    #def punch(self):
    #    self.change_value(+1)

    def _update_text(self):
        self.x = self.to_x + 5
        self._set_text(self.label)
        w = self.image.get_width()
        h = self.image.get_height()
        self._set_text(self.label + " " * 20)
        self.image.blit(self.volume, (w + 10, 0), (0, 0, 18 * self.variable, h))


class Cursor(SpriteAnimated):
    "Representa el cursor que indicará la opción a punto de seleccionar."

    def __init__(self, menu, x, y, initial_index=0):
        image = common.load_image("cursor.png", "menu")
        SpriteAnimated.__init__(self, image, sprite.LEFT, x - 40, y)
        self.control = control.Control()
        self.menu = menu
        self.index = initial_index
        self.initial_y = y
        self.initial_x = x
        self.can_select = False
        self.dy = menu.get_item_height()

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            self.control.update(event, True)
        elif event.type == pygame.KEYUP:
            self.control.update(event, False)
        else:
            return

        if self.control.up:
            self.change_index(-1)
        elif self.control.down:
            self.change_index(+1)
        elif self.control.right:
            self.change_value(+1)
        elif self.control.left:
            self.change_value(-1)
        elif self.can_select and self.control.attack:
            self.punch()
            self.menu.select_by_index(self.index)

    def update(self):
        SpriteAnimated.update(self)
        self.can_select = self.is_movement_done()
        self.control.post_update()

    def change_index(self, delta):
        self.index += delta

        if self.index < 0:
            self.index = self.menu.get_items_len() -1
        elif self.index > self.menu.get_items_len() - 1:
            self.index = 0

        self.to_y = self.initial_y + self.index * self.dy + 5

    def change_value(self, delta):
        item = self.menu.items[self.index]
        if item.change_value(delta):
            self.punch()

    def punch(self):
        self.x = self.to_x + 30
        common.audio.play('punch2')


if __name__ == "__main__":

    def test():
        "Debe retornar True para indicar un cambio de texto en la opción."
        return True

    import pygame
    from font import Font

    screen = pygame.display.set_mode((459, 350))
    pygame.font.init()

    font = Font()
    value = 2

    salir = False
    sprites = pygame.sprite.Group()
    options = [
                ("Mode: fullscreen", "Mode: window", test),
                ("Sound: enabled", "Sound: disabled", test),
                ["Volume:", "|", value, test],
                ["Music:", "|", value, test],
            ]
    menu = Menu(90, 100, sprites, font, options)

    while not salir:

        for e in pygame.event.get():
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_q:
                    salir = True
                else:
                    menu.update_control(e)

        menu.update()

        screen.fill((200, 200, 200))
        sprites.draw(screen)
        pygame.display.flip()
        pygame.time.delay(10)
