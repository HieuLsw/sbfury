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

class Mouse:

    def __init__(self, editor):
        self.editor = editor
        self.stage = editor.stage
        self.selected_object = None
        self.last_button = None

    def update(self):
        x, y = pygame.mouse.get_pos()

        button = self.editor.get_button_at(x, y)

        # Movimiento del mouse sobre los botones
        if button:
            self._set_focus(button)
        else:
            if self.last_button:
                self.last_button.set_focus(False)
                self.last_button = None

        # gestiona el cursor de objetos en pantalla
        x, y = self.editor.camera.get_relative_position(x, y)
        object = self.stage.get_object_at(x, y)

        if object:
            self.editor.cursor.set_visible(True)
            self.editor.cursor.set_position(object.x, object.y)
        else:
            self.editor.cursor.set_visible(False)

    def on_click_in_stage(self):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        x, y = self.editor.camera.get_relative_position(mouse_x, mouse_y)

        object = self.stage.get_object_at(x, y)

        if self.selected_object:
            name = self.selected_object
            self.stage.create_object(name, (x, y))
            msg = "Creating a '%s' at (%d, %d)" %(name, x, y)
            self.editor.status.set_text(msg)
        else:
            msg = "You must select an object before ..."
            self.editor.status.set_text(msg)

    def on_erase_in_stage(self):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        x, y = self.editor.camera.get_relative_position(mouse_x, mouse_y)

        object = self.stage.get_object_at(x, y)

        if object:
            self.stage.erase_object(object)
        else:
            msg = "You has to move the mouse over an object to erase em"
            self.editor.status.set_text(msg)

    def on_click_event(self, button):
        if button == 1:
            self._on_click_button_left()
        elif button == 3:
            self._on_click_button_right()
        elif button == 4:
            self.editor.camera.move(-5)
        elif button == 5:
            self.editor.camera.move(+5)

    def _on_click_button_left(self):
        x, y = pygame.mouse.get_pos()
        button = self.editor.get_button_at(x, y)
        
        if button:
            button.do_click()
        else:
            self.on_click_in_stage()

    def _on_click_button_right(self):
        self.on_erase_in_stage()

    def _set_focus(self, button):
        "Destaca el boton que se encuentra debajo del puntero."
        button.set_focus(True)

        if self.last_button != button:
            if self.last_button:
                self.last_button.set_focus(False)
            self.last_button = button
