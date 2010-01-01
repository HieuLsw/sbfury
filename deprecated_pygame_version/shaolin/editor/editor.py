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

import os
import pygame
import stage
import group

import camera
import mouse
import button
import common
import status
import cursor
import config
import game

class Editor:

    def __init__(self, world):
        self.world = world
        self.sprites = group.Group()
        self.stage = stage.Stage(self, self.sprites)
        self.sprites.camera = self.stage
        self.sprites_in_front = pygame.sprite.RenderPlain()
        self.camera = camera.Camera(320, 5000)
        self.stage.object_to_follow = self.camera
        self.stage.load_level(1)
        self.mouse = mouse.Mouse(self)
        self.cursor = cursor.Cursor()
        self.sprites.add(self.cursor)
        self._create_status()
        self._create_ui()

    def _create_status(self):
        self.status = status.Status(self.world.font)
        self.sprites_in_front.add(self.status)

    def _create_ui(self):
        self.buttons = []
        ui = [
                ("quit", 0, 0, self.do_quit),
                ("save", 1, 0, self.do_save),
                ("previous", 3, 0, self.do_previous),
                ("next", 4, 0, self.do_next),
                ("test", 6, 0, self.do_test),
                ]
        stage_objects = [
                "box",
                "stonea",
                "stoneb",
                "miscstonea",
                "miscstoneb",
                "miscstonec",
                "light",
                "dark",
                "camera_stop",
                "fatninja",
                "lamp",
                "border_back",
                "border_front",
                "red",
                ]

        for b in ui:
            type, column, row, callback = b
            new = button.Button(type, column, row, callback, self.status)
            self.buttons.append(new)

        column = 9
        row = 3
        callback = self.do_select_object

        for b in stage_objects:
            type = b
            new = button.Button(type, column, row, callback, self.status)
            self.buttons.append(new)

            if column > 10:
                row += 1
                column = 9
            else:
                column += 1

        self.sprites_in_front.add(self.buttons)

    def do_quit(self, button):
        self.do_save()
        self.world.quit = True

    def do_save(self, button=None):
        self.stage.save()
        self.status.set_text("Saving stage ...")

    def do_test(self, button):
        self.do_save()
        dx = self.stage.object_to_follow.x
        level = self.stage.level
        gametest = game.GameTestLevel(self.world, level, self, dx)
        self.world.change_state(gametest, do_animate=False)

    def do_previous(self, button):
        ok = self.stage.previous()

        if not ok:
            self.status.set_text("I can't go to previous level (it exists?)")

    def do_next(self, button):
        ok = self.stage.next()

        if not ok:
            self.status.set_text("I can't go to next level (it exists?)")

    def do_select_object(self, button):
        self.status.set_text("You has select a '%s' object" %(button.name))
        self.mouse.selected_object = button.name

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.mouse.on_click_event(event.button)

    def update(self):
        "Actualización lógica."
        self.camera.update()
        self.stage.update()
        self.mouse.update()
        self.sprites_in_front.update()

    def draw(self, screen):
        "Actualiza la pantalla."
        self.stage.draw(screen)
        self.sprites.draw(screen)
        self.stage.last_draw(screen)
        self.sprites_in_front.draw(screen)
        pygame.display.flip()

    def get_button_at(self, x, y):
        "Devuelve una referencia al botón apuntado por el cursor."
        for b in self.buttons:
            if b.rect.collidepoint(x, y):
                return b
